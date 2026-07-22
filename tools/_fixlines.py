"""Repair horizontal corruption lines in a photo by interpolating anomalous rows.
Detects rows whose mean color deviates strongly from the local vertical median
(thin saturated bands) and replaces them with linear interpolation of the
nearest clean rows above/below. Usage: python tools/_fixlines.py <in> <out>
"""
import sys, numpy as np
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im, dtype=np.float32)
H, W, _ = a.shape
rowmean = a.mean(axis=1)  # (H,3)
# local median over window
win = 9
med = np.zeros_like(rowmean)
for c in range(3):
    for y in range(H):
        lo = max(0, y - win); hi = min(H, y + win + 1)
        med[y, c] = np.median(rowmean[lo:hi, c])
dev = np.abs(rowmean - med).max(axis=1)  # per-row max channel deviation
thr = 18.0
bad = dev > thr
# dilate bad rows by 1 to catch anti-aliased edges
bad = bad | np.r_[bad[1:], False] | np.r_[False, bad[:-1]]
# expand bad rows by 1px each side (lines are ~1-2px)
badidx = set(np.where(bad)[0].tolist())
print("detected corrupted rows:", sorted(badidx))
clean = ~bad
out = a.copy()
ys_clean = np.where(clean)[0]
for y in np.where(bad)[0]:
    # nearest clean above and below
    above = ys_clean[ys_clean < y]
    below = ys_clean[ys_clean > y]
    if len(above) and len(below):
        ya, yb = above[-1], below[0]
        t = (y - ya) / (yb - ya)
        out[y] = (1 - t) * a[ya] + t * a[yb]
    elif len(above):
        out[y] = a[above[-1]]
    elif len(below):
        out[y] = a[below[0]]
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sys.argv[2])
print("saved", sys.argv[2])
