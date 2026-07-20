import struct
from pathlib import Path
import olefile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import classify_objects as C

root = Path(__file__).resolve().parent.parent
rel = '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx'
wd, table = C._read_streams(root / rel)
pieces = C._piece_table(wd, table)
runs = C._parse_chpx_fkps(wd, table)
print('num chpx runs:', len(runs))
print('first 3 runs:', [(a, b, g.hex()) for a, b, g in runs[:3]])

# find first special char fc
special_fcs = []
for cp0, cp1, fc, comp in pieces:
    num = cp1 - cp0
    step = 1 if comp else 2
    raw = wd[fc:fc + (num if comp else num*2)]
    text = raw.decode('cp1252' if comp else 'utf-16-le', errors='replace')
    for j, ch in enumerate(text):
        if ch == '\x01':
            special_fcs.append(fc + j*step)
print('special fcs:', special_fcs[:6], 'total', len(special_fcs))

for cfc in special_fcs[:4]:
    matched = None
    for a, b, g in runs:
        if a <= cfc < b:
            matched = (a, b, g); break
    if matched:
        a, b, g = matched
        print(f'fc={cfc} run=[{a},{b}) grpprl={g.hex()}')
        for sprm, op in C._iter_sprms(g):
            print(f'   sprm={sprm:#06x} op={op.hex()}')
    else:
        print(f'fc={cfc} NO RUN (max run end={runs[-1][1] if runs else None})')
