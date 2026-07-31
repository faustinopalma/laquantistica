"""Allinea i pedici delle formule inglesi del Cap.5: l'autore aveva tradotto le
parole ma non il pedice, cosi' nella stessa lingua lo stesso w compariva come
w_Effettiva e w_Effective."""
import html
import json
import pathlib
import re
import subprocess

PERCORSO = pathlib.Path('publish/05-rutherford.html')
t = PERCORSO.read_text(encoding='utf-8')

# le versioni inglesi si riconoscono dalle parole gia' tradotte
INGLESE = ('Effective flux density', 'Beam cross-section', 'Number of scattering atoms')


def fine_elemento(testo, apertura):
    prof = 0
    for m in re.finditer(r'<span\b|</span>', testo[apertura:]):
        prof += 1 if m.group(0).startswith('<span') else -1
        if prof == 0:
            return apertura + m.end()
    raise ValueError('span non chiuso')


bersagli = []
for m in re.finditer(r'data-tex="([^"]*)"', t):
    tex = html.unescape(m.group(1))
    if any(k in tex for k in INGLESE) and (r'\text{Effettiva}' in tex or r'\text{Unitaria}' in tex):
        bersagli.append((m.start(), tex))

print(f'formule inglesi con pedice italiano: {len(bersagli)}')
for off, tex in reversed(bersagli):
    nuovo_tex = tex.replace(r'\text{Effettiva}', r'\text{Effective}') \
                   .replace(r'\text{Unitaria}', r'\text{Unit}')
    apertura = t.rfind('<span', 0, off)
    chiusura = fine_elemento(t, apertura)
    classi = re.search(r'class="([^"]*)"', t[apertura:off]).group(1)
    p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                       input=json.dumps([{'i': 'x', 'tex': nuovo_tex,
                                          'display': 'eq-mml-block' in classi}]),
                       capture_output=True, text=True, encoding='utf-8')
    r = json.loads(p.stdout)[0]
    if 'err' in r:
        raise SystemExit(f'LaTeX rifiutato: {r["err"]}')
    t = (t[:apertura]
         + f'<span class="{classi}" data-tex="{html.escape(nuovo_tex, quote=True)}">{r["html"]}</span>'
         + t[chiusura:])
    print(f'   sistemata a {off}')

PERCORSO.write_text(t, encoding='utf-8')
print('fatto')
