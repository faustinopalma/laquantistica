import collections
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import NodiTesto, Potatore  # noqa: E402

RADICE = pathlib.Path('sorgenti')
PUNTO = re.compile(r'(?<![\d.])(\d+)\.(\d+)(?![\d.])')
MIGLIAIA = re.compile(r'(?<!\d)\d{1,3}\.\d{3}(?!\d)')


def intervalli(t, l):
    p = Potatore(t, l)
    p.feed(t)
    p.close()
    return sorted(p.intervalli)


def ctx(int_it, int_en, pos):
    for a, b in int_it:
        if a <= pos < b:
            return 'it'
    for a, b in int_en:
        if a <= pos < b:
            return 'en'
    return 'condiviso'


tot = collections.Counter()
print('=== TESTO con il punto, in contesto italiano o condiviso ===')
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'class="it"' not in t:
        continue
    ii, ie = intervalli(t, 'it'), intervalli(t, 'en')
    p = NodiTesto(t)
    p.feed(t)
    p.close()
    trovati = []
    for off, dati in p.nodi:
        if not PUNTO.search(dati):
            continue
        c = ctx(ii, ie, off)
        if c != 'en':
            trovati.append((c, PUNTO.findall(dati)[:3], dati.strip()[:50]))
            if MIGLIAIA.search(dati):
                print(f'   !! {f.name}: possibile separatore di migliaia in "{dati.strip()[:60]}"')
    if trovati:
        print(f'  {f.name}: {len(trovati)}')
        for c, n, s in trovati[:4]:
            print(f'      [{c}] {n}  "{s}"')
        tot['testo'] += len(trovati)

print('\n=== FORMULE con il punto, in contesto italiano o condiviso ===')
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'data-tex' not in t or 'class="it"' not in t:
        continue
    ii, ie = intervalli(t, 'it'), intervalli(t, 'en')
    trovate = []
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        if PUNTO.search(tex):
            c = ctx(ii, ie, m.start())
            if c != 'en':
                trovate.append((c, tex[:70].replace('\n', ' ')))
    if trovate:
        print(f'  {f.name}: {len(trovate)}')
        for c, s in trovate[:4]:
            print(f'      [{c}] {s}')
        tot['formule'] += len(trovate)

print(f'\ntotale: testo {tot["testo"]}, formule {tot["formule"]}')
