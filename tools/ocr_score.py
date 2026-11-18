#!/usr/bin/env python3
"""Measure how well a machine reading of scan pages matches the reference text of those pages.

Usage, from the workspace folder:
    uv run tools/ocr_score.py <reference folder> <reading folder> [<reading folder> ...]

    <reference folder>  one text file per page, <page>.txt or <page>.draft.txt (a draft is a
                        reference not yet confirmed by a person; the output says so).
    <reading folder>    one text file per page with the same <page> name, <page>.txt: what a
                        reading model (or any other source) gave for that page.

For each reading folder it prints, over all pages together:
- CER, the character error rate: the number of characters to insert, delete or replace to turn
  the reading into the reference, divided by the number of characters of the reference.
- CER without Greek: the same after removing every Greek letter from both texts, a measure of
  the English (and Latin) alone, since the Greek of the notes is not what these models are for.
- CER typography ignored: the CER without Greek, after removing all spaces and making every
  quote mark straight (' or ") and every dash or hyphen (– — ¬) a plain hyphen, and superscript
  digits plain digits. What is left is the misreading of letters, digits and punctuation;
  spacing and the shape of quotes and dashes are a matter of transcription rules, not of
  reading.
- WER, the word error rate: the same as CER at the level of whole words.

Before comparing, both texts are brought to the same form: Unicode composed form (NFC), so that
an accented letter written as one or as two code points counts the same; lines are joined with
a space; runs of spaces are made one. Nothing else is changed: case, punctuation, quotes and
note numbers count.
"""
import re, sys, unicodedata
from pathlib import Path

GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")
TYPO = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "¬": "-",
                      "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6",
                      "⁷": "7", "⁸": "8", "⁹": "9", "⁰": "0"})


def typo(text):
    return "".join(text.translate(TYPO).split())


def norm(text):
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())


def distance(a, b):
    """Levenshtein distance between two sequences (strings or lists of words)."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def references(folder):
    refs = {}
    for f in sorted(Path(folder).glob("*.txt")):
        page = f.name.removesuffix(".txt").removesuffix(".draft")
        refs[page] = (f.read_text(encoding="utf-8"), f.name.endswith(".draft.txt"))
    return refs


def score(refs, folder):
    totals = {"cer": [0, 0], "cer_nogreek": [0, 0], "cer_typo": [0, 0], "wer": [0, 0]}
    missing = []
    for page, (ref, _) in refs.items():
        f = Path(folder) / f"{page}.txt"
        if not f.exists():
            missing.append(page)
            continue
        r, h = norm(ref), norm(f.read_text(encoding="utf-8"))
        rg, hg = norm(GREEK.sub("", r)), norm(GREEK.sub("", h))
        for key, (x, y) in {"cer": (r, h), "cer_nogreek": (rg, hg),
                            "cer_typo": (typo(rg), typo(hg)),
                            "wer": (r.split(), h.split())}.items():
            totals[key][0] += distance(x, y)
            totals[key][1] += len(x)
    return {k: e / n if n else float("nan") for k, (e, n) in totals.items()}, missing


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    refs = references(argv[0])
    drafts = sum(d for _, d in refs.values())
    print(f"{len(refs)} reference pages, {drafts} of them drafts not yet confirmed by a person")
    print(f"{'reading':<20} {'CER':>7} {'CER without Greek':>18} {'CER typography ignored':>23} {'WER':>7}")
    for folder in argv[1:]:
        s, missing = score(refs, folder)
        note = f"  (missing pages: {', '.join(missing)})" if missing else ""
        print(f"{Path(folder).name:<20} {s['cer']:>7.2%} {s['cer_nogreek']:>18.2%}"
              f" {s['cer_typo']:>23.2%} {s['wer']:>7.2%}{note}")


if __name__ == "__main__":
    main(sys.argv[1:])
