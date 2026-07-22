"""Locate photo regions on a scanned page and crop one.
Finds the horizontal band with high 'ink' density (the photo row), then splits
it into column clusters (the individual photos), and crops the requested one.
Usage: python tools/_croprow.py <page.png> <rowFracLo> <rowFracHi> <whichCol> <out.png>
"""
import sys, numpy as np
from PIL import Image

page = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(page, dtype=np.float32)
H, W, _ = a.shape
lo = float(sys.argv[2]); hi = float(sys.argv[3]); which = int(sys.argv[4]); out = sys.argv[5]
# restrict to vertical band
y0, y1 = int(lo * H), int(hi * H)
band = a[y0:y1]
# 'ink' = dark block (photo has near-black background; body text is sparse black on white)
gray = band.mean(axis=2)
ink = gray < 110
colden = ink.mean(axis=0)  # per-column dark density
# find contiguous column runs with density>0.20
cols = colden > 0.20
runs = []
s = None
for x in range(W):
    if cols[x] and s is None:
        s = x
    elif not cols[x] and s is not None:
        if x - s > W * 0.04:
            runs.append((s, x))
        s = None
if s is not None and W - s > W * 0.04:
    runs.append((s, W))
print("column runs:", runs)
if not runs:
    print("no runs found"); sys.exit(1)
cs, ce = runs[which]
# tighten vertical extent within this column run
sub = ink[:, cs:ce]
rowden = sub.mean(axis=1)
rows = np.where(rowden > 0.20)[0]
r0 = y0 + int(rows.min()); r1 = y0 + int(rows.max()) + 1
pad = 4
crop = page.crop((max(0, cs - pad), max(0, r0 - pad), min(W, ce + pad), min(H, r1 + pad)))
crop.save(out)
print("cropped", crop.size, "-> box", (cs, r0, ce, r1))
