"""Inventario dei simboli usati nel MathML del sito.

Uso:  python tools/math_inventory.py publish/*.html
Elenca i contenuti distinti di <mo>, <mi>, <mtext>, gli attributi usati e i tag,
in modo da costruire mappe di conversione complete invece che a tentoni.
"""
import glob
import re
import sys
from collections import Counter
from html import unescape
from pathlib import Path

MATH_RE = re.compile(r'<math\b.*?</math>', re.S)
LEAF_RE = re.compile(r'<(mo|mi|mn|mtext)\b([^>]*)>(.*?)</\1>', re.S)
TAG_RE = re.compile(r'<(m[a-z]+)\b([^>]*)>')
ATTR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')


def describe(ch: str) -> str:
    return ' '.join(f'U+{ord(c):04X}' for c in ch)


def main(patterns):
    leaves = {t: Counter() for t in ('mo', 'mi', 'mn', 'mtext')}
    attrs = Counter()
    tags = Counter()
    for pat in patterns:
        for f in glob.glob(pat):
            src = Path(f).read_text(encoding='utf-8')
            for m in MATH_RE.finditer(src):
                frag = m.group(0)
                for t, a, body in LEAF_RE.findall(frag):
                    leaves[t][unescape(body)] += 1
                for t, a in TAG_RE.findall(frag):
                    tags[t] += 1
                    for k, v in ATTR_RE.findall(a):
                        attrs[f'{t}@{k}={v}'] += 1

    for t in ('mo', 'mi', 'mtext', 'mn'):
        print(f'\n===== <{t}> — {len(leaves[t])} valori distinti =====')
        for val, n in leaves[t].most_common():
            if t == 'mn' and val.isdigit():
                continue
            print(f'{n:6d}  {val!r:28}  {describe(val)}')

    print('\n===== attributi =====')
    for k, n in attrs.most_common():
        print(f'{n:6d}  {k}')


if __name__ == '__main__':
    main(sys.argv[1:] or ['publish/*.html'])
