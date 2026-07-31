"""Testo visibile che NON sta dentro un marcatore di lingua: resta uguale in entrambe.

Va bene per numeri e simboli, non per parole italiane: quelle restano italiane
anche nella versione inglese.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import Potatore  # noqa: E402

RADICE = pathlib.Path('publish')

SOSPETTE = re.compile(
    r'\b(Esperimento|Capitolo|Cap\.|Nota|Torna|Indietro|Simulatore|Laboratorio|Vedi|'
    r'della|dello|degli|delle|nella|nel|con|per|sul|una|uno|gli|dei|che|non|piu|più)\b',
    re.I)


def fuori_lingua(testo):
    """Ritorna gli intervalli NON coperti da nessuno span di lingua."""
    coperti = []
    for l in ('it', 'en'):
        p = Potatore(testo, l)
        p.feed(testo)
        p.close()
        coperti += p.intervalli
    coperti.sort()
    fusi = []
    for a, b in coperti:
        if fusi and a <= fusi[-1][1]:
            fusi[-1][1] = max(fusi[-1][1], b)
        else:
            fusi.append([a, b])
    fuori, ultimo = [], 0
    for a, b in fusi:
        fuori.append((ultimo, a))
        ultimo = b
    fuori.append((ultimo, len(testo)))
    return fuori


totale = 0
for f in sorted(RADICE.glob('*.html')):
    testo = f.read_text(encoding='utf-8')
    if 'class="it"' not in testo:
        continue
    corpo = testo
    trovate = []
    for a, b in fuori_lingua(corpo):
        frammento = corpo[a:b]
        frammento = re.sub(r'<script\b.*?</script>|<style\b.*?</style>|<head\b.*?</head>', '', frammento, flags=re.S)
        # solo il testo visibile, non gli attributi
        for m in re.finditer(r'>([^<>]+)<', frammento):
            s = m.group(1).strip()
            if len(s) < 3 or not SOSPETTE.search(s):
                continue
            if 'katex' in frammento[max(0, m.start() - 200):m.start()]:
                continue
            trovate.append(s[:70])
    if trovate:
        unici = list(dict.fromkeys(trovate))
        totale += len(unici)
        print(f'{f.name}:')
        for s in unici[:8]:
            print(f'    "{s}"')
        if len(unici) > 8:
            print(f'    ... e altre {len(unici) - 8}')

print(f'\ntotale frasi sospette fuori dai marcatori di lingua: {totale}')
