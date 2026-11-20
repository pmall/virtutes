#!/usr/bin/env python3
"""Run the kraken or the dfine command line for the layout model, without any fetch from the Internet.

Both programs otherwise ask Hugging Face for the starting weights of the model's backbone, which the
model file already holds. Usage, from the workspace folder:
    uv run tools/layout_cli.py kraken <kraken arguments>
    uv run tools/layout_cli.py dfine <dfine arguments>

Mark the blocks of page images with a layout model (PAGE XML out):
    uv run tools/layout_cli.py kraken -r --threads 8 -x -i <image> <out.xml> [-i ... ...] \
        segment -bl -i <model file>

Retrain a layout model on the fixed pages of one fine-tuning folder (docs/Layout_fine_tuning.md),
after tools/layout_pages.py has written its lists:
    F=finetuning/layout/<name>
    uv run tools/layout_cli.py dfine -d cpu --threads 8 --workers 2 -s 42 train -f page \
        -i models/18715364/ladas_l.safetensors --model-variant large --resize union \
        -B 2 -N 30 -F 30 -r 0.00005 -o $F/work/model -t $F/work/train.txt -e $F/work/held_out.txt
(-F 30: the model is saved once, at the end; each saved state takes 375 MB.)
"""
import os, sys

os.environ["HF_HUB_OFFLINE"] = "1"
import timm

_orig = timm.create_model
timm.create_model = lambda name, pretrained=False, **kw: _orig(name, pretrained=False, **kw)

if len(sys.argv) < 2 or sys.argv[1] not in ("kraken", "dfine"):
    sys.exit(__doc__)
prog = sys.argv.pop(1)
sys.argv[0] = prog
if prog == "kraken":
    from kraken.kraken import cli
    cli()
else:
    from dfine.cli import dfine
    dfine()
