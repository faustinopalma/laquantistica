"""Build a labelled contact sheet of all raster images in a folder.
Usage: python scripts/montage.py <imgdir> <out.png> [cols]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

d = Path(sys.argv[1])
out = Path(sys.argv[2])
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
exts = {'.png', '.jpg', '.jpeg', '.gif'}
files = sorted([f for f in d.iterdir() if f.suffix.lower() in exts])

cell_w, cell_h, lab_h, pad = 340, 300, 26, 6
rows = (len(files) + cols - 1) // cols
W = cols * (cell_w + pad) + pad
H = rows * (cell_h + lab_h + pad) + pad
sheet = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype('arial.ttf', 16)
except Exception:
    font = ImageFont.load_default()

for i, f in enumerate(files):
    r, c = divmod(i, cols)
    x0 = pad + c * (cell_w + pad)
    y0 = pad + r * (cell_h + lab_h + pad)
    try:
        im = Image.open(f).convert('RGB')
    except Exception as e:
        draw.text((x0, y0), f'{f.name}: ERR', fill='red', font=font)
        continue
    im.thumbnail((cell_w, cell_h))
    # paste centered on a light gray tile so white figures are visible
    tile = Image.new('RGB', (cell_w, cell_h), (235, 235, 235))
    tile.paste(im, ((cell_w - im.width) // 2, (cell_h - im.height) // 2))
    sheet.paste(tile, (x0, y0 + lab_h))
    draw.rectangle([x0, y0 + lab_h, x0 + cell_w, y0 + lab_h + cell_h], outline=(180, 180, 180))
    draw.text((x0 + 2, y0 + 4), f'{i+1}. {f.name}', fill='black', font=font)

sheet.save(out)
print(f'wrote {out}  ({len(files)} imgs, {rows}x{cols})')
