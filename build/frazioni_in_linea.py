"""Frazioni in linea in forma con la barra: in text style TeX compone numeratore e
denominatore in scriptstyle (70%) e i loro esponenti in scriptscriptstyle (50%),
cioe' 14 px e 10 px contro i 20 px del testo."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

CAMBI = {
    '05-rutherford.html': {
        '\\omega=\\frac{\\hbar k^2}{2m}': '\\omega=\\hbar k^2/2m',
        'V(r&#x27;)=\\frac{1}{4\\pi\\varepsilon_0}\\frac{Q}{r&#x27;}':
            'V(r&#x27;)=Q/(4\\pi\\varepsilon_0 r&#x27;)',
        'V(r&#x27;)=\\frac{1}{4\\pi\\varepsilon_0}\\frac{Q}{r&#x27;}e^{-\\frac{r&#x27;}{a}}':
            'V(r&#x27;)=Qe^{-r&#x27;/a}/(4\\pi\\varepsilon_0 r&#x27;)',
        '\\frac{1}{\\sin^4\\frac{\\vartheta}{2}}': '1/\\sin^4(\\vartheta/2)',
        'w=\\frac{q^2Q^2}{64\\pi^2\\varepsilon_0^2m^2v^4}\\frac{1}{\\sin^4\\frac{\\vartheta}{2}}':
            'w=q^2Q^2/(64\\pi^2\\varepsilon_0^2m^2v^4\\sin^4(\\vartheta/2))',
        '\\psi=-\\frac{1}{4\\pi}\\frac{e^{ik|\\overline{r}-{\\overline{r}}&#x27;|}}{|\\overline{r}-{\\overline{r}}&#x27;|}':
            '\\psi=-e^{ik|\\overline{r}-{\\overline{r}}&#x27;|}/(4\\pi|\\overline{r}-{\\overline{r}}&#x27;|)',
        '\\psi=-\\frac{1}{4\\pi}\\frac{e^{ik|\\vec{r}-\\vec{r}{\\:}&#x27;|}}{|\\vec{r}-\\vec{r}{\\:}&#x27;|}':
            '\\psi=-e^{ik|\\vec{r}-\\vec{r}{\\:}&#x27;|}/(4\\pi|\\vec{r}-\\vec{r}{\\:}&#x27;|)',
    },
    '06-ulteriori-sviluppi.html': {
        'V(r)=\\frac{1}{4\\pi\\varepsilon_0}\\frac{e}{r}': 'V(r)=e/(4\\pi\\varepsilon_0 r)',
    },
}


def da_html(t):
    return t.replace('&#x27;', "'").replace('&amp;', '&')


for nome, coppie in CAMBI.items():
    P = Path('sorgenti', nome)
    s = P.read_text(encoding='utf-8')

    richieste = [{'i': k, 'tex': da_html(n), 'display': False}
                 for k, n in enumerate(coppie.values())]
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
    for k, (vecchio, nuovo) in enumerate(coppie.items()):
        da = 0
        while True:
            i = s.find('data-tex="%s"' % vecchio, da)
            if i < 0:
                break
            a = s.rfind('<span class="', 0, i)
            b = fine_span(s, a)
            pezzo = s[a:s.find('>', i) + 1].replace(vecchio, nuovo) + reso[k] + '</span>'
            s = s[:a] + pezzo + s[b:]
            da = a + len(pezzo)
            fatte += 1
    assert s.count('<span') == s.count('</span>')
    P.write_text(s, encoding='utf-8', newline='')
    print(f'{nome}: {fatte} frazioni in linea convertite')
