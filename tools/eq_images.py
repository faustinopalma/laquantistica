"""Elenca le formule ancora servite come immagini SVG invece che come matematica.

Per un lettore di schermo queste sono mute: l'alternativa testuale dice solo
"formula". Non scalano col testo, non partecipano alla lettura vocale e usano
un carattere diverso da tutte le altre.

    python tools/eq_images.py
"""
from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path

PUB = Path('publish')
IMG = re.compile(r'<img[^>]*class="([^"]*)"[^>]*src="(img/eq_[^"?]+)[^"]*"[^>]*>')
TEXT = re.compile(r'<text[^>]*>(.*?)</text>', re.S)
TSPAN = re.compile(r'<tspan[^>]*>(.*?)</tspan>', re.S)


def testo_svg(path: Path) -> str:
    if not path.exists():
        return '(file mancante)'
    src = path.read_text(encoding='utf-8', errors='replace')
    pezzi = []
    for blocco in TEXT.findall(src):
        for t in TSPAN.findall(blocco) or [blocco]:
            t = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
            if t:
                pezzi.append(t)
    return ' '.join(pezzi) or '(nessun testo)'


uso: dict[str, list[str]] = defaultdict(list)
for pagina in sorted(PUB.glob('*.html')):
    src = pagina.read_text(encoding='utf-8')
    for classe, rel in IMG.findall(src):
        uso[rel].append(f'{pagina.name} [{classe.strip()}]')

print(f'{len(uso)} immagini-formula distinte, {sum(len(v) for v in uso.values())} inserimenti\n')
for rel in sorted(uso):
    pagine = sorted({p.split(' [')[0] for p in uso[rel]})
    classi = sorted({p.split('[')[1].rstrip(']') for p in uso[rel]})
    print(f'{Path(rel).name:14} x{len(uso[rel])}  {", ".join(pagine)}  ({"; ".join(classi)})')
    print(f'               {testo_svg(PUB / rel)[:100]}')
