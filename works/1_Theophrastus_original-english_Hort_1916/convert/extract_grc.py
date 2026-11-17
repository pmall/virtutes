#!/usr/bin/env python3
"""Extract Hort's Greek Theophrastus (First1KGreek typed text) as it is: the raw text.

Run:  uv run convert/extract_grc.py   (no arguments; writes work/raw/grc.jsonl,
      work/raw/grc.info.json and work/raw/grc.pages.csv in this version folder)

First step. This one copies the typed file into the unified text format without
correcting anything: what is wrong in the typed file is wrong here in the same way.
convert/repair_grc.py then makes text/ from work/raw/.

THE BOOK
Hort's Loeb edition (1916), two volumes: books 1-5 in volume 1, books 6-9 in volume 2
(then minor works, not in the typed file). Greek on the left-hand (even) pages, English
on the right-hand (odd) pages. Only the Greek is typed; the English is in the scan only.

THE SOURCE
source/tlg0093.tlg001.1st1K-grc1.xml, TEI (EpiDoc), books 1-9 of the Enquiry into Plants,
typed by First1KGreek. Layout of the body:
- div type=edition > div subtype=book (n=1..9) > div subtype=chapter > div subtype=section,
  each with its number in @n. This is the usual citation (book.chapter.section), with the
  usual 119 chapters.
- All words are inside <head> (11: the title of the work before books 1 and 6, the
  number of each book as a Greek letter), <p> and <note type="footnote">. No text lies
  directly in a div.
- <pb n="…"/>: Hort's printed page, without volume, even numbers only (the Greek pages);
  the numbering starts again at 2 for volume 2 (book 6). Four page pairs are missing at
  book boundaries in each volume (e.g. 100 -> 104).
- <lb n="…"/>: four, stray. No word is cut at a line break.
- Footnotes (<note>), typed in a block where each Greek page ends, mostly in the middle of
  a <p>, some between sections. They mix variant readings ("τὰ ins. Sch., om. Ald.H.") and
  Hort's explanations in English ("i.e. flower, catkin, …"); one <note> may hold several
  numbered notes.
- <add> (all with cause="omitted"), <del> (two with status="error"), <gap reason=
  "omitted"/>. A <del> holds one <note> and one <pb>.

WHAT THIS SCRIPT DOES: plain extraction, no judgement on the content
- One passage per <head> (kind head), per <p> (kind text) and per <note> (kind note).
  A note is written right after the passage it sits in, with an anchor at the place it
  sits; a note lying between sections is anchored at the end of the last passage.
- ref = the @n of the enclosing book, chapter and section divs, joined with dots, exactly
  as the typed file has them. Notes get the ref of where they sit; a head the ref of its
  book.
- page: each <pb> gives the page "v<volume>p<n>"; the volume goes up by one each time
  n is smaller than the page before. "printed" keeps the number as typed.
- Words: all characters of <head>, <p> and <note>, chapter numbers included, as typed.
  Line breaks and runs of white space become one space; each piece of text is put in
  Unicode NFC form. <lb> is dropped. Invisible control characters are dropped.
- Marks: <add> -> add, <del> -> del (whatever its status), <gap/> -> the character "…"
  marked gap.
- grc.pages.csv: the pages in reading order, with their volume and number as typed.

SOURCE FILES NEEDED: the typed file only. The scan is not opened.
"""
import csv, json, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
SOURCES = ["tlg0093.tlg001.1st1K-grc1.xml"]            # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require
RAW = VDIR / "work" / "raw"
LANG = "grc"
NS = "{http://www.tei-c.org/ns/1.0}"
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")  # invisible; white space aside


class Passage:
    """Collects the raw text of one passage, with breaks, marks and notes at raw positions."""

    def __init__(self, kind, ref, page):
        self.kind, self.ref, self.page = kind, ref, page
        self.raw = []          # pieces of text
        self.len = 0
        self.breaks, self.marks, self.notes = [], [], []

    def add(self, s):
        if s:
            s = CONTROL.sub("", unicodedata.normalize("NFC", s))
            self.raw.append(s)
            self.len += len(s)

    def finish(self):
        """Collapse white space; return text and a function mapping raw positions to it."""
        raw = "".join(self.raw)
        pos, out, space = [], [], False
        for c in raw:
            pos.append(len(out))
            if c.isspace():
                if out and not space:
                    out.append(" ")
                space = True
            else:
                out.append(c)
                space = False
        pos.append(len(out))
        if out and out[-1] == " ":
            out.pop()
        text = "".join(out)
        return text, lambda i: min(pos[i], len(text))


