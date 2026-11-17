#!/usr/bin/env python3
"""Extract Mayhoff's Latin Pliny (Perseus typed text) as it is: the raw text.

Run:  uv run convert/extract_lat.py   (no arguments; writes work/raw/lat.jsonl,
      work/raw/lat.info.json and work/raw/lat.pages.csv in this version folder)

First step. This one copies the typed file into the unified text format without
correcting anything: what is wrong in the typed file is wrong here in the same way.
convert/repair_lat.py then makes text/ from work/raw/.

THE SOURCE
source/phi0978.phi001.perseus-lat2.xml, TEI (EpiDoc), Mayhoff's Teubner text of the 37
books (5 volumes, 1892-1909), typed by Perseus. Layout of the body:
- div type=edition > div subtype=book (n=1..37) > div subtype=chapter (n="praef", 1, 2 ...).
  The chapter divs are the chapters Mayhoff prints in bold in the text ("17. Non est
  omittenda") and first in the running heads ("NAT. HIST. XXII 25 (75-82)"); seen on the
  page images. Their numbers are not in the typed words. Book 29 has 6 of them.
- Two more numberings, both as empty <milestone/> inside the paragraphs:
  - unit="section" (6,927): Mayhoff's section numbers (§), running through each book. This
    is the citation scholars use today ("NH 25.92" = book 25, § 92). Some numbers carry a
    "?" typed by Perseus ("31?"). Eight markers of book 18 are typed unit="para"
    (n=147-154); their numbers continue the § sequence of the book (146 before, 155 after).
  - unit="paragraph" (4,807): an older chapter numbering, the one Mayhoff prints in
    parentheses in the running heads (book 29 has 39); taken to be Hardouin's, not
    verified. 84 of them begin inside a §.
- Book 1 is Pliny's own: his preface (letter to Titus, div n="praef", § 1-33), then for
  each of books 2-37 a summary of its content and a list of its authors (div n=2..37,
  each with a <head> "LIBRO II CONTINENTVR" ...). In the summaries, the unit="paragraph"
  markers stand at the end of a line and give the chapter of the summarised book.
- Each book begins with three <head>: "C. PLINI SECVNDI", "NATVRALIS HISTORIAE", "LIBER ...".
  The first book of each volume is preceded by three more heads, the title of the volume
  ("LIBRI XVI-XXII"); in volumes 1, 3, 4 and 5 they are followed by an empty <pb/>.
- Pages: <pb xml:id="v.3.p.100"/> = volume 3, page 100. Volume 5 is typed "4b"
  (metadata/note.txt). Five <pb/> have no number: four after a volume title, one at the
  very end of the file.
- Footnotes: <note place="unspecified"> (68,321), put by the typists at the word they
  concern. They mix the editor's variant readings ("cretā v. -ta ll") and the sources and
  parallels ("Diosc. IV 4."); the second sort is usually typed right after a § marker.
  Inside them, <hi rend="bold"> are the manuscript sigla, italics the editor's own Latin,
  <hi rend="sup"> the hand of a corrector (R with 1 above). 28 notes lie inside notes;
  some notes are empty, a few of these holding a note.
- Marginal notes: <note type="margin"|"marg"|"marginal"> (820), cross-references printed in
  the margin ("3,43" = book 3, § 43).
- <add> (5,790): letters or words supplied by the editor (angle brackets in the book).
  <foreign xml:lang="grc">: Greek. <hi>: italics, bold, superscript, overline (Roman
  numerals). <quote>/<l>: a few lines of verse. No <del>, <gap>, <sic>.

WHAT THIS SCRIPT DOES: plain extraction, no judgement on the content
- ref = book.§ (ref_scheme ["book", "section"]), the § being the n of the last section
  marker met in the book, as typed ("2.31?" included). In book 1, the preface gets
  "praef.<§>", the usual citation, and each summary "1.<n of its div>" (1.25 = the summary
  of book 25). Text before the first § of a book (its heads) gets the book alone.
- Passages: one per <head> (kind head) and per <p> (kind text), cut again wherever a §
  marker or an older chapter marker stands, so that each passage lies within one § and
  one chapter of each numbering. A cut may fall inside a sentence: the markers are where the edition puts them.
  A marker with no words before it in the passage does not cut; it only changes the label.
  Book 1 summaries are not cut at chapter markers (see x_old_chapter).
- x_chapter and x_old_chapter (fields of this version, "x_" in the format), on passages of
  kind text and head. x_chapter: Mayhoff's chapter, the n of the chapter div, in books
  2-37 ("praef" for a book's preface). x_old_chapter: the older chapter number in which
  the passage lies, as typed; absent before the first such marker of a book. In book 1
  summaries, the chapter of the summarised book that the line announces (the marker inside
  the line), absent when the line has none.
- Kinds: book 1 is text, summaries included (Pliny wrote them as part of the work).
  Footnotes are kind note (the typed file does not separate the variant readings from the
  sources, and they are not separated here); marginal notes kind margin. Each is written
  after the passage it sits in, with an anchor at the place it sits; a note inside a note is
  anchored to the outer note. A note lying directly in a div is anchored at the end of the
  passage before it. An empty note is dropped (counted below); a note it holds takes its place.
- page: "v<volume>p<n>" from each numbered <pb>, volume "4b" read as 5. A page without
  number gets "v<volume>t" (front pages of a volume, printed number empty), the volume
  being that of the next numbered page; the book-1 heads, before any <pb>, are on v1t.
  A page id is listed in lat.pages.csv only once something lies on it.
- Words: all characters of <head>, <p> and <note>, as typed. Line breaks and runs of white
  space become one space; each piece of text is put in Unicode NFC form. Verse lines (<l>)
  are joined with one space.
- Marks: <add> -> add, <foreign> -> foreign, <hi> (any rend) -> hi. A mark cut by a
  passage boundary is split between the two passages.
- lat.pages.csv: the pages in reading order, with their volume and number as typed.

SOURCE FILES NEEDED: the typed file only. The scans are not opened.
"""
import csv, json, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
SOURCES = ["phi0978.phi001.perseus-lat2.xml"]          # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require
RAW = VDIR / "work" / "raw"
LANG = "lat"
NS = "{http://www.tei-c.org/ns/1.0}"
XID = "{http://www.w3.org/XML/1998/namespace}id"
PB = re.compile(r"^v\.(\d+b?)\.p\.(\d+)$")
MARGIN_TYPES = {"margin", "marg", "marginal"}
MARK_OF = {"add": "add", "foreign": "foreign", "hi": "hi"}
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")


