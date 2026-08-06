"""Stampa l'estensione reale dei tracciati di una SVG e la confronta con la viewBox."""
import re
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
pts = []
for d in re.findall(r' d="([^"]+)"', s):
    pts += [(float(a), float(b)) for a, b in
            re.findall(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', d)]
xs = [x for x, _ in pts]
ys = [y for _, y in pts]
print("punti:", len(pts))
print("x:", min(xs), max(xs))
print("y:", min(ys), max(ys))
print("viewBox:", re.search(r'viewBox="([^"]+)"', s).group(1))
