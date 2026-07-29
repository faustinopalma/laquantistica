"""Confronta formula per formula la resa attuale (MathJax) con quella di KaTeX.

Non basta sapere che KaTeX compila tutte le formule: bisogna vedere se le
disegna uguali. Questa pagina mette le due rese una accanto all'altra, con lo
stesso modo (in linea o a blocco) di come stanno nel capitolo, e misura lo
scarto di ciascuna così che le divergenze vere saltino fuori da sole.

    python tools/katex_compare.py publish/05-rutherford.html
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import index_page   # noqa: E402

OUT = Path('build/katexcheck')

PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>MathJax contro KaTeX · {name}</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<script>window.MathJax = {{
  svg: {{ fontCache: 'none' }},
  loader: {{ paths: {{ fonts: '../../publish/assets/mathjax/fonts' }} }},
  options: {{ ignoreHtmlClass: 'kx', enableMenu: false }}
}};</script>
<script defer src="../../publish/assets/mathjax/tex-mml-svg.js"></script>
<script defer src="node_modules/katex/dist/katex.min.js"></script>
<style>
body{{font:15px/1.6 Georgia,serif;margin:0;padding:0 16px 60px;background:#fff;color:#1c1c1c}}
h1{{font:600 14px ui-monospace,Consolas,monospace;background:#1c1c1c;color:#fff;
   margin:0 -16px 16px;padding:10px 16px;position:sticky;top:0;z-index:9}}
.r{{border-bottom:1px solid #eee;padding:8px 0;display:grid;
   grid-template-columns:46px 1fr 1fr;gap:12px;align-items:center}}
.r.big{{background:#fff6f6}}
.n{{font:11px ui-monospace,Consolas,monospace;color:#999}}
.mj,.kx{{min-width:0;overflow-x:auto}}
.kx{{border-left:1px solid #f0f0f0;padding-left:12px}}
.d{{font:11px ui-monospace,monospace;color:#c00}}
</style>
</head>
<body>
<h1>sinistra: MathJax (attuale) · destra: KaTeX — {name}</h1>
{items}
<script>
window.addEventListener('load', function () {{
  document.querySelectorAll('.kx').forEach(function (b) {{
    try {{
      katex.render(b.getAttribute('data-tex'), b, {{
        displayMode: b.getAttribute('data-display') === '1',
        throwOnError: false, strict: false
      }});
    }} catch (e) {{ b.textContent = 'ERRORE: ' + e.message; }}
  }});
  MathJax.startup.promise.then(function () {{
    setTimeout(function () {{
      var righe = [].map.call(document.querySelectorAll('.r'), function (r, i) {{
        var a = r.querySelector('.mj mjx-container'), b = r.querySelector('.kx .katex');
        if (!a || !b) return {{ i: i, mancante: !a ? 'mathjax' : 'katex' }};
        var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
        var dw = Math.abs(ra.width - rb.width) / Math.max(ra.width, 1);
        var dh = Math.abs(ra.height - rb.height) / Math.max(ra.height, 1);
        var d = Math.max(dw, dh);
        if (d > 0.25) r.classList.add('big');
        return {{ i: i, d: Math.round(d * 100),
                 mj: [Math.round(ra.width), Math.round(ra.height)],
                 kx: [Math.round(rb.width), Math.round(rb.height)] }};
      }});
      window.__c = {{
        righe: righe,
        rotte: document.querySelectorAll('.katex-error').length,
        erroriMathJax: document.querySelectorAll('[data-mml-node="merror"]').length
      }};
    }}, 500);
  }});
}});
</script>
</body>
</html>
"""


def build(path: Path) -> None:
    _src, _lang, formule = index_page(path)
    righe = []
    for i, f in enumerate(formule):
        mml = re.search(r'<math.*?</math>', f['raw'], re.S)
        if not mml:
            continue
        tex = html.escape(f['tex'], quote=True)
        righe.append(
            f'<div class="r"><span class="n">[{i}]</span>'
            f'<div class="mj">{mml.group(0)}</div>'
            f'<div class="kx" data-tex="{tex}" '
            f'data-display="{1 if f["display"] else 0}"></div></div>')
    OUT.mkdir(parents=True, exist_ok=True)
    nome = f'cmp-{path.stem}.html'
    (OUT / nome).write_text(PAGE.format(name=path.name, items='\n'.join(righe)),
                            encoding='utf-8')
    print(f'  build/katexcheck/{nome}  ({len(righe)} formule su {len(formule)})')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        build(Path(arg))
