#!/usr/bin/env python3
"""Download page images from a library that serves single pages (IIIF), then pack them.

For one volume: the library's page list (<id>_manifest.json, unchanged), every page image
at full size (or a range of pages), packed without recompression into <id>_jpg.zip with
the images at the top level, and <id>_pages.csv (one row per image: position, the library's
page label, source URL, size, md5). Every image in the zip is checked against its md5.
One row is appended to data/Downloads_report.csv.

Usage, from the workspace folder:
    python3 tools/download_iiif_pages.py <version folder> <identifier> <manifest URL> [--first N] [--last M]

    --first/--last   positions in the library's page list (1 = first image), inclusive

Example (Bayerische Staatsbibliothek):
    python3 tools/download_iiif_pages.py 6_Petit-Bauhin_original_1671 bsb10300968 \\
        https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb10300968/manifest

Rules (AGENTS.md, docs/Folder_structure.md): nothing is downloaded without the user's go-ahead;
one request per second; generic client name.
"""
import csv, hashlib, json, os, shutil, sys, time, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "data"
UA = "Mozilla/5.0 (research-client)"
PAUSE = 1


def get(url, dest=None, tries=5):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=180) as r:
                data = r.read()
            if dest is None:
                return data
            tmp = str(dest) + ".part"
            open(tmp, "wb").write(data)
            os.replace(tmp, dest)
            return None
        except Exception as e:
            if getattr(e, "code", None) in (401, 403, 404):
                raise
            print(f"  retry {a + 1} {url}: {e}", flush=True)
            time.sleep(15 * (a + 1))
    raise RuntimeError("failed " + url)


def pages(manifest):
    """Return [(label, image URL at full size)] for IIIF Presentation v2 or v3."""
    out = []
    if "sequences" in manifest:  # v2
        for c in manifest["sequences"][0]["canvases"]:
            svc = c["images"][0]["resource"]["service"]
            svc = svc[0] if isinstance(svc, list) else svc
            out.append((str(c.get("label", "")), svc["@id"].rstrip("/") + "/full/full/0/default.jpg"))
    else:  # v3
        for c in manifest["items"]:
            body = c["items"][0]["items"][0]["body"]
            svc = body["service"][0]
            sid = svc.get("id") or svc.get("@id")
            label = c.get("label", {})
            label = next(iter(label.values()))[0] if isinstance(label, dict) and label else str(label)
            out.append((label, sid.rstrip("/") + "/full/max/0/default.jpg"))
    return out


def main(argv):
    first = last = None
    for flag in ("--first", "--last"):
        if flag in argv:
            i = argv.index(flag)
            val = int(argv[i + 1])
            argv = argv[:i] + argv[i + 2:]
            if flag == "--first":
                first = val
            else:
                last = val
    if len(argv) != 3:
        sys.exit(__doc__)
    folder, ident, manifest_url = argv
    vdir = DATA / folder / "source"  # library files, kept as delivered
    work = vdir / f"{ident}.parts"
    work.mkdir(parents=True, exist_ok=True)
    mpath = vdir / f"{ident}_manifest.json"
    if not mpath.exists():
        get(manifest_url, mpath)
        time.sleep(PAUSE)
    plist = pages(json.load(open(mpath, encoding="utf-8")))
    a, b = (first or 1), (last or len(plist))
    print(f"{folder}/{ident}: pages {a}-{b} of {len(plist)}", flush=True)
    rows = []
    for n in range(a, b + 1):
        label, url = plist[n - 1]
        out = work / f"{n:04d}.jpg"
        if not (out.exists() and out.stat().st_size > 0):
            get(url, out)
            time.sleep(PAUSE)
        data = out.read_bytes()
        assert data[:2] == b"\xff\xd8", f"not a JPEG: page {n}"
        rows.append([n, label, url, len(data), hashlib.md5(data).hexdigest()])
        if (n - a + 1) % 50 == 0:
            print(f"  {n - a + 1}/{b - a + 1}", flush=True)
    with open(vdir / f"{ident}_pages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["position", "label", "source_url", "bytes", "md5"])
        w.writerows(rows)
    zpath = vdir / f"{ident}_jpg.zip"
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_STORED) as z:
        for r in rows:
            z.write(work / f"{r[0]:04d}.jpg", arcname=f"{r[0]:04d}.jpg")
    want = {f"{r[0]:04d}.jpg": r[4] for r in rows}
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None and len(z.namelist()) == len(rows)
        for name in z.namelist():
            assert hashlib.md5(z.read(name)).hexdigest() == want[name], name
    shutil.rmtree(work)
    h = hashlib.md5(zpath.read_bytes()).hexdigest()
    p = DATA / "Downloads_report.csv"
    with open(p, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([folder, f"{ident}_jpg.zip ({len(rows)} page images, positions {a}-{b}; "
                                f"per-page md5 in {ident}_pages.csv)", manifest_url, zpath.stat().st_size, h, "OK"])
    print(f"  {ident}_jpg.zip: {len(rows)} images, {zpath.stat().st_size / 1e6:.0f} MB, all verified", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
