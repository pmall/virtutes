#!/usr/bin/env python3
"""The source files of a version: its list, and the one way scripts get them (standard library only).

Each version folder has metadata/sources.csv, kept in git: one row per file of source/
that the version works from, with its size, its checksum (md5) and the address it can be
fetched from. Columns: file, bytes, md5, address. The libraries' own small records
(*.json, *_pages.csv), which are in git themselves, are not listed.

The list is written by the download tools, once a file is verified against what its
library publishes (add(), below). A file obtained another way gets its row by hand, after
the same verification, and metadata/note.txt says how it was verified.

Every script of a version's convert/ folder that opens a file of source/ gets it through
require(), before doing anything else. The file must be in the list, be present in
source/, and have the listed checksum. Otherwise the script stops, with the same messages
for every version, and gives the address of the file. A script names only the files its
result is made from: a script that makes a text from a typed file does not name the scans.

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

COLUMNS = ["file", "bytes", "md5", "address"]
LIST = "metadata/sources.csv"

Source = namedtuple("Source", "name path md5")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def listed(vdir):
    """The rows of a version's sources list, by file name (empty if there is no list)."""
    path = Path(vdir) / LIST
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {row["file"]: row for row in csv.DictReader(f)}


def add(vdir, name, size, md5sum, address):
    """Put one verified file in a version's sources list, replacing its row if it has one."""
    rows = listed(vdir)
    rows[name] = {"file": name, "bytes": size, "md5": md5sum, "address": address}
    path = Path(vdir) / LIST
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows.values())


def problem(vdir, name, rows):
    """Why this file cannot be used, or None if it is exactly the listed one."""
    if name not in rows:
        return f"{name}: not in {LIST} of {vdir.name}"
    path = vdir / "source" / name
    if not path.is_file():
        return (f"{name}: missing from works/{vdir.name}/source/ "
                f"(address: {rows[name]['address']})")
    found = md5(path)
    if found != rows[name]["md5"]:
        return (f"{name}: not the checksum of {LIST} "
                f"(listed {rows[name]['md5']}, found {found})")
    return None


def require(vdir, names):
    """Return one Source per name, in order; stop the script if any is not the listed file."""
    vdir = Path(vdir)
    rows = listed(vdir)
    problems = [p for p in (problem(vdir, name, rows) for name in names) if p]
    if problems:
        sys.exit("\n".join(["source files not as listed:"] + [f"  {p}" for p in problems]))
    return [Source(name, vdir / "source" / name, rows[name]["md5"]) for name in names]


