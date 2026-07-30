import pathlib
import re

# lang.js deve girare PRIMA del disegno, altrimenti l'italiano appare dopo un lampo d'inglese
vecchio = re.compile(r'<script\s+defer\s+src="assets/lang\.js\?v=\d+"></script>')
nuovo = '<script src="assets/lang.js?v=6"></script>'

pub = pathlib.Path('publish')
tocchi = []
for f in sorted(pub.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    t2, n = vecchio.subn(nuovo, t)
    if n:
        f.write_text(t2, encoding='utf-8')
        tocchi.append((f.name, n))

for nome, n in tocchi:
    print(f'{nome}: {n}')
print(f'totale pagine: {len(tocchi)}')

restanti = [f.name for f in sorted(pub.glob('*.html')) if 'lang.js' in f.read_text(encoding='utf-8') and 'lang.js?v=6' not in f.read_text(encoding='utf-8')]
print('non aggiornate:', restanti or 'nessuna')
