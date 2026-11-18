#!/usr/bin/env python3
"""Make the repaired text of Bostock and Riley's English Pliny from the raw extraction.

Run:  uv run convert/repair_eng.py   (no arguments; reads work/raw/, written by
      convert/extract_eng.py; writes text/eng.jsonl, text/eng.info.json, text/eng.pages.csv
      and work/eng.repairs.csv)

Second step, after convert/extract_eng.py. The raw text keeps every mistake of the typed
file. This script corrects them by the rules below. A rule never changes the words of the
work: rules 1, 3, 4 and 6 change only `ref`, rule 2 `kind` and `ref`, rule 5 only `page`.
Every change is written as one row of work/eng.repairs.csv (passage, rule, field, before,
after). The passages changed by rules 1 and 5 are also listed in CASES at the end, and
the number changed by rules 2, 3 and 4 in COUNTS, so that the repairs can be read without
running anything; the script stops if its rules do not give exactly these.

THE RULES, in the order they run
1. misnumbered_chapter: a chapter labelled X between chapters A and A+2 of the same book,
   X not A+1: it is chapter A+1. The typed file gives the same wrong number in the div and
   in the printed head, a digit lost or misread: 7."7" (17), 16."60" (66), 16."8" (84),
   27."11" (111), 34."3" (31). The head keeps its words ("CHAP. 7.").
2. paratext: passages that are not the work, typed by Perseus as paragraphs of a chapter,
   become kind paratext and lose their ref: the translators' note on the chapters at the
   head of book 2 ("[I have adopted the division ..."); and, from the paragraph named in
   PARATEXT_FROM to the end of the book, the list of corrections to volume 1 at the end
   of book 5 and the errata of volume 1 at the end of book 10, the printer's line at the
   end of book 17 (end of volume 3), the translators' afterword at the end of book 27
   ("*** Before quitting the Botanical Books ...").
3. book1_summary: at the end of each of books 2-37 the translators print the part of
   Pliny's book 1 that concerns it (the summary of facts, the lists of authors quoted);
   Perseus typed it in the last chapter. From the first paragraph of that chapter that
   begins with "Summary" to the end of the book (paratext aside), the ref becomes
   "1.<book>", as in the Latin text (3_Pliny_original_Mayhoff) where the summary of book N
   is 1.N.
4. preface_ref: the dedication (book 1, chapter "dedication" in the typed file) is Pliny's
   preface: its ref becomes "praef", the prefix the Latin text gives it.
5. volume2_first_page: the one page marker without number before book 6 is page 1 of
   volume 2 (the raw text calls it v2t; the next marker is page 2). Seen on the scan:
   image 19 of naturalhistoryof00plin_jp2.zip is the first page of book VI, without
   printed number, image 20 is printed 2. Page v2t becomes v2p1, printed number 1.
6. note_ref: a note takes the ref of the passage it is anchored to, or none if that has
   none (in the raw text every note had its host's ref; rules 1-4 change the host only).

SOURCE FILES NEEDED: none. This script reads work/raw/ only. Linking the pages to their
images is the separate, optional convert/images_eng.py; this script never touches its result.

NOT REPAIRED (they would need the page images or a change of words)
- Book 32 has no chapter 35: its text is presumably inside chapter 34 (not looked into).
- Book 14 chapter 1 is printed "CHAPS. 1 & 2.": both chapters are labelled 14.1.
- Book 3 chapter 0 is the introduction of book 3, as typed.
- Books 33 and 37 have one chapter more (58) and one less (77) than the older chapters of
  the Latin text (57 and 78); where they differ was not looked into.
- Words: Perseus' text was read from the printed book and keeps misreadings (e.g. the head
  of 16.66, "TET REEDOF ORCHOMENTFS"); none is corrected.
"""
import csv, json, re, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
RAW = VDIR / "work" / "raw"
TEXT = VDIR / "text"
LANG = "eng"
MAIN = ("text", "head")
PARATEXT_FROM = {"5": "APPENDIX OF CORRECTIONS.", "10": "ERRATA IN VOL. I.",
                 "17": "J. BILLING, PRINTER", "27": "*** Before quitting the Botanical Books"}
BOOK2_NOTE = "[I have adopted the division of the chapters from Hardouin"
SUMMARY = re.compile(r"summary", re.I)


def set_field(p, field, new, rule, log):
    log(p["id"], rule, field, p.get(field, ""), new)
    if new == "":
        del p[field]
    else:
        p[field] = new


def split(ref):
    book, _, chap = ref.partition(".")
    return book, chap


def number(label):
    return int(label) if label and label.isdigit() else None


