"""Sostituisce il MathML delle pagine con l'HTML pre-generato da KaTeX.

Il LaTeX resta la sorgente: sta nell'attributo data-tex e non viene mai toccato,
quindi la conversione e' ripetibile e reversibile. Cambia solo cio' che sta
dentro il contenitore della formula, che e' un prodotto rigenerabile.

Le pagine originali finiscono in backups/katex/ prima di essere riscritte.

    python tools/katex_apply.py publish/05-rutherford.html           # anteprima
    python tools/katex_apply.py publish/05-rutherford.html --write   # scrive
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import index_page   # noqa: E402

BACKUP = Path('backups/katex')
NODE = Path('tools/katexgen/tex2katex.js')


def tex_to_katex(formule: list[dict]) -> dict[int, str]:
    payload = json.dumps([{'i': i, 'tex': f['tex'], 'display': f['display']}
                          for i, f in enumerate(formule)])
    res = subprocess.run(['node', str(NODE)], input=payload,
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
    src, _lang, formule = index_page(path)
    if not formule:
        return {'formule': 0, 'scritto': False}

    reso = tex_to_katex(formule)

    pezzi, pos = [], 0
    for i, f in enumerate(formule):
        pezzi.append(src[pos:f['start']])
        pezzi.append(reso[i])
        pos = f['end']
    pezzi.append(src[pos:])
    nuovo = ''.join(pezzi)

    esito = {'formule': len(formule),
             'prima_kB': round(len(src) / 1024, 1),
             'dopo_kB': round(len(nuovo) / 1024, 1),
             'scritto': False}

    if write:
        BACKUP.mkdir(parents=True, exist_ok=True)
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
        if e['formule']:
            print(f'{p.name:34} {e["formule"]:4} formule  '
                  f'{e["prima_kB"]:7} -> {e["dopo_kB"]:7} kB  [{stato}]')
        else:
            print(f'{p.name:34}    - nessuna formula')
