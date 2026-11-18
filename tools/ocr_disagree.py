#!/usr/bin/env python3
"""List the reference lines that some reading model reads otherwise, with an image of each line.

Usage, from the workspace folder:
    uv run tools/ocr_disagree.py <version folder> <model> [<model> ...]

    <model>  a folder name of work/ocr_trial/ocr/ (the model's file name without extension);
             give the best two or three models.

For each reference page (convert/reference/<page>.txt or .draft.txt) and each of its lines, it
finds the most similar line in each model's reading. If any model's line has other words than
the reference line, compared as tools/ocr_score.py compares them (case, punctuation, numbers,
long s, ligatures, u/v and i/j set aside), it saves an image of that line, cut from the page
image with the position Kraken found (work/ocr_trial/seg/<page>.xml), to
work/ocr_trial/check/<page>_<line number>.png, and prints the reference line and each reading.
These are the lines to look at again on the image, to settle who is right
(skills/test-scan-reading/SKILL.md). Lines of the running head and the page number are skipped.
"""
import difflib, re, sys, unicodedata
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ocr_score import words

ROOT = Path(__file__).resolve().parents[1]


def boxes(xml):
    """The image file and the bounding box of each line, in the order of the PAGE XML."""
    image = re.search(r'imageFilename="([^"]+)"', xml).group(1)
    out = []
    for m in re.finditer(r"<TextLine.*?<Coords points=\"([^\"]+)\"", xml, re.S):
        pts = [tuple(map(int, p.split(","))) for p in m.group(1).split()]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append((min(xs), min(ys), max(xs), max(ys)))
    return image, out


def similar(a, b):
    return difflib.SequenceMatcher(None, " ".join(words(a)), " ".join(words(b))).ratio()


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    vdir = ROOT / "works" / Path(argv[0]).name
    trial = vdir / "work" / "ocr_trial"
    models = argv[1:]
    check = trial / "check"
    check.mkdir(exist_ok=True)
    count = 0
    for ref in sorted((vdir / "convert" / "reference").glob("*.txt")):
        page = ref.name.removesuffix(".txt").removesuffix(".draft")
        blocks = unicodedata.normalize("NFC", ref.read_text(encoding="utf-8")).strip("\n").split("\n\n")
        lines = [l for b in blocks[1:3] for l in b.splitlines()]      # main text and notes
        image, bx = boxes((trial / "seg" / f"{page}.xml").read_text(encoding="utf-8"))
        img = Image.open(image).convert("L")
        reads = {m: (trial / "ocr" / m / f"{page}.txt").read_text(encoding="utf-8").splitlines()
                 for m in models}
        main_count = len(blocks[1].splitlines())
        for i, line in enumerate(lines):
            got = {m: max(r, key=lambda x: similar(line, x)) for m, r in reads.items()}
            if all(words(g) == words(line) for g in got.values()):
                continue
            first = reads[models[0]]
            j = first.index(got[models[0]])
            x0, y0, x1, y1 = bx[j] if j < len(bx) else (0, 0, img.width, img.height)
            crop = img.crop((max(0, x0 - 20), max(0, y0 - 25), min(img.width, x1 + 20),
                             min(img.height, y1 + 25)))
            part = "main" if i < main_count else "note"
            name = f"{page}_{part}{i + 1:02d}.png"
            crop.save(check / name)
            count += 1
            print(f"== {name}\n   reference    : {line}")
            for m, g in got.items():
                print(f"   {m[:13]:<13}: {g}")
    print(f"\n{count} lines to look at again, images in {check.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
