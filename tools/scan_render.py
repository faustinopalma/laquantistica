"""Render a scan PDF (scansioni/NN-*.pdf) to PNG pages for page-by-page review.

Usage:
    python tools/scan_render.py <pdf-basename-without-ext> [zoom]

Example:
    python tools/scan_render.py 01-stern-gerlach
    python tools/scan_render.py 04-diffrazione 2.5

Outputs to scansioni/_png/<basename>/pNN.png
"""
import sys
import os
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageEnhance


def enhance(path_in: str, path_out: str) -> None:
    img = Image.open(path_in).convert("L")            # grayscale
    img = ImageOps.autocontrast(img, cutoff=1)         # stretch histogram
    img = ImageEnhance.Contrast(img).enhance(1.8)      # boost contrast
    img = ImageEnhance.Sharpness(img).enhance(1.6)     # sharpen text
    img.save(path_out)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python tools/scan_render.py <basename> [zoom]")
        raise SystemExit(2)
    base = sys.argv[1]
    zoom = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    src = os.path.join("scansioni", base + ".pdf")
    if not os.path.exists(src):
        print("NOT FOUND:", src)
        raise SystemExit(1)
    out = os.path.join("scansioni", "_png", base)
    os.makedirs(out, exist_ok=True)
    doc = fitz.open(src)
    mat = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=mat)
        raw = os.path.join(out, f"p{i:02d}.png")
        pix.save(raw)
        enh = os.path.join(out, f"p{i:02d}_e.png")
        enhance(raw, enh)
        print("saved", enh, f"{pix.width}x{pix.height}")
    print(f"DONE: {doc.page_count} pages -> {out}")


if __name__ == "__main__":
    main()
