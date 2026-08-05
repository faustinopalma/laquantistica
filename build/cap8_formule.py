"""Scheda 8: le due formule dell'osservazione relativistica tornano alla forma
dell'originale - la graffa che raccoglie le due relazioni, e la catena su una riga."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/08-effetto-fotoelettrico.html')
s = P.read_text(encoding='utf-8')

CAMBI = {
    '\\begin{aligned}\nE &amp; =mc^2,\\ p \\\\\n&amp; =mc\\Rightarrow \\\\\np &amp; =\\frac{E}{c}\n\\end{aligned}':
        '\\left.\\begin{array}{l}E=mc^2 \\\\ p=mc\\end{array}\\right\\}\\Rightarrow p=\\frac{E}{c}',
    '\\begin{aligned}\np &amp; =\\frac{E}{c} \\\\\n&amp; =\\frac{h\\nu}{c} \\\\\n&amp; =\\frac{h}{\\lambda}\\Rightarrow \\\\\np\\lambda &amp; =h\n\\end{aligned}':
        'p=\\frac{E}{c}=\\frac{h\\nu}{c}=\\frac{h}{\\lambda}\\Rightarrow p\\lambda=h',
}


def da_html(t):
    return t.replace('&amp;', '&').replace('&#x27;', "'")


def a_html(t):
    return t.replace('&', '&amp;').replace("'", '&#x27;')


richieste = [{'i': k, 'tex': da_html(n), 'display': True} for k, n in enumerate(CAMBI.values())]
r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps(richieste), capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = {}
for x in json.loads(r.stdout):
    if 'err' in x:
        raise SystemExit('%s\n%s' % (richieste[x['i']]['tex'], x['err']))
    reso[richieste[x['i']]['tex']] = x['html']

fatte = 0
for vecchio, nuovo in CAMBI.items():
    while True:
        i = s.find('data-tex="%s"' % vecchio)
        if i < 0:
            break
        a = s.rfind('<span class="', 0, i)
        b = fine_span(s, a)
        apertura = s[a:s.find('>', i) + 1].replace(vecchio, a_html(da_html(nuovo)))
        s = s[:a] + apertura + reso[da_html(nuovo)] + '</span>' + s[b:]
        fatte += 1

assert fatte == len(CAMBI), f'{fatte} sostituzioni su {len(CAMBI)}'
assert s.count('<span') == s.count('</span>')
P.write_text(s, encoding='utf-8', newline='')
print(f'scheda 8: {fatte} formule ricomposte')
