"""Cerca nelle formule i difetti lasciati dalla conversione da Word.

Tre classi di difetto, tutte invisibili leggendo il LaTeX di sfuggita:

1. graffe e parentesi FISSE davanti a un blocco su piu' righe: `\\{\\begin{...}`
   disegna una graffa di altezza normale accanto a righe alte il doppio, invece
   di una graffa che le abbraccia (serve \\left\\{ ... \\right.);
2. parole scritte lettera per lettera come `\\mathrm{c}\\mathrm{o}\\mathrm{m}\\mathrm{e}`,
   che nessuno scriverebbe a mano e che impedisce di accorgersi che li' c'e' una parola;
3. quelle stesse parole lasciate in italiano dentro la versione inglese.

    python tools/eq_difetti.py
"""
from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path

FISSA = re.compile(r'(?<!\\left)(?<!\\bigl)(?<!\\Bigl)\\([{[(|])\s*\\begin\{(gathered|aligned|array|matrix)')
SPEZZATA = re.compile(r'(?:\\mathrm\{[a-zA-Z]\}){2,}')
PAROLE_IT = ('come', 'con', 'dove', 'quindi', 'sostituendo', 'tutto lo spazio',
             'per', 'analogamente', 'essendo', 'ponendo')

difetti: dict[str, list[tuple[str, int, str]]] = defaultdict(list)

for p in sorted(Path('publish').rglob('*.html')):
    src = p.read_text(encoding='utf-8')
    for m in re.finditer(r'data-tex="([^"]*)"', src):
        tex = html.unescape(m.group(1))
        riga = src[:m.start()].count('\n') + 1
        # in quale lingua sta la formula
        prima = src[max(0, m.start() - 4000):m.start()]
        aperture = re.findall(r'<span class="(it|en)"', prima)
        lingua = aperture[-1] if aperture else '?'

        if FISSA.search(tex):
            difetti['parentesi fissa su blocco alto'].append((p.name, riga, tex))
        for s in SPEZZATA.findall(tex):
            parola = ''.join(re.findall(r'\\mathrm\{([a-zA-Z])\}', s))
            difetti['parola scritta lettera per lettera'].append(
                (p.name, riga, f'{parola!r}  in  {tex[:60]}'))
        if lingua == 'en':
            for w in re.findall(r'\\text\{\s*([^}]+?)\s*\}', tex):
                if w.lower().strip() in PAROLE_IT:
                    difetti['parola italiana nella versione inglese'].append(
                        (p.name, riga, f'{w!r}  in  {tex[:60]}'))

for tipo, casi in difetti.items():
    print(f'\n=== {tipo}: {len(casi)} ===')
    for pagina, riga, dettaglio in casi:
        print(f'  {pagina:32} riga {riga:5}  {dettaglio.splitlines()[0][:90]}')
