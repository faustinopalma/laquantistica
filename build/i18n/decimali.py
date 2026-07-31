"""Numeri decimali: in italiano si scrivono con la virgola, in inglese col punto.
Quelli fuori dai marcatori di lingua compaiono uguali in entrambe le versioni."""
import collections
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from testo_in_formule2 import coperti, dentro  # noqa: E402

RADICE = pathlib.Path('sorgenti')
DECIMALE = re.compile(r'\d[.,]\d')


def campioni(s, n=4):
    return list(dict.fromkeys(re.findall(r'\d+[.,]\d+', s)))[:n]


tot = collections.Counter()
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'class="it"' not in t:
        continue
    fusi = coperti(t)
    conti = collections.Counter()
    esempi = collections.defaultdict(list)

    # formule
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        if not DECIMALE.search(tex):
            continue
        dove = 'formula dentro marcatore' if dentro(fusi, m.start()) else 'formula FUORI'
        conti[dove] += 1
        esempi[dove] += campioni(tex, 2)

    # testo visibile (fuori da script/style e fuori dal katex generato)
    ripulito = re.sub(r'<script\b.*?</script>|<style\b.*?</style>|<span class="katex".*?</span></span>',
                      lambda m: ' ' * len(m.group(0)), t, flags=re.S)
    for m in re.finditer(r'>([^<>]{2,})<', ripulito):
        s = m.group(1)
        if not DECIMALE.search(s):
            continue
        dove = 'testo dentro marcatore' if dentro(fusi, m.start()) else 'testo FUORI'
        conti[dove] += 1
        esempi[dove] += campioni(s, 2)

    if conti:
        print(f'{f.name}:')
        for k in sorted(conti):
            print(f'   {conti[k]:>4}  {k}   es. {list(dict.fromkeys(esempi[k]))[:5]}')
        tot.update(conti)

print('\n--- totale ---')
for k in sorted(tot):
    print(f'   {tot[k]:>4}  {k}')
