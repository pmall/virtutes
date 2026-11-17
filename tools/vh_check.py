#!/usr/bin/env python3
"""Check that everything the scripts of a version produced is whole and in step (standard library only).

One check for every version, whatever its source (typed text, scan of a printed book, scan
of a manuscript). It knows the process, not the book: the scripts of convert/ run in the
order extract.py, repair.py, images.py (docs/Conversion_method.md), and each one, when it
finishes, writes a record of what it made: its own checksum, the checksum of every file it
read and of every file it wrote (record(), below). The record is the file
made_by_<script>.json beside the files the script wrote.

Usage, from the workspace folder:
    uv run tools/vh_check.py <version folder> [<version folder> ...]
    uv run tools/vh_check.py --all        every version that has a convert/ folder

For each script the check prints one of:
    OK         its files are as it made them, from the files and the script as they are now
    not made   the script has not been run (or has not been written): nothing to check
    PROBLEM    followed by what is wrong:
               - a file it wrote has changed or is gone (edited by hand, deleted);
               - a file it read has changed since (an earlier script was run again, and
                 this one was not: its result is out of date);
               - the script itself has changed since it was run;
               - a source file it read is not the one recorded in data/Downloads_report.csv;
               - a file lies in work/raw/ or text/ that no record accounts for.
Then it verifies the shape of the raw text and of the final text (tools/vh_text.py).
A source file that is absent is not a problem: its recorded checksum is enough to compare.
"Not made" is not a problem either; images.py is optional. The command ends with OK, or
with the number of problems.

In a script of convert/, as the last thing it does:
    sys.path.insert(0, str(ROOT / "tools"))          # ROOT: the workspace folder
    from vh_check import record
    record(__file__, read=[...], wrote=[...])
`read` and `wrote` are paths, or the Source values returned by vh_sources.require().
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vh_sources, vh_text

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
DATA = ROOT / "data"
STEPS = [("extract", "work/raw"), ("repair", "text"), ("images", "text")]  # script, where its record is
OPTIONAL = {"images"}
CHECKED_FOLDERS = ["work/raw", "text"]      # every file in them must be accounted for


def record(script, read, wrote):
    """Write made_by_<script>.json beside the first file written. Same content at every run."""
    script = Path(script).resolve()
    vdir = script.parents[1]

    def entry(item):
        path = Path(getattr(item, "path", item)).resolve()
        return {"file": path.relative_to(vdir).as_posix(),
                "md5": getattr(item, "md5", None) or vh_sources.md5(path)}

    rec = {"script": script.relative_to(vdir).as_posix(), "script_md5": vh_sources.md5(script),
           "read": [entry(i) for i in read], "wrote": [entry(i) for i in wrote]}
    out = Path(getattr(wrote[0], "path", wrote[0])).resolve().parent / f"made_by_{script.stem}.json"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")


def check_step(vdir, name, folder, recorded, md5_now, accounted):
    """Return (state, problems) for one script; add the files it accounts for to `accounted`."""
    path = vdir / folder / f"made_by_{name}.json"
    if not path.exists():
        return "not made", []
    accounted.add(path)
    try:
        rec = json.load(open(path, encoding="utf-8"))
        script, wrote, read = vdir / rec["script"], rec["wrote"], rec["read"]
    except (ValueError, KeyError, TypeError):
        return "PROBLEM", [f"{path.name}: not a valid record; run convert/{name}.py again"]
    problems = []
    again = f"run convert/{name}.py again"
    if not script.exists():
        problems.append(f"{rec['script']} is gone")
    elif md5_now(script) != rec["script_md5"]:
        problems.append(f"{rec['script']} has changed since it was run; {again}")
    for e in wrote:
        f = vdir / e["file"]
        accounted.add(f)
        if not f.exists():
            problems.append(f"{e['file']} is gone; {again}")
        elif md5_now(f) != e["md5"]:
            problems.append(f"{e['file']} is not as {rec['script']} wrote it (changed by hand "
                            f"or by something else); {again}")
    for e in read:
        f = vdir / e["file"]
        if e["file"].startswith("source/"):
            row = recorded.get(f.name)
            if row is None or row["md5"] != e["md5"]:
                problems.append(f"{e['file']}: the file read is not the one recorded in "
                                f"data/Downloads_report.csv; {again} with the recorded file")
            elif f.exists() and md5_now(f) != e["md5"]:
                problems.append(f"{e['file']}: the file now in source/ is not the recorded one")
        elif not f.exists():
            problems.append(f"{e['file']}, which {rec['script']} read, is gone")
        elif md5_now(f) != e["md5"]:
            problems.append(f"{e['file']} has changed since {rec['script']} read it: "
                            f"its result is out of date; {again}")
    return ("PROBLEM" if problems else "OK"), problems


def check(folder):
    """Check one version folder; print its state; return the number of problems."""
    vdir = DATA / Path(folder).name
    print(f"{vdir.name}")
    if not (vdir / "convert").is_dir():
        print("  no convert/ folder: nothing has been made")
        return 0
    recorded = vh_sources.recorded(vdir.name)
    cache = {}
    md5_now = lambda p: cache.setdefault(p, vh_sources.md5(p))
    accounted, bad, made = set(), 0, set()
    for name, where in STEPS:
        state, problems = check_step(vdir, name, where, recorded, md5_now, accounted)
        if state == "not made":
            if not (vdir / "convert" / f"{name}.py").exists():
                state += ", no script yet"
            if name in OPTIONAL:
                state += " (optional)"
        else:
            made.add(where)
        print(f"  convert/{name}.py: {state}")
        for p in problems:
            print(f"    PROBLEM {p}")
        bad += len(problems)
    for where in CHECKED_FOLDERS:
        d = vdir / where
        for f in sorted(d.iterdir()) if d.is_dir() else []:
            if f.is_file() and f not in accounted:
                print(f"  PROBLEM {where}/{f.name}: no record says which script made it")
                bad += 1
    for where in CHECKED_FOLDERS:
        if where in made:
            problems = vh_text.check(vdir, where, indent="  ")
            for p in problems[:50]:
                print(f"    PROBLEM {p}")
            if len(problems) > 50:
                print(f"    ... and {len(problems) - 50} more")
            bad += len(problems)
    return bad


def main(argv):
    if not argv:
        sys.exit(__doc__)
    folders = argv
    if argv == ["--all"]:
        folders = sorted(d.parent.name for d in DATA.glob("*/convert") if d.is_dir())
        if not folders:
            sys.exit("no version folder has a convert/ folder yet")
    bad = sum(check(folder) for folder in folders)
    print("OK" if not bad else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
