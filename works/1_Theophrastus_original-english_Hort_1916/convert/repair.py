#!/usr/bin/env python3
"""Make the repaired text of Hort's Greek Theophrastus from the raw extraction.

Run:  uv run convert/repair.py   (no arguments; reads work/raw/, written by
      convert/extract.py; writes text/grc.jsonl, text/grc.info.json, text/pages.csv
      and work/repairs.csv)

Second step, after convert/extract.py. The raw text keeps every mistake of the typed file.
This script corrects them by the rules below. A rule never changes the words of the work:
it changes `ref`, `page`, or where a passage is cut. Every change is written as one row of
work/repairs.csv (passage, rule, field, before, after).

HOW THE MISTAKES WERE FOUND
The chapters of the typed file are those of the book: each book's chapters run 1 to 14, 8,
18, 16, 9, 8, 15, 11, 20 in order, and each opens with its printed number (Ι., ΙΙ. …). Two
section labels break the order 1, 2, 3 … of their chapter (7.3, 7.4). The page numbers were
compared with the scan (source/Theophrastus_Enquiry_Plants_Loeb.pdf): the first words
of each typed page were looked for in the PDF's own text layer at the expected image, and
the pages that did not match were looked at. One page number is wrong. The script itself
does not open the scan.

THE RULES, in the order they run
1. section_label: 7.4.5s -> 7.4.5, a typing slip (one passage). Page 84 of volume 2 prints
   5 in the margin at the start of this passage ("Ὡσαύτως").
2. section_7_3_4: the typed file has no section 4 in chapter 7.3. Page 78 of volume 2
   prints 4 in the margin at "ἅπαντα δὲ ξηρανθέντα", inside the passage labelled 7.3.3
   that begins "Δυσξήραντα"; the two passages after it, labelled 7.3.3, come before the
   printed 5. The passage is cut before "ἅπαντα δὲ ξηρανθέντα" (the editor's addition
   marked add that runs over the cut becomes two marks); its second part and the two
   passages after it become 7.3.4. Footnotes keep their place: the three anchored in this
   passage sit before the cut.
3. page_216: in volume 2 the typed file numbers page 216 as 214 (it reads 212, 214, 218).
   On the scan, the image after page 213 is blank, the next prints "BOOK IX" and the next
   prints 216 and holds the start of book 9, which the typed file puts on its page 214.
   That page becomes v2p216 (printed 216).
4. renumber: after the cut of rule 2 the passages are numbered again 000001, 000002 … in
   reading order, and the anchors of the notes follow. Logged once, as a count, not per
   passage.

After the rules the script verifies that the chapters of each book, and the sections of
each chapter, follow 1, 2, 3 … without a gap or a repeat, and stops otherwise.

SOURCE FILES NEEDED: none. This script reads work/raw/ only. Rules 1-3 were decided
after looking at page images, but running them does not open the scan.

NOT REPAIRED (the words are not changed by rules)
- Five passages begin with their section number typed as a word (2.2.8, 2.2.11, 2.3.3,
  3.4.4, 3.13.3).
- Typing slips in the words, e.g. Latin letters among Greek in the title heads
  ("ΘEOΦPAΣTOΥ") and in some chapter numbers, "“0 τε" for "Ὅ τε" (3.18.3), and the
  passage of 9.20.5 beginning "δ᾿ ἕλμις" whose first word is missing.
- Footnotes are all kind note: variant readings and Hort's explanations are printed
  together under the Greek and are not separated. A note is anchored where the typists put
  it, at the end of its printed page, not at the word it comments.
"""
import csv, json, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
RAW = VDIR / "work" / "raw"
TEXT = VDIR / "text"
LANG = "grc"
CHAPTERS = [14, 8, 18, 16, 9, 8, 15, 11, 20]          # chapters of books 1-9


def set_field(p, field, new, rule, log):
    if p[field] != new:
        log(p["id"], rule, field, p[field], new)
        p[field] = new


# ---------------------------------------------------------------------------- rules
def section_label(passages, log):
    for p in passages:
        if p["kind"] == "text" and p["ref"] == "7.4.5s":
            set_field(p, "ref", "7.4.5", "section_label", log)


SECTION_4_AT = "ἅπαντα δὲ ξηρανθέντα"


def section_7_3_4(passages, log):
    """Cut the passage holding the start of 7.3.4; label 7.3.4 up to section 5."""
    T = [i for i, p in enumerate(passages) if p["kind"] == "text" and p["ref"] == "7.3.3"]
    hosts = [i for i in T if SECTION_4_AT in passages[i]["text"]]
    if len(hosts) != 1:
        sys.exit("section_7_3_4: the start of section 4 is not in exactly one passage")
    i = hosts[0]
    p = passages[i]
    cut = p["text"].index(SECTION_4_AT)
    if p["text"][cut - 1] != " ":
        sys.exit("section_7_3_4: the cut is not at a word boundary")
    first, second = p["text"][:cut - 1], p["text"][cut:]
    shift = cut                                         # positions in the second part
    new = {"id": p["id"] + "b", "kind": "text", "ref": "7.3.4"}
    page_at_cut = p["page"]
    for pos, pg in p.get("breaks", []):
        if pos <= cut:
            page_at_cut = pg
    new["page"] = page_at_cut
    new["text"] = second
    b1 = [b for b in p.get("breaks", []) if b[0] < len(first)]
    b2 = [[b[0] - shift, b[1]] for b in p.get("breaks", []) if b[0] > cut]
    m1, m2 = [], []
    for s, e, t in p.get("marks", []):
        if s < len(first):
            m1.append([s, min(e, len(first)), t])
        if e > cut:
            m2.append([max(s, cut) - shift, e - shift, t])
    for q in passages:                                  # notes anchored after the cut
        if q.get("anchor", [None])[0] == p["id"] and q["anchor"][1] > len(first):
            sys.exit("section_7_3_4: a note is anchored after the cut")
    log(p["id"], "section_7_3_4", "cut", f"{len(p['text'])} characters",
        f"cut at {cut}: {len(first)} + {len(second)} characters")
    p["text"] = first
    for key, val in (("breaks", b1), ("marks", m1)):
        if val:
            p[key] = val
        else:
            p.pop(key, None)
    if b2:
        new["breaks"] = b2
    if m2:
        new["marks"] = m2
    j = i + 1                                           # after the notes of the passage
    while j < len(passages) and passages[j]["kind"] == "note":
        j += 1
    passages.insert(j, new)
    log(new["id"], "section_7_3_4", "ref", "7.3.3", "7.3.4")
    k = j + 1
    while passages[k]["ref"] == "7.3.3":
        set_field(passages[k], "ref", "7.3.4", "section_7_3_4", log)
        k += 1
    if passages[k]["ref"] != "7.3.5":
        sys.exit("section_7_3_4: section 5 does not follow")


