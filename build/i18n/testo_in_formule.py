"""Formule con parole in lingua naturale dentro \\text{} o \\mathrm{}: restano
nella lingua in cui sono scritte, qualunque sia la lingua della pagina."""
import html
import pathlib
import re

RADICE = pathlib.Path('publish')
# parole di almeno 3 lettere: scarto simboli, unita' e indici
PAROLA = re.compile(r'[A-Za-zÀ-ÿ]{4,}')
UNITA = {'text', 'mathrm', 'begin', 'aligned', 'gathered', 'left', 'right', 'frac', 'Omega',
         'times', 'quad', 'qquad', 'hbox', 'mbox', 'displaystyle', 'operatorname', 'sqrt',
         'cdot', 'theta', 'alpha', 'beta', 'gamma', 'delta', 'lambda', 'sigma', 'omega',
         'infty', 'partial', 'over', 'atop', 'mathbf', 'mathit', 'vphantom', 'phantom'}

totale = 0
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'data-tex' not in t:
        continue
    trovate = []
    for m in re.finditer(r'data-tex="([^"]*)"', t):
        tex = html.unescape(m.group(1))
        for c in re.finditer(r'\\(?:text|mathrm|textrm|textit)\{([^{}]*)\}', tex):
            parole = [w for w in PAROLA.findall(c.group(1)) if w.lower() not in UNITA]
            if parole:
                dentro_lingua = False
                # lo span di lingua piu' vicino prima dell'elemento
                pre = t[max(0, m.start() - 3000):m.start()]
                ap = max(pre.rfind('<span class="it">'), pre.rfind('<span class="en">'))
                if ap >= 0 and pre.count('</span>', ap) < pre.count('<span', ap):
                    dentro_lingua = True
                trovate.append((c.group(1)[:60], dentro_lingua))
    if trovate:
        unici = list(dict.fromkeys(trovate))
        fuori = [s for s, d in unici if not d]
        totale += len(fuori)
        print(f'{f.name}: {len(unici)} frasi in formula, di cui {len(fuori)} FUORI dai marcatori')
        for s in fuori[:6]:
            print(f'      "{s}"')

print(f'\ntotale frasi in formula fuori dai marcatori di lingua: {totale}')
