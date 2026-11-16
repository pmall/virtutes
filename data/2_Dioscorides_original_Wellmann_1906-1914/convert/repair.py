#!/usr/bin/env python3
"""Make the repaired text of Wellmann's Dioscorides from the raw extraction.

Run:  uv run convert/repair.py   (no arguments; reads work/raw/, written by
      convert/extract.py; writes text/grc.jsonl, text/grc.info.json, text/pages.csv
      and work/repairs.csv)

Second of two steps. The raw text keeps every mistake of the typed file (listed in the
notes of work/raw/grc.info.json). This script corrects them by rules, each one a function
in RULES below. A rule never changes the words of the work; it may change the labels
around them (ref, kind, page) and where a passage is cut. Every change a rule makes is
written as one row of work/repairs.csv (passage, rule, field, before, after), so that a
person can read what was repaired.

RULES WRITTEN SO FAR: none. text/ is the raw text unchanged.
The mistakes to repair are listed in NOTES at the end of convert/extract.py.
"""
import csv, json, shutil, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parents[1]            # this version folder
ROOT = VDIR.parents[1]                                 # the workspace folder
RAW = VDIR / "work" / "raw"
TEXT = VDIR / "text"
LANG = "grc"

# Each rule is a function(passages, log): it changes the list of passages in place and
# calls log(id, rule, field, before, after) once per change. Rules run in this order.
RULES = []


def main():
    if not (RAW / f"{LANG}.jsonl").exists():
        sys.exit("work/raw/ is missing: run convert/extract.py first")
    with open(RAW / f"{LANG}.jsonl", encoding="utf-8") as f:
        passages = [json.loads(line) for line in f]
    info = json.load(open(RAW / f"{LANG}.info.json", encoding="utf-8"))

    repairs = []
    for rule in RULES:
        rule(passages, lambda *row: repairs.append(row))

    TEXT.mkdir(exist_ok=True)
    with open(TEXT / f"{LANG}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False, separators=(",", ":")) + "\n")
    shutil.copyfile(RAW / "pages.csv", TEXT / "pages.csv")
    info["converter"] = str((VDIR / "convert" / "repair.py").relative_to(ROOT))
    info["notes"] += " No repair rule is written yet: this is the raw text unchanged."
    with open(TEXT / f"{LANG}.info.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=1) + "\n")
    with open(VDIR / "work" / "repairs.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "rule", "field", "before", "after"])
        w.writerows(repairs)
    print(f"{len(passages)} passages, {len(repairs)} repairs")


if __name__ == "__main__":
    main()
