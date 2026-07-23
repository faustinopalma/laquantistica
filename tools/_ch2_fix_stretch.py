import re, pathlib, glob

# Force NON-stretch on delimiters that must stay single-line height:
#  - bra-ket angle brackets  ⟨ ⟩   and the bra/ket bar |
#  - round parentheses that do NOT wrap a column vector (<mtable>)
# Column-vector parens (…<mo>(</mo><mtable>…</mtable><mo>)</mo>…) keep stretching.

ANGLE_PIPE = re.compile(r'<mo>(\u27e8|\u27e9|\||&#10216;|&#10217;|&#124;)</mo>')
OPEN  = re.compile(r'<mo>(\(|&#40;)</mo>(?!<mtable>)')
CLOSE = re.compile(r'(?<!</mtable>)<mo>(\)|&#41;)</mo>')

def fix(t):
    n = 0
    t, a = ANGLE_PIPE.subn(r'<mo stretchy="false">\1</mo>', t); n += a
    t, b = OPEN.subn(r'<mo stretchy="false">\1</mo>', t);       n += b
    t, c = CLOSE.subn(r'<mo stretchy="false">\1</mo>', t);      n += c
    return t, n

files = ['publish/leggi/02-stern-gerlach-cascata.html',
         'site/mathml/02-stern-gerlach-cascata.html']
files += sorted(glob.glob('build/ch2_overrides/*.mml'))
total = 0
for f in files:
    p = pathlib.Path(f)
    if not p.exists():
        print('MISSING', f); continue
    t = p.read_text(encoding='utf-8')
    t2, n = fix(t)
    if n:
        p.write_text(t2, encoding='utf-8')
        print(f'{f}: {n} delimiters set stretchy=false')
    total += n
print('TOTAL:', total)
