#!/usr/bin/env python3
"""Verify the shape of texts in the project's unified text format (standard library only).

The format is defined in docs/Unified_text_format.md. Every converter, whatever its
source (typed text, scan of a printed book, scan of a manuscript), must produce files
of this shape.

Not a command: check() is called by tools/vh_check.py. It verifies
one folder (text/ or work/raw/) of a version: for every <lang>.jsonl, its <lang>.info.json
and <lang>.pages.csv, and <lang>.page_images.csv if it is there. It prints one line per file and
returns the problems found.
"""
import csv, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "works"
FORMAT = "vh-text/0.3"

KINDS = {"head", "text", "commentary", "note", "apparatus", "margin", "caption", "paratext"}
ANCHORED = {"note", "apparatus", "margin"}
MARKS = {"add", "del", "gap", "unclear", "hi", "foreign"}
PASSAGE_KEYS = {"id", "kind", "page", "text", "ref", "breaks", "marks", "anchor", "lang",
                "conf", "checked"}
PAGE_COLUMNS = ["page", "volume", "printed"]
IMAGE_COLUMNS = ["page", "source_file", "image", "mapping"]
MAPPINGS = {"checked", "computed"}
INFO_KEYS = {"format", "version", "work_no", "work", "lang", "origin", "sources",
             "converter", "ref_scheme", "rights", "status", "review", "notes"}
ORIGINS = {"typed", "ocr", "htr"}
STATUSES = {"draft", "complete"}
REVIEWS = {"none", "sampled", "full"}
LANG = re.compile(r"^[a-z]{3}$")
BAD_SPACE = re.compile(r"\s\s|[^\S ]")  # two spaces in a row, or any space that is not U+0020


def text_problem(t):
    if not isinstance(t, str) or not t:
        return "text empty or not a string"
    if t != unicodedata.normalize("NFC", t):
        return "text not in Unicode NFC form"
    if t != t.strip() or BAD_SPACE.search(t):
        return "text has leading, trailing, doubled or non-plain spaces"
    if any(unicodedata.category(c) == "Cc" for c in t):
        return "text has control characters"
    return None


def check_pages(path, err):
    pages = set()
    if not path.exists():
        err(f"{path.name}: missing")
        return pages
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        if next(r, None) != PAGE_COLUMNS:
            err(f"{path.name}: header must be {','.join(PAGE_COLUMNS)}")
            return pages
        for n, row in enumerate(r, 2):
            if len(row) != len(PAGE_COLUMNS):
                err(f"{path.name} line {n}: {len(row)} fields instead of {len(PAGE_COLUMNS)}")
                continue
            page = row[0]
            if not page or page in pages:
                err(f"{path.name} line {n}: page id empty or repeated ({page!r})")
            pages.add(page)
    return pages


def check_images(path, pages, err):
    """page_images.csv, the optional link from pages to scan images. Returns the number of rows."""
    seen = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        if next(r, None) != IMAGE_COLUMNS:
            err(f"{path.name}: header must be {','.join(IMAGE_COLUMNS)}")
            return 0
        for n, row in enumerate(r, 2):
            if len(row) != len(IMAGE_COLUMNS):
                err(f"{path.name} line {n}: {len(row)} fields instead of {len(IMAGE_COLUMNS)}")
                continue
            page, source_file, image, mapping = row
            if page not in pages or page in seen:
                err(f"{path.name} line {n}: page {page!r} not in the pages file, or repeated")
            seen.add(page)
            if not source_file or not image:
                err(f"{path.name} line {n}: source_file and image must be filled")
            if mapping not in MAPPINGS:
                err(f"{path.name} line {n}: mapping must be one of {sorted(MAPPINGS)}")
    return len(seen)


def check_info(path, lang, version, err):
    if not path.exists():
        err(f"{path.name}: missing")
        return
    try:
        info = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        err(f"{path.name}: not valid JSON ({e})")
        return
    for k in sorted(INFO_KEYS - set(info)):
        err(f"{path.name}: key '{k}' missing")
    for k in sorted(set(info) - INFO_KEYS):
        if not k.startswith("x_"):
            err(f"{path.name}: unknown key '{k}'")
    for key, want in (("format", {FORMAT}), ("lang", {lang}), ("version", {version}),
                      ("origin", ORIGINS), ("status", STATUSES), ("review", REVIEWS)):
        if key in info and info[key] not in want:
            err(f"{path.name}: '{key}' is {info[key]!r}, expected {' or '.join(sorted(want))}")
    if not isinstance(info.get("ref_scheme", []), list):
        err(f"{path.name}: 'ref_scheme' must be a list")
    src = info.get("sources", [])
    if not isinstance(src, list) or not src or any(
            not isinstance(s, dict) or not s.get("file") or not s.get("md5") for s in src):
        err(f"{path.name}: 'sources' must list at least one {{file, md5}}")


