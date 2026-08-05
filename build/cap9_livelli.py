"""Scheda 9: la formula dei livelli in forma con la barra, per non rimpicciolire
numeratore e denominatore. In linea TeX compone le frazioni in scriptstyle."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/09-spettri-atomici.html')
s = P.read_text(encoding='utf-8')

VECCHIA = 'E_n=-\\frac{me^4}{8\\varepsilon_0^2h^2n^2}'
NUOVA = 'E_n=-me^4/(8\\varepsilon_0^2h^2n^2)'

r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': 0, 'tex': NUOVA, 'display': False}]),
                   capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = json.loads(r.stdout)[0]
if 'err' in reso:
    raise SystemExit(reso['err'])

fatte, da = 0, 0
while True:
    i = s.find('data-tex="%s"' % VECCHIA, da)
    if i < 0:
        break
    a = s.rfind('<span class="', 0, i)
    b = fine_span(s, a)
    apertura = s[a:s.find('>', i) + 1].replace(VECCHIA, NUOVA)
    pezzo = apertura + reso['html'] + '</span>'
    s = s[:a] + pezzo + s[b:]
    da = a + len(pezzo)
    fatte += 1

assert fatte >= 1
assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')
print(f'scheda 9: {fatte} formule in forma con la barra')