def tag(el):
    return el.tag[len(NS):]


def volume_of(label):
    return "5" if label == "4b" else label


class Passage:
    """Collects the raw text of one passage, with breaks, marks and notes at raw positions."""

    def __init__(self, kind, ref, chapter, page):
        self.kind, self.ref, self.chapter, self.page = kind, ref, chapter, page
        self.raw, self.len = [], 0
        self.breaks, self.marks, self.notes = [], [], []
        self.open = {}         # id -> (start, type) of marks not yet closed
        self.div = None

    def add(self, s):
        if s:
            s = CONTROL.sub("", unicodedata.normalize("NFC", s))
            self.raw.append(s)
            self.len += len(s)

    def has_words(self):
        return any(piece.strip() for piece in self.raw)

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
        lead = 1 if out and out[0] == " " else 0
        if out and out[-1] == " ":
            out.pop()
        text = "".join(out[lead:])
        return text, lambda i: max(0, min(pos[i] - lead, len(text)))


class Converter:
    def __init__(self, root):
        self.pages, self.listed = [], set()
        self.page = "v1t"
        self.pending_page = None      # a <pb/> without number: its page id
        self.lines = []
        self.last_main = None
        self.empty_notes = 0
        self.book = None
        self.section = None           # n of the last § marker in this book
        self.chapter = None           # the older chapter
        self.div = None               # Mayhoff's chapter: n of the chapter div, books 2-37
        self.summary = None           # book 1: n of the summary div, "praef" for the preface
        self.cur = None               # the passage being filled
        self.carry = []               # notes of a paragraph without words, for the next one
        # volume of the next numbered page, for each <pb/> without number
        self.next_volume = {}
        last = None
        for pb in reversed(list(root.iter(f"{NS}pb"))):
            m = PB.match(pb.get(XID) or "")
            if m:
                last = volume_of(m.group(1))
            elif pb.get(XID) is None:
                self.next_volume[pb] = last

    # pages -----------------------------------------------------------------
    def use_page(self, pid, volume, printed):
        if pid not in self.listed:
            self.listed.add(pid)
            self.pages.append([pid, volume, printed])

    def on_pb(self, pb):
        xid = pb.get(XID)
        if xid is None:
            vol = self.next_volume[pb]
            if vol is None:
                return None               # the <pb/> at the very end: nothing follows
            pid, info = f"v{vol}t", (vol, "")
        else:
            m = PB.match(xid)
            if not m:
                sys.exit(f"unexpected page id {xid!r}")
            vol, n = volume_of(m.group(1)), m.group(2)
            pid, info = f"v{vol}p{n}", (vol, n)
        self.page_info = getattr(self, "page_info", {})
        self.page_info[pid] = info
        self.page = pid
        return pid

    def list_page(self, pid):
        if pid == "v1t":
            self.use_page(pid, "1", "")
        else:
            vol, n = self.page_info[pid]
            self.use_page(pid, vol, n)

    # labels ----------------------------------------------------------------
    def ref(self):
        if self.book == "1":
            if self.summary == "praef":
                return f"praef.{self.section}" if self.section else "1"
            return f"1.{self.summary}" if self.summary else "1"
        return f"{self.book}.{self.section}" if self.section else self.book

    # walking ---------------------------------------------------------------
    def walk(self, el):
        for c in el:
            t = tag(c)
            if t == "div":
                st = c.get("subtype")
                if st == "book":
                    self.book, self.section, self.chapter, self.summary = c.get("n"), None, None, None
                    self.div = None
                elif st == "chapter" and self.book == "1":
                    self.summary, self.section, self.chapter = c.get("n"), None, None
                elif st == "chapter":
                    self.div = c.get("n")
                self.walk(c)
            elif t == "pb":
                self.on_pb(c)
            elif t in ("p", "head", "quote"):
                self.start("head" if t == "head" else "text")
                self.fill(c)
                self.end()
            elif t == "milestone":
                self.milestone(c)
            elif t == "note":
                self.emit_note(c, self.last_main, None)
            else:
                sys.exit(f"unexpected element <{t}> in a div")

    def start(self, kind):
        self.cur = Passage(kind, self.ref(), self.chapter, self.page)
        self.cur.div = self.div
        if kind != "head":
            self.cur.notes, self.carry = self.carry, []

    def end(self):
        p = self.cur
        for mid, (start, typ) in list(p.open.items()):
            sys.exit("a mark is still open at the end of a passage")
        if p.has_words():
            self.emit(p)
        else:
            self.carry += p.notes        # anchored at the start of the next passage
        self.cur = None

    def cut(self):
        """Close the current passage at this point and open the next one, same kind."""
        p = self.cur
        if not p.has_words():
            p.ref, p.chapter = self.ref(), self.chapter    # nothing before: only relabel
            return
        carried = [(mid, typ) for mid, (start, typ) in p.open.items()]
        for mid, (start, typ) in p.open.items():
            p.marks.append((start, p.len, typ))
        p.open = {}
        self.emit(p)
        self.start(p.kind)
        for mid, typ in carried:
            self.cur.open[mid] = (0, typ)

    def milestone(self, m):
        unit, n = m.get("unit"), m.get("n")
        if unit in ("section", "para"):
            self.section = n
        elif unit == "paragraph":
            if self.book == "1" and self.summary != "praef":
                if self.cur is not None:
                    self.cur.chapter = n                   # the line announces this chapter
                return
            self.chapter = n
        else:
            sys.exit(f"unexpected milestone unit {unit!r}")
        if self.cur is not None:
            self.cut()

    def fill(self, el, depth=0):
        """Add the content of el to the current passage (el's own tail is handled by the caller)."""
        self.cur.add(el.text)
        for c in el:
            t = tag(c)
            p = self.cur
            if t == "pb":
                pid = self.on_pb(c)
                if pid is not None:
                    p.breaks.append((p.len, pid))
            elif t == "note":
                p.notes.append((c, p.len, self.page))
            elif t == "milestone":
                self.milestone(c)
            elif t in MARK_OF:
                mid = id(c)
                p.open[mid] = (p.len, MARK_OF[t])
                self.fill(c, depth + 1)
                start, typ = self.cur.open.pop(mid)
                self.cur.marks.append((start, self.cur.len, typ))
            elif t in ("quote", "l"):
                if t == "l":
                    self.cur.add(" ")
                self.fill(c, depth + 1)
                if t == "l":
                    self.cur.add(" ")
            else:
                sys.exit(f"unexpected element <{t}> inside <{tag(el)}>")
            self.cur.add(c.tail)

    def emit(self, p, anchor=None):
        text, at = p.finish()
        if not text:
            sys.exit(f"empty passage on page {p.page}")
        line = {"id": f"{len(self.lines) + 1:06d}", "kind": p.kind}
        if p.ref:
            line["ref"] = p.ref
        page, breaks = p.page, []
        for raw, pg in p.breaks:
            off = at(raw)
            if off == 0:
                page, breaks = pg, []           # the passage really begins on that page
            elif off < len(text):
                if breaks and breaks[-1][0] == off:
                    breaks[-1][1] = pg
                else:
                    breaks.append([off, pg])
            # a break at the very end belongs to the next passage
        self.list_page(page)
        for _, pg in breaks:
            self.list_page(pg)
        marks = []
        for s, e, t in sorted(p.marks):
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
        if p.kind in ("text", "head"):
            if p.div is not None:
                line["x_chapter"] = p.div
            if p.chapter is not None:
                line["x_old_chapter"] = p.chapter
        self.lines.append(line)
        if p.kind not in ("note", "margin"):
            self.last_main = line
        for note, raw, page_at in p.notes:
            self.emit_note(note, line, (at(raw), page_at, p.ref))

    def emit_note(self, note, host, where):
        if host is None:
            sys.exit("a note comes before any passage")
        if where is None:                       # note directly in a div
            offset, page, ref = len(host["text"]), self.page, host.get("ref")
        else:
            offset, page, ref = where
        kind = "margin" if note.get("type") in MARGIN_TYPES else "note"
        if note.get("type") not in MARGIN_TYPES | {None}:
            sys.exit(f"unexpected note type {note.get('type')!r}")
        saved = self.cur
        self.cur = Passage(kind, ref, None, page)
        self.fill(note)
        p, self.cur = self.cur, saved
        if not p.has_words():
            self.empty_notes += 1
            for inner, _, _ in p.notes:          # a note inside an empty note: put in its place
                self.emit_note(inner, host, (offset, page, ref))
            return
        self.emit(p, anchor=[host["id"], offset])


