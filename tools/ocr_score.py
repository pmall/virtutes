#!/usr/bin/env python3
"""Measure how well a machine reading of scan pages matches the reference text of those pages.

Usage, from the workspace folder:
    uv run tools/ocr_score.py [--show] <reference folder> <reading folder> [<reading folder> ...]

    <reference folder>  one text file per page, <page>.txt or <page>.draft.txt (a draft is a
                        reference not yet confirmed by a person; the output says so). A page is
                        written in blocks separated by one empty line: running head, main text,
                        notes, page number (docs/OCR_Kraken_approach.md, "Reference pages");
                        an empty block is an empty line, so a page without page
                        number ends with two empty lines.
    <reading folder>    one text file per page with the same <page> name, <page>.txt: what a
                        reading model (or any other source) gave for that page.
    --show              also list, for each reading, the main-text words it got wrong.

What is measured, over all pages together:
- Main-text words wrong: the share of the words of the main text (second block) that the
  reading misses or gets wrong, plus the words it adds there. This is the measure that matters
  for the project: use records are taken from the words of the main text, so a word wrong there
  can change a plant, a part, a preparation or a virtue. Words are compared as the extraction
  will see them: a word cut by a hyphen at the end of a line is joined again, case is ignored,
  and punctuation and numbers (note numbers) are left out. Printing habits that do not change
  a word are set aside too: long s (ſ) counts as s, a ligature (ﬁ, ﬀ, ﬆ...) as its letters, u and
  v as one letter, i and j as one letter. Abbreviations are compared as written.
- CER, the character error rate on the whole page, every character counted (running head and
  notes included): the number of characters to insert, delete or replace to turn the reading
  into the reference, divided by the number of characters of the reference. A general measure,
  comparable with what other projects publish.
Before comparing, both texts are brought to Unicode composed form (NFC), so that an accented
letter written as one or as two code points counts the same.
"""
import difflib, re, sys, unicodedata
from pathlib import Path

WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
LIGATURES = "ﬀﬁﬂﬃﬄﬅﬆ"
FOLD = str.maketrans({"ſ": "s", "v": "u", "j": "i"})


def words(text):
    text = unicodedata.normalize("NFC", text)
    text = "".join(unicodedata.normalize("NFKC", c) if c in LIGATURES else c for c in text)
    text = re.sub(r"(\w)[-¬]+\s*\n\s*(\w)", r"\1\2", text)  # join a word cut at the line end
    text = "".join(" " if unicodedata.category(c)[0] == "N" else c for c in text)  # numbers, ¹ ²
    return [w.lower().replace("’", "'").translate(FOLD) for w in WORD.findall(text)]


def distance(a, b):
    """Levenshtein distance between two strings."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def references(folder):
    refs = {}
    for f in sorted(Path(folder).glob("*.txt")):
        page = f.name.removesuffix(".txt").removesuffix(".draft")
        text = unicodedata.normalize("NFC", f.read_text(encoding="utf-8"))
        # the file ends with one newline; an empty last block (no page number) leaves "\n\n\n"
        blocks = text.removesuffix("\n").split("\n\n")
        if len(blocks) != 4:
            sys.exit(f"{f}: {len(blocks)} blocks, 4 expected (head, main text, notes, page number)")
        refs[page] = (text, blocks, f.name.endswith(".draft.txt"))
    return refs


def main_text_errors(blocks, reading):
    """Word errors that fall in the main text: (errors, main-text words, list of errors)."""
    ref, tag = [], []
    for k, b in enumerate(blocks):
        w = words(b)
        ref += w
        tag += [k == 1] * len(w)
    hyp = words(reading)
    errors, shown = 0, []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, ref, hyp, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        in_main = any(tag[a1:a2]) if a2 > a1 else (0 < a1 < len(tag) and tag[a1 - 1] and tag[a1])
        if in_main:
            errors += max(a2 - a1, b2 - b1)
            shown.append((" ".join(ref[a1:a2]), " ".join(hyp[b1:b2])))
    return errors, sum(tag), shown


def score(refs, folder):
    err = n = cerr = cn = 0
    shown, missing = [], []
    for page, (text, blocks, _) in refs.items():
        f = Path(folder) / f"{page}.txt"
        if not f.exists():
            missing.append(page)
            continue
        reading = unicodedata.normalize("NFC", f.read_text(encoding="utf-8"))
        e, m, s = main_text_errors(blocks, reading)
        err, n = err + e, n + m
        shown += [(page, a, b) for a, b in s]
        r, h = " ".join(text.split()), " ".join(reading.split())
        cerr, cn = cerr + distance(r, h), cn + len(r)
    return err, n, cerr / cn if cn else float("nan"), shown, missing


def main(argv):
    show = "--show" in argv
    argv = [a for a in argv if a != "--show"]
    if len(argv) < 2:
        sys.exit(__doc__)
    refs = references(argv[0])
    drafts = sum(d for *_, d in refs.values())
    print(f"{len(refs)} reference pages, {drafts} of them drafts not yet confirmed by a person")
    print(f"{'reading':<20} {'main-text words wrong':>22} {'CER (whole page)':>17}")
    details = []
    for folder in argv[1:]:
        err, n, cer, shown, missing = score(refs, folder)
        note = f"  (missing pages: {', '.join(missing)})" if missing else ""
        print(f"{Path(folder).name:<20} {err:>5} of {n:<5} {err / n:>7.2%} {cer:>17.2%}{note}")
        details.append((Path(folder).name, shown))
    if show:
        for name, shown in details:
            print(f"\n{name}:")
            for page, a, b in shown:
                print(f"  {page}  reference [{a}]  reading [{b}]")


if __name__ == "__main__":
    main(sys.argv[1:])
