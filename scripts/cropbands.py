"""Crop a tall screenshot into horizontal bands for legible viewing.
Usage: python scripts/cropbands.py <in.png> <out_prefix> [band_h] [overlap]
"""
import sys
from pathlib import Path
from PIL import Image

inp = Path(sys.argv[1])
prefix = sys.argv[2]
band = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
overlap = int(sys.argv[4]) if len(sys.argv) > 4 else 40
im = Image.open(inp)
W, H = im.size
i = 0
y = 0
while y < H:
    y2 = min(y + band, H)
    im.crop((0, y, W, y2)).save(f'{prefix}_{i}.png')
    i += 1
    if y2 >= H:
        break
    y = y2 - overlap
print(f'{inp.name}: {W}x{H} -> {i} bands')
