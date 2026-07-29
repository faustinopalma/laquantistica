"""Pre-genera anche le formule scritte in LaTeX dentro il testo.

Alcune pagine non hanno il MathML nel sorgente: la formula e' scritta fra \\( \\)
o \\[ \\] e veniva composta dal browser. Senza motore a runtime resterebbero
grezze, quindi vengono disegnate qui e chiuse in un contenitore che conserva il
LaTeX in data-tex, come tutte le altre.

Salta il contenuto di script e style, dove quelle sequenze non sono formule.

    python tools/katex_inline.py publish/nota-tecnica-01-stern-gerlach.html --write
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BACKUP = Path('backups/katex')
NODE = Path('tools/katexgen/tex2katex.js')

SALTA = re.compile(r'<(script|style)\b.*?</\1>', re.S | re.I)
FORMULA = re.compile(r'\\\[(.+?)\\\]|\\\((.+?)\\\)', re.S)


def genera(items: list[dict]) -> dict[int, str]:
    res = subprocess.run(['node', str(NODE)], input=json.dumps(items),
                         capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(f'tex2katex.js: {res.stderr.strip()}')
    out = {}
    for row in json.loads(res.stdout):
        if row.get('err'):
            raise RuntimeError(f'formula [{row["i"]}]: {row["err"]}')
        out[row['i']] = row['html']
    return out


def convert(path: Path, write: bool = False) -> dict:
    src = path.read_text(encoding='utf-8')

    # gli intervalli da non toccare
    vietati = [(m.start(), m.end()) for m in SALTA.finditer(src)]

    def dentro_vietato(i: int) -> bool:
        return any(a <= i < b for a, b in vietati)

    trovate = []
    for m in FORMULA.finditer(src):
        if dentro_vietato(m.start()):
            continue
        display = m.group(1) is not None
        tex = (m.group(1) or m.group(2)).strip()
        trovate.append({'m': m, 'tex': html.unescape(tex), 'display': display})

    if not trovate:
        return {'formule': 0, 'scritto': False}

    reso = genera([{'i': i, 'tex': f['tex'], 'display': f['display']}
                   for i, f in enumerate(trovate)])

    pezzi, pos = [], 0
    for i, f in enumerate(trovate):
        m = f['m']
        pezzi.append(src[pos:m.start()])
        classe = 'eq-mml eq-mml-block' if f['display'] else 'eq-inline eq-mml'
        attr = html.escape(f['tex'], quote=True)
        pezzi.append(f'<span class="{classe}" data-tex="{attr}">{reso[i]}</span>')
        pos = m.end()
    pezzi.append(src[pos:])
    nuovo = ''.join(pezzi)

    esito = {'formule': len(trovate), 'scritto': False}
    if write:
        BACKUP.mkdir(parents=True, exist_ok=True)
        if not (BACKUP / path.name).exists():
            shutil.copy2(path, BACKUP / path.name)
        path.write_text(nuovo, encoding='utf-8', newline='')
        esito['scritto'] = True
    return esito


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    write = '--write' in sys.argv
    for arg in args:
        p = Path(arg)
        e = convert(p, write)
        stato = 'scritta' if e['scritto'] else 'anteprima'
        print(f'{p.name:38} {e["formule"]:3} formule  [{stato if e["formule"] else "-"}]')
