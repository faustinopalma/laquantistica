"""Genera la pagina di confronto fra le formule MathML originali e la loro
traduzione in LaTeX, per la verifica automatica e per la rilettura a occhio.

Uso:  python tools/math_compare.py publish/09-spettri-atomici.html
Produce build/mathcheck/<nome>.html : ogni formula compare due volte, a sinistra
il MathML di oggi, a destra il LaTeX nuovo, con il sorgente sotto.
Un piccolo script nella pagina misura le due rese e segnala quelle che
differiscono, cosi' la rilettura umana si concentra solo su quelle.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from math_extract import extract          # noqa: E402
from mml2tex import mml_to_tex, MathMLUnsupported   # noqa: E402

OUT_DIR = Path('build/mathcheck')

PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Confronto formule · {name}</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'none' }},
  startup: {{ typeset: true }}
}};
</script>
<script defer src="../../publish/assets/mathjax/tex-mml-svg.js"></script>
<style>
body{{font:14px/1.5 -apple-system,"Segoe UI",Roboto,sans-serif;margin:0;background:#f6f5f2;color:#1c1c1c}}
header{{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:10px 18px;z-index:5;
  display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}}
h1{{font-size:16px;margin:0}}
#sum{{font-family:ui-monospace,Consolas,monospace;font-size:13px}}
#sum b{{color:#a33}}
label{{font-size:13px;color:#555}}
.item{{background:#fff;border:1px solid #e2e0dc;border-radius:6px;margin:14px 18px;overflow:hidden}}
.item.diff{{border-color:#d08a2a;box-shadow:0 0 0 2px rgba(208,138,42,.18)}}
.item.err{{border-color:#c0392b;box-shadow:0 0 0 2px rgba(192,57,43,.18)}}
.hd{{display:flex;gap:14px;align-items:baseline;padding:6px 12px;background:#faf9f7;
  border-bottom:1px solid #eee;font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#666}}
.hd .n{{font-weight:700;color:#1c1c1c}}
.hd .tag{{margin-left:auto}}
.cols{{display:grid;grid-template-columns:1fr 1fr}}
.cell{{padding:14px 16px;min-width:0;overflow-x:auto}}
.cell+.cell{{border-left:1px dashed #e2e0dc}}
.cap{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#999;margin-bottom:8px}}
pre{{margin:0;padding:10px 16px;background:#fbfaf8;border-top:1px solid #f0eeea;
  font-family:ui-monospace,Consolas,monospace;font-size:12px;white-space:pre-wrap;word-break:break-word;color:#444}}
pre.tex{{color:#1a4d7a}}
.hide .item:not(.diff):not(.err){{display:none}}
</style>
</head>
<body class="">
<header>
  <h1>Confronto formule · {name}</h1>
  <span id="sum">misuro…</span>
  <label><input type="checkbox" id="only"> mostra solo quelle da rivedere</label>
</header>
<div id="list">
{items}
</div>
<script>
var DATA = {data};
document.getElementById('only').addEventListener('change', function(){{
  document.body.classList.toggle('hide', this.checked);
}});
function box(el){{
  var c = el.querySelector('mjx-container');
  if(!c) return null;
  var r = c.getBoundingClientRect();
  return {{w: r.width, h: r.height}};
}}
function check(){{
  var diff = 0, err = 0;
  document.querySelectorAll('.item').forEach(function(it){{
    var a = box(it.querySelector('.old')), b = box(it.querySelector('.new'));
    var tag = it.querySelector('.tag');
    if(it.querySelector('.new [data-mml-node="merror"], .new mjx-merror') || !b){{ it.classList.add('err'); tag.textContent = 'ERRORE LaTeX'; err++; return; }}
    if(!a){{ it.classList.add('err'); tag.textContent = 'MathML non reso'; err++; return; }}
    var dw = Math.abs(a.w-b.w)/Math.max(a.w,1), dh = Math.abs(a.h-b.h)/Math.max(a.h,1);
    var d = Math.max(dw, dh);
    tag.textContent = 'scarto ' + (100*d).toFixed(1) + '%';
    if(d > 0.08){{ it.classList.add('diff'); diff++; }}
  }});
  var n = document.querySelectorAll('.item').length;
  document.getElementById('sum').innerHTML =
    n + ' formule · <b>' + err + '</b> errori · <b>' + diff + '</b> con resa diversa · ' +
    (n-err-diff) + ' identiche';
  window.__check = {{n: n, err: err, diff: diff}};
}}
// MathJax e' caricato con defer, quindi qui startup puo' non esistere ancora:
// aspetto che i contenitori compaiano invece di fidarmi di un solo evento.
(function wait(n){{
  var want = document.querySelectorAll('.item').length * 2;
  if (document.querySelectorAll('mjx-container').length >= want || n > 200) {{
    setTimeout(check, 150);
  }} else {{
    setTimeout(function(){{ wait(n + 1); }}, 100);
  }}
}})(0);
</script>
</body>
</html>
"""

ITEM = """<div class="item" id="f{i}">
  <div class="hd"><span class="n">[{i}]</span><span>riga {line}</span><span>{display}</span>
    <span>{wrap}</span><span class="tag">…</span></div>
  <div class="cols">
    <div class="cell"><div class="cap">MathML attuale</div><div class="old">{old}</div></div>
    <div class="cell"><div class="cap">LaTeX nuovo</div><div class="new">{new}</div></div>
  </div>
  <pre class="tex">{tex}</pre>
</div>"""


def build(path: Path) -> Path:
    _, items = extract(path)
    blocks, data = [], []
    for it in items:
        try:
            tex, unknown = mml_to_tex(it['src'], f'{path.name}[{it["i"]}]')
            err = '; '.join(unknown)
        except MathMLUnsupported as e:
            tex, err = '', str(e)
        delim = ('\\[', '\\]') if it['display'] == 'block' else ('\\(', '\\)')
        rendered = f'{delim[0]}{tex}{delim[1]}' if tex else '(conversione fallita)'
        blocks.append(ITEM.format(
            i=it['i'], line=it['line'], display=it['display'],
            wrap=html.escape(it['wrap']),
            old=it['src'], new=html.escape(rendered),
            tex=html.escape(tex + (('\n⚠ ' + err) if err else '')),
        ))
        data.append({'i': it['i'], 'tex': tex, 'err': err,
                     'display': it['display'], 'line': it['line']})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / (path.stem + '.html')
    out.write_text(PAGE.format(name=path.name, items='\n'.join(blocks),
                               data=json.dumps(data, ensure_ascii=False)),
                   encoding='utf-8')
    (OUT_DIR / (path.stem + '.json')).write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return out


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        p = build(Path(arg))
        print(f'{arg} -> {p}')
