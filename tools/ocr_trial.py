#!/usr/bin/env python3
"""Read the sample pages of a scan with every model a version lists, for the test of a reading.

Usage, from the workspace folder:
    uv run tools/ocr_trial.py <version folder>

Before: the sample page images are in works/<version>/work/ocr_trial/pages/<page>.png
(how to make them: skills/test-scan-reading/SKILL.md), and the models are fetched
(tools/ocr_models.py).

It reads works/<version>/convert/ocr_models.csv. With the one model of role "segmentation" it
finds the lines of each page and writes them to work/ocr_trial/seg/<page>.xml (PAGE XML).
Then, with each model of role "recognition", it reads those same lines and writes the text to
work/ocr_trial/ocr/<model>/<page>.txt, <model> being the model's file name without its
extension. All models read the same lines, so they are compared on the reading alone.
A page or model already done is not done again; delete its output to redo it.
The scores are given by tools/ocr_score.py.

Kraken runs on the CPU unless the computer has a GPU that PyTorch can use.
"""
import subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ocr_models import ROOT, model_path, rows


def kraken(args):
    r = subprocess.run(["kraken", "-r", "--threads", "8", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout[-2000:] + r.stderr[-2000:])


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__)
    version = Path(argv[0]).name
    trial = ROOT / "works" / version / "work" / "ocr_trial"
    pages = sorted((trial / "pages").glob("*.png"))
    if not pages:
        sys.exit(f"no page images in {trial / 'pages'}")
    models = rows(version)
    seg = [m for m in models if m["role"] == "segmentation"]
    if len(seg) != 1:
        sys.exit(f"{len(seg)} segmentation models listed, 1 expected")
    for m in models:
        if not model_path(m).exists():
            sys.exit(f"{m['name']} is not fetched: run tools/ocr_models.py {version}")

    (trial / "seg").mkdir(exist_ok=True)
    todo = [p for p in pages if not (trial / "seg" / f"{p.stem}.xml").exists()]
    if todo:
        # absolute image paths, so that the XML files point to their images from anywhere
        args = [a for p in todo for a in ("-i", str(p), str(trial / "seg" / f"{p.stem}.xml"))]
        kraken(["-x", *args, "segment", "-bl", "-i", str(model_path(seg[0]))])
        print(f"lines found on {len(todo)} pages")

    for m in models:
        if m["role"] != "recognition":
            continue
        out = trial / "ocr" / Path(m["file"]).stem
        out.mkdir(parents=True, exist_ok=True)
        todo = [p for p in pages if not (out / f"{p.stem}.txt").exists()]
        if todo:
            args = [a for p in todo
                    for a in ("-i", str(trial / "seg" / f"{p.stem}.xml"), str(out / f"{p.stem}.txt"))]
            kraken(["-f", "page", *args, "ocr", "-m", str(model_path(m))])
        print(f"read {len(pages)} pages with {m['name']}")


if __name__ == "__main__":
    main(sys.argv[1:])
