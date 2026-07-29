import re, pathlib
t = pathlib.Path('build/ch9_svg/image1.svg').read_text(encoding='utf-8', errors='replace')
vb = re.search(r'viewBox="([\d.\- ]+)"', t).group(1)
print('viewBox', vb)
# horizontal lines: M x y l dx 0
for m in re.finditer(r'M ([\d.]+) ([\d.]+) l ([\d.\-]+) (-?0(?:\.0+)?) ', t):
    x, y, dx, dy = m.groups()
    print('H y=%s x=%s..%.0f' % (y, x, float(x)+float(dx)))
print('--- path starts ---')
for m in re.finditer(r'<path d="([^"]{1,60})', t):
    print('  ', m.group(1))
