"""Correlate ch3 gallery leftovers against in-flow figures (blurred-silhouette, no vision).
Usage: python tools/_corr_leftover.py
"""
import glob, os, numpy as np
from PIL import Image, ImageFilter

IMGDIR = "publish/leggi/img/03_elettroni"
RENDER = "build/lo_sub3_png"  # rendered flow SVGs (FIG7,8,9,10,13,14)


def sil(path, size=128):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    ink = a < 200
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return np.zeros(size * size, dtype=np.float32)
    crop = (ink[ys.min():ys.max()+1, xs.min():xs.max()+1].astype(np.uint8) * 255)
    ci = Image.fromarray(crop); w, h = ci.size; s = max(w, h)
    sq = Image.new("L", (s, s), 0); sq.paste(ci, ((s-w)//2, (s-h)//2))
    sq = sq.resize((size, size), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    v = np.asarray(sq, dtype=np.float32).ravel(); v -= v.mean()
    n = np.linalg.norm(v); return v/n if n else v


leftovers = ["FIG11.png", "FIG12.png", "FIG15.png", "NEBULI~1.png"]

# candidate flow figures: rendered SVGs + the JPG photos
cand = {}
for p in ["FIG7", "FIG8", "FIG9", "FIG10", "FIG13", "FIG14"]:
    fp = os.path.join(RENDER, p + ".png")
    if os.path.exists(fp):
        cand["flow:" + p + ".svg"] = sil(fp)
for j in ["APPARATO.jpg", "APPARA~1.jpg", "PIASTRE.jpg", "GOCCIO~1.jpg", "IMG19.jpg"]:
    fp = os.path.join(IMGDIR, j)
    if os.path.exists(fp):
        cand["flow:" + j] = sil(fp)
# also include the leftover PNGs' own SVG counterparts if any (FIG13.png etc not relevant)

for lo in leftovers:
    ov = sil(os.path.join(IMGDIR, lo))
    ranked = sorted(((float(np.dot(ov, cv)), cn) for cn, cv in cand.items()), reverse=True)
    print(f"\n{lo}:")
    for sc, cn in ranked[:6]:
        print(f"   {sc:6.3f}  {cn}")
