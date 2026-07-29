"""Costruisce una pagina di prova con KaTeX a partire dalle formule di una pagina
del sito, per confrontarla con quella resa da MathJax.

Legge il LaTeX da data-tex, che è la sorgente da cui tutto viene rigenerato.

    python tools/katex_page.py publish/05-rutherford.html
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

OUT = Path('build/katexcheck')

PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>KaTeX · {name}</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<script defer src="node_modules/katex/dist/katex.min.js"></script>
<style>
body{{font:16px/1.6 Georgia,serif;margin:0;padding:0 24px 40px;background:#fff;color:#1c1c1c;max-width:900px}}
h1{{font:600 15px ui-monospace,Consolas,monospace;background:#1c1c1c;color:#fff;margin:0 -24px 20px;padding:10px 24px}}
.f{{border-bottom:1px solid #eee;padding:10px 0;display:flex;gap:14px;align-items:baseline}}
.n{{font:11px ui-monospace,Consolas,monospace;color:#aaa;flex:0 0 44px}}
.b{{flex:1;min-width:0;overflow-x:auto}}
</style>
</head>
<body>
<h1>KaTeX — {name}</h1>
{items}
<script>
window.addEventListener('load', function () {{
  var t0 = performance.now();
  var errori = 0;
  document.querySelectorAll('.b').forEach(function (b) {{
    try {{
      katex.render(b.getAttribute('data-tex'), b, {{ displayMode: true, throwOnError: false, strict: false }});
    }} catch (e) {{ errori++; }}
  }});
  window.__k = {{
    ms: Math.round(performance.now() - t0),
    errori: errori,
    rotte: document.querySelectorAll('.katex-error').length,
    misure: [].map.call(document.querySelectorAll('.b .katex'), function (c) {{
      var r = c.getBoundingClientRect();
      return [Math.round(r.width * 10) / 10, Math.round(r.height * 10) / 10];
    }})
  }};
}});
</script>
</body>
</html>
"""


def build(path: Path) -> None:
    src = path.read_text(encoding='utf-8')
    tex = re.findall(r'data-tex="([^"]*)"', src)
    items = '\n'.join(
        f'<div class="f"><span class="n">[{i}]</span>'
        f'<span class="b" data-tex="{t}"></span></div>'
        for i, t in enumerate(tex))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'katex.html').write_text(
        PAGE.format(name=path.name, items=items), encoding='utf-8')
    print(f'  build/katexcheck/katex.html  ({len(tex)} formule)')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        build(Path(arg))
