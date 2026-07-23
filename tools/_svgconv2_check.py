import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
ch = '02-stern-gerlach-cascata'
svg = (ROOT/f'site/svg/{ch}.html').read_text(encoding='utf-8')
pub = (ROOT/f'publish/{ch}.html').read_text(encoding='utf-8')

def body(html):
    m = re.search(r'<article\b[^>]*>(.*)</article>', html, re.DOTALL)
    return m.group(1) if m else html

BLOCK = re.compile(r'<figure\b.*?</figure>|<div class="equation">.*?</div>|<p\b.*?</p>|<h2\b.*?</h2>|<h3\b.*?</h3>|<hr\b[^>]*/?>|<nav\b.*?</nav>', re.DOTALL)

def blocks(html):
    return [m.group(0) for m in BLOCK.finditer(body(html))]

def kind(b):
    if b.startswith('<figure'): return 'fig'
    if b.startswith('<div'): return 'div'
    if b.startswith('<p'): return 'p'
    if b.startswith('<h2'): return 'h2'
    if b.startswith('<h3'): return 'h3'
    if b.startswith('<hr'): return 'hr'
    if b.startswith('<nav'): return 'nav'
    return '?'

def strip(s):
    s = re.sub(r'<math\b.*?</math>', ' ', s, flags=re.DOTALL)
    s = re.sub(r'<img\b[^>]*>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def it_text(b):
    # for pub blocks: take the it-span text; for svg: whole
    m = re.search(r'<span class="it">(.*?)</span>', b, re.DOTALL)
    return strip(m.group(1) if m else b)

sb = blocks(svg); pb = blocks(pub)
print(f'svg blocks={len(sb)}  pub blocks={len(pb)}')
n = max(len(sb), len(pb))
mism = 0
for i in range(n):
    s = sb[i] if i < len(sb) else ''
    p = pb[i] if i < len(pb) else ''
    ks = kind(s) if s else '--'
    kp = kind(p) if p else '--'
    ts = strip(s)[:34]
    tp = it_text(p)[:34]
    ok = (ks == kp) and (ts[:20] == tp[:20])
    if not ok:
        mism += 1
        if mism <= 25:
            print(f'{i:3} MISMATCH  svg[{ks}]:{ts:<36} | pub[{kp}]:{tp}')
print(f'blocchi disallineati = {mism}')
