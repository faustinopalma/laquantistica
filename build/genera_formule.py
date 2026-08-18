"""Rende in HTML KaTeX le formule nuove, con lo stesso KaTeX del sito.

Legge righe `display\ttex` o `inline\ttex` da un file e stampa i frammenti gia'
avvolti come li vogliono le pagine.

  python build/genera_formule.py build/formule.txt
"""
import json
import pathlib
import subprocess
import sys

SORGENTE = pathlib.Path(sys.argv[1])
RENDER = pathlib.Path('tools/katexgen/tex2katex.js')

voci = []
for riga in SORGENTE.read_text(encoding='utf-8').splitlines():
    if not riga.strip():
        continue
    modo, tex = riga.split('\t', 1)
    voci.append({'i': len(voci), 'tex': tex, 'display': modo == 'display'})

reso = subprocess.run(['node', str(RENDER)], input=json.dumps(voci),
                      capture_output=True, text=True, encoding='utf-8', check=True)
uscita = {v['i']: v for v in json.loads(reso.stdout)}

fuori = []
for v in voci:
    r = uscita[v['i']]
    if 'err' in r:
        sys.exit(f'KaTeX: {v["tex"]} -> {r["err"]}')
    tex = v['tex'].replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
    if v['display']:
        fuori.append(f'<div class="equation"><span class="eq-mml eq-mml-block" '
                     f'data-tex="{tex}">{r["html"]}</span></div>')
    else:
        fuori.append(f'<span class="eq-inline eq-mml" data-tex="{tex}">{r["html"]}</span>')

SORGENTE.with_suffix('.html').write_text('\n'.join(fuori), encoding='utf-8', newline='')
print(f'{len(fuori)} formule in {SORGENTE.with_suffix(".html")}')
