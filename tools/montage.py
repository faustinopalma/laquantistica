"""Build a labeled contact-sheet (montage) from PNGs in a folder, for quick review.

Usage:
    python tools/montage.py <indir> <outpath> [cols] [glob]

Example:
    python tools/montage.py diagrammi-dwg/01 scansioni/_montage/01_dwg.png 3 "*.png"
    python tools/montage.py scansioni/_png/01-stern-gerlach scansioni/_montage/01_scan.png 3 "*_e.png"
"""
import sys
import os
import glob
from PIL import Image, ImageDraw, ImageFont


def montage(indir: str, outpath: str, cols: int = 3, pattern: str = "*.png", cell: int = 560) -> None:
    files = sorted(glob.glob(os.path.join(indir, pattern)))
    if not files:
        print("no files matching", pattern, "in", indir)
        return
    labelh = 28
    rows = (len(files) + cols - 1) // cols
    W, H = cols * cell, rows * (cell + labelh)
    sheet = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x, y = c * cell, r * (cell + labelh)
        im = Image.open(f).convert("RGB")
        im.thumbnail((cell - 12, cell - 12))
        ox = x + (cell - im.width) // 2
        oy = y + labelh + (cell - labelh - im.height) // 2
        sheet.paste(im, (ox, max(oy, y + labelh)))
        draw.rectangle([x, y, x + cell - 1, y + cell + labelh - 1], outline="#bbbbbb")
        draw.rectangle([x, y, x + cell - 1, y + labelh - 1], fill="#222222")
        draw.text((x + 6, y + 5), os.path.basename(f), fill="white", font=font)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    sheet.save(outpath)
    print("saved", outpath, sheet.size)


def main() -> None:
    indir = sys.argv[1]
    outpath = sys.argv[2]
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    pattern = sys.argv[4] if len(sys.argv) > 4 else "*.png"
    montage(indir, outpath, cols=cols, pattern=pattern)


if __name__ == "__main__":
    main()
