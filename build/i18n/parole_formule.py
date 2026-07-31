"""Elenca le parole dentro \\text{} nelle formule di ciascun albero, per vedere
se in una lingua compaiono parole dell'altra."""
import collections
import html
import pathlib
import re

PAROLA = re.compile(r'[A-Za-zÀ-ÿ]{4,}')
SCARTA = {'text', 'mathrm', 'begin', 'aligned', 'gathered', 'left', 'right', 'frac', 'Omega',
          'times', 'quad', 'qquad', 'displaystyle', 'operatorname', 'sqrt', 'cdot', 'over'}

for lingua in ('it', 'en'):
    print(f'===== albero {lingua} =====')
    for f in sorted((pathlib.Path('publish/v2') / lingua).glob('*.html')):
        frasi = collections.Counter()
        t = f.read_text(encoding='utf-8')
        for m in re.finditer(r'data-tex="([^"]*)"', t):
            tex = html.unescape(m.group(1))
            for c in re.finditer(r'\\(?:text|mathrm|textrm|textit)\{([^{}]*)\}', tex):
                s = c.group(1).strip()
                if [w for w in PAROLA.findall(s) if w.lower() not in SCARTA]:
                    frasi[s] += 1
        if frasi:
            print(f'  {f.name}:')
            for s, n in sorted(frasi.items()):
                print(f'      {n}x  "{s}"')