def chapter_runs(passages):
    """Consecutive main passages grouped by (book, chapter): [book, chapter, [passages]]."""
    out = []
    for p in passages:
        if p["kind"] not in MAIN or "." not in p.get("ref", ""):
            continue
        book, chap = split(p["ref"])
        if out and out[-1][0] == book and out[-1][1] == chap:
            out[-1][2].append(p)
        else:
            out.append([book, chap, [p]])
    return out


def misnumbered_chapter(passages, log):
    rs = chapter_runs(passages)
    for i in range(1, len(rs) - 1):
        before, this, after = rs[i - 1], rs[i], rs[i + 1]
        if not before[0] == this[0] == after[0]:
            continue
        a, x, c = number(before[1]), number(this[1]), number(after[1])
        if a is not None and c == a + 2 and x != a + 1:
            for p in this[2]:
                set_field(p, "ref", f"{this[0]}.{a + 1}", "misnumbered_chapter", log)


def book_of(p):
    return split(p["ref"])[0] if "ref" in p else None


def paratext(passages, log):
    current = None                             # the book whose paratext runs to its end
    for p in passages:
        if p["kind"] not in MAIN:
            continue
        book = book_of(p)
        if current is not None and book != current:
            current = None
        start = PARATEXT_FROM.get(book)
        if p["kind"] == "text" and start and p["text"].startswith(start):
            current = book
        if current is not None or (p["kind"] == "text" and p.get("ref") == "2"
                                   and p["text"].startswith(BOOK2_NOTE)):
            set_field(p, "kind", "paratext", "paratext", log)
            set_field(p, "ref", "", "paratext", log)


def book1_summary(passages, log):
    last = {}                                  # book -> its last chapter
    for p in passages:
        if p["kind"] in MAIN and "." in p.get("ref", ""):
            last[book_of(p)] = p["ref"]
    current = None
    for p in passages:
        if p["kind"] not in MAIN:
            continue
        if p["kind"] == "paratext" or "ref" not in p:
            continue
        book = book_of(p)
        if current is not None and book != current:
            current = None
        if (current is None and book not in ("1", "praef") and p["kind"] == "text"
                and p["ref"] == last.get(book) and SUMMARY.match(p["text"])):
            current = book
        if current is not None:
            set_field(p, "ref", f"1.{book}", "book1_summary", log)


def preface_ref(passages, log):
    for p in passages:
        if p["kind"] in MAIN and p.get("ref") == "1.dedication":
            set_field(p, "ref", "praef", "preface_ref", log)


def volume2_first_page(passages, pages, log):
    old, new = "v2t", "v2p1"
    for p in passages:
        if p["page"] == old:
            set_field(p, "page", new, "volume2_first_page", log)
        for b in p.get("breaks", []):
            if b[1] == old:
                log(p["id"], "volume2_first_page", "breaks", old, new)
                b[1] = new
    rows = [row for row in pages if row["page"] == old]
    if len(rows) != 1:
        sys.exit("page v2t: not found once in the pages")
    rows[0].update({"page": new, "volume": "2", "printed": "1"})


def note_ref(passages, log):
    by_id = {p["id"]: p for p in passages}
    for p in passages:                       # hosts come before their notes
        if "anchor" in p:
            host = by_id[p["anchor"][0]]
            if host.get("ref") != p.get("ref"):
                set_field(p, "ref", host.get("ref", ""), "note_ref", log)


def check_order(passages, pages):
    """After the rules, the chapters of each book are numbers and never go backwards."""
    rs = chapter_runs(passages)
    for a, b in zip(rs, rs[1:]):
        if a[0] == b[0] and a[0] not in ("1",) and number(b[1]) is not None \
                and number(a[1]) is not None and number(b[1]) <= number(a[1]):
            sys.exit(f"chapter {b[0]}.{b[1]} comes after {a[0]}.{a[1]}")
    for book, chap, ps in rs:
        if book not in ("1",) and number(chap) is None:
            sys.exit(f"chapter label {book}.{chap} is not a number after repair")
    if any(p["page"].endswith("t") for p in passages):
        sys.exit("a page without number is left")
    if len({row["page"] for row in pages}) != len(pages):
        sys.exit("page ids repeated after repair")


