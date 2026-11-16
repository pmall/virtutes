#!/usr/bin/env python3
"""Write one page image of a scan as a PNG file, to look at it (needs Pillow).

The scans are archives of JPEG 2000 images, which few viewers open. This reads one image
straight from the archive in source/ (nothing is unpacked there) and writes it to
data/<version folder>/work/pages/<image name>.png.

Usage, from the workspace folder:
    uv run tools/page_image.py <version folder> <archive in source/> <image number>

    <image number> is the position number at the end of the image's name in the archive
    (b21459162_0001_0134.jp2 is image 134); it is not the printed page number.

Example:
    uv run tools/page_image.py 2_Dioscorides_original_Wellmann_1906-1914 b21459162_0002_jp2.zip 134
"""
import io, re, sys, zipfile
from pathlib import Path

from PIL import Image

DATA = Path(__file__).resolve().parents[1] / "data"


def main(argv):
    if len(argv) != 3 or not argv[2].isdigit():
        sys.exit(__doc__)
    vdir = DATA / Path(argv[0]).name
    with zipfile.ZipFile(vdir / "source" / argv[1]) as z:
        names = [n for n in z.namelist()
                 if (m := re.search(r"_(\d+)\.(jp2|jpg)$", n)) and int(m.group(1)) == int(argv[2])]
        if len(names) != 1:
            sys.exit(f"{len(names)} images numbered {argv[2]} in {argv[1]}")
        data = z.read(names[0])
    out = vdir / "work" / "pages" / (Path(names[0]).stem + ".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.open(io.BytesIO(data)).save(out)
    print(out.relative_to(DATA.parent))


if __name__ == "__main__":
    main(sys.argv[1:])
