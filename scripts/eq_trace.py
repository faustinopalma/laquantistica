"""Trace the MTEF record stream of one equation to debug slot boundaries."""
import sys, struct
from pathlib import Path
import olefile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mtef2latex import mtef_from_eqnstream

root = Path(__file__).resolve().parent.parent
rel = sys.argv[1]
idx = int(sys.argv[2])
p = root / rel
ole = olefile.OleFileIO(str(p))
eqs = []
for e in ole.listdir(streams=True):
    if len(e) >= 3 and e[0] == 'ObjectPool' and e[-1] == 'Equation Native':
        eqs.append((e[1], ole.openstream(e).read()))
ole.close()
eqs.sort(key=lambda t: t[0])
data = eqs[idx][1]
body = mtef_from_eqnstream(data)

names = {0:'END',1:'LINE',2:'CHAR',3:'TMPL',4:'PILE',5:'MATRIX',6:'EMBELL',7:'RULER',8:'FONT',9:'SIZE',10:'sz10',11:'sz11',12:'sz12',13:'sz13',14:'sz14'}
import io
s = io.BytesIO(body)
depth = 0
while True:
    b = s.read(1)
    if not b:
        break
    tag = b[0]
    rec = tag & 0x0F
    nm = names.get(rec, f'?{rec}')
    if rec == 2:  # CHAR
        tf = s.read(1)[0]
        ch = struct.unpack('<H', s.read(2))[0]
        print(f'{"  "*depth}CHAR tf={tf:#x} ch={ch:#x} {chr(ch) if 0x20<=ch<0x3000 else ""!r}')
    elif rec == 3:  # TMPL
        sel = s.read(1)[0]; var = s.read(1)[0]; opt = s.read(1)[0]
        print(f'{"  "*depth}TMPL sel={sel} var={var} opt={opt}')
    elif rec == 4:
        ha=s.read(1)[0]; va=s.read(1)[0]
        print(f'{"  "*depth}PILE h={ha} v={va}')
    elif rec == 0:
        print(f'{"  "*depth}END')
    else:
        print(f'{"  "*depth}{nm} (tag={tag:#x})')
