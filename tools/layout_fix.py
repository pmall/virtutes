#!/usr/bin/env python3
"""Write the fixed layout of a page (PAGE XML) from a layout model's result and a list of fixes
(needs OpenCV, which comes with kraken).

Usage: uv run tools/layout_fix.py <model layout .xml> <page image> <fix list .txt> <output .xml>

Fix list, one instruction per line (# starts a comment); coordinates are x0 y0 x1 y1 in pixels of
the page image, region numbers are those tools/layout_view.py prints and draws:
    m 3 5 8                  keep the model's regions 3, 5 and 8 as they are
    m 3 as MainZone-P        keep region 3 with another label
    MainZone-P 70 140 520 1770    add a region; it is shrunk to the ink it holds
    MainZone-P 70 140 520 1770 =  add a region exactly as given
Model regions not named are dropped. Labels are the SegmOnto names the model was trained with.
The output names its image by file name only: it must be written beside the image.
"""
import re, sys, uuid, cv2, numpy as np
src, img, spec, out = sys.argv[1:5]
t = open(src, encoding="utf-8").read()
model = []
for m in re.finditer(r'<TextRegion([^>]*)>\s*<Coords points="([^"]*)"', t):
    pts = [tuple(map(int, p.split(","))) for p in m.group(2).split()]
    model.append((re.search(r"type:([^;]*);", m.group(1)).group(1), min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))
g = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
ink = g.astype(int) < cv2.medianBlur(g, 51).astype(int) - 45
def shrink(x0, y0, x1, y1):
    sub = ink[y0:y1, x0:x1]
    ys = np.where(sub.sum(1) >= 3)[0]; xs = np.where(sub.sum(0) >= 3)[0]
    if not len(ys) or not len(xs): sys.exit(f"no ink in {x0} {y0} {x1} {y1}")
    return max(x0 + xs[0] - 3, 0), max(y0 + ys[0] - 3, 0), x0 + xs[-1] + 4, y0 + ys[-1] + 4
regions = []
for line in open(spec, encoding="utf-8"):
    f = line.split("#")[0].split()
    if not f: continue
    if f[0] == "m":
        lab = None
        if "as" in f: lab = f[f.index("as") + 1]; f = f[:f.index("as")]
        for i in f[1:]:
            r = model[int(i) - 1]; regions.append((lab or r[0], *r[1:]))
    else:
        box = tuple(map(int, f[1:5]))
        regions.append((f[0], *(box if f[-1] == "=" else shrink(*box))))
h, w = g.shape
head = t[:t.index("<TextRegion")] if "<TextRegion" in t else t[:t.index("</Page>")]
head = re.sub(r'imageFilename="[^"]*"', f'imageFilename="{img.rsplit("/", 1)[-1]}"', head)
head = re.sub(r"<Creator>[^<]*</Creator>", "<Creator>layout model, then fixed</Creator>", head)
body = "".join(f'        <TextRegion id="_{uuid.uuid5(uuid.NAMESPACE_URL, f"{img}{k}")}" custom="structure {{type:{l};}}">\n<Coords points="{x0},{y0} {x0},{y1} {x1},{y1} {x1},{y0}"/>        </TextRegion>\n' for k, (l, x0, y0, x1, y1) in enumerate(regions))
open(out, "w", encoding="utf-8").write(head + body + "    </Page>\n</PcGts>\n")
print(len(regions), "regions")
