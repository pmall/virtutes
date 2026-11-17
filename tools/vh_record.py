#!/usr/bin/env python3
"""Record the results of a version's scripts as the reference: convert/results.md5 (standard library only).

Usage, from the workspace folder:
    uv run tools/vh_record.py <version folder>

To be run by whoever writes or changes the scripts of a version, before committing them.
It deletes the results there are (work/raw/, text/, work/repairs.csv) and runs the
version's scripts in order (convert/extract.py, repair.py, images.py, those that exist),
so that every result is made from nothing by the scripts as they are now. It then verifies the shape of the
results (tools/vh_check.py) and writes convert/results.md5: one line per produced file,
its checksum and its path from the version folder.

Every source file the scripts need must be present, the scans included: the reference
lists all results, the optional ones too. Checking against the reference
(tools/vh_check.py) has no such need.

The file is in the format of the standard command md5sum, so the results can also be
verified without this project's tools, from the version folder:
    md5sum -c convert/results.md5
convert/results.md5 is committed with the scripts: git then shows, for every change of a
script, whether and how it changed the results.
"""
import shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vh_check, vh_sources, vh_text

SCRIPTS = ["extract.py", "repair.py", "images.py"]     # the order of the process


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__)
    vdir = vh_check.DATA / Path(argv[0]).name
    scripts = [vdir / "convert" / s for s in SCRIPTS if (vdir / "convert" / s).exists()]
    if not scripts:
        sys.exit(f"no script in data/{vdir.name}/convert/")
    for folder in vh_check.RESULT_FOLDERS:
        shutil.rmtree(vdir / folder, ignore_errors=True)
    for name in vh_check.RESULT_FILES:
        (vdir / name).unlink(missing_ok=True)
    for script in scripts:
        print(f"convert/{script.name}", flush=True)
        if subprocess.run([sys.executable, str(script)], cwd=vdir).returncode:
            sys.exit(f"convert/{script.name} stopped: nothing recorded")
    problems = [p for folder in vh_check.RESULT_FOLDERS for p in vh_text.check(vdir, folder)]
    if problems:
        sys.exit("\n".join(["the results do not have the required shape: nothing recorded"]
                           + [f"  {p}" for p in problems[:50]]))
    lines = [f"{vh_sources.md5(vdir / name)}  {name}\n" for name in vh_check.produced(vdir)]
    with open(vdir / "convert" / "results.md5", "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)
    print(f"{len(lines)} results recorded in convert/results.md5")


if __name__ == "__main__":
    main(sys.argv[1:])
