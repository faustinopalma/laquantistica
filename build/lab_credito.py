"""Riga di credito in fondo ai laboratori: come sono nati e che cosa sono.

Eseguire una sola volta: salta i laboratori che ce l'hanno gia'.
"""
import re
import sys
from pathlib import Path

SORGENTI = Path(__file__).resolve().parents[1] / 'sorgenti'

CREDITO = ('<div class="con-credit">'
           '<span class="it">Laboratorio simulato, scritto nel 2026 insieme a GitHub Copilot: '
           'modello didattico, non software scientifico.</span>'
           '<span class="en">Simulated laboratory, written in 2026 together with GitHub Copilot: '
           'a teaching model, not scientific software.</span></div>')

fatti = []
for f in sorted(SORGENTI.glob('lab-*.html')):
    t = f.read_text(encoding='utf-8')
    if 'con-credit' in t:
        continue
    m = re.search(r'([ \t]*)<div class="con-foot">.*?</div>\n', t, re.S)
    if not m:
        sys.exit(f'{f.name}: manca il piede')
    t = t[:m.end()] + m.group(1) + CREDITO + '\n' + t[m.end():]
    t = t.replace('sim-sg.css?v=10', 'sim-sg.css?v=11')
    f.write_text(t, encoding='utf-8')
    fatti.append(f.name)

print(f'laboratori aggiornati: {len(fatti)}')
for n in fatti:
    print(f'  {n}')
