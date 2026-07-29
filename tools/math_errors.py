"""Elenca le formule il cui LaTeX non viene accettato da MathJax.

Uso:  python tools/math_errors.py publish/04-diffrazione.html ...
Per ognuna stampa riga, LaTeX prodotto, messaggio d'errore e MathML di partenza,
cosi' si capisce se il difetto e' nel convertitore o nel contenuto della pagina.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from math_extract import extract            # noqa: E402
from mml2tex import mml_to_tex, MathMLUnsupported   # noqa: E402

NODE_SCRIPT = Path('tools/mathgen/tex2mml.js')
# MathJax segnala in due modi: <merror> per gli errori di sintassi e testo rosso
# per i comandi che non conosce. Il secondo non e' un nodo di errore: va cercato
# a parte, altrimenti passa inosservato.
MERROR = re.compile(r'<merror[\s>]|data-mjx-error="([^"]*)"')
UNDEF = re.compile(r'<mtext mathcolor="red">([^<]*)</mtext>')


def check(path: Path):
    _, items = extract(path)
    rows = []
    for it in items:
        try:
            tex, unknown = mml_to_tex(it['src'], f'{path.name}[{it["i"]}]')
        except MathMLUnsupported as e:
            rows.append((it, '', f'MathML non ben formato: {e}'))
            continue
        if unknown:
            rows.append((it, tex, 'convertitore: ' + '; '.join(unknown)))
            continue
        it['tex'] = tex

    todo = [it for it in items if 'tex' in it]
    payload = json.dumps([{'i': it['i'], 'tex': it['tex'],
                           'display': it['display'] == 'block'} for it in todo])
    res = subprocess.run(['node', str(NODE_SCRIPT)], input=payload,
                         capture_output=True, text=True, encoding='utf-8')
    out = {r['i']: r for r in json.loads(res.stdout)} if res.returncode == 0 else {}
    for it in todo:
        r = out.get(it['i'], {})
        mml = r.get('mml', '')
        if r.get('err'):
            rows.append((it, it['tex'], 'node: ' + r['err']))
        elif MERROR.search(mml):
            m = re.search(r'data-mjx-error="([^"]*)"', mml)
            rows.append((it, it['tex'], 'LaTeX: ' + (m.group(1) if m else 'merror')))
        elif UNDEF.search(mml):
            names = sorted(set(UNDEF.findall(mml)))
            rows.append((it, it['tex'], 'comando sconosciuto: ' + ', '.join(names)))
    return rows


if __name__ == '__main__':
    total = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        rows = check(p)
        total += len(rows)
        if not rows:
            print(f'\n===== {p.name}: nessun errore')
            continue
        print(f'\n===== {p.name}: {len(rows)} errori')
        for it, tex, msg in rows:
            print(f'\n[{it["i"]}] riga {it["line"]} · {it["display"]}')
            print(f'  errore : {msg}')
            print(f'  latex  : {tex[:300]}')
            print(f'  mathml : {it["src"][:400]}')
    print(f'\ntotale: {total}')
