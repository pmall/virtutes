#!/usr/bin/env python3
"""Extract Bostock and Riley's English Pliny (Perseus typed text) as it is: the raw text.

Run:  uv run convert/extract_eng.py   (no arguments; writes work/raw/eng.jsonl,
      work/raw/eng.info.json and work/raw/eng.pages.csv in this version folder)

First step. This one copies the typed file into the unified text format without
correcting anything: what is wrong in the typed file is wrong here in the same way.
convert/repair_eng.py then makes text/ from work/raw/.

THE SOURCE
source/phi0978.phi001.perseus-eng1.xml, TEI P4 (no namespace), the translation by John
Bostock and H. T. Riley (London, Bohn, 6 volumes, 1855-1857), typed by Perseus. Layout of
the body:
- div1 type=book (n=1..37) > div2 type=chapter. Each div2 begins with a <head> that gives
  the chapter as printed: "CHAP. 1. (1.)&mdash;WHETHER THE WORLD BE FINITE ...". The first
  number is Hardouin's chapter (the translators' own note at the head of book 2 says so);
  the number in parentheses is that of the older editions (Dalechamps ...). These are the
  same chapter numbers as the older chapters of the Latin text (x_old_chapter in
  3_Pliny_original_Mayhoff). There are no section (§) numbers.
  - Book 1 is the dedication alone (div2 n="dedication"): Pliny's preface to Titus. The
    summaries of each book that make up the rest of Pliny's book 1 are printed by the
    translators at the end of the book they describe ("SUMMARY.&mdash;...", "ROMAN AUTHORS
    QUOTED.&mdash;..."), and Perseus typed them inside the last chapter of that book.
  - Book 3 opens with div2 n="0", head "INTRODUCTION." (no chapter number printed).
  - Book 14 div2 n="1" has the head "CHAPS. 1 &amp; 2." (two chapters printed as one).
  - Book 2 has one <p> directly in the div1, before chapter 1: the translators' note on
    the division of the chapters, in square brackets.
  - The last chapters of books 5 and 10 end with the errata lists of volume 1, book 17
    with the printer's line, book 27 with the translators' afterword on Dr. Yates; all
    typed as paragraphs of the chapter.
- Pages: <pb n="3125"/> = volume 3, page 125 (volume x 1000 + page; metadata/note.txt).
  The marker stands at the start of the page. Volumes: 1 = books 1-5, 2 = 6-10,
  3 = 11-17, 4 = 18-23, 5 = 24-31, 6 = 32-37. Two <pb/> have no number: one before
  book 6 (the next numbered page is 2002), one at the very end of the file (pb n="6469",
  after the last words, is the other end marker: nothing lies on it). The front matter of
  the volumes (pages in Roman numerals) is not in the typed file.
- Footnotes: <note anchored="yes" place="foot"> (21,020), at the word they concern, in <p>
  and in <head>; one directly in a div1 (book 33) and one in a div2. No note in a note;
  seven notes hold several paragraphs (<p> inside the note).
- <hi rend="ital"> (italics), <hi rend="super"> (superscripts), <foreign lang="greek">
  (750: Greek, typed in Beta Code, e.g. "Bore/as"), <lb/> (line breaks of verse),
  <table>/<row>/<cell> (4 small tables, three in notes), <date>, <dateRange>, <placeName>
  (tags around words, nothing to add), one <corr>rings</corr> <sic>kings</sic> in a note.
- Named entities from the ISO/HTML sets (&aelig; &mdash; &eacute; ...), declared in a DTD
  that is not in the file, so the standard library cannot parse it as it is. Perseus also
  writes "&lt;*&gt;", i.e. "<*>", for a character it could not read (11 places).

WHAT THIS SCRIPT DOES: plain extraction, no judgement on the content
- ref = book.chapter (ref_scheme ["book", "chapter"]), the n of the div1 and div2 as
  typed ("1.dedication", "3.0" included). The book head gets the book alone. Paragraphs
  typed in a chapter keep its ref, wherever they belong (summaries, errata: see
  convert/repair_eng.py).
- Passages: one per <head> (kind head) and per <p> (kind text). The book 2 note directly in
  its div1 is kind text, ref "2", like any <p>.
- Footnotes are kind note. Each is written after the passage it sits in, with an anchor at
  the place it sits. A note lying directly in a div is anchored at the end of the passage
  before it.
- page: "v<volume>p<n>" from each numbered <pb>. A <pb/> without number gets "v<volume>t"
  (printed number empty), the volume being that of the next numbered page; the one at the
  end, which nothing follows, is ignored. A page id is listed in eng.pages.csv only once
  something lies on it.
- Entities: each named entity used in the file is read as the character of the standard
  table of HTML (Python's html.entities, which follows the ISO entity sets), except
  &cdot;: there it would be "ċ" (c with dot above), while the file uses it, 20 times and
  always between digits, as the raised decimal point of the book ("87&cdot;9705" days);
  it is read as "·" (U+00B7). An entity outside the list stops the script.
- Words: all characters of <head>, <p> and <note>, as typed, both <corr> and <sic>
  included, Greek left in Beta Code. Runs of white space become one space, except after
  a letter and a hyphen at the end of a typed line ("na-", "never-"): there the line break
  is dropped and the two parts are written together ("na-ture"), hyphen kept, since the
  file does not tell a word cut at the end of a line from a hyphenated word. Line breaks
  of verse (<lb/>), the cells and rows of a table and the paragraphs inside a note are
  separated by one space (a note stays one passage). Each piece
  of text is put in Unicode NFC form.
- Marks: <hi> (any rend) -> hi, <foreign> -> foreign. Nothing in the file marks additions,
  deletions or gaps.
- eng.pages.csv: the pages in reading order, with their volume and number as typed.

SOURCE FILES NEEDED: the typed file only. The scans are not opened.
"""
import csv, html.entities, json, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
SOURCES = ["phi0978.phi001.perseus-eng1.xml"]          # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require
RAW = VDIR / "work" / "raw"
LANG = "eng"
# The named entities of the typed file; any other stops the parser.
ENTITY_NAMES = """aelig mdash eacute AElig oelig euml iuml uuml OElig acirc ndash deg ouml
    egrave prime sect pound auml ocirc icirc agrave ecirc ccedil Iuml aacute uacute ucirc
    yuml ugrave Ouml Uuml ntilde ograve iacute emacr Euml""".split()
