"""Mette in una pagina sola le formule ancora servite come immagini.

Serve per leggerle tutte insieme e riscriverle in LaTeX: il testo dentro gli SVG
c'e', ma nell'ordine in cui e' stato disegnato, quindi non basta a ricostruire la
formula. Vanno guardate.

    python tools/eq_images_page.py
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

PUB = Path('publish')
OUT = Path('build/eqimg')
IMG = re.compile(r'<img[^>]*class="([^"]*eq-[^"]*)"[^>]*src="(img/eq_[^"?]+)[^"]*"[^>]*>')

uso: dict[str, list[str]] = defaultdict(list)
for pagina in sorted(PUB.glob('*.html')):
    src = pagina.read_text(encoding='utf-8')
    for classe, rel in IMG.findall(src):
        riga = src[:src.find(rel)].count('\n') + 1
        uso[rel].append(f'{pagina.name}:{riga} [{classe.strip()}]')

righe = []
for i, rel in enumerate(sorted(uso)):
    dove = '<br>'.join(uso[rel])
    righe.append(
        f'<div class="r"><div class="n">[{i}]<br>{Path(rel).name}</div>'
        f'<div class="i"><img src="../../publish/{rel}"></div>'
        f'<div class="d">{dove}</div></div>')

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'immagini.html').write_text(f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8"><title>Formule ancora immagini</title>
<style>
body{{font:14px/1.5 system-ui,sans-serif;margin:0;padding:20px;background:#fff}}
.r{{display:grid;grid-template-columns:130px 1fr 250px;gap:16px;align-items:center;
   border-bottom:1px solid #eee;padding:14px 0}}
.n{{font:11px ui-monospace,monospace;color:#888}}
.i img{{max-width:100%;background:#fafafa;padding:6px;border:1px solid #eee}}
.d{{font:11px ui-monospace,monospace;color:#666}}
</style></head><body>
<h1>{len(uso)} formule ancora servite come immagini</h1>
{chr(10).join(righe)}
</body></html>""", encoding='utf-8')
print(f'build/eqimg/immagini.html  ({len(uso)} immagini)')
