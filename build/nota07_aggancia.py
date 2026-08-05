"""Aggancia la nota 07 alla scheda 6 e corregge la formula dei livelli nella scheda 9."""
import json
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

# --- 1. richiamo nella scheda 6, subito prima del paragrafo che rinuncia al calcolo
p6 = Path('sorgenti/06-ulteriori-sviluppi.html')
s6 = p6.read_text(encoding='utf-8')
ancora = ('<p><span class="it">In questa scheda non risolviamo questi complicati problemi '
          'matematici;')
assert s6.count(ancora) == 1
richiamo = (
    '<div class="nota-link" id="nota-7">\n'
    '<span class="k"><span class="it">Nota 07</span><span class="en">Note 07</span></span>\n'
    '<span class="it">Il calcolo che porta a questa formula, per intero: '
    '<a href="nota-07-livelli-idrogeno.html?ret=06-ulteriori-sviluppi.html%23nota-7">'
    'l\u2019approfondimento \u2192</a></span>'
    '<span class="en">The full calculation leading to this formula: '
    '<a href="nota-07-livelli-idrogeno.html?ret=06-ulteriori-sviluppi.html%23nota-7">'
    'the derivation \u2192</a></span>\n'
    '</div>\n')
s6 = s6.replace(ancora, richiamo + ancora)
p6.write_text(s6, encoding='utf-8', newline='')
print('scheda 6: richiamo inserito')

# --- 2. la scheda 9 riporta la formula senza il quadrato su epsilon zero
p9 = Path('sorgenti/09-spettri-atomici.html')
s9 = p9.read_text(encoding='utf-8')
VECCHIA = r'E_n=-\frac{me^4}{8\varepsilon_0h^2n^2}'
NUOVA = r'E_n=-\frac{me^4}{8\varepsilon_0^2h^2n^2}'
n = s9.count('data-tex="%s"' % VECCHIA)
assert n >= 1, 'formula non trovata'

r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': 0, 'tex': NUOVA, 'display': True}]),
                   capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = json.loads(r.stdout)[0]
if 'err' in reso:
    raise SystemExit(reso['err'])

sostituzioni = 0
while True:
    i = s9.find('data-tex="%s"' % VECCHIA)
    if i < 0:
        break
    a = s9.rfind('<span class="', 0, i)
    b = fine_span(s9, a)
    apertura = s9[a:s9.find('>', i) + 1].replace(VECCHIA, NUOVA)
    s9 = s9[:a] + apertura + reso['html'] + '</span>' + s9[b:]
    sostituzioni += 1
assert s9.count('<span') == s9.count('</span>')
p9.write_text(s9, encoding='utf-8', newline='')
print(f'scheda 9: {sostituzioni} formule corrette (epsilon zero al quadrato)')

# --- 3. registrazione nel costruttore
sp = Path('build/i18n/split.py')
t = sp.read_text(encoding='utf-8')
assert 'nota-07-livelli-idrogeno.html' not in t
chiave = "    'nota-06-ehrenfest.html': {"
i = t.find(chiave)
assert i > 0
j = t.find('\n    },\n', i) + len('\n    },\n')
voce = (
    "    'nota-07-livelli-idrogeno.html': {\n"
    "        'it': ('Nota 07 \u00b7 I livelli energetici dell\u2019atomo di idrogeno \u2014 La Quantistica', None),\n"
    "        'en': ('Note 07 \u00b7 The energy levels of the hydrogen atom \u2014 La Quantistica',\n"
    "               'The hydrogen level formula derived from the eigenvalue problem: restriction to '\n"
    "               'spherically symmetric states, the substitution u=r\u03c8, a power series and the '\n"
    "               'termination condition from which the integer n emerges.'),\n"
    "    },\n")
t = t[:j] + voce + t[j:]
sp.write_text(t, encoding='utf-8', newline='')
print('split.py: nota 07 registrata')