ENTITIES = {name: html.entities.html5[name + ";"] for name in ENTITY_NAMES}
ENTITIES["cdot"] = "·"                            # decimal point, see above
MARK_OF = {"hi": "hi", "foreign": "foreign"}
TRANSPARENT = {"date", "dateRange", "placeName", "corr", "sic"}
SPACED = {"lb", "table", "row", "cell", "p"}          # a space at each start and end
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
PB = re.compile(r"^([1-9])(\d{3})$")


def parse(path):
    parser = ET.XMLParser()
    parser.entity.update(ENTITIES)
    with open(path, "rb") as f:
        parser.feed(f.read())
    return parser.close()


class Passage:
    """Collects the raw text of one passage, with breaks, marks and notes at raw positions."""

    def __init__(self, kind, ref, page):
        self.kind, self.ref, self.page = kind, ref, page
        self.raw, self.len = [], 0
        self.breaks, self.marks, self.notes = [], [], []

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
        pos, out = [], []
        i = 0
        while i < len(raw):
            if raw[i].isspace():
                j = i
                while j < len(raw) and raw[j].isspace():
                    j += 1
                hyphen = (len(out) >= 2 and out[-1] == "-" and out[-2].isalpha()
                          and "\n" in raw[i:j])
                keep = bool(out) and not hyphen
                for _ in range(i, j):
                    pos.append(len(out))
                if keep:
                    out.append(" ")
                i = j
            else:
                pos.append(len(out))
                out.append(raw[i])
                i += 1
        pos.append(len(out))
        if out and out[-1] == " ":
            out.pop()
        text = "".join(out)
        return text, lambda k: max(0, min(pos[k], len(text)))


