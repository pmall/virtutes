#!/usr/bin/env python3
"""Link each page of Mayhoff's Latin Pliny to its image in the scans.

Run:  uv run convert/images_lat.py   (no arguments; reads text/lat.pages.csv, written by
      convert/repair_lat.py; writes text/lat.page_images.csv)

Optional third step. The text is complete without it: convert/extract_lat.py and
convert/repair_lat.py make it from the typed file alone. This script only adds, for each
page, where its image is, so that the page can be shown beside the text.

SOURCE FILES NEEDED: the five scans (about 910 MB in all), one per volume. Volumes 1, 2, 3
and 5 are archives of JPEG 2000 images numbered from 0; volume 4 is a PDF of 521 pages
(count read with pdfinfo), whose image is given as its page number in the PDF.

THE RULE
Image number = printed page + 22 in volume 1, + 20 in volume 2, + 20 in volume 3,
+ 16 in volume 5; PDF page = printed page + 17 in volume 4. The script stops if a page has
no image under this rule. Every row gets mapping "computed". The front pages of each
volume (page ids "v<volume>t", without printed number) are not matched and get no row.

HOW THE RULE WAS CHECKED
By reading the page number printed at the head of the image: volume 1 pages 10, 100, 250,
400, 522; volume 2 pages 5, 150, 323, 432, 555; volume 3 pages 3, 100, 250, 400, 491;
volume 4 pages 5, 53, 150, 300, 474; volume 5 pages 2, 48, 200, 350, 477. The shift is
the same on every one. The shifts were first suggested by Internet Archive's own reading
of the page numbers (page_numbers in each scan's _metadata.json), which gives one
constant shift per volume over the whole text. Pages 323 and 432 of volume 2, which the
typed file does not mark, are in the scan at the place the rule gives.
"""
import csv, re, sys, zipfile
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
TEXT = VDIR / "text"
LANG = "lat"
SHIFTS = {"1": ("cplinisecvndinat0001caro_jp2.zip", 22),
          "2": ("cplinisecvndinat0002caro_jp2.zip", 20),
          "3": ("naturalhistoriae0003caro_jp2.zip", 20),
          "4": ("cplinisecundina13plingoog.pdf", 17),
          "5": ("cplinisecundinat0000caro_jp2.zip", 16)}   # volume: (scan, image - printed page)
PDF_PAGES = {"cplinisecundina13plingoog.pdf": 521}
SOURCES = [scan for scan, _ in SHIFTS.values()]        # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require


def images(scan, path):
    """Image number -> image as written in the page images file."""
    if scan in PDF_PAGES:
        return {k: k for k in range(1, PDF_PAGES[scan] + 1)}
    with zipfile.ZipFile(path) as z:
        return {int(m.group(1)): n for n in z.namelist() if (m := re.search(r"_(\d+)\.jp2$", n))}


def main():
    if not (TEXT / f"{LANG}.pages.csv").exists():
        sys.exit("text/lat.pages.csv is missing: run convert/extract_lat.py then convert/repair_lat.py first")
    scans = {s.name: s.path for s in require(VDIR, SOURCES)}
    with open(TEXT / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    rows = []
    for volume, (scan, shift) in SHIFTS.items():
        names = images(scan, scans[scan])
        for page in pages:
            if page["volume"] == volume and page["printed"]:
                k = int(page["printed"]) + shift
                if k not in names:
                    sys.exit(f"page {page['page']}: no image {k} in {scan}")
                rows.append([page["page"], scan, names[k], "computed"])
    if any(page["volume"] not in SHIFTS for page in pages):
        sys.exit("some pages are in a volume without a scan")
    if len({(r[1], r[2]) for r in rows}) != len(rows):
        sys.exit("two pages of the text are linked to the same image")

    with open(TEXT / f"{LANG}.page_images.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "source_file", "image", "mapping"])
        w.writerows(rows)
    print(f"{len(rows)} pages linked to their image")


if __name__ == "__main__":
    main()
