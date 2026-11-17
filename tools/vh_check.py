#!/usr/bin/env python3
"""Check what the scripts of a version produced, against its recorded checksums (standard library only).

One check for every version, whatever its source (typed text, scan of a printed book, scan
of a manuscript). The checksums are in convert/results.md5 of the version, kept in git:
one line per file the version's scripts produce. A researcher who runs the scripts on the
recorded source files must obtain files with these checksums.

Usage, from the workspace folder:
    uv run tools/vh_check.py <version folder> [<version folder> ...]
    uv run tools/vh_check.py                 every version that has a convert/ folder

For each version it verifies, and prints:
1. the source files present in source/ are the ones recorded in works/Downloads_report.csv
   (an absent one is only reported: not every script needs every file);
2. which of the files the scripts must produce are missing (text/page_images.csv is
   optional), and that no other file lies in work/raw/ or text/;
3. the shape of the raw text and of the final text (tools/vh_text.py);
4. the checksums:
   - if convert/results.md5 exists, each produced file must have the checksum it gives;
   - if it does not exist, and nothing above is wrong, the check writes it from the files
     that are there. It is then to be committed with the scripts.
The command ends with OK or the number of problems, and the number of missing files.

The check never changes an existing convert/results.md5. After a script was changed on
purpose and gives other results, delete the file and run the check again.

A different checksum means the result is not reproduced: another source file, a changed
script, a file edited by hand, or a script not run again after an earlier one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vh_sources, vh_text

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "works"
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


def missing(vdir, here, ref):
    """The files that should be there and are not: those of the reference, or, without one,
    those every version produces."""
    if ref is not None:
        return [name for name in ref if name not in here]
    gone = [f"{folder}/{name}" for folder in RESULT_FOLDERS for name in ("<lang>.jsonl", "pages.csv")
            if not (list((vdir / folder).glob("*.jsonl")) if name[0] == "<" else (vdir / folder / name).is_file())]
    return gone + [name for name in RESULT_FILES + sorted(OPTIONAL) if name not in here]


def check(folder):
    """Check one version folder; print its state; return (problems, missing files)."""
    vdir = DATA / Path(folder).name
    print(vdir.name)
    if not (vdir / "convert").is_dir():
        print("  no convert/ folder: nothing has been made")
        return 0, 0
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
    gone = missing(vdir, here, ref)
    for name in gone:
        print(f"  {name}: missing" + (" (optional)" if name in OPTIONAL else ""))
    required_gone = [name for name in gone if name not in OPTIONAL]

    for folder in RESULT_FOLDERS:
        if any(name.startswith(folder + "/") for name in here):
            problems += vh_text.check(vdir, folder)

    if ref is not None:
        for name in here:
            if name not in ref:
                problems.append(f"{name}: not in convert/results.md5")
            elif vh_sources.md5(vdir / name) != ref[name]:
                problems.append(f"{name}: not the checksum of convert/results.md5")
            else:
                print(f"  {name}: the recorded checksum")
    elif problems or required_gone:
        print("  convert/results.md5 does not exist; not written, because files are missing "
              "or have problems")
    else:
        with open(vdir / "convert" / "results.md5", "w", encoding="utf-8", newline="\n") as f:
            f.writelines(f"{vh_sources.md5(vdir / name)}  {name}\n" for name in here)
        print(f"  convert/results.md5 did not exist: written with the checksums of {len(here)} "
              f"files; commit it with the scripts")

    for p in problems[:50]:
        print(f"  PROBLEM {p}")
    if len(problems) > 50:
        print(f"  ... and {len(problems) - 50} more")
    return len(problems), len(gone)


def main(argv):
    folders = argv or sorted(d.parent.name for d in DATA.glob("*/convert") if d.is_dir())
    if not folders:
        sys.exit("no version folder has a convert/ folder yet")
    counts = [check(folder) for folder in folders]
    bad, gone = sum(c[0] for c in counts), sum(c[1] for c in counts)
    print((f"{bad} problem(s)" if bad else "OK") + (f", {gone} file(s) missing" if gone else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
