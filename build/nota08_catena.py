"""Nota 08: la catena degli autovalori passa da quattro righe a due."""
import json
import subprocess
import sys
from pathlib import Path

F = Path('sorgenti/nota-08-matrici-hermitiane.html')
t = F.read_text(encoding='utf-8')

TEX = (r'\begin{aligned}'
       '\n' r'a\langle\psi|\psi\rangle & =\langle\psi|H|\psi\rangle={\left(\langle\psi|H^+|\psi\rangle\right)}^* \\'
       '\n' r'& ={\left(\langle\psi|H|\psi\rangle\right)}^*=a^*\langle\psi|\psi\rangle'
       '\n' r'\end{aligned}')

p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': 0, 'tex': TEX, 'display': True}]),
                   capture_output=True, text=True, encoding='utf-8')
if p.returncode:
    sys.exit(p.stderr)
r = json.loads(p.stdout)[0]
if 'err' in r:
    sys.exit(r['err'])

i = t.find('a\\langle\\psi|\\psi\\rangle &amp; =\\langle\\psi|H|\\psi\\rangle')
if i == -1:
    sys.exit('catena non trovata')
inizio = t.rfind('<div class="equation">', 0, i)
fine = t.find('</div>', i) + len('</div>')
if t[inizio:fine].count('<div') != 1:
    sys.exit('il blocco contiene altri div')

esc = TEX.replace('&', '&amp;').replace("'", '&#x27;')
t = (t[:inizio]
     + '<div class="equation"><span class="eq-mml eq-mml-block" data-tex="%s">%s</span></div>' % (esc, r['html'])
     + t[fine:])
F.write_text(t, encoding='utf-8')
print('catena della nota 08 compattata su due righe')
