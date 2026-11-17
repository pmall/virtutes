#!/usr/bin/env python3
"""Check what the scripts of a version produced against the recorded results (standard library only).

One check for every version, whatever its source (typed text, scan of a printed book, scan
of a manuscript). The reference is convert/results.md5 of the version, kept in git: the
checksum of every file the version's scripts produce (written by tools/vh_record.py). A
researcher who runs the scripts on the recorded source files must obtain these files.

Usage, from the workspace folder:
    uv run tools/vh_check.py <version folder> [<version folder> ...]
    uv run tools/vh_check.py                 every version that has a convert/ folder

For each version it verifies, and prints:
1. the source files present in source/ are the ones recorded in data/Downloads_report.csv
   (an absent one is only reported: not every script needs every file);
2. each produced file has the checksum of convert/results.md5; a file not made yet is only
   reported (text/page_images.csv is optional); a file in work/raw/ or text/ that the
   reference does not list is a problem;
3. the shape of the raw text and of the final text (tools/vh_text.py), which includes
   that text/page_images.csv, if there, names only pages of text/pages.csv.
The command ends with OK, or with the number of problems.

A different checksum means one of two things: the result is not reproduced (another
source file, a changed script, a file edited by hand, a script not run again after an
earlier one), or the scripts were changed on purpose and the new results have not been
recorded yet with tools/vh_record.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vh_sources, vh_text

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "data"
RESULT_FOLDERS = ["work/raw", "text"]       # everything in them is a result
RESULT_FILES = ["work/repairs.csv"]         # and these single files
OPTIONAL = {"text/page_images.csv"}


def produced(vdir):
    """The result files now in a version folder, as paths relative to it, in a fixed order."""
    found = []
    for folder in RESULT_FOLDERS:
        d = vdir / folder
        found += sorted(f"{folder}/{f.name}" for f in d.iterdir() if f.is_file()) if d.is_dir() else []
    return found + [f for f in RESULT_FILES if (vdir / f).is_file()]


def reference(vdir):
    """convert/results.md5 as {file: md5}, or None if nothing has been recorded."""
    path = vdir / "convert" / "results.md5"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return {name: md5 for md5, name in (line.rstrip("\n").split("  ", 1) for line in f if line.strip())}


def check(folder):
    """Check one version folder; print its state; return the number of problems."""
    vdir = DATA / Path(folder).name
    print(vdir.name)
    if not (vdir / "convert").is_dir():
        print("  no convert/ folder: nothing has been made")
        return 0
    problems = []

    rows = vh_sources.recorded(vdir.name)
    for name in rows:
        if not (vdir / "source" / name).is_file():
            print(f"  source/{name}: absent")
        elif p := vh_sources.problem(vdir, name, rows):
            problems.append(f"source/{p}")
        else:
            print(f"  source/{name}: the recorded file")

    ref = reference(vdir)
    here = produced(vdir)
    if ref is None:
        print("  no results recorded yet (convert/results.md5): only the shape is verified")
    else:
        for name, md5 in ref.items():
            if name not in here:
                print(f"  {name}: not made" + (" (optional)" if name in OPTIONAL else ""))
            elif vh_sources.md5(vdir / name) != md5:
                problems.append(f"{name}: not the recorded result")
            else:
                print(f"  {name}: the recorded result")
        problems += [f"{name}: not among the recorded results" for name in here if name not in ref]

    for folder in RESULT_FOLDERS:
        if any(name.startswith(folder + "/") for name in here):
            problems += vh_text.check(vdir, folder)

    for p in problems[:50]:
        print(f"  PROBLEM {p}")
    if len(problems) > 50:
        print(f"  ... and {len(problems) - 50} more")
    return len(problems)


def main(argv):
    folders = argv or sorted(d.parent.name for d in DATA.glob("*/convert") if d.is_dir())
    if not folders:
        sys.exit("no version folder has a convert/ folder yet")
    bad = sum(check(folder) for folder in folders)
    print("OK" if not bad else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
