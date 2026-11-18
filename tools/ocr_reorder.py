#!/usr/bin/env python3
"""Put the lines of a reading back in column order, from their positions on the page (standard library only).

Usage, from the workspace folder:
    uv run tools/ocr_reorder.py <version folder> <model> <output folder>

    <model>          a folder name of work/ocr_trial/ocr/ (the model's file name without extension)
    <output folder>  where <page>.txt is written, the same lines in the new order

Why: on pages in two columns, Kraken's line finder can give the lines in an order that mixes
the blocks of the two columns (first seen on Du Pinet 1561, convert/ocr_test.md). A line out of
order is a record out of place, and tools/ocr_score.py counts its words as wrong twice. This puts
the lines back in order, to measure the reading apart from the order; it is a test of a possible
fix, not part of the conversion.

How: line i of the reading is TextLine i of work/ocr_trial/seg/<page>.xml. The gutter is the
narrowest strip, between 30% and 65% of the page width, that the fewest lines cross. A line
whose middle is left of the gutter is in the left column, otherwise in the right one; a line
that lies wholly outside the main text (left of where most left-column lines start, or right of
where most right-column lines end) is a margin note and goes last. Lines are sorted by column,
then from top to bottom by the height of their baseline. A line that the line finder drew across
the gutter stays one line.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def order(xml):
    """The new order of the lines of a PAGE XML file, as a list of their old positions."""
    width = int(re.search(r'imageWidth="(\d+)"', xml).group(1))
    lines = []
    for m in re.finditer(r"<TextLine.*?</TextLine>", xml, re.S):
        pts = [tuple(map(int, p.split(","))) for p in
               re.search(r'<Baseline points="([^"]+)"', m.group(0)).group(1).split()]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        lines.append((min(xs), max(xs), sum(ys) / len(ys)))
    bins = 200
    cover = [0] * bins
    for x0, x1, _ in lines:
        for k in range(int(x0 / width * bins), min(bins, int(x1 / width * bins) + 1)):
            cover[k] += 1
    gutter = min(range(int(bins * 0.3), int(bins * 0.65)), key=lambda k: cover[k]) / bins * width
    middle = lambda l: (l[0] + l[1]) / 2
    median = lambda v: sorted(v)[len(v) // 2]
    left_start = median([l[0] for l in lines if middle(l) < gutter])
    right_end = median([l[1] for l in lines if middle(l) >= gutter])

    def column(l):
        if l[1] < left_start or l[0] > right_end - 0.02 * width:
            return 2
        return 0 if middle(l) < gutter else 1

    return sorted(range(len(lines)), key=lambda i: (column(lines[i]), lines[i][2]))


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    trial = ROOT / "works" / Path(argv[0]).name / "work" / "ocr_trial"
    out = Path(argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for reading in sorted((trial / "ocr" / argv[1]).glob("*.txt")):
        xml = (trial / "seg" / f"{reading.stem}.xml").read_text(encoding="utf-8")
        new = order(xml)
        text = reading.read_text(encoding="utf-8").split("\n")
        text += [""] * (len(new) - len(text))
        (out / reading.name).write_text("\n".join(text[i] for i in new), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
