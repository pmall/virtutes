#!/usr/bin/env python3
"""Make the repaired text of Wellmann's Dioscorides from the raw extraction.

Run:  uv run convert/repair_grc.py   (no arguments; reads work/raw/, written by
      convert/extract_grc.py; writes text/grc.jsonl, text/grc.info.json, text/grc.pages.csv
      and work/grc.repairs.csv)

Second step, after convert/extract_grc.py. The raw text keeps every mistake of the typed file. This script
corrects them by the rules below. A rule never changes the words of the work: rules 1-5
change only `ref`, rule 6 only `page`. Every change is written as one row of work/grc.repairs.csv (passage,
rule, field, before, after). The full list of passages each rule changes is also kept in
this file, in CASES at the end, so that the repairs can be read without running anything;
the script stops if its rules do not give exactly CASES.

HOW A WRONG LABEL IS RECOGNISED
Wellmann prints the chapter number at the start of each chapter ("164 κυκλάμινος…") and
section numbers in the margin; the typists kept both in the words. Book 1 has chapters 1 to
129, book 2 1 to 186, book 3 1 to 158, book 4 1 to 192, book 5 1 to 162, in order. A label
is wrong when it contradicts these printed numbers or this order. After the rules, the
script verifies that in each book the chapters follow 1, 2, 3 … without a gap or a repeat
(the RV chapters of rule 1 aside), and stops otherwise.

THE RULES, in the order they run
1. rv_chapter: chapters of the "RV" tradition. Wellmann prints, at ten places, a chapter as
   transmitted by the manuscripts he calls RV, beginning "N RV:" and usually in square
   brackets (the typed file marks them del, wholly or in part). They stay kind text, as
   printed in the main text block. They get the ref "book.N" of the printed number N,
   without section, from the "N RV:" passage up to the next passage beginning with a
   chapter number (a number of at least N; a smaller one is a section number). The
   typists had labelled six of them with the chapter before (e.g. "178 RV" as 2.177) or
   with letters (3.73a). Decided with the user.
2. section_label: section labels with a typing slip, fixed one by one: 4.93.91 -> 4.93.1,
   4.157.2s -> 4.157.2, 4.164.22 -> 4.164.2, 3.73b -> 3.73 (Wellmann's chapter 73; the
   bracketed RV chapter before it, also numbered 73, is rule 1), 5.11.2a -> 5.11.2 and
   5.11.2b -> 5.11.3 (checked on the page image: page 14 of volume 3 prints 3 in the margin;
   the typed words of the passage begin with "2", which stays as typed), and the second
   passage of 1.127.1, whose printed number is 2 -> 1.127.2.
3. chapter_start: a chapter the typists did not open. A passage that begins with the
   printed number N+1 while labelled chapter N starts chapter N+1; the passages after it
   with the same label follow it. Five chapters: 2.66, 2.145, 2.149, 4.151, 5.132. Their
   sections keep their numbers (2.148.2 -> 2.149.2); the first passage gets section 1 only
   if later passages of the chapter have sections.
4. stray_chapter: a chapter label that belongs to no chapter around it. Inside chapter N,
   a run of passages labelled X, where the passage before is in chapter N and the passage
   after in chapter N or N+1, and X is neither: the run belongs to chapter N; the last
   number of its label is its section. In each case the passages hold the section numbers
   printed by Wellmann for chapter N. Nine places: 1.101, 1.123, 2.49, 2.74, 2.164, 2.166,
   4.182, 5.109, 5.123 (e.g. 2.112.2-4 -> 2.164.2-4, 5.4 -> 5.109.4).
5. note_ref: a footnote takes the ref of the passage it is anchored to (in the raw text
   every note had its host's ref; rules 1-4 change the host only).
6. page_83: in volume 1 the typed file numbers page 83 as 89 (it reads 82, 89, 84 … 89).
   Checked on the scan: image 97 prints 83 and holds the start of chapter 1.89, which the
   typed file puts on its first page 89. That page becomes v1p83 (printed 83), and the
   second page 89, v1p89-2 in the raw text, becomes v1p89.

SOURCE FILES NEEDED: none. This script reads work/raw/ only. Two rules were decided after
looking at a page image (2 and 6), but running them does not open the scans. Linking the
pages to their images is the separate, optional convert/images_grc.py; this script never
touches its result.

NOT REPAIRED (the words are not changed by rules)
- Numbers typed inside sentences where the margin number stood, and 13 sections whose
  printed number is missing from the typed words.
- Footnotes stay anchored where the typists put them, and their three sorts (plant-name
  lists, parallel passages, variant readings) are not separated.
"""
import csv, json, re, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
RAW = VDIR / "work" / "raw"
TEXT = VDIR / "text"
LANG = "grc"
CHAPTERS = {"1": 129, "2": 186, "3": 158, "4": 192, "5": 162}   # Wellmann's chapters per book

