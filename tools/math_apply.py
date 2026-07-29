"""Riscrive una pagina sostituendo il MathML con quello generato dal LaTeX.

Architettura B: il LaTeX diventa la SORGENTE (attributo data-tex sul contenitore
della formula) e il MathML nel file e' un prodotto rigenerabile. Chi deve
correggere una formula tocca il data-tex e rilancia questo script; il giorno in
cui si vorra' togliere MathJax bastera' smettere di caricarlo, perche' il MathML
e' gia' nella pagina.

Uso:
    python tools/math_apply.py publish/09-spettri-atomici.html            # anteprima
    python tools/math_apply.py publish/09-spettri-atomici.html --write    # scrive
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from math_extract import extract            # noqa: E402
from mml2tex import mml_to_tex, MathMLUnsupported   # noqa: E402

BACKUP_DIR = Path('backups/mathml')
NODE_SCRIPT = Path('tools/mathgen/tex2mml.js')
SPAN_BEFORE = re.compile(r'<(span|div)\b([^>]*)>\s*$')


def tex_to_mml(items: list[dict]) -> dict[int, str]:
    payload = json.dumps([{'i': it['i'], 'tex': it['tex'],
                           'display': it['display'] == 'block'} for it in items])
    res = subprocess.run(['node', str(NODE_SCRIPT)], input=payload,
                         capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(f'tex2mml.js: {res.stderr.strip()}')
    out = {}
    for row in json.loads(res.stdout):
        if row.get('err'):
            raise RuntimeError(f'formula [{row["i"]}]: {row["err"]}')
        out[row['i']] = row['mml']
    return out


def compact(mml: str) -> str:
    """MathJax indenta il MathML; qui lo si compatta senza toccare il testo."""
    return re.sub(r'>\s+<', '><', mml).strip()


def convert_page(path: Path, write: bool = False) -> dict:
    src, items = extract(path)
    for it in items:
        try:
            tex, unknown = mml_to_tex(it['src'], f'{path.name}[{it["i"]}]')
        except MathMLUnsupported as e:
            raise RuntimeError(str(e)) from e
        if unknown:
            raise RuntimeError(f'[{it["i"]}] riga {it["line"]}: {"; ".join(unknown)}')
        it['tex'] = tex

    mml = tex_to_mml(items)

    pieces, pos, added, wrapped = [], 0, 0, 0
    for it in items:
        start, end = it['start'], it['start'] + len(it['src'])
        head = src[pos:start]
        attr = ' data-tex="' + html.escape(it['tex'], quote=True) + '"'
        body = compact(mml[it['i']])
        m = SPAN_BEFORE.search(head)
        if m and 'data-tex=' not in m.group(2):
            cut = m.end() - 1                   # il '>' che chiude il tag di apertura
            pieces.append(head[:cut] + attr + head[cut:])
            pieces.append(body)
            added += 1
        else:
            pieces.append(head)
            pieces.append(f'<span class="eq"{attr}>{body}</span>')
            wrapped += 1
        pos = end
    pieces.append(src[pos:])
    return {'src': src, 'out': ''.join(pieces), 'items': items,
            'added': added, 'wrapped': wrapped}


if __name__ == '__main__':
    p = Path(sys.argv[1])
    write = '--write' in sys.argv
    r = convert_page(p, write)
    print(f'{p.name}: {len(r["items"])} formule · '
          f'{len(r["src"]):,} -> {len(r["out"]):,} byte '
          f'({100 * len(r["out"]) / len(r["src"]):.0f}%)')
    if write:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        (BACKUP_DIR / p.name).write_text(r['src'], encoding='utf-8')
        p.write_text(r['out'], encoding='utf-8')
        print(f'scritto · originale in {BACKUP_DIR / p.name}')
    else:
        print('(anteprima: usa --write per scrivere)')
