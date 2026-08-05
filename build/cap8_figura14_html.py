"""Inserisce la figura 14 dopo la tabella, la richiama nel testo e corregge
l'unita' della pendenza (era scritta al quadrato)."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/08-effetto-fotoelettrico.html')
s = P.read_text(encoding='utf-8')

# --- 1. la figura, subito dopo la tabella
FIGURA = (
    '<figure id="fig-08_effetto_fotoelettrico-14" class="fig-inline">'
    '<img class="it" loading="lazy" src="img/08_effetto_fotoelettrico/GRAFICO.svg?v=1" '
    'alt="Energia degli elettroni in funzione della frequenza della luce.">'
    '<img class="en" loading="lazy" src="img/08_effetto_fotoelettrico/GRAFICO-en.svg?v=1" '
    'alt="Electron energy as a function of the frequency of the light.">'
    '<figcaption><b>Fig. 14</b> \u2014 '
    '<span class="it">Energia degli elettroni in funzione della frequenza della luce.</span>'
    '<span class="en">Electron energy as a function of the frequency of the light.</span>'
    '</figcaption></figure>')

righe = s.split('\n')
k = next(i for i, r in enumerate(righe) if r.strip() == '</table>')
assert righe[k + 1].startswith('<p><span class="it">Si osserva che i punti')
righe.insert(k + 1, FIGURA)
s = '\n'.join(righe)
print('figura 14 inserita dopo la tabella')

# --- 2. il richiamo nel testo
RIF = ('<a class="ref" href="#fig-08_effetto_fotoelettrico-14" '
       'data-ref="fig-08_effetto_fotoelettrico-14">14</a>')
for vecchio, nuovo in [
        ('Si osserva che i punti si dispongono su una retta con una pendenza di',
         'Si osserva che i punti si dispongono su una retta (fig. %s) con una pendenza di' % RIF),
        ('the points lie on a straight line with a slope of',
         'the points lie on a straight line (fig. %s) with a slope of' % RIF)]:
    n = s.count(vecchio)
    assert n == 1, f'{n} occorrenze di {vecchio[:50]!r}'
    s = s.replace(vecchio, nuovo)
print('richiamo alla figura 14 aggiunto')

# --- 3. la pendenza di una retta energia/frequenza si misura in eV s, non in (eV s)^2
VECCHIA = ('3{,}6\\cdot10^{-15}\\ {\\text{eV}\\:\\mathrm{s}}^2\\equiv5{,}8\\cdot10^{-34}\\ '
           '{\\mathrm{J}\\:\\mathrm{s}}^2')
NUOVA = ('3{,}6\\cdot10^{-15}\\ \\text{eV}\\:\\mathrm{s}\\equiv5{,}8\\cdot10^{-34}\\ '
         '\\mathrm{J}\\:\\mathrm{s}')
n = s.count('data-tex="%s"' % VECCHIA)
assert n >= 1, 'formula della pendenza non trovata'

r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': 0, 'tex': NUOVA, 'display': False}]),
                   capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = json.loads(r.stdout)[0]
if 'err' in reso:
    raise SystemExit(reso['err'])

fatte = 0
while True:
    i = s.find('data-tex="%s"' % VECCHIA)
    if i < 0:
        break
    a = s.rfind('<span class="', 0, i)
    b = fine_span(s, a)
    apertura = s[a:s.find('>', i) + 1].replace(VECCHIA, NUOVA)
    s = s[:a] + apertura + reso['html'] + '</span>' + s[b:]
    fatte += 1
print(f'unita\u2019 della pendenza corretta in {fatte} formule')

assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')
