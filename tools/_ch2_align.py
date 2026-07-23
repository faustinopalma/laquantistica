import re, pathlib, difflib
from lxml import etree

root = pathlib.Path('.')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# ---- ordered stream of (text|math) from the docx ----
doc = etree.parse(str(root/'build'/'ch2_document.xml'))
stream = []
def walk(el):
    for child in el:
        q = etree.QName(child)
        if q.namespace == M and q.localname == 'oMath':
            stream.append(('math', child)); 
        elif q.namespace == M and q.localname == 'oMathPara':
            walk(child)
        elif q.namespace == W and q.localname == 't':
            stream.append(('text', child.text or ''))
        elif q.namespace == W and q.localname in ('p','br','tab'):
            stream.append(('text', ' ')); walk(child)
        else:
            walk(child)
walk(doc.getroot())
ws = re.compile(r'\s+')
def clean(s): return ws.sub(' ', s).strip()
maths = [i for i,(k,_) in enumerate(stream) if k=='math']
forms = []  # (idx1, before, after)
for n, si in enumerate(maths, 1):
    before = clean(''.join(t for k,t in stream[max(0,si-60):si] if k=='text'))[-90:]
    after  = clean(''.join(t for k,t in stream[si+1:si+61] if k=='text'))[:90]
    forms.append((n, before, after))

# ---- ordered distinct formula-images from the existing HTML (first occ) ----
exi = (root/'publish'/'leggi'/'02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
strip = re.compile(r'<[^>]+>')
def cleanh(s): return ws.sub(' ', strip.sub(' ', s)).strip()
imgre = re.compile(r'<img\b[^>]*?class="([^"]*)"[^>]*?src="img/pandoc_ch2/(image\d+\.svg)"[^>]*?>')
# eq-block/eq-inline images that are actually DIAGRAMS, not formulas -> keep as image
DIAG = {'image3.svg'}
seen={}; order=[]
for m in imgre.finditer(exi):
    cls, src = m.group(1), m.group(2)
    if 'eq-figure' in cls: continue
    if src in DIAG: continue
    if not ('eq-block' in cls or 'eq-inline' in cls): continue
    if src not in seen:
        be = cleanh(exi[max(0,m.start()-120):m.start()])[-90:]
        af = cleanh(exi[m.end():m.end()+120])[:90]
        seen[src]=(cls,be,af); order.append(src)
imgs = [(s, seen[s][0], seen[s][1], seen[s][2]) for s in order]  # src,cls,before,after

def sim(a,b): return difflib.SequenceMatcher(None,a,b).ratio()
def score(im, fm):
    _,_,be,af = im; _,fb,fa = fm
    # english fragments pollute HTML anchors; take best of both directions
    return 0.6*max(sim(af,fa), sim(af,fb)) + 0.4*max(sim(be,fb), sim(be,fa))

n, mm = len(imgs), len(forms)
NEG = -1.0
dp = [[0.0]*(mm+1) for _ in range(n+1)]
bk = [[None]*(mm+1) for _ in range(n+1)]
for i in range(1,n+1):
    dp[i][0] = NEG*i
for i in range(1,n+1):
    for j in range(1,mm+1):
        skip = dp[i][j-1]            # skip formula j
        take = dp[i-1][j-1] + score(imgs[i-1], forms[j-1])
        if take >= skip:
            dp[i][j]=take; bk[i][j]=('take',)
        else:
            dp[i][j]=skip; bk[i][j]=('skip',)
# backtrack
i,j = n,mm; assign={}
while i>0 and j>0:
    if bk[i][j]==('take',):
        assign[i-1]=j-1; i-=1; j-=1
    else:
        j-=1
rows=[]
for ii,(src,cls,be,af) in enumerate(imgs):
    fj = assign.get(ii)
    idx = forms[fj][0] if fj is not None else 0
    sc = round(score(imgs[ii], forms[fj]),2) if fj is not None else 0.0
    rows.append((src,cls,idx,sc,af[:46]))
out = '\n'.join(f'{s}\t{c}\t->{idx:03}\tr={r}\t…{af}' for s,c,idx,r,af in rows)
(root/'build'/'ch2_map2.tsv').write_text(out, encoding='utf-8')
lo=[r for r in rows if r[3]<0.6]
# monotonic check
idxs=[r[2] for r in rows]
nonmono=sum(1 for a,b in zip(idxs,idxs[1:]) if b<a)
print(f'images={n} forms={mm} matched={sum(1 for r in rows if r[2])}')
print(f'monotonic violations: {nonmono}')
print(f'low (<0.6): {len(lo)} -> '+' '.join(r[0] for r in lo))
print('map -> build/ch2_map2.tsv')
