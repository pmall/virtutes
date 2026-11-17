#!/usr/bin/env python3
"""Link each page of Wellmann's Dioscorides to its image in the scans.

Run:  uv run convert/images.py   (no arguments; reads text/pages.csv, written by
      convert/repair.py; writes text/page_images.csv)

Optional third step. The text is complete without it: convert/extract.py and
convert/repair.py make it from the typed file alone. This script only adds, for each
page, where its image is, so that the page can be shown beside the text.

SOURCE FILES NEEDED: the three scans (b21459162_0001_jp2.zip, _0002, _0003; 465 MB in
all), one per volume, each an archive of images numbered from 1.

THE RULE
Image number = printed page + 14 in volume 1, + 34 in volume 2, + 14 in volume 3. The
script stops if a page has no image under this rule. Every row gets mapping "computed".

HOW THE RULE WAS CHECKED
By reading the page number printed on the image: volume 1 pages 6, 26, 46, 81-90,
106-109, 146, 186, 226, 254, 255; volume 2 pages 2, 3, 50, 81, 84, 85, 100, 150, 200, 286,
289, 300, 339; volume 3 pages 14, 16, 26, 50, 80, 106-108. The shift is the same on every
one. Page 1 of each volume prints no number at the top; it is the image before page 2.
The pages are those of text/pages.csv, after the repair of page 83 of volume 1
(convert/repair.py, rule 6).
"""
import csv, re, sys, zipfile
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
TEXT = VDIR / "text"
SHIFTS = {"1": ("b21459162_0001_jp2.zip", 14), "2": ("b21459162_0002_jp2.zip", 34),
          "3": ("b21459162_0003_jp2.zip", 14)}        # volume: (scan, image - printed page)
SOURCES = [scan for scan, _ in SHIFTS.values()]        # the files of source/ this script reads
sys.path.insert(0, str(ROOT / "tools"))
from vh_sources import require
from vh_check import record


def main():
    if not (TEXT / "pages.csv").exists():
        sys.exit("text/pages.csv is missing: run convert/extract.py then convert/repair.py first")
    sources = require(VDIR, SOURCES)
    scans = {s.name: s.path for s in sources}
    with open(TEXT / "pages.csv", newline="", encoding="utf-8") as f:
        pages = list(csv.DictReader(f))

    rows = []
    for volume, (scan, shift) in SHIFTS.items():
        with zipfile.ZipFile(scans[scan]) as z:
            names = {int(m.group(1)): n for n in z.namelist()
                     if (m := re.search(r"_(\d+)\.jp2$", n))}
        for page in pages:
            if page["volume"] == volume:
                k = int(page["printed"]) + shift
                if k not in names:
                    sys.exit(f"page {page['page']}: no image {k} in {scan}")
                rows.append([page["page"], scan, names[k], "computed"])
    if len(rows) != len(pages):
        sys.exit("some pages are in a volume without a scan")

    with open(TEXT / "page_images.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "source_file", "image", "mapping"])
        w.writerows(rows)
    record(__file__, read=[TEXT / "pages.csv"] + sources, wrote=[TEXT / "page_images.csv"])
    print(f"{len(rows)} pages linked to their image")


if __name__ == "__main__":
    main()