def main():
    (typed,) = require(VDIR, SOURCES)
    root = ET.parse(typed.path).getroot()
    edition = root.find(f"{NS}text/{NS}body/{NS}div")
    conv = Converter(root)
    conv.walk(edition)
    if conv.carry:
        sys.exit("notes left without a passage at the end")

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
        "work_no": 3,
        "work": "Pliny the Elder, Naturalis historia",
        "lang": LANG,
        "origin": "typed",
        "sources": [{"file": typed.name, "md5": typed.md5}],
        "converter": str((VDIR / "convert" / "extract_lat.py").relative_to(ROOT)),
        "ref_scheme": ["book", "section"],
        "rights": "Text public domain (Mayhoff died 1914); typed text by Perseus Digital "
                  "Library, CC BY-SA 4.0.",
        "status": "complete",
        "review": "none",
        "notes": NOTES.format(empty=conv.empty_notes),
    }
    with open(RAW / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(conv.lines)} passages, {len(conv.pages)} pages, {conv.empty_notes} empty notes dropped")


NOTES = (
    "Plain extraction of the typed text: words, numbers and labels as Perseus typed them, "
    "errors included. "
    "ref is book.§ (Mayhoff's sections, the modern citation); the preface of book 1 is "
    "'praef.<§>' and the summary of book N in book 1 is '1.<N>'. A passage is cut at every "
    "§ and at every older chapter, so a cut may fall inside a sentence. Mayhoff's chapter "
    "numbers (printed in bold in the book, not in the words) are in the field x_chapter; "
    "the older chapter numbers, printed in parentheses in the running heads (taken to be "
    "Hardouin's), in x_old_chapter. "
    "The § labels are those typed: some carry a '?', some are missing (their text lies in "
    "the § before) or out of order. "
    "All footnotes are kind 'note': the typed file does not separate the variant readings "
    "from the sources and parallel passages, and they are not separated here. "
    "{empty} empty notes of the typed file were dropped. "
    "A few hundred words of the main text are in italics or bold in the typed file; some "
    "look like sigla of the apparatus typed into the text. They are kept, marked 'hi'. "
    "Pages 323 and 432 of volume 2 have no page marker in the typed file: their text is on "
    "the page before. Volume title heads before page 1 of volumes 2 to 5 lie on the last "
    "page of the volume before, where the typed file puts them."
)

if __name__ == "__main__":
    main()
