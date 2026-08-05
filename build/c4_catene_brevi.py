"""Le due verifiche K^+=K e H^+=H stavano su cinque righe: una sola basta.

Sono catene di passaggi brevissimi: andare a capo a ogni uguale le faceva
sembrare un conto lungo. Le altre derivazioni del capitolo hanno termini lunghi
e restano a capo.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

F = Path('sorgenti/04-diffrazione.html')
t = F.read_text(encoding='utf-8')

NUOVE = {
    'K^+ &amp; =(iD)^+': 'K^+=(iD)^+=i^*D^+=(-i)(-D)=iD=K',
    'H^+ &amp; ={\\left(iA\\right)}^+': 'H^+={\\left(iA\\right)}^+=i^*A^+=(-i)(-A)=iA=H',
}

p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': i, 'tex': tex, 'display': True}
                                     for i, tex in enumerate(NUOVE.values())]),
                   capture_output=True, text=True, encoding='utf-8')
if p.returncode:
    sys.exit(p.stderr)
reso = {}
for r in json.loads(p.stdout):
    if 'err' in r:
        sys.exit(r['err'])
    reso[list(NUOVE.values())[r['i']]] = r['html']


def esc(x):
    return x.replace('&', '&amp;').replace("'", '&#x27;')


for marcatore, tex in NUOVE.items():
    i = t.find(marcatore)
    if i == -1:
        sys.exit(f'non trovato: {marcatore}')
    inizio = t.rfind('<div class="equation">', 0, i)
    fine = t.find('</div>', i) + len('</div>')
    vecchio = t[inizio:fine]
    if vecchio.count('<div') != 1:
        sys.exit('il blocco contiene altri div: sostituzione non sicura')
    nuovo = ('<div class="equation"><span class="eq-mml eq-mml-block" data-tex="%s">%s</span></div>'
             % (esc(tex), reso[tex]))
    t = t[:inizio] + nuovo + t[fine:]
    print(f'compattata: {tex}')

F.write_text(t, encoding='utf-8')
print('capitolo 4 riscritto,', t.count('data-tex='), 'formule in tutto')
