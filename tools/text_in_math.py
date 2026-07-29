"""Trova le formule che contengono testo in una lingua, non notazione.

Uso:  python tools/text_in_math.py
Elenca ogni \\text{...} dentro un data-tex, con pagina, riga, il LaTeX completo e
la frase che circonda la formula, per decidere caso per caso se quel testo debba
restare notazione (unita' di misura, dominio di integrazione, nome di una
grandezza) oppure uscire dalla formula e diventare prosa.
"""
from __future__ import annotations

import html
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import index_page, PUBLISH   # noqa: E402

TEXT_RE = re.compile(r'\\text\{([^{}]*)\}')
TAG = re.compile(r'<[^>]+>')


def context(src: str, start: int, end: int, span: int = 260) -> tuple[str, str]:
    before = TAG.sub(' ', src[max(0, start - span):start])
    after = TAG.sub(' ', src[end:end + span])
    norm = lambda s: re.sub(r'\s+', ' ', html.unescape(s)).strip()
    return norm(before)[-140:], norm(after)[:140]


def main() -> None:
    words = Counter()
    total = 0
    for path in sorted(PUBLISH.glob('*.html')):
        src, _lang, tex = index_page(path)
        hits = [t for t in tex if TEXT_RE.search(t['tex'])]
        if not hits:
            continue
        print(f'\n{"=" * 78}\n{path.name} — {len(hits)} formule con testo dentro\n{"=" * 78}')
        for t in hits:
            total += 1
            for w in TEXT_RE.findall(t['tex']):
                words[w.strip()] += 1
            b, a = context(src, t['start'], t['end'])
            print(f'\n  riga {t["line"]}  ({"blocco" if t["display"] else "in linea"})')
            print(f'    …{b}')
            print(f'    LATEX: {t["tex"]}')
            print(f'    {a}…')

    print(f'\n\n{"=" * 78}\nRIEPILOGO — {total} formule contengono testo\n{"=" * 78}')
    for w, n in words.most_common():
        print(f'{n:4d}  {w!r}')


if __name__ == '__main__':
    main()
