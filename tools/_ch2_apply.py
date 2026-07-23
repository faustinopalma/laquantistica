import re, pathlib, sys
root = pathlib.Path('.')
mml2 = root/'build'/'ch2_mml2'
ovr  = root/'build'/'ch2_overrides'   # optional hand-authored {src}.mml
ovr.mkdir(exist_ok=True)

# broken-vector detection (same heuristic as _ch2_broken)
def is_broken(t):
    return ('<mrow/><mo>)</mo>' in t or '<mo>|</mo><mrow/>' in t
            or '<mtd><mrow><maligngroup/></mrow></mtd>' in t
            or re.search(r'<mo>\|</mo><mrow/><mo/>', t) is not None)

# load map: src -> (cls, idx)
mp = {}
for ln in (root/'build'/'ch2_map2.tsv').read_text(encoding='utf-8').splitlines():
    p = ln.split('\t')
    if len(p) < 3: continue
    src = p[0]; cls = p[1]; idx = int(p[2].replace('->',''))
    mp[src] = (cls, idx)

def with_display(mml, inline):
    disp = 'inline' if inline else 'block'
    return mml.replace('<math ', f'<math display="{disp}" ', 1)

conv = {}       # src -> replacement html
pending = []    # broken w/o override (keep image)
for src,(cls,idx) in mp.items():
    o = ovr/f'{src}.mml'
    if o.exists():
        mml = o.read_text(encoding='utf-8').strip()
    else:
        mml = (mml2/f'{idx:03}.mml').read_text(encoding='utf-8').strip()
        if is_broken(mml):
            pending.append(src); continue
    inline = 'eq-inline' in cls
    conv[src] = with_display(mml, inline)

def apply_to(path):
    html = pathlib.Path(path).read_text(encoding='utf-8')
    n = 0
    for src, repl in conv.items():
        pat = re.compile(r'<img\b[^>]*?src="img/pandoc_ch2/'+re.escape(src)+r'"[^>]*?>')
        html, c = pat.subn(lambda m: repl, html)
        n += c
    pathlib.Path(path).write_text(html, encoding='utf-8')
    return n

targets = ['publish/leggi/02-stern-gerlach-cascata.html',
           'site/mathml/02-stern-gerlach-cascata.html']
for tpath in targets:
    if pathlib.Path(tpath).exists():
        cnt = apply_to(tpath)
        print(f'{tpath}: {cnt} img-occurrences replaced')
    else:
        print(f'{tpath}: MISSING')

print(f'\nconverted srcs: {len(conv)}   pending (broken vectors, kept as image): {len(pending)}')
print('pending:', ' '.join(sorted(pending, key=lambda s:int(re.search(r"\d+",s).group()))))
