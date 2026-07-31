import pathlib
import re

for n in ['nota-01-stern-gerlach', 'nota-tecnica-01-stern-gerlach', 'lab-01-stern-gerlach']:
    s = (pathlib.Path('publish') / f'{n}.html').read_text(encoding='utf-8')
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    print(n)
    print('   ', m.group(1) if m else '(nessuna)')
    print()