class Converter:
    def __init__(self, body):
        self.pages, self.listed, self.page_info = [], set(), {}
        self.page = None
        self.lines = []
        self.last_main = None
        self.book = self.chapter = None
        self.cur = None
        self.carry = []               # notes of a paragraph without words, for the next one
        self.next_volume = {}         # volume of the next numbered page, for each <pb/> without n
        last = None
        for pb in reversed(list(body.iter("pb"))):
            m = PB.match(pb.get("n") or "")
            if m:
                last = str(int(m.group(1)))
            elif pb.get("n") is None:
                self.next_volume[pb] = last
            else:
                sys.exit(f"unexpected page number {pb.get('n')!r}")

    # pages -----------------------------------------------------------------
    def on_pb(self, pb):
        n = pb.get("n")
        if n is None:
            vol = self.next_volume[pb]
            if vol is None:
                return None               # the <pb/> at the very end: nothing follows
            pid, info = f"v{vol}t", (vol, "")
        else:
            m = PB.match(n)
            vol, printed = str(int(m.group(1))), str(int(m.group(2)))
            pid, info = f"v{vol}p{printed}", (vol, printed)
        self.page_info[pid] = info
        self.page = pid
        return pid

    def list_page(self, pid):
        if pid not in self.listed:
            self.listed.add(pid)
            self.pages.append([pid, *self.page_info[pid]])

    def ref(self):
        return f"{self.book}.{self.chapter}" if self.chapter is not None else self.book

    # walking ---------------------------------------------------------------
    def walk(self, el):
        for c in el:
            t = c.tag
            if t == "div1":
                if c.get("type") != "book":
                    sys.exit(f"unexpected div1 type {c.get('type')!r}")
                self.book, self.chapter = c.get("n"), None
                self.walk(c)
            elif t == "div2":
                if c.get("type") != "chapter":
                    sys.exit(f"unexpected div2 type {c.get('type')!r}")
                self.chapter = c.get("n")
                self.walk(c)
            elif t == "pb":
                self.on_pb(c)
            elif t in ("p", "head"):
                self.start("head" if t == "head" else "text")
                self.fill(c)
                self.end()
            elif t == "note":
                self.emit_note(c, self.last_main, None)
            else:
                sys.exit(f"unexpected element <{t}> in a div")

    def start(self, kind):
        if self.page is None:
            sys.exit("text before the first page marker")
        self.cur = Passage(kind, self.ref(), self.page)
        self.cur.notes, self.carry = self.carry, []

    def end(self):
        p = self.cur
        if p.has_words():
            self.emit(p)
        else:
            self.carry += p.notes        # anchored at the start of the next passage
        self.cur = None

    def fill(self, el):
        """Add the content of el to the current passage (el's own tail is handled by the caller)."""
        self.cur.add(el.text)
        for c in el:
            t = c.tag
            p = self.cur
            if t == "pb":
                pid = self.on_pb(c)
                if pid is not None:
                    p.breaks.append((p.len, pid))
            elif t == "note":
                p.notes.append((c, p.len, self.page))
            elif t in MARK_OF:
                start = p.len
                self.fill(c)
                p.marks.append((start, p.len, MARK_OF[t]))
            elif t in TRANSPARENT:
                self.fill(c)
            elif t in SPACED:
                p.add(" ")
                self.fill(c)
                p.add(" ")
            else:
                sys.exit(f"unexpected element <{t}> inside <{el.tag}>")
            p.add(c.tail)

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
        self.lines.append(line)
        if p.kind != "note":
            self.last_main = line
        for note, raw, page_at in p.notes:
            self.emit_note(note, line, (at(raw), page_at))

    def emit_note(self, note, host, where):
        if host is None:
            sys.exit("a note comes before any passage")
        if note.get("place") != "foot":
            sys.exit(f"unexpected note place {note.get('place')!r}")
        if where is None:                       # note directly in a div
            offset, page = len(host["text"]), self.page
        else:
            offset, page = where
        saved = self.cur
        self.cur = Passage("note", host.get("ref"), page)
        self.fill(note)
        p, self.cur = self.cur, saved
        if p.notes:
            sys.exit("a note inside a note")
        if not p.has_words():
            sys.exit("an empty note")
        self.emit(p, anchor=[host["id"], offset])


def main():
    (typed,) = require(VDIR, SOURCES)
    root = parse(typed.path)
    body = root.find("text/body")
    conv = Converter(body)
    conv.walk(body)
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
        "converter": str((VDIR / "convert" / "extract_eng.py").relative_to(ROOT)),
        "ref_scheme": ["book", "chapter"],
        "rights": "Text public domain (published 1855-1857); typed text by Perseus Digital "
                  "Library, CC BY-SA 4.0.",
        "status": "complete",
        "review": "none",
        "notes": NOTES,
    }
    with open(RAW / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(conv.lines)} passages, {len(conv.pages)} pages")


NOTES = (
    "Plain extraction of the typed text: words, numbers and labels as Perseus typed them, "
    "errors included. "
    "ref is book.chapter, Hardouin's chapters as printed by the translators (the same "
    "numbers as the older chapters of the Latin text, field x_old_chapter of "
    "3_Pliny_original_Mayhoff); the translation has no section numbers. The chapter "
    "numbers are those of the typed file: some are wrong, and the summaries of Pliny's "
    "book 1, the errata and the translators' afterword are labelled with the chapter they "
    "are typed in. "
    "Greek is in Beta Code, as typed. Perseus' '<*>' (a character it could not read) is "
    "kept. The entity &cdot; is read as '·', the decimal point. A hyphen at the end of a "
    "typed line is kept and the word written together ('na-ture'). Tables are written as "
    "their cells in order, separated by spaces."
)

if __name__ == "__main__":
    main()
