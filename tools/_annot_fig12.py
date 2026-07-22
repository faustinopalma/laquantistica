"""Annotate the Millikan Fig.12 photo (APPARA~1.jpg) with the original labels
(Microscopio / Lampada / Nebulizzatore) placed in a margin with arrows pointing
to each component, mirroring the scanned original.
Usage: python tools/_annot_fig12.py <in.jpg> <out.jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
photo = Image.open(src).convert("RGB")
pw, ph = photo.size

L, T, R, B = 118, 58, 34, 58            # margins
W, H = L + pw + R, T + ph + B
# sample background colour from photo top-left corner
bg = photo.crop((0, 0, 8, 8)).resize((1, 1)).getpixel((0, 0))
canvas = Image.new("RGB", (W, H), bg)
canvas.paste(photo, (L, T))
dr = ImageDraw.Draw(canvas)

def font(sz):
    for p in [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\Arialbd.ttf",
              r"C:\Windows\Fonts\arial.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

F = font(23)
ink = (20, 20, 20)

def arrow(p0, p1, w=3):
    dr.line([p0, p1], fill=ink, width=w)
    import math
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for da in (-0.45, 0.45):
        hx = p1[0] - 15 * math.cos(ang + da)
        hy = p1[1] - 15 * math.sin(ang + da)
        dr.line([(hx, hy), p1], fill=ink, width=w)

def label(text, xy):
    dr.text(xy, text, fill=ink, font=F)

# photo-space feature points -> canvas coords (offset by L,T)
def C(px, py):
    return (L + px, T + py)

# Microscopio (eyepiece far left) — label top-left margin
label("Microscopio", (6, 20))
arrow((120, 40), C(46, 70))
# Lampada (black box right) — label top-right margin
label("Lampada", (past := W - 150, 20))
arrow((W - 92, 42), C(pw - 120, 40))
# Nebulizzatore (glowing bulb centre-right) — label bottom-right margin
label("Nebulizzatore", (W - 210, H - 34))
arrow((W - 150, H - 30), C(pw - 235, ph - 150))

canvas.save(out, quality=92)
print("saved", out, canvas.size, "bg", bg)
