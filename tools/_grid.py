"""Overlay a viewBox-coordinate grid on a rendered SVG PNG, to plan <text> label positions.
Usage: python tools/_grid.py <png> <svg> <out.png>
Prints the pixel->viewBox mapping. Grid lines every ~1/12 of the image, labelled with
the SVG user-space coordinate at that line.
"""
import sys, re
from PIL import Image, ImageDraw

png, svg, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(svg, encoding="utf-8").read(1000)
m = re.search(r'viewBox="([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)"', s)
minx, miny, vbw, vbh = [float(x) for x in m.groups()]
im = Image.open(png).convert("RGB")
W, H = im.size
dr = ImageDraw.Draw(im)
print(f"PNG {W}x{H}  viewBox minx={minx} miny={miny} w={vbw} h={vbh}")
nx, ny = 12, 12
for i in range(nx + 1):
    px = int(i * W / nx)
    vx = minx + (px / W) * vbw
    dr.line([(px, 0), (px, H)], fill=(0, 170, 0), width=1)
    dr.text((px + 2, 2), str(int(vx)), fill=(0, 120, 0))
for j in range(ny + 1):
    py = int(j * H / ny)
    vy = miny + (py / H) * vbh
    dr.line([(0, py), (W, py)], fill=(0, 170, 0), width=1)
    dr.text((2, py + 2), str(int(vy)), fill=(0, 120, 0))
im.save(out)
print("saved", out, im.size)
print(f"map: vx = {minx} + (px/{W})*{vbw} ; vy = {miny} + (py/{H})*{vbh}")