def main():
    if not (RAW / f"{LANG}.jsonl").exists():
        sys.exit("work/raw/ is missing: run convert/extract_eng.py first")
    with open(RAW / f"{LANG}.jsonl", encoding="utf-8") as f:
        passages = [json.loads(line) for line in f]
    info = json.load(open(RAW / f"{LANG}.info.json", encoding="utf-8"))
    with open(RAW / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    repairs = []
    log = lambda *row: repairs.append(row)
    misnumbered_chapter(passages, log)
    paratext(passages, log)
    book1_summary(passages, log)
    preface_ref(passages, log)
    volume2_first_page(passages, pages, log)
    note_ref(passages, log)
    check_order(passages, pages)

    counts = {}
    for row in repairs:
        if row[2] in ("ref", "kind"):
            counts[(row[1], row[2])] = counts.get((row[1], row[2]), 0) + 1
    got = {f"{r} {f}": n for (r, f), n in counts.items() if r in ("paratext", "book1_summary", "preface_ref")}
    if got != COUNTS:
        sys.exit(f"rules 2, 3 and 4 changed {got}, not {COUNTS}")
    found = [f"{i} {r} {b} -> {a}" for i, r, f, b, a in repairs
             if r in ("misnumbered_chapter", "volume2_first_page")]
    if found != CASES.split("\n")[1:-1]:
        sys.exit("the rules do not give exactly the CASES listed in this script:\n"
                 + "\n".join(found))

    TEXT.mkdir(exist_ok=True)
    with open(TEXT / f"{LANG}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(TEXT / f"{LANG}.pages.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["page", "volume", "printed"], lineterminator="\n")
        w.writeheader()
        w.writerows(pages)
    info["converter"] = str((VDIR / "convert" / "repair_eng.py").relative_to(ROOT))
    info["notes"] = NOTES
    with open(TEXT / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    with open(VDIR / "work" / f"{LANG}.repairs.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "rule", "field", "before", "after"])
        w.writerows(repairs)
    per_rule = {}
    for row in repairs:
        per_rule[row[1]] = per_rule.get(row[1], 0) + 1
    print(f"{len(passages)} passages, {len(pages)} pages, {len(repairs)} repairs: "
          + ", ".join(f"{k} {v}" for k, v in per_rule.items()))


NOTES = (
    "Words, numbers and marks as Perseus typed them, errors included; only the labels "
    "(ref, kind, page) were repaired, by the rules in convert/repair_eng.py, which lists "
    "every passage changed. "
    "ref is book.chapter, Hardouin's chapters as printed by the translators (the same "
    "numbers as the older chapters of the Latin text, field x_old_chapter of "
    "3_Pliny_original_Mayhoff); the translation has no section numbers. The dedication is "
    "'praef'; the summary and lists of authors printed at the end of book N, which are "
    "Pliny's book 1, are '1.<N>'. "
    "Book 32 has no chapter 35 (its text is presumably in chapter 34); book 14 chapter 1 "
    "covers chapters 1 and 2, as printed; book 3 chapter 0 is the introduction. Books 33 and "
    "37 have 58 and 77 chapters, the Latin text 57 and 78: where they differ was not looked "
    "into. "
    "The errata of volume 1, the printer's line ending volume 3, and the translators' notes "
    "at the head of book 2 and at the end of book 27 are paratext. The front matter of the "
    "volumes (pages in Roman numerals) is not in the typed file. "
    "Greek is in Beta Code, as typed. Perseus' '<*>' (a character it could not read) is "
    "kept. The entity &cdot; is read as '·', the decimal point. A hyphen at the end of a "
    "typed line is kept and the word written together ('na-ture'), since the typed file does "
    "not tell a word cut at the end of a line from a hyphenated word. Tables are written as "
    "their cells in order, separated by spaces. One note keeps both the printed word and "
    "Perseus' correction, as typed ('rings kings', book 37). "
    "The page numbers were checked against the scans only where convert/images_eng.py says."
)

COUNTS = {"paratext kind": 43, "paratext ref": 43, "book1_summary ref": 115,
          "preface_ref ref": 49}

# Every passage whose label rules 1 and 5 change (notes following their host aside):
# id, rule, label before -> after. Filled from the rules' output, then checked at each run.
CASES = """
006470 misnumbered_chapter 7.7 -> 7.17
006471 misnumbered_chapter 7.7 -> 7.17
006475 misnumbered_chapter 7.7 -> 7.17
013154 misnumbered_chapter 16.60 -> 16.66
013155 misnumbered_chapter 16.60 -> 16.66
013166 misnumbered_chapter 16.60 -> 16.66
013169 misnumbered_chapter 16.60 -> 16.66
013176 misnumbered_chapter 16.60 -> 16.66
013333 misnumbered_chapter 16.8 -> 16.84
013334 misnumbered_chapter 16.8 -> 16.84
013337 misnumbered_chapter 16.8 -> 16.84
013340 misnumbered_chapter 16.8 -> 16.84
022240 misnumbered_chapter 27.11 -> 27.111
022241 misnumbered_chapter 27.11 -> 27.111
026426 misnumbered_chapter 34.3 -> 34.31
026427 misnumbered_chapter 34.3 -> 34.31
005184 volume2_first_page v2t -> v2p1
005185 volume2_first_page v2t -> v2p1
005186 volume2_first_page v2t -> v2p1
005187 volume2_first_page v2t -> v2p1
005188 volume2_first_page v2t -> v2p1
005189 volume2_first_page v2t -> v2p1
005190 volume2_first_page v2t -> v2p1
"""

if __name__ == "__main__":
    main()
