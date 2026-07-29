"""Estrae le formule MathML di una pagina, con il contesto che le avvolge.

Uso:  python tools/math_extract.py publish/09-spettri-atomici.html
Stampa un elenco numerato: indice, display, classi del contenitore, sorgente.
"""
import re
import sys
from pathlib import Path

MATH_RE = re.compile(r'<math\b.*?</math>', re.S)


def wrapper_of(src: str, start: int) -> str:
    """Classi del <span>/<div> che avvolge immediatamente la formula."""
    head = src[max(0, start - 400):start]
    m = None
    for m in re.finditer(r'<(?:span|div)[^>]*class="([^"]*)"[^>]*>', head):
        pass
    return m.group(1) if m else ''


def extract(path: Path):
    src = path.read_text(encoding='utf-8')
    out = []
    for i, m in enumerate(MATH_RE.finditer(src)):
        frag = m.group(0)
        out.append({
            'i': i,
            'start': m.start(),
            'line': src.count('\n', 0, m.start()) + 1,
            'display': 'block' if 'display="block"' in frag else 'inline',
            'wrap': wrapper_of(src, m.start()),
            'src': frag,
        })
    return src, out


if __name__ == '__main__':
    p = Path(sys.argv[1])
    _, items = extract(p)
    print(f'{p.name}: {len(items)} formule')
    for it in items:
        print(f'\n--- [{it["i"]}] riga {it["line"]} · {it["display"]} · wrap="{it["wrap"]}"')
        print(it['src'])
