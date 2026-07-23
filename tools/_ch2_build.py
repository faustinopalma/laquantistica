import re, pathlib, difflib
from lxml import etree

root = pathlib.Path('.')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
xsl_path = r'C:\Program Files\Microsoft Office\root\Office16\OMML2MML.XSL'

doc = etree.parse(str(root/'build'/'ch2_document.xml'))
xslt = etree.XSLT(etree.parse(xsl_path))

# ordered walk: collect ('text', str) and ('math', element) in document order,
# NOT descending into oMath (so math text isn't counted as body text)
stream = []
def walk(el):
    for child in el:
        q = etree.QName(child)
        if q.namespace == M and q.localname == 'oMath':
            stream.append(('math', child))
        elif q.namespace == M and q.localname == 'oMathPara':
            walk(child)
        elif q.namespace == W and q.localname == 't':
            stream.append(('text', child.text or ''))
        elif q.namespace == W and q.localname in ('p','br','tab'):
            stream.append(('text', ' '))
            walk(child)
        else:
            walk(child)
walk(doc.getroot())

ws = re.compile(r'\s+')
def clean(s): return ws.sub(' ', s).strip()

# build math list with anchors
outdir = root/'build'/'ch2_mml2'
outdir.mkdir(parents=True, exist_ok=True)
for f in outdir.glob('*.mml'): f.unlink()

maths = [i for i,(k,_) in enumerate(stream) if k=='math']
omml = []  # (idx, before, after, mathml)
for n, si in enumerate(maths, 1):
    el = stream[si][1]
    res = xslt(el)
    mml = etree.tostring(res.getroot(), encoding='unicode')
    mml = re.sub(r'\s+xmlns:mml="[^"]*"','',mml)
    (outdir/f'{n:03}.mml').write_text(mml, encoding='utf-8')
    before = clean(''.join(t for k,t in stream[max(0,si-40):si] if k=='text'))[-70:]
    after  = clean(''.join(t for k,t in stream[si+1:si+41] if k=='text'))[:70]
    omml.append((n, before, after, mml))

# existing HTML formula images
exi = (root/'publish'/'leggi'/'02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
strip = re.compile(r'<[^>]+>')
def cleanh(s): return ws.sub(' ', strip.sub(' ', s)).strip()
imgre = re.compile(r'<img\b[^>]*?class="([^"]*)"[^>]*?src="img/pandoc_ch2/(image\d+\.svg)"[^>]*?>')
seen={}; order=[]; figs=set()
for m in imgre.finditer(exi):
    cls, src = m.group(1), m.group(2)
    if 'eq-figure' in cls: figs.add(src); continue
    if not ('eq-block' in cls or 'eq-inline' in cls): continue
    if src not in seen:
        be = cleanh(exi[max(0,m.start()-90):m.start()])[-70:]
        af = cleanh(exi[m.end():m.end()+90])[:70]
        seen[src]=(cls,be,af,m.start()); order.append(src)

def ratio(a,b): return difflib.SequenceMatcher(None,a,b).ratio()
rows=[]
for src in order:
    cls,be,af,pos = seen[src]
    best=(0,0)
    for (i,pb,pa,_) in omml:
        r = max(ratio(af,pa), ratio(be,pb), ratio(be+' '+af, pb+' '+pa))
        if r>best[0]: best=(r,i)
    rows.append((pos,src,cls,best[1],round(best[0],2),af))
rows.sort()
lines=[f'{src}\t{cls}\t->{idx:03}\tr={r}\t…{af[:44]}' for pos,src,cls,idx,r,af in rows]
(root/'build'/'ch2_final_map.tsv').write_text('\n'.join(lines), encoding='utf-8')
print(f'oMath transformed: {len(omml)}   formula-images: {len(order)}   diagrams kept: {len(figs)}')
print('diagrams:', ' '.join(sorted(figs,key=lambda s:int(re.search(r"\d+",s).group()))))
lo=[r for r in rows if r[4]<0.6]
print(f'low-confidence (<0.6): {len(lo)}  -> ' + ' '.join(r[1] for r in lo))
print('map -> build/ch2_final_map.tsv ; mathml -> build/ch2_mml2/')
