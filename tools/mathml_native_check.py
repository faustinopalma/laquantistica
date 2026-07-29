"""Confronta il MathML reso da MathJax con quello reso dal browser da solo.

Serve a decidere se si puo' smettere di caricare MathJax (2 MB, 614 kB
trasferiti) lasciando che sia il browser a rendere il MathML gia' presente nelle
pagine. Il LaTeX in data-tex resta comunque: e' la sorgente e non si tocca.

Genera build/mathnative/<pagina>.html con ogni formula due volte, a sinistra
MathJax e a destra il rendering nativo (ottenuto dicendo a MathJax di ignorare
quella parte della pagina con ignoreHtmlClass). Misura da sola lo scarto.

    python tools/mathml_native_check.py publish/05-rutherford.html
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import index_page   # noqa: E402

OUT_DIR = Path('build/mathnative')

PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>MathJax contro MathML nativo · {name}</title>
<script>
window.MathJax = {{
  options: {{ ignoreHtmlClass: 'nomj' }},
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
.item.bad{{border-color:#c0392b;box-shadow:0 0 0 2px rgba(192,57,43,.20)}}
.hd{{display:flex;gap:14px;align-items:baseline;padding:6px 12px;background:#faf9f7;
  border-bottom:1px solid #eee;font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#666}}
.hd .n{{font-weight:700;color:#1c1c1c}} .hd .tag{{margin-left:auto}}
.cols{{display:grid;grid-template-columns:1fr 1fr}}
.cell{{padding:16px;min-width:0;overflow-x:auto}}
.cell+.cell{{border-left:1px dashed #e2e0dc;background:#fcfcfa}}
.cap{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#999;margin-bottom:10px}}
.nat math{{font-size:1.05em}}
pre{{margin:0;padding:9px 16px;background:#fbfaf8;border-top:1px solid #f0eeea;
  font-family:ui-monospace,Consolas,monospace;font-size:12px;white-space:pre-wrap;color:#1a4d7a}}
.hide .item:not(.diff):not(.bad){{display:none}}
</style>
</head>
<body>
<header>
  <h1>MathJax contro MathML nativo · {name}</h1>
  <span id="sum">misuro…</span>
  <label><input type="checkbox" id="only"> mostra solo quelle che differiscono</label>
</header>
<div id="list">
{items}
</div>
<script>
document.getElementById('only').addEventListener('change', function(){{
  document.body.classList.toggle('hide', this.checked);
}});
function box(el){{ var r = el.getBoundingClientRect(); return {{w:r.width, h:r.height}}; }}
function check(){{
  var diff = 0, bad = 0, tot = 0, somma = 0;
  document.querySelectorAll('.item').forEach(function(it){{
    var a = it.querySelector('.mj mjx-container'), b = it.querySelector('.nat math');
    var tag = it.querySelector('.tag');
    if(!a || !b){{ it.classList.add('bad'); tag.textContent = 'non reso'; bad++; return; }}
    var A = box(a), B = box(b);
    var dw = Math.abs(A.w-B.w)/Math.max(A.w,1), dh = Math.abs(A.h-B.h)/Math.max(A.h,1);
    var d = Math.max(dw, dh); tot++; somma += d;
    tag.textContent = 'scarto ' + (100*d).toFixed(0) + '%  ·  h ' + A.h.toFixed(0) + ' → ' + B.h.toFixed(0);
    if(d > 0.25){{ it.classList.add('bad'); bad++; }}
    else if(d > 0.08){{ it.classList.add('diff'); diff++; }}
  }});
  var n = document.querySelectorAll('.item').length;
  document.getElementById('sum').innerHTML =
    n + ' formule · <b>' + bad + '</b> molto diverse · <b>' + diff + '</b> diverse · ' +
    (n-bad-diff) + ' equivalenti · scarto medio ' + (100*somma/Math.max(tot,1)).toFixed(1) + '%';
  window.__nat = {{n:n, bad:bad, diff:diff, medio:somma/Math.max(tot,1)}};
}}
(function wait(k){{
  var want = document.querySelectorAll('.item').length;
  if (document.querySelectorAll('.mj mjx-container').length >= want || k > 300) setTimeout(check, 200);
  else setTimeout(function(){{ wait(k+1); }}, 100);
}})(0);
</script>
</body>
</html>
"""

ITEM = """<div class="item" id="f{i}">
  <div class="hd"><span class="n">[{i}]</span><span>riga {line}</span><span>{display}</span><span class="tag">…</span></div>
  <div class="cols">
    <div class="cell"><div class="cap">MathJax · come è oggi</div><div class="mj">{mml}</div></div>
    <div class="cell nomj"><div class="cap">MathML nativo · senza MathJax</div><div class="nat">{mml}</div></div>
  </div>
  <pre>{tex}</pre>
</div>"""


def build(path: Path) -> Path:
    _src, _lang, tex = index_page(path)
    blocks = []
    for i, t in enumerate(tex):
        blocks.append(ITEM.format(i=i, line=t['line'],
                                  display='blocco' if t['display'] else 'in linea',
                                  mml=t['raw'], tex=html.escape(t['tex'][:400])))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / (path.stem + '.html')
    out.write_text(PAGE.format(name=path.name, items='\n'.join(blocks)), encoding='utf-8')
    return out


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(f'{arg} -> {build(Path(arg))}')
