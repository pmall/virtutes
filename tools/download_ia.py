#!/usr/bin/env python3
"""Download Internet Archive items into the source/ folder of a version folder (standard library only).

For each item: its record (<id>_metadata.json, unchanged) and one file, by default the
page-image archive <id>_jp2.zip, kept exactly as delivered and checked against the md5
published by Internet Archive. A file that passes is put in the version's list of source
files, metadata/sources.csv; one row per attempt is appended to the log
works/Downloads_report.csv.

Usage, from the workspace folder:
    uv run tools/download_ia.py <version folder> <item id> [<item id> ...] [--file NAME]

    --file NAME   download this file instead of <id>_jp2.zip (e.g. a PDF when no image
                  archive exists); use {id} for the item id, e.g. --file "{id}.pdf"

Example:
    uv run tools/download_ia.py 2_Dioscorides_french_Mathee_1553 lessixlivresdepe00dios

Nothing is downloaded without the user's go-ahead (AGENTS.md).
"""
import csv, hashlib, json, os, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "works"
UA = "Mozilla/5.0 (research-client)"
PAUSE = 2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import vh_sources


def fetch(url, dest, tries=5):
    part = str(dest) + ".part"
    for a in range(tries):
        try:
            have = os.path.getsize(part) if os.path.exists(part) else 0
            h = {"User-Agent": UA}
            if have:
                h["Range"] = "bytes=%d-" % have
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=180) as r:
                with open(part, "ab" if have and r.status == 206 else "wb") as f:
                    while True:
                        c = r.read(1 << 20)
                        if not c:
                            break
                        f.write(c)
            os.replace(part, dest)
            return
        except Exception as e:
            if getattr(e, "code", None) in (401, 403, 404):
                raise
            print(f"  retry {a + 1}: {e}", flush=True)
            time.sleep(15 * (a + 1))
    raise RuntimeError("failed " + url)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def report(row):
    p = DATA / "Downloads_report.csv"
    new = not p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["folder", "file", "source", "bytes", "md5", "check"])
        w.writerow(row)


def main(argv):
    if "--file" in argv:
        i = argv.index("--file")
        pattern = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    else:
        pattern = "{id}_jp2.zip"
    if len(argv) < 2:
        sys.exit(__doc__)
    folder, items = argv[0], argv[1:]
    d = DATA / folder / "source"  # library files, kept as delivered
    d.mkdir(parents=True, exist_ok=True)
    for item in items:
        meta_path = d / f"{item}_metadata.json"
        if not meta_path.exists():
            fetch(f"https://archive.org/metadata/{item}", meta_path)
            time.sleep(PAUSE)
        files = {f["name"]: f for f in json.load(open(meta_path, encoding="utf-8"))["files"]}
        name = pattern.format(id=item)
        if name not in files:
            print(f"{item}: no file {name} in this item", flush=True)
            report([folder, name, f"https://archive.org/details/{item}", "", "", "FAILED: file not in item"])
            continue
        out = d / name
        want = int(files[name]["size"])
        if not (out.exists() and out.stat().st_size == want):
            print(f"{folder}: {name} ({want / 1e6:.0f} MB)", flush=True)
            fetch(f"https://archive.org/download/{item}/{name}", out)
            time.sleep(PAUSE)
        ok = md5(out) == files[name].get("md5")
        print(f"  {name}: md5 {'OK' if ok else 'MISMATCH'}", flush=True)
        if ok:
            vh_sources.add(DATA / folder, name, out.stat().st_size, files[name]["md5"],
                           f"https://archive.org/download/{item}/{name}")
        report([folder, name, f"https://archive.org/details/{item}", out.stat().st_size,
                files[name].get("md5"), "OK" if ok else "MD5 MISMATCH"])


if __name__ == "__main__":
    main(sys.argv[1:])
