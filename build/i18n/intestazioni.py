import pathlib
import re


def testo_piano(s):
    s = re.sub(r'<span class="katex-mathml">.*?</span></span>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()


for n in ['nota-01-stern-gerlach', 'nota-tecnica-01-stern-gerlach', 'lab-01-stern-gerlach', 'index', '01-stern-gerlach']:
    print(f'--- {n} ---')
    for l in ('it', 'en'):
        t = (pathlib.Path('publish/v2') / l / f'{n}.html').read_text(encoding='utf-8')
        h = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
        intestazione = testo_piano(h.group(1)) if h else None
        if not intestazione:
            m = re.search(r'<header[^>]*>(.*?)</header>', t, re.S)
            intestazione = testo_piano(m.group(1))[:120] if m else '(nessuna)'
        d = re.search(r'<meta name="description" content="([^"]*)"', t)
        print(f'  [{l}] h1: {intestazione[:110]}')
        if d:
            print(f'       descr: {d.group(1)[:130]}')
