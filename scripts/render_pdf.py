import fitz  # PyMuPDF
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pdf = root / "3. Esperimenti con gli Elettroni" / "esperimenti con gli elettroni.pdf"
out = root / "build" / "pdf_pages"
out.mkdir(parents=True, exist_ok=True)

doc = fitz.open(str(pdf))
print("pages:", doc.page_count)
zoom = 2.0
mat = fitz.Matrix(zoom, zoom)
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=mat)
    p = out / f"page_{i+1:02d}.png"
    pix.save(str(p))
    print("saved", p.name, pix.width, "x", pix.height)
