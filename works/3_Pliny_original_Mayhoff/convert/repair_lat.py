#!/usr/bin/env python3
"""Make the repaired text of Mayhoff's Latin Pliny from the raw extraction.

Run:  uv run convert/repair_lat.py   (no arguments; reads work/raw/, written by
      convert/extract_lat.py; writes text/lat.jsonl, text/lat.info.json, text/lat.pages.csv
      and work/lat.repairs.csv)

Second step, after convert/extract_lat.py. The raw text keeps every mistake of the typed
file. This script corrects them by the rules below. A rule never changes the words of the
work: rules 1-5 change only `ref` or `x_old_chapter`, rule 6 only `page`. Every change is
written as one row of work/lat.repairs.csv (passage, rule, field, before, after). The
passages changed by rules 2, 3, 4 and 6 are also listed in CASES at the end, so that the
repairs can be read without running anything; the script stops if its rules do not give
exactly CASES, or if rule 1 does not change exactly TIDY_COUNT labels.

HOW A WRONG LABEL IS RECOGNISED
Mayhoff numbers the sections (§) of each book 1, 2, 3 … in the margin, and gives the older
chapter numbers 1, 2, 3 … in parentheses in the running heads (x_old_chapter). Mayhoff's
own chapters (x_chapter) are the divs of the typed file and need no repair. A label is wrong when it breaks this order. A passage is labelled by
the last marker before it, so a wrong marker gives a wrong label to every passage up to
the next marker; the rules relabel those passages as a whole. No rule was decided by
looking at a page image.

THE RULES, in the order they run
1. tidy_label: the § part of a ref with a "?" or a space typed by Perseus next to the
   number ("2.31?", "7.79 "). The "?" and the space are dropped.
2. misnumbered_section: a § labelled X between § A and § A+2, X not A+1: it is § A+1.
   Two places: 10.112 -> 10.122 (the digits of 122 in another order) and 11.praef ->
   11.1 (the first § of book 11).
3. stray_section: a § marker between § A and § A+1 whose number is neither (e.g. 147, 139,
   148): it stands inside § A, and the passages it labels belong to it. Seven places: 3.139, 4.14, 8.127, 12.36, 15.66, 16.245, 32.66. What the marker
   stood for in the typed file (a cross-reference, a slip) was not looked into.
4. stray_chapter: the same for the older chapters (x_old_chapter): a marker between
   chapters A and A+1 whose number is neither. Two places, both typed "2": book 14
   between 24 and 25, book 15 between 38 and 39; the passages go to the chapter before.
5. note_ref: a note or marginal note takes the ref of the passage it is anchored to (in
   the raw text every note had its host's ref; rules 1-3 change the host only).
6. volume_title: the three heads giving the title of volumes 2 to 5 ("C. PLINI SECVNDI",
   "NATVRALIS HISTORIAE", "LIBRI VII-XV") are typed before the volume's first page marker,
   so the raw text puts them on the last page of the volume before. They move to the
   front pages of their volume, page "v<volume>t" (printed number empty), listed just
   before page 1, as the title of volume 1 already is. Page v1p523, on which nothing else
   lies, leaves the list of pages.

SOURCE FILES NEEDED: none. This script reads work/raw/ only. Linking the pages to their
images is the separate, optional convert/images_lat.py; this script never touches its result.

NOT REPAIRED (they would need the page images or a change of words)
- Ten § markers are missing from the typed file (2.20, 2.24, 3.49, 16.152, 22.22, 22.54,
  23.27, 33.100, 33.124, 34.51): the text of that § is labelled with the § before.
- Older chapters: the first chapter of books 2, 4, 5 and 6 has no marker (its passages
  have no x_old_chapter), and chapters 20.80 and 24.110 have none either.
- Pages 323 and 432 of volume 2 have no page marker: their text is on the page before.
- Footnotes are anchored where the typists put them; their two sorts (variant readings,
  sources and parallels) are not separated.
"""
import csv, json, re, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
RAW = VDIR / "work" / "raw"
TEXT = VDIR / "text"
LANG = "lat"
TIDY_COUNT = 189
MAIN = ("text", "head")


def split(ref):
    book, _, sec = ref.partition(".")
    return book, sec


def set_field(p, field, new, rule, log):
    log(p["id"], rule, field, p.get(field, ""), new)
    p[field] = new


