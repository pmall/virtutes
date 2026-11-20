#!/usr/bin/env python3
"""Make the page images and the page lists of one layout fine-tuning folder (needs Pillow).

Usage, from the workspace folder:
    uv run tools/layout_pages.py finetuning/layout/<name>

Reads <folder>/pages.csv (columns version, archive, image, set; set is train or held_out). For each
row it writes, if missing, <folder>/pages/<version>/img<image>.jpg: the image read straight from the
scan archive in the version's source/, reduced to 2000 px high (the size the model is trained at).
The fixed layout of the page is the file img<image>.xml beside it (PAGE XML, in git; it names its
image by file name only, so the folder can be moved). The images are not in git: this makes them again.

Then it writes <folder>/work/train.txt and <folder>/work/held_out.txt, the lists the trainer reads:
one fixed page per line, only pages whose .xml exists.
"""
import csv, io, sys, zipfile
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__)
    folder = Path(argv[0]).resolve()
    rows = list(csv.DictReader(open(folder / "pages.csv", newline="")))
    lists = {"train": [], "held_out": []}
    for arc in sorted({(r["version"], r["archive"]) for r in rows}):
        want = {int(r["image"]): r for r in rows if (r["version"], r["archive"]) == arc}
        out = folder / "pages" / arc[0]
        out.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ROOT / "works" / arc[0] / "source" / arc[1]) as z:
            for name in z.namelist():
                if not name.endswith((".jp2", ".jpg")) or int(name[-8:-4]) not in want:
                    continue
                jpg = out / f"img{name[-8:-4]}.jpg"
                if not jpg.exists():
                    im = Image.open(io.BytesIO(z.read(name))).convert("RGB")
                    im = im.resize((round(im.width * 2000 / im.height), 2000), Image.LANCZOS)
                    im.save(jpg, quality=90)
                    print("made", jpg.relative_to(folder))
                if jpg.with_suffix(".xml").exists():
                    lists[want[int(name[-8:-4])]["set"]].append(str(jpg.with_suffix(".xml")))
    (folder / "work").mkdir(exist_ok=True)
    for name, paths in lists.items():
        (folder / "work" / f"{name}.txt").write_text("".join(p + "\n" for p in sorted(paths)))
        print(f"{name}: {len(paths)} fixed pages")


if __name__ == "__main__":
    main(sys.argv[1:])