def check_text(path, pages, err):
    seen, order, kinds, chars = {}, [], Counter(), 0
    anchors = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            where = f"{path.name} line {n}"
            try:
                p = json.loads(line)
            except ValueError as e:
                err(f"{where}: not valid JSON ({e})")
                continue
            if not isinstance(p, dict):
                err(f"{where}: not a JSON object")
                continue
            for k in ("id", "kind", "page", "text"):
                if k not in p:
                    err(f"{where}: key '{k}' missing")
            for k in set(p) - PASSAGE_KEYS:
                if not k.startswith("x_"):
                    err(f"{where}: unknown key '{k}'")
            pid, text = p.get("id"), p.get("text", "")
            if not isinstance(pid, str) or not pid or pid in seen:
                err(f"{where}: id empty, not a string or repeated ({pid!r})")
            else:
                seen[pid] = len(text) if isinstance(text, str) else 0
                order.append(pid)
            if p.get("kind") not in KINDS:
                err(f"{where}: kind {p.get('kind')!r} not in {sorted(KINDS)}")
            kinds[p.get("kind")] += 1
            if p.get("page") not in pages:
                err(f"{where}: page {p.get('page')!r} not in the pages file")
            problem = text_problem(text)
            if problem:
                err(f"{where}: {problem}")
                continue
            chars += len(text)
            last = 0
            for b in p.get("breaks", []):
                ok = (isinstance(b, list) and len(b) == 2 and isinstance(b[0], int)
                      and last < b[0] <= len(text) and b[1] in pages)
                if not ok:
                    err(f"{where}: bad page break {b!r} (offset must increase and stay inside "
                        f"the text; page must be in the pages file)")
                    break
                last = b[0]
            for m in p.get("marks", []):
                ok = (isinstance(m, list) and len(m) == 3 and isinstance(m[0], int)
                      and isinstance(m[1], int) and 0 <= m[0] < m[1] <= len(text)
                      and m[2] in MARKS)
                if not ok:
                    err(f"{where}: bad mark {m!r} (expected [start, end, one of {sorted(MARKS)}])")
            if "anchor" in p:
                a = p["anchor"]
                if p.get("kind") not in ANCHORED:
                    err(f"{where}: only {sorted(ANCHORED)} passages may carry an anchor")
                elif not (isinstance(a, list) and len(a) == 2 and isinstance(a[1], int)):
                    err(f"{where}: bad anchor {a!r} (expected [passage id, offset])")
                else:
                    anchors.append((where, a))
            if "lang" in p and not LANG.match(str(p["lang"])):
                err(f"{where}: lang must be a three-letter code")
            if "conf" in p and not (isinstance(p["conf"], (int, float)) and 0 <= p["conf"] <= 1):
                err(f"{where}: conf must be a number between 0 and 1")
            if "checked" in p and not isinstance(p["checked"], bool):
                err(f"{where}: checked must be true or false")
            if "ref" in p and not (isinstance(p["ref"], str) and p["ref"]):
                err(f"{where}: ref must be a non-empty string")
    for where, (target, offset) in anchors:
        if target not in seen or not 0 <= offset <= seen[target]:
            err(f"{where}: anchor points outside the text ({target!r}, {offset})")
    return len(order), chars, kinds


def check(folder, sub="text", indent="  "):
    """Verify the shape of one version folder's text/ or work/raw/. Returns the list of problems."""
    problems = []
    vdir = Path(folder) if (Path(folder) / sub).is_dir() else DATA / Path(folder).name
    folder, tdir = vdir.resolve().name, vdir / sub
    if not tdir.is_dir():
        return [f"no {sub}/ folder in works/{folder}"]
    texts = sorted(tdir.glob("*.jsonl"))
    if not texts:
        problems.append("no <lang>.jsonl file")
    for path in texts:
        lang = path.stem
        if not LANG.match(lang):
            problems.append(f"{path.name}: file name must be a three-letter language code")
        check_info(tdir / f"{lang}.info.json", lang, folder, problems.append)
        pages = check_pages(tdir / f"{lang}.pages.csv", problems.append)
        images = tdir / f"{lang}.page_images.csv"
        if images.exists():
            if sub != "text":
                problems.append(f"{images.name} belongs in text/ only")
            else:
                k = check_images(images, pages, problems.append)
                print(f"{indent}{sub}/{images.name}: {k} of {len(pages)} pages have an image")
        n, chars, kinds = check_text(path, pages, problems.append)
        detail = ", ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: str(x[0])))
        print(f"{indent}{sub}/{path.name}: {n} passages, {chars} characters ({detail})")
    return problems
