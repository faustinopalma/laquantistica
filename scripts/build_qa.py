"""Build per-chapter QA comparison pages: for each formula index, show the ORIGINAL
(WMF->PNG), the SVG (WMF->SVG), and the MathML (LibreOffice) side by side so
mismatches/offsets are visible. Served from repo root."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EQIMG = ROOT / 'img'                 # originals: img/eq_<key>/objNNN.png
EQSVG = ROOT / 'build' / 'eqsvg'
MML = ROOT / 'build' / 'mml'
QA = ROOT / 'build' / 'qa'
QA.mkdir(parents=True, exist_ok=True)

KEYS = ['00_introduzione', '04_diffrazione', '05_rutherford', '06_ulteriori_sviluppi',
        '08_effetto_fotoelettrico', '09_spettri_atomici']

CSS = """body{font:15px system-ui;margin:0;background:#fff;color:#111}
h1{padding:12px 16px;background:#2b2622;color:#fff;margin:0;position:sticky;top:0}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid #ddd;padding:8px 10px;vertical-align:middle;text-align:center}
th{background:#f3f0e9;position:sticky;top:44px}
td.idx{font-weight:bold;color:#7b2d26;background:#faf8f3}
td.o img{max-height:60px}
td.s img{max-height:60px}
td.m math{font-size:22px}
tr:nth-child(even){background:#fbfbfb}
.miss{color:#b00;font-style:italic}"""


def build(key):
    mmlf = MML / f'{key}.json'
    maths = json.loads(mmlf.read_text(encoding='utf-8')) if mmlf.exists() else []
    svgdir = EQSVG / key
    svgs = sorted(svgdir.glob('obj*.svg')) if svgdir.exists() else []
    nsvg = (max(int(p.stem[3:]) for p in svgs) + 1) if svgs else 0
    n = max(nsvg, len(maths))
    rows = []
    for i in range(n):
        png = EQIMG / f'eq_{key}' / f'obj{i:03d}.png'
        svg = svgdir / f'obj{i:03d}.svg'
        o = (f'<img src="/img/eq_{key}/obj{i:03d}.png">' if png.exists()
             else '<span class="miss">—</span>')
        s = (f'<img src="/build/eqsvg/{key}/obj{i:03d}.svg">' if svg.exists()
             else '<span class="miss">—</span>')
        m = maths[i] if i < len(maths) and maths[i] else '<span class="miss">—</span>'
        rows.append(f'<tr><td class="idx">{i}</td><td class="o">{o}</td>'
                    f'<td class="s">{s}</td><td class="m">{m}</td></tr>')
    html = (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><h1>{key} — {n} formule (originale | SVG | MathML)</h1>'
            f'<table><thead><tr><th>#</th><th>Originale (PNG)</th><th>SVG</th>'
            f'<th>MathML</th></tr></thead><tbody>{"".join(rows)}</tbody></table></body></html>')
    (QA / f'{key}.html').write_text(html, encoding='utf-8')
    return n


def main():
    idx = ['<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{font:16px system-ui;padding:20px}a{display:block;padding:6px}</style></head><body><h1>QA comparison</h1>']
    for k in KEYS:
        n = build(k)
        idx.append(f'<a href="{k}.html">{k} — {n} formule</a>')
    idx.append('</body></html>')
    (QA / 'index.html').write_text('\n'.join(idx), encoding='utf-8')
    print('QA pages ->', QA)


if __name__ == '__main__':
    main()
