"""Elenco definitivo degli attributi da tradurre.

Esclude: i vuoti (immagini decorative), quelli gia' bilingui ("Lingua / Language")
e quelli su elementi che stanno gia' dentro uno span di lingua (come le due
immagini app4/app4-en, che hanno gia' un alt per lingua).
"""
import collections
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import Potatore  # noqa: E402

RADICE = pathlib.Path('sorgenti')
ATTRIBUTI = ('alt', 'aria-label', 'title', 'placeholder')
GIA_BILINGUE = {'Lingua / Language'}


def coperti(t):
    tutti = []
    for l in ('it', 'en'):
        p = Potatore(t, l)
        p.feed(t)
        p.close()
        tutti += p.intervalli
    fusi = []
    for a, b in sorted(tutti):
        if fusi and a <= fusi[-1][1]:
            fusi[-1][1] = max(fusi[-1][1], b)
        else:
            fusi.append([a, b])
    return fusi


def dentro(fusi, pos):
    for a, b in fusi:
        if a <= pos < b:
            return True
        if a > pos:
            return False
    return False


valori = collections.OrderedDict()
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'class="it"' not in t:
        continue
    fusi = coperti(t)
    senza_script = re.sub(r'<script\b.*?</script>', lambda m: ' ' * len(m.group(0)), t, flags=re.S)
    for a in ATTRIBUTI:
        for m in re.finditer(rf'\b{a}="([^"]*)"', senza_script):
            v = m.group(1).strip()
            if not v or v in GIA_BILINGUE or dentro(fusi, m.start()):
                continue
            valori.setdefault(v, []).append(f'{f.name}:{a}')

print(f'# {len(valori)} valori distinti da tradurre')
for v, dove in valori.items():
    print(f'    {v!r}:')
    print(f'        {"":<4}# {dove[0]}' + (f' (+{len(dove) - 1})' if len(dove) > 1 else ''))
