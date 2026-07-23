import pathlib
ovr = pathlib.Path('build/ch2_overrides')
rows = ['image47','image28','image50','image103','image129','image90']
parts = ["""<!doctype html><html><head><meta charset='utf-8'><style>
body{font-family:sans-serif;background:#fff;margin:16px}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid #ccc;padding:10px;vertical-align:middle}
th{background:#eef}
td.svg img{max-height:80px}
math{font-size:1.4rem}
.n{font:12px monospace;color:#555}
</style></head><body>
<h3>Confronto: SVG originale (sinistra) &harr; MathML convertito (destra)</h3>
<table><tr><th>#</th><th>SVG originale</th><th>MathML (nuovo)</th></tr>"""]
for n in rows:
    svg = f'../publish/leggi/img/pandoc_ch2/{n}.svg'
    mml = (ovr/f'{n}.svg.mml').read_text(encoding='utf-8').strip()
    parts.append(f"<tr><td class='n'>{n}</td><td class='svg'><img src='{svg}'></td><td>{mml}</td></tr>")
parts.append("</table></body></html>")
out = pathlib.Path('build/ch2_compare.html')
out.write_text('\n'.join(parts), encoding='utf-8')
print('wrote', out)
