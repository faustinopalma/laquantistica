import pathlib
import re

RADICE = pathlib.Path('publish')

print('=== chi collega nota-02-prodotto-scalare.html ===')
for f in sorted(RADICE.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'nota-02-prodotto-scalare' in t and f.name != 'nota-02-prodotto-scalare.html':
        print(f'   {f.name}')

print('\n=== pagine collegate dal capitolo 2 ===')
t = pathlib.Path('publish/02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
visti = []
for m in re.finditer(r'href="((?:lab|nota)-[^"?#]+)', t):
    if m.group(1) not in visti:
        visti.append(m.group(1))
print('  ', ', '.join(visti))


def piano(s):
    s = re.sub(r'<span class="katex".*?</span></span></span>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


print('\n=== intestazioni delle pagine del capitolo 2 ===')
for n in ['02-stern-gerlach-cascata', 'lab-02a-sg-angolo-relativo', 'lab-02b-sg-tre-macchine',
          'lab-02c-sg-ricombinazione', 'lab-02d-sg-sfasamento', 'nota-02-prodotto-scalare']:
    print(f'--- {n} ---')
    print('   title attuale:', re.search(r'<title>(.*?)</title>',
          (RADICE / f'{n}.html').read_text(encoding='utf-8'), re.S).group(1).strip())
    for l in ('it', 'en'):
        s = (RADICE / 'v2' / l / f'{n}.html').read_text(encoding='utf-8')
        h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        if h:
            print(f'   [{l}] h1: {piano(h.group(1))[:100]}')
        else:
            m = re.search(r'<div class="tit"[^>]*>(.*?)</div>|<header[^>]*>(.*?)</header>', s, re.S)
            print(f'   [{l}] intestazione: {piano(m.group(0))[:120] if m else "(nessuna)"}')
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        if d and l == 'it':
            print(f'   descrizione IT: {d.group(1)}')