LEAD = re.compile(r"^\W*(\d+)(?= )")                  # printed number at the start
RV = re.compile(r"^\W*(\d+) RV:")


def chapter(ref):
    return ref.split(".")[1] if ref and ref.count(".") >= 1 else None


def set_ref(p, new, rule, log):
    if p["ref"] != new:
        log(p["id"], rule, "ref", p["ref"], new)
        p["ref"] = new


def texts(passages):
    return [p for p in passages if p["kind"] == "text"]


# ---------------------------------------------------------------------------- rules
def rv_chapter(passages, log):
    rv = set()
    run = None                                  # (book, N) while inside an RV chapter
    for p in texts(passages):
        m, lead = RV.match(p["text"]), LEAD.match(p["text"])
        if m:
            run = (p["ref"].split(".")[0], m.group(1))
        elif run and lead and int(lead.group(1)) >= int(run[1]):
            run = None                          # a chapter begins (a smaller number is a section)
        if run:
            set_ref(p, f"{run[0]}.{run[1]}", "rv_chapter", log)
            rv.add(p["id"])
    return rv


SECTION_LABELS = {"4.93.91": "4.93.1", "4.157.2s": "4.157.2", "4.164.22": "4.164.2",
                  "3.73b": "3.73", "5.11.2a": "5.11.2", "5.11.2b": "5.11.3"}


def section_label(passages, log):
    for p in texts(passages):
        if p["ref"] in SECTION_LABELS:
            set_ref(p, SECTION_LABELS[p["ref"]], "section_label", log)
        elif p["ref"] == "1.127.1" and p["text"].startswith("2 "):
            set_ref(p, "1.127.2", "section_label", log)


def chapter_start(passages, log, rv):
    T = [p for p in texts(passages) if p["id"] not in rv]
    i = 0
    while i < len(T):
        p = T[i]
        m = LEAD.match(p["text"])
        parts = p["ref"].split(".")
        # a printed N+1 that is not this passage's own section number
        if (m and len(parts) >= 2 and parts[1].isdigit() and int(m.group(1)) == int(parts[1]) + 1
                and (len(parts) < 3 or m.group(1) != parts[2])):
            book, new = parts[0], m.group(1)
            group = [p]
            j = i + 1                           # followers: same chapter label, no new chapter
            while (j < len(T) and chapter(T[j]["ref"]) == parts[1]
                   and not ((n := LEAD.match(T[j]["text"])) and int(n.group(1)) >= int(new))):
                group.append(T[j])
                j += 1
            sectioned = any(len(q["ref"].split(".")) == 3 and q["ref"] != p["ref"] for q in group)
            for q in group:
                qp = q["ref"].split(".")
                sec = qp[2] if len(qp) == 3 and sectioned else None
                set_ref(q, f"{book}.{new}" + (f".{sec}" if sec else ""), "chapter_start", log)
            i = j
        else:
            i += 1


