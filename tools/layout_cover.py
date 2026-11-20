#!/usr/bin/env python3
"""Measure a layout model on the sample pages: how many of the lines Kraken's line finder found
lie inside a block the layout model marked (standard library only).

Usage: uv run tools/layout_cover.py <folder>
<folder> holds one folder per version, named as in works/, with the model's result for each sample
page (<page>.xml). The lines are those of works/<version>/work/ocr_trial/seg/<page>.xml. A line
counts as inside when its middle, 10 px above the baseline, is in a block or within 20 px of one.
The lines are the line finder's, mistakes included: the figure tells how much of the page the
blocks hold, not whether each block is right.
"""
import re, sys
from pathlib import Path
root, S = Path(__file__).resolve().parents[1], Path(sys.argv[1])
for vdir in sorted(S.glob("[1-6]_*")):
    tot = inside = 0; rows = []
    for rx in sorted(vdir.glob("*.xml")):
        seg = root / "works" / vdir.name / "work/ocr_trial/seg" / rx.name
        boxes = []
        for m in re.finditer(r'<TextRegion([^>]*)>\s*<Coords points="([^"]*)"', rx.read_text()):
            pts = [tuple(map(int, p.split(","))) for p in m.group(2).split()]
            boxes.append((min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))
        n = k = 0
        for m in re.finditer(r'<Baseline points="([^"]*)"', seg.read_text()):
            pts = [tuple(map(int, p.split(","))) for p in m.group(1).split()]
            x = sum(p[0] for p in pts) / len(pts); y = sum(p[1] for p in pts) / len(pts) - 10
            n += 1
            k += any(a - 20 <= x <= c + 20 and b - 20 <= y <= d + 20 for a, b, c, d in boxes)
        rows.append(f"{rx.stem} {k}/{n}"); tot += n; inside += k
    print(f"{vdir.name}: {inside}/{tot} = {100*inside/tot:.0f}%   " + "  ".join(rows))
