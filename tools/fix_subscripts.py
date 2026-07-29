"""Ripristina i pedici persi nella traduzione inglese.

Nel capitolo 2 l'italiano scrive <em>m<sub>0</sub>=+k</em> mentre l'inglese ha il
testo appiattito, m0=+k: la traduzione e' stata scritta senza il marcatore di
pedice. Qui si riallinea l'inglese all'italiano.

La sostituzione tocca SOLO i nodi di testo: il sorgente viene spezzato sui tag,
cosi' non si rischia mai di modificare un attributo, un nome di tag o il MathML
di una formula.

    python tools/fix_subscripts.py            # anteprima
    python tools/fix_subscripts.py --write
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from edit_server import PUBLISH, index_page   # noqa: E402

PAGES = ('02-stern-gerlach-cascata.html',)
LANG = 'en'

# m seguito da un indice e, se c'e', dall'uguaglianza: m0=+k, mϑ=-k, m90=+k …
PAT = re.compile(
    r'(?<![\w])m(0|90|45|\u03D12|\u03D1|\u03C6|\u03D5|\u03B8)'
    r'(\s*=\s*[+\u2212-]?\s*k)?(?![\w])')


def fix_text(s: str) -> tuple[str, int]:
    n = 0

    def repl(m):
        nonlocal n
        n += 1
        tail = re.sub(r'\s+', '', m.group(2) or '')
        return f'<em>m<sub>{m.group(1)}</sub>{tail}</em>'

    return PAT.sub(repl, s), n


def fix_fragment(raw: str) -> tuple[str, int]:
    """Spezza sui tag e trasforma solo il testo."""
    parts = re.split(r'(<[^>]*>)', raw)
    total = 0
    for i in range(0, len(parts), 2):
        parts[i], n = fix_text(parts[i])
        total += n
    return ''.join(parts), total


def main() -> None:
    write = '--write' in sys.argv
    for name in PAGES:
        path = PUBLISH / name
        src, lang, _tex = index_page(path)
        rows = lang[LANG]
        pieces, pos, total, shown = [], 0, 0, 0
        for r in rows:
            new, n = fix_fragment(r['raw'])
            if n:
                total += n
                if shown < 4:
                    shown += 1
                    print(f'  riga {r["line"]}')
                    print(f'    prima : {re.sub(r"[ ]+", " ", r["raw"])[:150]}')
                    print(f'    dopo  : {re.sub(r"[ ]+", " ", new)[:150]}')
            pieces.append(src[pos:r['start']])
            pieces.append(new)
            pos = r['end']
        pieces.append(src[pos:])
        out = ''.join(pieces)
        print(f'{name}: {total} pedici ripristinati in <{LANG}>')
        if write:
            path.write_text(out, encoding='utf-8')
            print(f'  scritto {name}')
    if not write:
        print('\n(anteprima: usa --write per scrivere)')


if __name__ == '__main__':
    main()
