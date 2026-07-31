"""Dettagli che lo splitter deve gestire: description, img bilingui, forma dei path."""
import collections
import pathlib
import re

PAGINE = sorted(pathlib.Path('publish').glob('*.html'))

print('=== <meta name="description"> ===')
for p in PAGINE:
    t = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<meta\s+name="description"[^>]*>', t):
        print(f'  {p.name}: {m.group(0)[:150]}')

print('\n=== <img> con classe di lingua ===')
for p in PAGINE:
    t = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<img[^>]*class="(?:it|en)"[^>]*>', t):
        print(f'  {p.name}: {m.group(0)[:120]}')

print('\n=== forma dei riferimenti ad assets/ e img/ ===')
forme = collections.Counter()
for p in PAGINE:
    t = p.read_text(encoding='utf-8')
    for m in re.finditer(r'(?:src|href)="([^"]+)"', t):
        u = m.group(1)
        if re.match(r'^(https?:|mailto:|#|data:)', u):
            continue
        forme[u.split('/')[0] + '/' if '/' in u else '(file nella stessa cartella)'] += 1
for k, v in forme.most_common():
    print(f'  {k:<30} {v}')

print('\n=== url(...) dentro CSS inline ===')
u = collections.Counter()
for p in PAGINE:
    for m in re.finditer(r'url\(([^)]*)\)', p.read_text(encoding='utf-8')):
        u[m.group(1)] += 1
print('  ', dict(u) or 'nessuno')

print('\n=== span di lingua ANNIDATI in 06 ===')
t = pathlib.Path('publish/06-ulteriori-sviluppi.html').read_text(encoding='utf-8')
for m in re.finditer(r'<span class="(it|en)">(?:(?!</?span).)*<span class="(it|en)">', t):
    i = m.start()
    print(f'  offset {i}: ...{t[max(0,i-60):i+160]}...')
    break
n = len(re.findall(r'<span class="(?:it|en)"[^>]*>[^<]*<span class="(?:it|en)"', t))
print(f'  occorrenze dirette annidate: {n}')