def stray_chapter(passages, log, rv):
    T = [p for p in texts(passages) if p["id"] not in rv and chapter(p["ref"]) not in (None, "preface")]
    i = 1
    while i < len(T):
        book, n = T[i - 1]["ref"].split(".")[0], int(chapter(T[i - 1]["ref"]))
        j = i                                   # the run of labels that are neither n nor n+1
        while (j < len(T) and T[j]["ref"].split(".")[0] == book
               and int(chapter(T[j]["ref"])) not in (n, n + 1)):
            j += 1
        if j > i and j < len(T) and T[j]["ref"].split(".")[0] == book:
            for q in T[i:j]:
                sec = q["ref"].split(".")[-1]
                set_ref(q, f"{book}.{n}.{sec}", "stray_chapter", log)
            i = j
        else:
            i += 1


def note_ref(passages, log):
    by_id = {p["id"]: p for p in passages}
    for p in passages:
        if "anchor" in p:
            host = by_id[p["anchor"][0]]
            set_ref(p, host["ref"], "note_ref", log)


PAGE_IDS = {"v1p89": "v1p83", "v1p89-2": "v1p89"}     # rule 6, applied in this order


def page_83(passages, pages, log):
    for old, new in PAGE_IDS.items():
        for row in pages:
            if row["page"] == old:
                row["page"] = new
                row["printed"] = new.split("p")[1]
        for p in passages:
            if p["page"] == old:
                log(p["id"], "page_83", "page", old, new)
                p["page"] = new
            for b in p.get("breaks", []):
                if b[1] == old:
                    log(p["id"], "page_83", "breaks", old, new)
                    b[1] = new


# ---------------------------------------------------------------------------- checks
def check_order(passages, rv):
    """Each book: chapters 1..n in order, no gap, no repeat (RV chapters aside)."""
    seen = {}
    for p in texts(passages):
        if p["id"] in rv:
            continue
        book, ch = p["ref"].split(".")[0], chapter(p["ref"])
        if ch in (None, "preface"):
            continue
        run = seen.setdefault(book, [])
        if not run or run[-1] != ch:
            run.append(ch)
    for book, n in CHAPTERS.items():
        if seen.get(book) != [str(k) for k in range(1, n + 1)]:
            sys.exit(f"book {book}: chapters not 1..{n} in order after repair")


