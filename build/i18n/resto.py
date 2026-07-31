import pathlib
import re

RADICE = pathlib.Path('publish')

RESTANTI = ['03-elettroni', '04-diffrazione', '05-rutherford', '06-ulteriori-sviluppi',
            '07-franck-hertz', '08-effetto-fotoelettrico', '09-spettri-atomici',
            'lab-03a-corrente-vuoto', 'lab-03b-deflessione-em', 'lab-03c-millikan',
            'lab-04-diffrazione', 'lab-05-rutherford', 'lab-07-franck-hertz',
            'lab-08-fotoelettrico', 'lab-09-spettri']


def piano(s):
    s = re.sub(r'<span class="katex-mathml">.*?</math></span>', '', s, flags=re.S)
    s = re.sub(r'<span class="katex-html".*?</span></span></span>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


for n in RESTANTI:
    t = (RADICE / f'{n}.html').read_text(encoding='utf-8')
    print(f'--- {n} ---')
    print('  title:', re.search(r'<title>(.*?)</title>', t, re.S).group(1).strip())
    d = re.search(r'<meta name="description" content="([^"]*)"', t)
    if d:
        print('  descr IT:', d.group(1))
    for l in ('it', 'en'):
        s = (RADICE / 'v2' / l / f'{n}.html').read_text(encoding='utf-8')
        h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        if h:
            print(f'  [{l}] h1: {piano(h.group(1))[:95]}')
        else:
            m = re.search(r'<div class="tit"[^>]*>(.*?)</div>', s, re.S) or re.search(r'<header[^>]*>(.*?)</header>', s, re.S)
            print(f'  [{l}] intestazione: {piano(m.group(1))[:110] if m else "(nessuna)"}')

print('\n=== etichette delle note da tradurre ===')
for n in ['nota-01-stern-gerlach', 'nota-02-prodotto-scalare', 'nota-tecnica-01-stern-gerlach']:
    t = (RADICE / f'{n}.html').read_text(encoding='utf-8')
    print(f'--- {n} ---')
    for pat in (r'<span class="tag[^"]*">[^<]*</span>', r'<div class="doc-foot".*?</div>',
                r'class="sep">[^<]*</span>', r'<span class="k">[^<]*</span>'):
        for m in re.finditer(pat, t, re.S):
            print('   ', m.group(0)[:190].replace('\n', ' '))
