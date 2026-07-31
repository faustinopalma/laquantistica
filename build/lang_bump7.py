import pathlib
import re

vecchio = re.compile(r'<script src="assets/lang\.js\?v=\d+"></script>')
nuovo = '<script src="assets/lang.js?v=7"></script>'

pub = pathlib.Path('publish')
n_tot = 0
for f in sorted(pub.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    t2, n = vecchio.subn(nuovo, t)
    if n:
        f.write_text(t2, encoding='utf-8')
        n_tot += n

print(f'pagine aggiornate: {n_tot}')
restanti = [f.name for f in sorted(pub.glob('*.html'))
            if 'lang.js' in f.read_text(encoding='utf-8')
            and 'lang.js?v=7' not in f.read_text(encoding='utf-8')]
print('non aggiornate:', restanti or 'nessuna')
