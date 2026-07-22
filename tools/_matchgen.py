"""Generic: extract clusters from a composite SVG, render, correlate to given PNGs.
Usage: python tools/_matchgen.py <composite.svg> <gap> <orig1.png> [orig2.png ...]
Prints best cluster match per original (blurred-silhouette correlation, no vision).
Also renders full composite as candidate FULL.
"""
import sys, subprocess, os, glob, numpy as np
from PIL import Image, ImageFilter

PROF = "-env:UserInstallation=file:///C:/code/TesiLaureaR2/build/lo_conv_profile"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.com"
OUT = "build/matchgen"


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


def main():
    comp = sys.argv[1]; gap = sys.argv[2]; origs = sys.argv[3:]
    base = os.path.splitext(os.path.basename(comp))[0].replace("~", "")
    od = f"{OUT}/{base}"; os.makedirs(od, exist_ok=True)
    for f in glob.glob(f"{od}/*"):
        os.remove(f)
    # how many clusters?
    out = subprocess.run([sys.executable, "tools/crop_svg.py", "analyze", comp, gap],
                         capture_output=True, text=True).stdout
    n = sum(1 for ln in out.splitlines() if ln.strip().startswith("["))
    print(out.strip())
    for i in range(n):
        subprocess.run([sys.executable, "tools/crop_svg.py", "extract", comp, str(i),
                        f"{od}/C{i}.svg", gap], check=True, capture_output=True)
    import shutil
    shutil.copy(comp, f"{od}/FULL.svg")
    subprocess.run([SOFFICE, "--headless", "--norestore", PROF, "--convert-to", "png",
                    "--outdir", od] + [os.path.abspath(p) for p in glob.glob(f"{od}/*.svg")],
                   check=False, capture_output=True)
    cand = {os.path.splitext(os.path.basename(p))[0]: sil(p) for p in glob.glob(f"{od}/*.png")}
    for o in origs:
        ov = sil(o)
        ranked = sorted(((float(np.dot(ov, cv)), cn) for cn, cv in cand.items()), reverse=True)
        top = ", ".join(f"{cn}={sc:.3f}" for sc, cn in ranked[:4])
        print(f"{os.path.basename(o):16s} -> {top}")


if __name__ == "__main__":
    main()
