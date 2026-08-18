"""Controlla che ogni link etichettato con un numero punti al capitolo di quel numero."""
import pathlib
import re
import sys

sys.path.insert(0, 'build')
from ordine_schede import SCHEDE  # noqa: E402

posizione = {slug: n for n, (slug, _, _) in enumerate(SCHEDE, 1)}
LINK = re.compile(
    r'href="([0-9][^"?#]*?)(?:\.html)?(?:[#?][^"]*)?"[^>]*>'
    r'((?:(?!</a>).)*?)(?:Cap\.|Ch\.|Capitolo|Chapter)\s+0?(\d+)', re.S)

guasti = []
pagine = sorted(pathlib.Path('publish/it').glob('*.html'))
pagine += sorted(pathlib.Path('publish/en').glob('*.html'))
for p in pagine:
    for slug, _, n in LINK.findall(p.read_text(encoding='utf-8')):
        slug += '.html'
        if slug in posizione and posizione[slug] != int(n):
            guasti.append(f'{p.parent.name}/{p.name}: {slug} etichettato {n}, '
                          f'e\u0300 il {posizione[slug]}')

print('\n'.join(guasti) if guasti else
      f'link numerati coerenti in {len(pagine)} pagine')
