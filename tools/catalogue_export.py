#!/usr/bin/env python3
"""Flatten the five catalogue spreadsheets into one CSV (standard library only).

Usage, from the workspace folder:
    python3 tools/catalogue_export.py            # writes catalogue/catalogue_rows.csv
    python3 tools/catalogue_export.py --notes    # also prints the 'Notes' sheets

Reads the spreadsheets in catalogue/ (copies, 12 Nov 2026, of the project's
catalogue in the original project folder, which remains the source of truth).

The spreadsheets are never modified. Each work has three rows in the source
(original, English translation, French translation); the 'version' column
below is derived from that row order.
"""
import csv, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # the workspace folder
SRC = ROOT / "catalogue"
OUT = SRC / "catalogue_rows.csv"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
T = "{%s}t" % NS["m"]


def col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n


def read_xlsx(path):
    """Return {sheet name: [row, ...]} with every cell as a string."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(T)))
    names = [s.get("name") for s in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS)]
    files = sorted((n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n)),
                   key=lambda s: int(re.findall(r"\d+", s)[0]))
    out = {}
    for name, f in zip(names, files):
        rows = []
        for row in ET.fromstring(z.read(f)).iter("{%s}row" % NS["m"]):
            cells = {}
            for c in row.findall("m:c", NS):
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None:
                    val = shared[int(v.text)]
                elif c.get("t") == "inlineStr":
                    val = "".join(t.text or "" for t in c.iter(T))
                else:
                    val = v.text if v is not None else ""
                cells[col_index(c.get("r"))] = val
            if cells:
                rows.append([cells.get(i, "") for i in range(1, max(cells) + 1)])
        out[name] = rows
    return out


def main():
    show_notes = "--notes" in sys.argv
    OUT.parent.mkdir(exist_ok=True)
    versions = ["original", "english", "french"]
    n_rows = n_works = 0
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["continent", "work_no", "version", "work", "author", "year",
                    "edition_note", "link1", "link2", "link3", "retrieved"])
        for path in sorted(SRC.glob("manuscrits_vertus_plantes_*.xlsx")):
            continent = path.stem.rsplit("_", 1)[1]
            sheets = read_xlsx(path)
            last, work_no, k = None, 0, 0
            for r in sheets["Manuscrits"][1:]:
                r = (r + [""] * 8)[:8]
                key = (r[0], r[1], r[2])
                if key != last:
                    last, work_no, k = key, work_no + 1, 0
                    n_works += 1
                version = versions[k] if k < 3 else "extra"
                k += 1
                w.writerow([continent, work_no, version] + r)
                n_rows += 1
            if show_notes:
                print("#####", path.name)
                for r in sheets.get("Notes", []):
                    print("  -", " | ".join(r))
    print(f"{n_works} works, {n_rows} rows -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