def runs(passages, key):
    """Consecutive main passages of the books 2-37 grouped by (book, label): [book, label, [passages]]."""
    out = []
    for p in passages:
        if p["kind"] != "text":
            continue
        book, sec = split(p["ref"])
        if book in ("1", "praef"):
            continue
        label = key(p)
        if label is None:
            continue
        if out and out[-1][0] == book and out[-1][1] == label:
            out[-1][2].append(p)
        else:
            out.append([book, label, [p]])
    return out


def section(p):
    return split(p["ref"])[1] or None


def tidy_label(passages, log):
    for p in passages:
        if p["kind"] in MAIN and "ref" in p:
            book, sec = split(p["ref"])
            clean = sec.replace("?", "").replace(" ", "")
            if clean != sec:
                set_field(p, "ref", f"{book}.{clean}", "tidy_label", log)


def number(label):
    return int(label) if label and label.isdigit() else None


def relabel(passages, key, field, rule, log, new_label):
    """Shared walk of rules 2-4: new_label(previous, this, next) gives the label or None."""
    rs = runs(passages, key)
    for i in range(len(rs) - 1):
        this, after = rs[i], rs[i + 1]
        if this[0] != after[0]:
            continue
        # the label before; 0 at the start of a book
        a = number(rs[i - 1][1]) if i and rs[i - 1][0] == this[0] else 0
        new = new_label(a, this[1], number(after[1]))
        if new is None:
            continue
        for p in this[2]:
            if field == "ref":
                set_field(p, "ref", f"{this[0]}.{new}", rule, log)
            else:
                set_field(p, field, new, rule, log)


def misnumbered(a, x, nxt):
    if a is not None and nxt == a + 2 and number(x) != a + 1:
        return str(a + 1)


def stray(a, x, nxt):
    if a is not None and number(x) is not None and number(x) != a + 1 and nxt == a + 1:
        return str(a)


def misnumbered_section(passages, log):
    relabel(passages, section, "ref", "misnumbered_section", log, misnumbered)


def stray_section(passages, log):
    relabel(passages, section, "ref", "stray_section", log, stray)


def stray_chapter(passages, log):
    relabel(passages, lambda p: p.get("x_old_chapter"), "x_old_chapter", "stray_chapter", log, stray)


def note_ref(passages, log):
    by_id = {p["id"]: p for p in passages}
    for p in passages:                       # hosts come before their notes
        if "anchor" in p:
            host = by_id[p["anchor"][0]]
            if host.get("ref") != p.get("ref"):
                set_field(p, "ref", host["ref"], "note_ref", log)


def volume_title(passages, pages, log):
    for i, p in enumerate(passages):
        if p["kind"] == "head" and p["text"].startswith("LIBRI ") and p["page"] != "v1t":
            volume = str(int(p["page"][1:].split("p")[0]) + 1)
            new = f"v{volume}t"
            for q in passages[i - 2:i + 1]:
                if q["kind"] != "head":
                    sys.exit(f"volume title of volume {volume}: not three heads")
                set_field(q, "page", new, "volume_title", log)
            first = next(k for k, row in enumerate(pages) if row["page"] == f"v{volume}p1")
            pages.insert(first, {"page": new, "volume": volume, "printed": ""})
    used = {p["page"] for p in passages} | {b[1] for p in passages for b in p.get("breaks", [])}
    pages[:] = [row for row in pages if row["page"] in used]


def check_order(passages):
    """After the rules, every § label of books 2-37 is a number and none goes backwards."""
    for book, label, ps in runs(passages, section):
        if number(label) is None:
            sys.exit(f"§ label {book}.{label} is not a number after repair")
    rs = runs(passages, section)
    for a, b in zip(rs, rs[1:]):
        if a[0] == b[0] and number(b[1]) <= number(a[1]):
            sys.exit(f"§ {b[0]}.{b[1]} comes after {a[0]}.{a[1]}")
    rs = runs(passages, lambda p: p.get("x_old_chapter"))
    for a, b in zip(rs, rs[1:]):
        if a[0] == b[0] and number(b[1]) <= number(a[1]):
            sys.exit(f"chapter {b[1]} comes after {a[1]} in book {b[0]}")


