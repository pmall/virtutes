#!/usr/bin/env python3
"""Fetch the reading models a version lists, and verify them (standard library only).

Usage, from the workspace folder:
    uv run tools/ocr_models.py <version folder>

Reads works/<version>/convert/ocr_models.csv (columns role, name, file, bytes, md5, address;
address is the DOI of the exact version of the model on Zenodo, https://doi.org/10.5281/
zenodo.<record>). Each model is kept once for all versions, in models/<record>/<file> at the
top of the workspace (not in git: it can be fetched again). A model already there is only
verified. A model missing is downloaded from Zenodo, then verified; a file whose size or
checksum is not the listed one is refused and removed, and the command stops.

This is a download: run it only after the user's go-ahead for the models listed (AGENTS.md).
"""
import csv, hashlib, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def model_path(row):
    """Where a listed model is kept: models/<Zenodo record>/<file>."""
    record = re.search(r"zenodo\.(\d+)$", row["address"])
    if not record:
        sys.exit(f"{row['name']}: the address is not a Zenodo DOI: {row['address']}")
    return MODELS / record.group(1) / row["file"]


def rows(version):
    with open(ROOT / "works" / version / "convert" / "ocr_models.csv", newline="") as f:
        return list(csv.DictReader(f))


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__)
    for row in rows(Path(argv[0]).name):
        path = model_path(row)
        if not path.exists():
            record = path.parent.name
            url = f"https://zenodo.org/records/{record}/files/{row['file']}?download=1"
            path.parent.mkdir(parents=True, exist_ok=True)
            part = path.with_suffix(path.suffix + ".part")
            req = urllib.request.Request(url, headers={"User-Agent": "generic-client"})
            with urllib.request.urlopen(req) as r, open(part, "wb") as out:
                while block := r.read(1 << 20):
                    out.write(block)
            part.rename(path)
            print(f"downloaded {path.relative_to(ROOT)}")
        if path.stat().st_size != int(row["bytes"]) or md5(path) != row["md5"]:
            path.unlink()
            sys.exit(f"{path.relative_to(ROOT)}: not the listed file (size or checksum); removed")
        print(f"ok  {row['role']:<12} {row['name']}")


if __name__ == "__main__":
    main(sys.argv[1:])
