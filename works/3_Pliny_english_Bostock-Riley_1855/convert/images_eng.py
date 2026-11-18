#!/usr/bin/env python3
"""Link each page of Bostock and Riley's English Pliny to its image in the scans.

Run:  uv run convert/images_eng.py   (no arguments; reads text/eng.pages.csv, written by
      convert/repair_eng.py; writes text/eng.page_images.csv)

Optional third step. The text is complete without it: convert/extract_eng.py and
convert/repair_eng.py make it from the typed file alone. This script only adds, for each
page, where its image is, so that the page can be shown beside the text.

SOURCE FILES NEEDED: the six scans (about 1.57 GB in all), one archive of JPEG 2000 images
per volume, the images numbered from 0 at the end of their name (..._0019.jp2).

THE RULE
Image number = printed page + shift. The shift is constant over a run of pages and grows
where the scan has leaves that carry no page number (plates and their blank backs):
RUNS gives, for each volume, the first page of each run and its shift; a run lasts up to
the page before the next one. Volume 1 has 18 runs (shift 34 for page 1, 36 from
page 2, growing by 2 up to 68 from page 498), volume 6 two (20, then 22 from page 404), the
others one (volume 2: 18, volume 3: 22, volumes 4 and 5: 26). The runs are those of Internet Archive's own reading
of the page numbers (page_numbers in each scan's _metadata.json), the first run of each
volume extended back to page 1 and the last up to the last page of the text; except in
volume 1, where the scan has two blurred images of a page being turned before page 2
(images 36 and 37) and two before page 498 (images 564 and 565), which that reading did
not see: page 1 is image 35, pages 498 to 500 images 566 to 568. The script
stops if a page has no image under this rule. Every row gets mapping "computed".

HOW THE RULE WAS CHECKED
By reading the page number printed at the head of the image (page 1 of a book carries no
number: there, the first words of the book; the last pages of volumes 1 and 2, the
corrections and the errata, are unnumbered too: there, their title) on the pages listed in
CHECKED below: at least six pages spread over each volume, the first and the last
included, and the pages on both sides of eight of the 17 changes of shift of volume 1 and
of the one of volume 6. The rule gave the right image on every one. The other nine
changes of shift of volume 1 rest on Internet Archive's reading alone.
"""
import csv, re, sys, zipfile
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
TEXT = VDIR / "text"
LANG = "eng"
SCANS = {"1": "naturalhistoryof1855plin_jp2.zip", "2": "naturalhistoryof00plin_jp2.zip",
         "3": "naturalhistoryof03plin_jp2.zip", "4": "naturalhistoryof04plin_jp2.zip",
         "5": "naturalhistoryof05plin_jp2.zip", "6": "naturalhistoryof06plin_jp2.zip"}
# volume: [(first printed page of the run, image number - printed page), ...]
RUNS = {
    "1": [(1, 34), (2, 36), (30, 38), (76, 40), (114, 42), (122, 44), (174, 46), (196, 48),
          (224, 50), (228, 52), (340, 54), (354, 56), (372, 58), (432, 60), (464, 62),
          (480, 64), (490, 66), (498, 68)],
    "2": [(1, 18)],
    "3": [(1, 22)],
    "4": [(1, 26)],
    "5": [(1, 26)],
    "6": [(1, 20), (404, 22)],
}
# The pages read on the images: volume: printed pages
CHECKED = {"1": [1, 2, 29, 30, 75, 76, 113, 114, 223, 224, 227, 228, 300, 431, 432, 489, 490,
                   497, 498, 499, 500],
           "2": [1, 2, 3, 150, 300, 450, 555, 556],
           "3": [1, 2, 100, 250, 400, 535, 536],
           "4": [1, 2, 100, 250, 400, 523],
           "5": [1, 2, 100, 250, 400, 523],
           "6": [1, 2, 200, 300, 403, 404, 405, 468]}
SOURCES = list(SCANS.values())                         # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require


def image_number(volume, printed):
    shift = None
    for first, s in RUNS[volume]:
        if printed >= first:
            shift = s
    return printed + shift


def images(path):
    """Image number -> image name in the archive."""
    with zipfile.ZipFile(path) as z:
        return {int(m.group(1)): n for n in z.namelist() if (m := re.search(r"_(\d+)\.jp2$", n))}


def main():
    if not (TEXT / f"{LANG}.pages.csv").exists():
        sys.exit("text/eng.pages.csv is missing: run convert/extract_eng.py then convert/repair_eng.py first")
    scans = {s.name: s.path for s in require(VDIR, SOURCES)}
    with open(TEXT / f"{LANG}.pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))
    if any(page["volume"] not in SCANS or not page["printed"] for page in pages):
        sys.exit("a page has no volume with a scan, or no printed number")

    rows = []
    for volume, scan in SCANS.items():
        names = images(scans[scan])
        for page in pages:
            if page["volume"] == volume:
                k = image_number(volume, int(page["printed"]))
                if k not in names:
                    sys.exit(f"page {page['page']}: no image {k} in {scan}")
                rows.append([page["page"], scan, names[k], "computed"])
    if len({(r[1], r[2]) for r in rows}) != len(rows):
        sys.exit("two pages of the text are linked to the same image")

    with open(TEXT / f"{LANG}.page_images.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "source_file", "image", "mapping"])
        w.writerows(rows)
    print(f"{len(rows)} pages linked to their image")


if __name__ == "__main__":
    main()