def main():
    if not (RAW / f"{LANG}.jsonl").exists():
        sys.exit("work/raw/ is missing: run convert/extract_lat.py first")
    with open(RAW / f"{LANG}.jsonl", encoding="utf-8") as f:
        passages = [json.loads(line) for line in f]
    info = json.load(open(RAW / f"{LANG}.info.json", encoding="utf-8"))
    with open(RAW / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    repairs = []
    log = lambda *row: repairs.append(row)
    tidy_label(passages, log)
    misnumbered_section(passages, log)
    stray_section(passages, log)
    stray_chapter(passages, log)
    note_ref(passages, log)
    check_order(passages)
    volume_title(passages, pages, log)
    if len({row["page"] for row in pages}) != len(pages):
        sys.exit("page ids repeated after repair")

    tidy = sum(1 for row in repairs if row[1] == "tidy_label")
    if tidy != TIDY_COUNT:
        sys.exit(f"tidy_label changed {tidy} labels, not {TIDY_COUNT}")
    found = [f"{i} {r} {b} -> {a}" for i, r, f, b, a in repairs
             if r not in ("tidy_label", "note_ref")]
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
    info["converter"] = str((VDIR / "convert" / "repair_lat.py").relative_to(ROOT))
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
    print(f"{len(passages)} passages, {len(pages)} pages, {len(repairs)} repairs: "
          + ", ".join(f"{k} {v}" for k, v in counts.items()))


NOTES = (
    "Words, numbers and marks as Perseus typed them, errors included; only the labels "
    "(ref, x_old_chapter, page) were repaired, by the rules in convert/repair_lat.py, which "
    "lists every passage changed. "
    "ref is book.§ (Mayhoff's sections, the modern citation); the preface of book 1 is "
    "'praef.<§>' and the summary of book N in book 1 is '1.<N>'. A passage is cut at every "
    "§ and at every older chapter, so a cut may fall inside a sentence. Mayhoff's chapter "
    "numbers (printed in bold in the book, not in the words) are in the field x_chapter; "
    "the older chapter numbers, printed in parentheses in the running heads (taken to be "
    "Hardouin's), in x_old_chapter. "
    "Ten § markers are missing from the typed file (2.20, 2.24, 3.49, 16.152, 22.22, 22.54, "
    "23.27, 33.100, 33.124, 34.51): the text of each is labelled with the § before. The "
    "first older chapter of books 2, 4, 5 and 6, and chapters 20.80 and 24.110, have no "
    "marker either. "
    "All footnotes are kind 'note': the typed file does not separate the variant readings "
    "from the sources and parallel passages, and they are not separated here. Six empty "
    "notes of the typed file were dropped. "
    "A few hundred words of the main text are in italics or bold in the typed file; some "
    "look like sigla of the apparatus typed into the text. They are kept, marked 'hi'. "
    "Pages 323 and 432 of volume 2 have no page marker in the typed file: their text is on "
    "the page before. The page numbers of volumes 1, 2 and 5 were not checked against the "
    "scans."
)

# Every passage whose label rules 2, 3, 4 and 6 change (notes following their host aside):
# id, rule, label before -> after. Filled from the rules' output, then checked at each run.
CASES = """
024967 misnumbered_section 10.112 -> 10.122
025764 misnumbered_section 11.praef -> 11.1
025768 misnumbered_section 11.praef -> 11.1
010316 stray_section 3.139 -> 3.147
010708 stray_section 4.14 -> 4.22
021392 stray_section 8.127 -> 8.129
029160 stray_section 12.36 -> 12.65
033661 stray_section 15.66 -> 15.67
034981 stray_section 16.245 -> 16.120
065767 stray_section 32.66 -> 32.111
032617 stray_chapter 2 -> 24
032619 stray_chapter 2 -> 24
034191 stray_chapter 2 -> 38
034193 stray_chapter 2 -> 38
017717 volume_title v1p523 -> v2t
017718 volume_title v1p523 -> v2t
017719 volume_title v1p523 -> v2t
034307 volume_title v2p555 -> v3t
034308 volume_title v2p555 -> v3t
034309 volume_title v2p555 -> v3t
047120 volume_title v3p492 -> v4t
047121 volume_title v3p492 -> v4t
047122 volume_title v3p492 -> v4t
062827 volume_title v4p475 -> v5t
062828 volume_title v4p475 -> v5t
062829 volume_title v4p475 -> v5t
"""

if __name__ == "__main__":
    main()
