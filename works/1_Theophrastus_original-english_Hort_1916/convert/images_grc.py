#!/usr/bin/env python3
"""Link each Greek page of Hort's Theophrastus to its image in the scan.

Run:  uv run convert/images_grc.py   (no arguments; reads text/grc.pages.csv, written by
      convert/repair_grc.py; writes text/grc.page_images.csv)

Third step, after convert/extract_grc.py and convert/repair_grc.py. It adds, for each page
of the Greek text, where its image is, so that the page can be shown beside the text.

SOURCE FILES NEEDED: the scan, Theophrastus_Enquiry_Plants_Loeb.pdf (both volumes in one
PDF of 1,014 pages; the page count was read with pdfinfo). The image of a page is given
as its page number in the PDF.

THE RULE
PDF page = printed page + 25 in volume 1.
In volume 2, PDF page = printed page + 509 up to page 31, and + 513 from page 32 on: the
scan holds pages 28 to 31 of volume 2 twice (PDF pages 537-540, then again 541-544, two
photographs of the same pages). Pages 28 and 30 are linked to the first of the two.
Every row gets mapping "computed".

HOW THE RULE WAS CHECKED
- By script, on every page: the first words of each page of the text were looked for in
  the PDF's own text layer. For 370 of the 390 pages (223 in volume 1, 147 in volume 2)
  they are found at the page the rule gives and nowhere else. For 6 they are found at that
  page and at one other. For 14 the text layer is too poor to find them. For none are
  they found only at another page.
- By eye, reading the page number printed at the foot of the image: volume 1 pages 2, 66,
  120, 240, 360, 436, 474 (PDF 27, 91, 145, 265, 385, 461, 499); volume 2 pages 2, 26, 28,
  30, 32, 160, 216, 320 (PDF 511, 535, 537, 539, 545, 673, 729, 833), and the second
  photographs of pages 28 and 30 (PDF 541, 543).
The pages are those of text/grc.pages.csv, after the repair of page 216 of volume 2
(convert/repair_grc.py).
"""
import csv, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
TEXT = VDIR / "text"
LANG = "grc"
SCAN = "Theophrastus_Enquiry_Plants_Loeb.pdf"
SOURCES = [SCAN]                                       # the files of source/ this script reads
PDF_PAGES = 1014
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require


def pdf_page(volume, printed):
    if volume == "1":
        return printed + 25
    return printed + (509 if printed <= 31 else 513)


def main():
    if not (TEXT / f"{LANG}.pages.csv").exists():
        sys.exit("text/grc.pages.csv is missing: run convert/extract_grc.py then convert/repair_grc.py first")
    require(VDIR, SOURCES)
    with open(TEXT / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    rows = []
    for page in pages:
        if page["volume"] not in ("1", "2"):
            sys.exit(f"page {page['page']}: volume {page['volume']} is not in the scan")
        k = pdf_page(page["volume"], int(page["printed"]))
        if not 1 <= k <= PDF_PAGES:
            sys.exit(f"page {page['page']}: no page {k} in {SCAN}")
        rows.append([page["page"], SCAN, k, "computed"])
    if len({r[2] for r in rows}) != len(rows):
        sys.exit("two pages of the text are linked to the same image")

    with open(TEXT / f"{LANG}.page_images.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "source_file", "image", "mapping"])
        w.writerows(rows)
    print(f"{len(rows)} pages linked to their image")


if __name__ == "__main__":
    main()
