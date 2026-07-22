"""Verify deployed SVGs match original PNGs. Args: <img_dir> <name1> <name2> ..."""
import sys, subprocess, os, numpy as np
from PIL import Image, ImageFilter

PROF = "-env:UserInstallation=file:///C:/code/TesiLaureaR2/build/lo_conv_profile"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.com"
OUT = "build/verify_deploy"
os.makedirs(OUT, exist_ok=True)


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


img_dir = sys.argv[1]; names = sys.argv[2:]
svgs = [os.path.abspath(f"{img_dir}/{n}.svg") for n in names]
subprocess.run([SOFFICE, "--headless", "--norestore", PROF, "--convert-to", "png",
                "--outdir", OUT] + svgs, check=False, capture_output=True)
allok = True
for n in names:
    sp = f"{OUT}/{n}.png"; op = f"{img_dir}/{n}.png"
    if not os.path.exists(sp):
        print(f"{n}: SVG NOT RENDERED"); allok = False; continue
    if not os.path.exists(op):
        print(f"{n}: no original PNG (skip)"); continue
    c = float(np.dot(sil(sp), sil(op)))
    ok = c > 0.85
    allok = allok and ok
    print(f"{n:12s}: corr={c:.3f} {'OK' if ok else 'CHECK'}")
print("ALL-OK" if allok else "SOME-CHECK")
