"""Mostra il testo attorno a ogni formula-immagine, per capire cosa dice.

Il disegno da solo non basta: `(*)` o una lettera isolata prendono senso solo
dalla frase che li ospita.

    python tools/eq_images_ctx.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

PUB = Path('publish')
IMG = re.compile(r'<img[^>]*class="[^"]*eq-[^"]*"[^>]*src="(img/eq_[^"?]+)[^"]*"[^>]*>')


def pulisci(s: str) -> str:
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


for pagina in sorted(PUB.glob('*.html')):
    src = pagina.read_text(encoding='utf-8')
    trovate = list(IMG.finditer(src))
    if not trovate:
        continue
    print(f'\n########## {pagina.name}')
    visti = set()
    for m in trovate:
        nome = Path(m.group(1)).name
        if nome in visti:
            continue
        visti.add(nome)
        prima = pulisci(src[max(0, m.start() - 320):m.start()])[-160:]
        dopo = pulisci(src[m.end():m.end() + 320])[:160]
        riga = src[:m.start()].count('\n') + 1
        print(f'\n--- {nome}  riga {riga}')
        print(f'    ...{prima}')
        print(f'    [IMMAGINE]')
        print(f'    {dopo}...')
