#!/usr/bin/env python3
"""Draw the regions of a PAGE XML file on its page image, numbered and labelled, with a 100 px
coordinate grid, to check a layout or to write its fix list (tools/layout_fix.py). Needs Pillow.

Usage: uv run tools/layout_view.py <layout .xml> <page image> <output .jpg>
Prints one line per region: number, label, x0 y0 x1 y1.
"""
import re, sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
xml, png, out = sys.argv[1:4]
t = open(xml, encoding="utf-8").read()
im = Image.open(png).convert("RGB")
d = ImageDraw.Draw(im)
w = max(4, im.width // 300)
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", im.width // 45)
except OSError: font = ImageFont.load_default()
cols = {"Main": (220, 0, 0), "Margin": (0, 90, 220), "Running": (0, 150, 0), "Numbering": (0, 150, 0), "Quire": (0, 150, 0), "Drop": (200, 0, 200), "Graphic": (230, 140, 0)}
n = 0
for m in re.finditer(r'<TextRegion([^>]*)>\s*<Coords points="([^"]*)"', t):
    n += 1
    tm = re.search(r"type:([^;]*);", m.group(1))
    typ = tm.group(1) if tm else "?"
    pts = [tuple(map(int, p.split(","))) for p in m.group(2).split()]
    c = next((v for k, v in cols.items() if typ.startswith(k)), (90, 90, 90))
    d.polygon(pts, outline=c, width=w)
    x, y = min(p[0] for p in pts), min(p[1] for p in pts)
    d.text((x + w * 2, y + w * 2), f"{n} {typ}", fill=c, font=font)
    print(n, typ, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
im.thumbnail((1500, 1500))
im.save(out, quality=80)
