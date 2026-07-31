"""Dove finiscono i numeri formattati con toFixed nei laboratori: se finiscono in
uno stile o in un attributo SVG, mettere la virgola li' romperebbe il disegno."""
import collections
import pathlib
import re

conti = collections.Counter()
esempi = collections.defaultdict(list)

for f in sorted(pathlib.Path('sorgenti').glob('lab-*.html')):
    t = f.read_text(encoding='utf-8')
    for m in re.finditer(r'\.toFixed\(\d*\)', t):
        riga_i = t.rfind('\n', 0, m.start()) + 1
        riga_f = t.find('\n', m.end())
        riga = t[riga_i:riga_f if riga_f > 0 else len(t)].strip()
        if re.search(r"\+\s*'px'|\+\s*\"px\"|\.style\.|setAttribute\(\s*['\"](?:x|y|cx|cy|d|points|width|height|transform|r|x1|x2|y1|y2)", riga):
            tipo = 'GRAFICA (stile o attributo)'
        elif re.search(r'innerHTML|textContent|innerText|\.title|label|readout|Val\b', riga):
            tipo = 'testo visibile'
        else:
            tipo = 'da guardare'
        conti[tipo] += 1
        if len(esempi[tipo]) < 5:
            esempi[tipo].append(f'{f.name}: {riga[:110]}')

for k in sorted(conti):
    print(f'{conti[k]:>4}  {k}')
    for e in esempi[k]:
        print(f'        {e}')
print(f'\ntotale: {sum(conti.values())}')