PAGE_IDS = {"v2p214": ("v2p216", "216")}


def page_216(passages, pages, log):
    for old, (new, printed) in PAGE_IDS.items():
        rows = [row for row in pages if row["page"] == old]
        if len(rows) != 1:
            sys.exit(f"page_216: page {old} not found once")
        rows[0]["page"], rows[0]["printed"] = new, printed
        for p in passages:
            if p["page"] == old:
                set_field(p, "page", new, "page_216", log)
            for b in p.get("breaks", []):
                if b[1] == old:
                    log(p["id"], "page_216", "breaks", old, new)
                    b[1] = new


def renumber(passages, log):
    ids = {p["id"]: f"{n:06d}" for n, p in enumerate(passages, 1)}
    changed = sum(1 for old, new in ids.items() if old != new)
    for p in passages:
        p["id"] = ids[p["id"]]
        if "anchor" in p:
            p["anchor"][0] = ids[p["anchor"][0]]
    log("", "renumber", "id", "", f"{changed} passages renumbered")


# ---------------------------------------------------------------------------- checks
def check_order(passages):
    """Chapters 1..n of each book, sections 1..n of each chapter, in order."""
    chapters, sections = {}, {}
    for p in passages:
        if p["kind"] != "text":
            continue
        b, c, s = p["ref"].split(".")
        run = chapters.setdefault(b, [])
        if not run or run[-1] != c:
            run.append(c)
        run = sections.setdefault((b, c), [])
        if not run or run[-1] != s:
            run.append(s)
    if [chapters.get(str(b)) for b in range(1, 10)] != [[str(k) for k in range(1, n + 1)]
                                                        for n in CHAPTERS]:
        sys.exit("chapters not in order after repair")
    for key, run in sections.items():
        if run != [str(k) for k in range(1, len(run) + 1)]:
            sys.exit(f"sections of {'.'.join(key)} not in order after repair: {run}")


def main():
    if not (RAW / f"{LANG}.jsonl").exists():
        sys.exit("work/raw/ is missing: run convert/extract.py first")
    with open(RAW / f"{LANG}.jsonl", encoding="utf-8") as f:
        passages = [json.loads(line) for line in f]
    info = json.load(open(RAW / f"{LANG}.info.json", encoding="utf-8"))
    with open(RAW / "pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    repairs = []
    log = lambda *row: repairs.append(row)
    section_label(passages, log)
    section_7_3_4(passages, log)
    page_216(passages, pages, log)
    renumber(passages, log)
    check_order(passages)

    TEXT.mkdir(exist_ok=True)
    with open(TEXT / f"{LANG}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(TEXT / "pages.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pages[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(pages)
    info["converter"] = str((VDIR / "convert" / "repair.py").relative_to(ROOT))
    info["notes"] = NOTES
    with open(TEXT / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    with open(VDIR / "work" / "repairs.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "rule", "field", "before", "after"])
        w.writerows(repairs)
    counts = {}
    for row in repairs:
        counts[row[1]] = counts.get(row[1], 0) + 1
    print(f"{len(passages)} passages, {len(repairs)} repairs: "
          + ", ".join(f"{k} {v}" for k, v in counts.items()))


NOTES = (
    "Words, numbers and marks as First1KGreek typed them, errors included; only labels "
    "were repaired, by the rules in convert/repair.py: one section label (7.4.5), the "
    "missing section 7.3.4 (one passage cut where the book prints 4), and page 216 of "
    "volume 2, typed as 214. After repair the chapters of books 1-9 run 1 to 14, 8, 18, 16, "
    "9, 8, 15, 11, 20, and the sections of each chapter 1, 2, 3 … in order. "
    "The page numbers were compared with the scan by the first words of each page. "
    "Only the Greek pages are here (even numbers); four page pairs are missing at the "
    "start of books 2-5 and three at the start of books 7-9: a blank page and the book's "
    "title page, checked on the scan. "
    "Chapter numbers printed by Hort are part of the text, as typed, some with Latin "
    "letters for Greek; five passages begin with their section number typed as a word. "
    "Known slips in the words are kept (e.g. the passage of 9.20.5 beginning \"δ᾿ ἕλμις\" "
    "lacks its first word). "
    "All footnotes are kind 'note': Hort's variant readings and his explanations in "
    "English are printed together under the Greek and are not separated; one note may "
    "hold several numbered notes. A note is anchored where the typists put it, at the end "
    "of its printed page, not at the word it comments."
)

if __name__ == "__main__":
    main()
