"""Rimette a blocco i disegni che sono in linea ma stanno da soli.

Nell'originale i vettori colonna incassati nel discorso stanno dentro la frase,
mentre le formule che valgono da sole sono centrate su una riga propria. Nella
conversione tutte sono finite marcate «in linea»: quelle che non hanno testo
accanto restano allora appese dentro un paragrafo vuoto, e il loro allineamento
al centro della riga sballa l'interlinea.

Distingue guardando se c'e' davvero del testo prima o dopo, nel loro contenitore.

    python tools/img_blocco.py publish/02-stern-gerlach-cascata.html
    python tools/img_blocco.py publish/02-stern-gerlach-cascata.html --write
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

IMG = re.compile(r'<img\b[^>]*class="(eq-inline[^"]*)"[^>]*>')
TAG = re.compile(r'<[^>]+>')


def testo_intorno(src: str, start: int, end: int) -> tuple[str, str]:
    """Testo vero (senza tag) fino al confine di paragrafo, prima e dopo."""
    prima = src[max(0, start - 900):start]
    taglio = max(prima.rfind('<p'), prima.rfind('</p>'), prima.rfind('<br'))
    prima = prima[taglio + 1:] if taglio >= 0 else prima
    dopo = src[end:end + 900]
    taglio = min([i for i in (dopo.find('</p>'), dopo.find('<p'), dopo.find('<br'))
                  if i >= 0] or [len(dopo)])
    dopo = dopo[:taglio]
    return TAG.sub(' ', prima).strip(), TAG.sub(' ', dopo).strip()


def lavora(path: Path, write: bool) -> dict:
    src = path.read_text(encoding='utf-8')
    pezzi, pos, sole, incassate = [], 0, 0, 0
    for m in IMG.finditer(src):
        prima, dopo = testo_intorno(src, m.start(), m.end())
        pezzi.append(src[pos:m.start()])
        if prima or dopo:
            incassate += 1
            pezzi.append(m.group(0))
        else:
            sole += 1
            nuova = m.group(0).replace(f'class="{m.group(1)}"', 'class="eq-figure"')
            pezzi.append(nuova)
        pos = m.end()
    pezzi.append(src[pos:])
    if write and sole:
        path.write_text(''.join(pezzi), encoding='utf-8', newline='')
    return {'sole': sole, 'incassate': incassate}


if __name__ == '__main__':
    write = '--write' in sys.argv
    for arg in (a for a in sys.argv[1:] if not a.startswith('--')):
        p = Path(arg)
        e = lavora(p, write)
        print(f'{p.name:34} {e["sole"]:3} da sole -> a blocco, '
              f'{e["incassate"]:3} restano nella frase '
              f'[{"scritto" if write else "anteprima"}]')
