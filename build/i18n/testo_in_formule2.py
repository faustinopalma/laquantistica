"""Come testo_in_formule.py ma usando il parser vero (Potatore) per stabilire
se la formula sta davvero dentro uno span di lingua."""
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import Potatore  # noqa: E402

RADICE = pathlib.Path('publish')
PAROLA = re.compile(r'[A-Za-zÀ-ÿ]{4,}')
SCARTA = {'text', 'mathrm', 'begin', 'aligned', 'gathered', 'left', 'right', 'frac', 'Omega',
          'times', 'quad', 'qquad', 'hbox', 'mbox', 'displaystyle', 'operatorname', 'sqrt',
          'cdot', 'theta', 'alpha', 'beta', 'gamma', 'delta', 'lambda', 'sigma', 'omega',
          'infty', 'partial', 'over', 'atop', 'mathbf', 'mathit', 'vphantom', 'phantom'}


def coperti(testo):
    fusi = []
    tutti = []
    for l in ('it', 'en'):
        p = Potatore(testo, l)
        p.feed(testo)
        p.close()
        tutti += p.intervalli
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


totale = 0
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'data-tex' not in t or 'class="it"' not in t:
        continue
    fusi = coperti(t)
    fuori = []
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        frasi = []
        for c in re.finditer(r'\\(?:text|mathrm|textrm|textit)\{([^{}]*)\}', tex):
            if [w for w in PAROLA.findall(c.group(1)) if w.lower() not in SCARTA]:
                frasi.append(c.group(1).strip())
        if frasi and not dentro(fusi, m.start()):
            fuori.append((m.start(), ' / '.join(frasi)[:80]))
    if fuori:
        totale += len(fuori)
        print(f'{f.name}: {len(fuori)} formule con parole, FUORI dai marcatori di lingua')
        for pos, s in fuori:
            print(f'      offset {pos}: "{s}"')

print(f'\ntotale: {totale}')
