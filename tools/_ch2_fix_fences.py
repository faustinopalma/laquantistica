import re, pathlib, glob

# Wrap bare  <mo>(</mo><mtable>...</mtable><mo>)</mo>  in an <mrow> so the
# parentheses stretch to the column-vector height. Skip ones already preceded
# by <mrow> (already correct) to avoid redundant double-wrapping.
pat = re.compile(r'(?<!<mrow>)(<mo[^>]*>\(</mo>)(<mtable>.*?</mtable>)(<mo[^>]*>\)</mo>)', re.S)

def fix(text):
    return pat.subn(lambda m: '<mrow>'+m.group(1)+m.group(2)+m.group(3)+'</mrow>', text)

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
    total += n
    if n:
        print(f'{f}: wrapped {n}')
print('TOTAL wrapped:', total)
