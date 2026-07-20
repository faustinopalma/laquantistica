import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('build/eqsvg/09_spettri_atomici/obj003.svg')
d = p.read_text(encoding='utf-8')
print('len', len(d))
# outer svg
m = re.search(r'<svg\b[^>]*>', d)
print('outer svg:', m.group(0)[:300] if m else None)
# all transforms and rect bounds
print('transforms:', re.findall(r'transform="[^"]+"', d)[:6])
print('rects:', re.findall(r'<rect[^>]*>', d)[:4])
# gather all numeric coords from path 'd' and points to estimate bbox
nums = []
for pathd in re.findall(r'\bd="([^"]+)"', d):
    nums += [float(x) for x in re.findall(r'-?\d+\.?\d*', pathd)]
for pts in re.findall(r'points="([^"]+)"', d):
    nums += [float(x) for x in re.findall(r'-?\d+\.?\d*', pts)]
if nums:
    xs = nums[0::2]
    ys = nums[1::2]
    print(f'approx coord range x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]  (n={len(nums)})')
else:
    print('no path/points numbers found')
