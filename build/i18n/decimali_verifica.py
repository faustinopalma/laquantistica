"""Controllo incrociato dei separatori decimali nei due alberi generati.

Nell'albero italiano non deve restare un punto decimale in un nodo di testo, e
in quello inglese non deve restare una virgola. Guarda anche le formule.
"""
import collections
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import NodiTesto  # noqa: E402

USCITA = pathlib.Path('publish')
SBAGLIATO = {'it': re.compile(r'\d\.\d'), 'en': re.compile(r'\d,\d')}

for lingua in ('it', 'en'):
    print(f'===== albero {lingua}: separatore sbagliato =====')
    tot = collections.Counter()
    for f in sorted((USCITA / lingua).glob('*.html')):
        t = f.read_text(encoding='utf-8')
        p = NodiTesto(t)
        p.feed(t)
        p.close()
        testo = [(o, d) for o, d in p.nodi if SBAGLIATO[lingua].search(d)]
        formule = [html.unescape(m.group(1)) for m in re.finditer(r'data-tex="([^"]*)"', t)
                   if SBAGLIATO[lingua].search(html.unescape(m.group(1)))]
        if testo or formule:
            print(f'  {f.name}: testo {len(testo)}, formule {len(formule)}')
            for _, d in testo[:3]:
                print(f'      testo:   {SBAGLIATO[lingua].findall(d)[:3]}  in "{d.strip()[:60]}"')
            for x in formule[:3]:
                print(f'      formula: {x[:90]}'.replace('\n', ' '))
            tot['testo'] += len(testo)
            tot['formule'] += len(formule)
    print(f'   totale: testo {tot["testo"]}, formule {tot["formule"]}')
