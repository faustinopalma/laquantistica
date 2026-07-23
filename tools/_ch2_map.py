import re, pathlib, difflib
root = pathlib.Path('.')
pan = (root/'build'/'ch2_from_docx.html').read_text(encoding='utf-8')
exi = (root/'publish'/'leggi'/'02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
strip = re.compile(r'<[^>]+>')
ws = re.compile(r'\s+')
def clean(s): return ws.sub(' ', strip.sub(' ', s)).strip()

# pandoc math blocks with anchors
tag = re.compile(r'<math\b.*?</math>', re.DOTALL)
pmath = []
for i, m in enumerate(tag.finditer(pan), 1):
    before = clean(pan[max(0,m.start()-90):m.start()])[-70:]
    after = clean(pan[m.end():m.end()+90])[:70]
    pmath.append((i, before, after))

# existing formula images (eq-block/eq-inline, not eq-figure)
imgre = re.compile(r'<img\b[^>]*?class="([^"]*)"[^>]*?src="img/pandoc_ch2/(image\d+\.svg)"[^>]*?>')
seen = {}
order = []
figs = set()
for m in imgre.finditer(exi):
    cls, src = m.group(1), m.group(2)
    if 'eq-figure' in cls:
        figs.add(src); continue
    if not ('eq-block' in cls or 'eq-inline' in cls):
        continue
    if src not in seen:
        before = clean(exi[max(0,m.start()-90):m.start()])[-70:]
        after = clean(exi[m.end():m.end()+90])[:70]
        seen[src] = (cls, before, after, m.start())
        order.append(src)

def ratio(a,b): return difflib.SequenceMatcher(None,a,b).ratio()
rows=[]
for src in order:
    cls, be, af, pos = seen[src]
    best=(0,0)
    for (i,pb,pa) in pmath:
        r = max(ratio(af,pa), ratio(be,pb), ratio(be+' '+af, pb+' '+pa))
        if r>best[0]: best=(r,i)
    rows.append((pos, src, cls, best[1], round(best[0],2), be, af))

rows.sort()
out=[]
for pos,src,cls,idx,r,be,af in rows:
    lx = ''
    idxfile = root/'build'/'ch2_mml'/f'{idx:03}.mml'
    la = re.search(r'<annotation encoding="application/x-tex">(.*?)</annotation>', (root/'build'/'ch2_from_docx.html').read_text(encoding='utf-8'))
    out.append(f'{src}\t{cls}\t->{idx:03}\tr={r}\t…{af[:46]}')
(root/'build'/'ch2_imgmap.tsv').write_text('\n'.join(out), encoding='utf-8')
print(f'distinct formula images: {len(order)}   |   eq-figure (kept as img): {len(figs)}')
print('kept diagrams:', ' '.join(sorted(figs, key=lambda s:int(re.search(r"\d+",s).group()))))
print('map -> build/ch2_imgmap.tsv')
lo=[r for r in rows if r[4]<0.55]
print(f'low-confidence (<0.55): {len(lo)}')
