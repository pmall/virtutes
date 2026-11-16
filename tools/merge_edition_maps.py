"""Check and merge per-work edition maps into one CSV.

Method: docs/Edition_mapping_method.md
Usage (from the workspace folder):  python3 tools/merge_edition_maps.py <folder with N_work.csv files> <output.csv>
"""
import collections
import csv
import glob
import os
import re
import sys

HEADER = ["work_no", "work", "type", "year", "place", "publisher_printer",
          "editor_translator", "language", "contents", "note", "source_url", "checked"]
TYPES = {"manuscripts", "manuscript", "edition", "translation",
         "edition+translation", "facsimile", "derivative"}


def first_year(text):
    m = re.search(r"\d{3,4}", text)
    return int(m.group()) if m else 9999


def main(folder, out):
    rows, problems = [], []
    for path in sorted(glob.glob(os.path.join(folder, "*.csv"))):
        if os.path.abspath(path) == os.path.abspath(out):
            continue
        data = list(csv.reader(open(path, encoding="utf-8-sig")))
        name = os.path.basename(path)
        if not data or data[0] != HEADER:
            problems.append(f"{name}: header differs")
            continue
        for i, r in enumerate(data[1:], 2):
            if len(r) != len(HEADER):
                problems.append(f"{name} line {i}: {len(r)} fields")
                continue
            if r[2].startswith("edition+translation"):
                r[2] = "edition+translation"
            if r[2] not in TYPES:
                problems.append(f"{name} line {i}: unknown type '{r[2]}'")
            if r[11] not in ("yes", "no"):
                problems.append(f"{name} line {i}: checked = '{r[11]}'")
            rows.append(r)

    rows.sort(key=lambda r: (int(r[0]) if r[0].isdigit() else 999,
                             0 if r[2] in ("manuscripts", "manuscript") else 1,
                             first_year(r[3])))
    with open(out, "w", newline="", encoding="utf-8-sig") as fh:  # BOM: opens cleanly in Excel
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"{len(rows)} rows written to {out}\n")
    print("| Work | Versions | Span | Confirmed in a catalogue |")
    print("|---|---|---|---|")
    works = collections.OrderedDict()
    for r in rows:
        works.setdefault(f"{r[0]}. {r[1]}", []).append(r)
    for name, v in works.items():
        years = [first_year(x[3]) for x in v if x[2] != "manuscripts" and first_year(x[3]) != 9999]
        span = f"{min(years)} – {max(years)}" if years else ""
        print(f"| {name} | {len(v)} | {span} | {sum(x[11] == 'yes' for x in v)} |")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" ", p)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
