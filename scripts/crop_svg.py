"""Crop LibreOffice-exported equation SVGs: they place the graphic on a full page.
Set the outer <svg> viewBox (and intrinsic width/height) to the union of the
`class="BoundingBox"` rects so the SVG is tight around the formula for inline use.
"""
import re
import sys
from pathlib import Path

RECT = re.compile(r'<rect\b[^>]*class="BoundingBox"[^>]*/?>')
ATTR = {k: re.compile(rf'{k}="(-?\d+\.?\d*)"') for k in ('x', 'y', 'width', 'height')}


def crop(text):
    boxes = []
    for m in RECT.finditer(text):
        tag = m.group(0)
        try:
            x = float(ATTR['x'].search(tag).group(1))
            y = float(ATTR['y'].search(tag).group(1))
            w = float(ATTR['width'].search(tag).group(1))
            h = float(ATTR['height'].search(tag).group(1))
        except AttributeError:
            continue
        if w <= 0 or h <= 0:
            continue
        boxes.append((x, y, x + w, y + h))
    if not boxes:
        return None
    minx = min(b[0] for b in boxes)
    miny = min(b[1] for b in boxes)
    maxx = max(b[2] for b in boxes)
    maxy = max(b[3] for b in boxes)
    w = maxx - minx
    h = maxy - miny
    if w <= 0 or h <= 0:
        return None
    # units are 1/100 mm -> mm for intrinsic size
    wmm = w / 100.0
    hmm = h / 100.0

    def fix_open(m):
        tag = m.group(0)
        tag = re.sub(r'\swidth="[^"]*"', f' width="{wmm:.3f}mm"', tag, count=1)
        tag = re.sub(r'\sheight="[^"]*"', f' height="{hmm:.3f}mm"', tag, count=1)
        tag = re.sub(r'\sviewBox="[^"]*"', f' viewBox="{minx:.0f} {miny:.0f} {w:.0f} {h:.0f}"', tag, count=1)
        return tag

    text = re.sub(r'<svg\b[^>]*>', fix_open, text, count=1)
    # remove the full-page background rect(s) that fill the old page
    text = re.sub(r'<rect x="0" y="0" width="\d+" height="\d+"/>', '', text, count=1)
    return text


def main():
    indir = Path(sys.argv[1])
    n = ok = 0
    for svg in indir.rglob('*.svg'):
        n += 1
        t = svg.read_text(encoding='utf-8')
        c = crop(t)
        if c:
            svg.write_text(c, encoding='utf-8')
            ok += 1
    print(f'cropped {ok}/{n} svg in {indir}')


if __name__ == '__main__':
    main()
