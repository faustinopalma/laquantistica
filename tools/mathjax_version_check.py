"""Confronta la resa di due versioni di MathJax sulle stesse formule.

Genera due pagine identiche, una che carica la versione attualmente in uso e una
che carica quella nuova, per misurare se aggiornare cambierebbe l'aspetto delle
formule — e quanto.

    python tools/mathjax_version_check.py publish/05-rutherford.html
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import index_page   # noqa: E402

OUT = Path('build/mjcheck')

PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>MathJax {ver} · {name}</title>
<script>window.MathJax = {{ svg: {{ fontCache: 'none' }} }};</script>
<script defer src="{src}"></script>
<style>
body{{font:16px/1.6 Georgia,serif;margin:0;padding:0 24px 40px;background:#fff;color:#1c1c1c;max-width:900px}}
h1{{font:600 15px ui-monospace,Consolas,monospace;background:#1c1c1c;color:#fff;margin:0 -24px 20px;padding:10px 24px}}
.f{{border-bottom:1px solid #eee;padding:10px 0;display:flex;gap:14px;align-items:baseline}}
.n{{font:11px ui-monospace,Consolas,monospace;color:#aaa;flex:0 0 44px}}
.b{{flex:1;min-width:0;overflow-x:auto}}
</style>
</head>
<body>
<h1>MathJax {ver} — {name}</h1>
{items}
<script>
(function wait(k){{
  var want = document.querySelectorAll('.f').length;
  if (document.querySelectorAll('mjx-container').length >= want || k > 400) {{
    setTimeout(function(){{
      window.__m = [].map.call(document.querySelectorAll('.b mjx-container'), function(c){{
        var r = c.getBoundingClientRect();
        return [Math.round(r.width*10)/10, Math.round(r.height*10)/10];
      }});
    }}, 300);
  }} else setTimeout(function(){{ wait(k+1); }}, 100);
}})(0);
</script>
</body>
</html>
"""


def build(path: Path) -> None:
    _src, _lang, tex = index_page(path)
    items = '\n'.join(
        f'<div class="f"><span class="n">[{i}]</span><span class="b">{t["raw"]}</span></div>'
        for i, t in enumerate(tex))
    OUT.mkdir(parents=True, exist_ok=True)
    for ver, src in (('3.2.2 (in uso)', '../../publish/assets/mathjax/tex-mml-svg.js'),
                     ('4.1.3 (nuova)', 'node_modules/mathjax/tex-mml-svg.js')):
        tag = ver.split()[0].replace('.', '')
        (OUT / f'v{tag}.html').write_text(
            PAGE.format(ver=ver, name=path.name, src=src, items=items), encoding='utf-8')
        print(f'  build/mjcheck/v{tag}.html')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(arg)
        build(Path(arg))
