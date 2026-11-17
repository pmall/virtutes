#!/usr/bin/env python3
"""Print a text of the unified text format for reading (standard library only).

Usage, from the workspace folder:
    uv run tools/vh_view.py <file.jsonl>                       the whole text
    uv run tools/vh_view.py <file.jsonl> <ref>                 one place, e.g. 2.164
    uv run tools/vh_view.py <file.jsonl> <first ref> <last ref>

Prints the work itself (kinds head, text, commentary; not the notes), one passage per
paragraph with its ref, page changes on their own line. A ref is given as it stands in
the file (docs/Unified_text_format.md); a ref without its last part, such as a chapter
without section, covers every passage inside it.
"""
import json, sys

KINDS = {"head", "text", "commentary"}


def inside(ref, place):
    return ref is not None and (ref == place or ref.startswith(place + "."))


def view(path, first, last):
    page, on, seen_last = None, first is None, False
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            if p["kind"] not in KINDS:
                continue
            ref = p.get("ref")
            if not on and inside(ref, first):
                on = True
            if not on:
                continue
            if last is not None:
                if inside(ref, last):
                    seen_last = True
                elif seen_last:
                    break
            if p["page"] != page:
                page = p["page"]
                print(f"\n[page {page}]")
            text, shift = p["text"], 0
            for offset, new_page in p.get("breaks", []):
                tag = f" [page {new_page}] "
                text = text[:offset + shift] + tag + text[offset + shift:]
                shift += len(tag)
                page = new_page
            print(f"\n{ref + '  ' if ref else ''}{'# ' if p['kind'] == 'head' else ''}{text}")


def main(argv):
    if not 1 <= len(argv) <= 3:
        sys.exit(__doc__)
    first = argv[1] if len(argv) > 1 else None
    view(argv[0], first, argv[2] if len(argv) > 2 else first)


if __name__ == "__main__":
    main(sys.argv[1:])
