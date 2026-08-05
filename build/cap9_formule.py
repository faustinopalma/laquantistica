"""Scheda 9: la catena del reticolo torna su una riga come nell'originale, e la
formula dei livelli viene rigenerata davvero in linea (era un blocco display
infilato dentro uno span in linea, alto 82 px su una riga da 34)."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/09-spettri-atomici.html')
s = P.read_text(encoding='utf-8')

CATENA_VECCHIA = ('\\begin{aligned}\n\\frac{\\lambda}{d} &amp; =\\sin\\vartheta\\Leftrightarrow \\\\\n'
                  '\\frac{c}{\\nu d} &amp; =\\sin\\vartheta\\Leftrightarrow \\\\\n'
                  '\\nu &amp; =\\frac{c}{d\\sin\\vartheta}\n\\end{aligned}')
CATENA_NUOVA = ('\\frac{\\lambda}{d}=\\sin\\vartheta\\Leftrightarrow\\frac{c}{\\nu d}='
                '\\sin\\vartheta\\Leftrightarrow\\nu=\\frac{c}{d\\sin\\vartheta}')
LIVELLI = 'E_n=-\\frac{me^4}{8\\varepsilon_0^2h^2n^2}'

# (tex vecchio, tex nuovo, display)
LAVORI = [(CATENA_VECCHIA, CATENA_NUOVA, True),
          (LIVELLI, LIVELLI, False)]

richieste = [{'i': k, 'tex': n.replace('&amp;', '&'), 'display': d}
             for k, (_, n, d) in enumerate(LAVORI)]
r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps(richieste), capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = {}
for x in json.loads(r.stdout):
    if 'err' in x:
        raise SystemExit('%s\n%s' % (richieste[x['i']]['tex'], x['err']))
    reso[x['i']] = x['html']

fatte = 0
for k, (vecchio, nuovo, _) in enumerate(LAVORI):
    da = 0                       # la ricerca deve avanzare: vecchio e nuovo possono coincidere
    while True:
        i = s.find('data-tex="%s"' % vecchio, da)
        if i < 0:
            break
        a = s.rfind('<span class="', 0, i)
        b = fine_span(s, a)
        apertura = s[a:s.find('>', i) + 1].replace(vecchio, nuovo)
        nuovo_span = apertura + reso[k] + '</span>'
        s = s[:a] + nuovo_span + s[b:]
        da = a + len(nuovo_span)
        fatte += 1

assert fatte >= 2, f'solo {fatte} sostituzioni'
assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')
print(f'scheda 9: {fatte} formule ricomposte')
