"""Sostituisce il caricamento di MathJax con il foglio di stile di KaTeX.

Con le formule pre-generate non c'e' piu' nulla da eseguire nel browser: resta
solo il foglio di stile che dice come disporle e quali caratteri usare.

    python tools/katex_head.py publish/*.html
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCCO = re.compile(
    r'[ \t]*<script>\s*\nwindow\.MathJax = \{.*?\};\s*\n</script>\s*\n'
    r'[ \t]*<script defer src="assets/mathjax/tex-mml-svg\.js[^"]*"></script>\s*\n',
    re.S)

CSS = '<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">\n'


def fix(path: Path) -> str:
    src = path.read_text(encoding='utf-8')
    if 'assets/katex/katex.min.css' in src:
        return 'gia\' fatta'
    if not BLOCCO.search(src):
        return 'ATTENZIONE: blocco MathJax non riconosciuto'
    out = BLOCCO.sub(CSS, src, count=1)
    path.write_text(out, encoding='utf-8', newline='')
    return 'convertita'


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        p = Path(arg)
        print(f'{p.name:38} {fix(p)}')
