#!/usr/bin/env python3
"""Verify that the source files a script needs are exactly the recorded ones (standard library only).

Every script of a version's convert/ folder that opens a file of source/ gets it through
require(), before doing anything else. The file must be listed for that version in
works/Downloads_report.csv, be present in source/, and have the checksum (md5) recorded
there. Otherwise the script stops, with the same messages for every version, and tells
where the file can be fetched again. A script names only the files its result is made
from: a script that makes a text from a typed file does not name the scans.

In a script:
    sys.path.insert(0, str(ROOT / "tools"))          # ROOT: the workspace folder
    from vh_sources import require
    (typed,) = require(VDIR, ["tlg0656.tlg001.1st1K-grc1.xml"])   # VDIR: the version folder
    typed.path   the file          typed.name   its name          typed.md5   its checksum

Not a command. tools/vh_check.py verifies the source files present in a version folder.
"""
import csv, hashlib, sys
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
REPORT = ROOT / "works" / "Downloads_report.csv"

Source = namedtuple("Source", "name path md5")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def recorded(folder):
    """The rows of the downloads report for one version folder, by file name."""
    with open(REPORT, newline="", encoding="utf-8-sig") as f:
        return {row["file"]: row for row in csv.DictReader(f) if row["folder"] == folder}


def problem(vdir, name, rows):
    """Why this file cannot be used, or None if it is exactly the recorded one."""
    if name not in rows:
        return f"{name}: not listed for {vdir.name} in works/Downloads_report.csv"
    path = vdir / "source" / name
    if not path.is_file():
        return (f"{name}: missing from works/{vdir.name}/source/ "
                f"(recorded address: {rows[name]['source']})")
    found = md5(path)
    if found != rows[name]["md5"]:
        return (f"{name}: checksum differs from works/Downloads_report.csv "
                f"(recorded {rows[name]['md5']}, found {found})")
    return None


def require(vdir, names):
    """Return one Source per name, in order; stop the script if any is not the recorded file."""
    vdir = Path(vdir)
    rows = recorded(vdir.name)
    problems = [p for p in (problem(vdir, name, rows) for name in names) if p]
    if problems:
        sys.exit("\n".join(["source files not as recorded:"] + [f"  {p}" for p in problems]))
    return [Source(name, vdir / "source" / name, rows[name]["md5"]) for name in names]