class Converter:
    def __init__(self):
        self.pages = []        # rows of grc.pages.csv
        self.seen = set()
        self.volume = 0
        self.last_n = None
        self.page = None
        self.lines = []        # output passages, in order
        self.last_main = None  # last passage written that is not a note

    # pages -----------------------------------------------------------------
    def new_page(self, n):
        if self.last_n is None or int(n) < self.last_n:
            self.volume += 1
        self.last_n = int(n)
        pid = f"v{self.volume}p{n}"
        if pid in self.seen:
            sys.exit(f"page {pid} twice in the typed file")
        self.seen.add(pid)
        self.pages.append([pid, str(self.volume), n])
        self.page = pid

    # walking ---------------------------------------------------------------
    def walk(self, el, refs):
        """Walk divs; refs maps book/chapter/section to the @n of the nearest div."""
        for c in el:
            tag = c.tag[len(NS):]
            if tag == "div":
                walk_refs = dict(refs)
                sub = c.get("subtype")
                if sub not in ("book", "chapter", "section"):
                    sys.exit(f"unexpected div subtype {sub}")
                walk_refs[sub] = c.get("n")
                if sub == "book":
                    walk_refs.pop("chapter", None)
                    walk_refs.pop("section", None)
                if sub == "chapter":
                    walk_refs.pop("section", None)
                self.walk(c, walk_refs)
            elif tag == "pb":
                self.new_page(c.get("n"))
            elif tag in ("p", "head"):
                p = Passage("text" if tag == "p" else "head", self.ref(refs), self.page)
                self.fill(c, p, refs)
                self.emit(p)
            elif tag == "note":
                # a note lying directly in a div: anchored at the end of the last passage
                self.emit_note(c, refs, self.last_main, None)
            elif tag == "lb":
                pass
            else:
                sys.exit(f"unexpected element <{tag}> in a div")
            if (c.tail or "").strip():
                sys.exit(f"text directly in a div after <{tag}>")

    @staticmethod
    def ref(refs):
        return ".".join(refs[k] for k in ("book", "chapter", "section") if k in refs)

    def fill(self, el, p, refs):
        """Add the content of el to passage p (el's own tail is handled by the caller)."""
        p.add(el.text)
        for c in el:
            tag = c.tag[len(NS):]
            if tag == "lb":
                pass
            elif tag == "pb":
                self.new_page(c.get("n"))
                p.breaks.append((p.len, self.page))
            elif tag == "note":
                p.notes.append((c, p.len, self.page))
            elif tag == "gap":
                start = p.len
                p.add("…")
                p.marks.append((start, start + 1, "gap"))
            elif tag in ("add", "del"):
                start = p.len
                self.fill(c, p, refs)
                p.marks.append((start, p.len, tag))
            else:
                sys.exit(f"unexpected element <{tag}> inside <{el.tag[len(NS):]}>")
            p.add(c.tail)

    def emit(self, p, anchor=None):
        text, at = p.finish()
        line = {"id": None, "kind": p.kind}
        if p.ref:
            line["ref"] = p.ref
        page = p.page
        breaks = []
        for raw, pg in p.breaks:
            off = at(raw)
            if off == 0:
                page = pg                       # the passage really begins on that page
                breaks = []
            elif off < len(text):
                if breaks and breaks[-1][0] == off:
                    breaks[-1][1] = pg
                else:
                    breaks.append([off, pg])
            # a break at the very end belongs to the next passage
        marks = []
        for s, e, t in p.marks:
            s, e = at(s), at(e)
            if s < e:
                marks.append([s, e, t])
        line.update({"page": page, "text": text})
        if breaks:
            line["breaks"] = breaks
        if marks:
            line["marks"] = marks
        if anchor:
            line["anchor"] = anchor
        if not text:
            sys.exit(f"empty passage on page {page}")
        line["id"] = f"{len(self.lines) + 1:06d}"
        self.lines.append(line)
        if p.kind != "note":
            self.last_main = line
        for note, raw, page_at in p.notes:
            self.emit_note(note, None, line, (at(raw), page_at, p.ref))

    def emit_note(self, note, refs, host, where):
        if host is None:
            sys.exit("a note comes before any passage")
        if where is None:                       # note directly in a div
            offset, page, ref = len(host["text"]), self.page, self.ref(refs)
        else:
            offset, page, ref = where
        p = Passage("note", ref, page)
        self.fill(note, p, refs)
        self.emit(p, anchor=[host["id"], offset])


def main():
    (typed,) = require(VDIR, SOURCES)
    root = ET.parse(typed.path).getroot()
    edition = root.find(f"{NS}text/{NS}body/{NS}div")
    conv = Converter()
    conv.walk(edition, {})

    RAW.mkdir(parents=True, exist_ok=True)
    with open(RAW / f"{LANG}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for line in conv.lines:
            f.write(json.dumps(line, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(RAW / f"{LANG}.pages.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "volume", "printed"])
        w.writerows(conv.pages)
    info = {
        "format": "vh-text/0.3",
        "version": VDIR.name,
        "work_no": 1,
        "work": "Theophrastus, Enquiry into Plants (Historia plantarum)",
        "lang": LANG,
        "origin": "typed",
        "sources": [{"file": typed.name, "md5": typed.md5}],
        "converter": str((VDIR / "convert" / "extract_grc.py").relative_to(ROOT)),
        "ref_scheme": ["book", "chapter", "section"],
        "rights": "Text public domain (Hort died 1935); typed text by First1KGreek, "
                  "CC BY-SA 4.0.",
        "status": "complete",
        "review": "none",
        "notes": NOTES,
    }
    with open(RAW / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(conv.lines)} passages, {len(conv.pages)} pages")


NOTES = (
    "Plain extraction of the typed text: words, numbers and labels as First1KGreek typed "
    "them, errors included. "
    "Only the Greek pages are here (even numbers). "
    "Chapter numbers printed by Hort are part of the text, as typed. "
    "The ref copies the typed file's labels: chapter 7.3 has no section 4 (its passages "
    "are labelled 3) and one section is labelled 7.4.5s. "
    "Page 216 of volume 2 is typed as 214. "
    "All footnotes are kind 'note': variant readings and Hort's explanations are not "
    "separated. A note is anchored where the typists put it, at the end of its printed "
    "page, not at the word it comments."
)

if __name__ == "__main__":
    main()
