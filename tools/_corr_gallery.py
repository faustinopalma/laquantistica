"""Correlate a gallery leftover image against candidate flow images (blurred-silhouette, no vision).
SVG candidates are rendered to PNG via LibreOffice first.
Usage: python tools/_corr_gallery.py <imgdir> <leftover> <cand1> <cand2> ...
Leftover and candidates are file names inside <imgdir> (with extension).
Prints ranked correlation (corr>0.9 = same content / duplicate).
"""
import sys, subprocess, os, numpy as np
from PIL import Image, ImageFilter

PROF = "-env:UserInstallation=file:///C:/code/TesiLaureaR2/build/lo_conv_profile"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.com"
OUT = "build/corr_gallery"
os.makedirs(OUT, exist_ok=True)


def sil(path, size=128):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    ink = a < 200
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return np.zeros(size * size, dtype=np.float32)
    crop = (ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8) * 255)
    ci = Image.fromarray(crop); w, h = ci.size; s = max(w, h)
    sq = Image.new("L", (s, s), 0); sq.paste(ci, ((s - w) // 2, (s - h) // 2))
    sq = sq.resize((size, size), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    v = np.asarray(sq, dtype=np.float32).ravel(); v -= v.mean()
    n = np.linalg.norm(v); return v / n if n else v


def resolve(imgdir, name):
    """Return a PNG path usable by sil(); render SVG if needed."""
    p = os.path.join(imgdir, name)
    if name.lower().endswith(".svg"):
        out = os.path.join(OUT, os.path.splitext(name)[0] + ".png")
        subprocess.run([SOFFICE, "--headless", "--norestore", PROF, "--convert-to", "png",
                        "--outdir", OUT, os.path.abspath(p)], check=False, capture_output=True)
        return out
    return p


imgdir = sys.argv[1]; leftover = sys.argv[2]; cands = sys.argv[3:]
lv = sil(resolve(imgdir, leftover))
ranked = []
for c in cands:
    cp = resolve(imgdir, c)
    if not os.path.exists(cp):
        print(f"  (missing render: {c})"); continue
    ranked.append((float(np.dot(lv, sil(cp))), c))
ranked.sort(reverse=True)
print(f"{leftover}:")
for sc, c in ranked:
    print(f"   {sc:6.3f}  {c}")