def main():
    if not (RAW / f"{LANG}.jsonl").exists():
        sys.exit("work/raw/ is missing: run convert/extract_grc.py first")
    with open(RAW / f"{LANG}.jsonl", encoding="utf-8") as f:
        passages = [json.loads(line) for line in f]
    info = json.load(open(RAW / f"{LANG}.info.json", encoding="utf-8"))
    with open(RAW / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    repairs = []
    log = lambda *row: repairs.append(row)
    rv = rv_chapter(passages, log)
    section_label(passages, log)
    chapter_start(passages, log, rv)
    stray_chapter(passages, log, rv)
    note_ref(passages, log)
    check_order(passages, rv)
    page_83(passages, pages, log)
    if len({row["page"] for row in pages}) != len(pages):
        sys.exit("page ids repeated after repair")

    found = [f"{i} {r} {b} -> {a}" for i, r, f, b, a in repairs
             if r not in ("note_ref", "page_83")]
    if found != CASES.split("\n")[1:-1]:
        sys.exit("the rules do not give exactly the CASES listed in this script:\n"
                 + "\n".join(found))

    TEXT.mkdir(exist_ok=True)
    with open(TEXT / f"{LANG}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(TEXT / f"{LANG}.pages.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pages[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(pages)
    info["converter"] = str((VDIR / "convert" / "repair_grc.py").relative_to(ROOT))
    info["notes"] = NOTES
    with open(TEXT / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    with open(VDIR / "work" / f"{LANG}.repairs.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "rule", "field", "before", "after"])
        w.writerows(repairs)
    counts = {}
    for row in repairs:
        counts[row[1]] = counts.get(row[1], 0) + 1
    print(f"{len(passages)} passages, {len(repairs)} repairs: "
          + ", ".join(f"{k} {v}" for k, v in counts.items()))


NOTES = (
    "Words, numbers and marks as First1KGreek typed them, errors included; only the "
    "labels (ref) were repaired, by the rules in convert/repair_grc.py, which lists every "
    "passage changed. After repair the chapters of each book run 1 to 129, 186, 158, 192 "
    "and 162 in order. "
    "Chapter and section numbers printed by Wellmann are part of the text, as typed, "
    "sometimes inside a sentence; 13 sections lack their printed number. "
    "Ten chapters of the RV tradition, printed by Wellmann in the main text (mostly in "
    "square brackets, marked del), are kind text with the ref of their printed number and "
    "no section; they share that ref with Wellmann's own chapter. "
    "Four invisible control characters (U+008D) in footnotes were dropped. "
    "All footnotes are kind 'note': the typed file does not separate the lists of plant "
    "names (RV), the parallel passages (SIM., EXC.) and the variant readings, and they are "
    "not separated here. A note is anchored where the typists put it, usually the end of "
    "its printed page, not the word it comments. "
    "The typed file numbers page 83 of volume 1 as 89; corrected to v1p83 after reading "
    "the page image."
)

# Every passage whose ref the rules change (footnotes following their host aside):
# id, rule, ref before -> ref after. Filled from the rules' output, then checked at each run.
CASES = """
002239 rv_chapter 2.177 -> 2.178
002240 rv_chapter 2.177 -> 2.178
002950 rv_chapter 3.63.1 -> 3.64
002951 rv_chapter 3.63.1 -> 3.64
002952 rv_chapter 3.63.2 -> 3.64
002953 rv_chapter 3.63.2 -> 3.64
002954 rv_chapter 3.63.2 -> 3.64
003032 rv_chapter 3.73a.1 -> 3.73
003033 rv_chapter 3.73a.2 -> 3.73
003034 rv_chapter 3.73a.2 -> 3.73
003912 rv_chapter 4.15.2 -> 4.16
004215 rv_chapter 4.57 -> 4.58
004221 rv_chapter 4.57 -> 4.58
005376 rv_chapter 4.189.2 -> 4.190
001011 section_label 1.127.1 -> 1.127.2
003039 section_label 3.73b -> 3.73
004539 section_label 4.93.91 -> 4.93.1
005048 section_label 4.157.2s -> 4.157.2
005121 section_label 4.164.22 -> 4.164.2
005510 section_label 5.11.2a -> 5.11.2
005511 section_label 5.11.2b -> 5.11.3
001341 chapter_start 2.65 -> 2.66
001342 chapter_start 2.65 -> 2.66
001951 chapter_start 2.144 -> 2.145
001973 chapter_start 2.148.1 -> 2.149.1
001986 chapter_start 2.148.2 -> 2.149.2
001987 chapter_start 2.148.3 -> 2.149.3
004996 chapter_start 4.150.7 -> 4.151
006246 chapter_start 5.131 -> 5.132
006247 chapter_start 5.131 -> 5.132
000787 stray_chapter 1.68.2 -> 1.101.2
000788 stray_chapter 1.68.3 -> 1.101.3
000789 stray_chapter 1.68.3 -> 1.101.3
000792 stray_chapter 1.68.4 -> 1.101.4
000985 stray_chapter 1.2 -> 1.123.2
001272 stray_chapter 2.2 -> 2.49.2
001405 stray_chapter 2.2 -> 2.74.2
002113 stray_chapter 2.112.2 -> 2.164.2
002114 stray_chapter 2.112.3 -> 2.164.3
002117 stray_chapter 2.112.4 -> 2.164.4
002128 stray_chapter 2.106.2 -> 2.166.2
002135 stray_chapter 2.106.3 -> 2.166.3
002140 stray_chapter 2.106.4 -> 2.166.4
005308 stray_chapter 4.136.2 -> 4.182.2
005309 stray_chapter 4.136.3 -> 4.182.3
005312 stray_chapter 4.136.4 -> 4.182.4
006094 stray_chapter 5.4 -> 5.109.4
006188 stray_chapter 5.2 -> 5.123.2
006189 stray_chapter 5.3 -> 5.123.3
"""

if __name__ == "__main__":
    main()
