"""Build a compact 2-column comparison page (Original PNG | MathML) per chapter,
so the MathML site can be visually checked against the ground-truth images.
Usage: python scripts/cmp.py <key>
"""
import sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
key = sys.argv[1]
mml = json.loads((ROOT / 'build' / 'mml' / f'{key}.json').read_text(encoding='utf-8'))
rows = []
for i, m in enumerate(mml):
    png = f'/img/eq_{key}/obj{i:03d}.png'
    cell_m = m if (m and m.strip()) else '<span class="miss">— (nessun MathML)</span>'
    rows.append(
        f'<tr><td class="i">{i}</td>'
        f'<td class="o"><img src="{png}"></td>'
        f'<td class="m">{cell_m}</td></tr>')
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{{margin:0;font:14px system-ui;background:#fff;color:#111}}
h1{{margin:0;padding:6px 10px;background:#2b2622;color:#fff;font-size:14px}}
table{{border-collapse:collapse;table-layout:fixed;width:1360px}}
col.ci{{width:40px}} col.co{{width:620px}} col.cm{{width:700px}}
td{{border:1px solid #e2e2e2;padding:4px 8px;vertical-align:middle}}
td.i{{color:#7b2d26;font-weight:bold;text-align:center;background:#faf8f3}}
td.o{{text-align:center}}
td.o img{{max-height:40px;max-width:600px}}
td.m{{padding-left:14px}}
td.m math{{font-size:20px}}
.miss{{color:#b00;font-style:italic}}
tr:nth-child(even){{background:#fbfbfb}}
</style></head><body>
<h1>{key} — confronto Originale (PNG) vs MathML — {len(mml)} formule</h1>
<table><colgroup><col class="ci"><col class="co"><col class="cm"></colgroup>
<tbody>{''.join(rows)}</tbody></table></body></html>'''
out = ROOT / 'build' / f'cmp_{key}.html'
out.write_text(html, encoding='utf-8')
print(f'wrote {out} ({len(mml)} formule)')
