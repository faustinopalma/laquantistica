import collections
import pathlib
import re

GRAFICA = re.compile(r"\+\s*'px'|\+\s*\"px\"|\.style\.|setAttribute\(\s*['\"](?:x|y|cx|cy|d|points|width|height|transform|r|x1|x2|y1|y2)")
conti = collections.Counter()
per_file = collections.Counter()

for f in sorted(pathlib.Path('sorgenti').glob('lab-*.html')):
    t = f.read_text(encoding='utf-8')
    for m in re.finditer(r'\.toFixed\((\d*)\)', t):
        cifre = int(m.group(1) or 0)
        i = t.rfind('\n', 0, m.start()) + 1
        j = t.find('\n', m.end())
        riga = t[i:j if j > 0 else len(t)]
        if cifre == 0:
            conti['senza decimali (non serve)'] += 1
        elif GRAFICA.search(riga):
            conti['grafica: NON toccare'] += 1
        else:
            conti['da convertire'] += 1
            per_file[f.name] += 1

for k in sorted(conti):
    print(f'{conti[k]:>4}  {k}')
print('\nda convertire, per file:')
for k, v in per_file.most_common():
    print(f'   {v:>3}  {k}')
