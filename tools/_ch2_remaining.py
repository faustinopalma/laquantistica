import pathlib, re
root = pathlib.Path('.')
html = (root/'publish/leggi/02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
ovr = root/'build/ch2_overrides'
have = {p.name[:-4] for p in ovr.glob('*.mml')}  # strip .mml -> 'imageN.svg'

# broken indices (from _ch2_broken heuristic)
d = root/'build/ch2_mml2'
broken=set()
for f in sorted(d.glob('*.mml')):
    t=f.read_text(encoding='utf-8')
    if '<mrow/><mo>)</mo>' in t or '<mo>|</mo><mrow/>' in t or re.search(r'<mtd><mrow><maligngroup/></mrow></mtd>', t):
        broken.add(int(f.stem))

rows=[]
for ln in (root/'build/ch2_final_map.tsv').read_text(encoding='utf-8').splitlines():
    p=ln.split('\t')
    if len(p)>=3:
        rows.append((p[0], int(p[2].replace('->',''))))

def cls_in_html(src):
    m=re.search(r'<img\b[^>]*?class="(eq-[^"]*)"[^>]*?src="img/pandoc_ch2/'+re.escape(src)+r'"', html)
    if not m:
        m=re.search(r'<img\b[^>]*?src="img/pandoc_ch2/'+re.escape(src)+r'"[^>]*?>', html)
        if m:
            m2=re.search(r'class="(eq-[^"]*)"', m.group(0))
            return m2.group(1) if m2 else '(no-class-img)'
        return 'NOT-IMG(converted?)'
    return m.group(1)

print(f"{'SRC':16} {'idx':>4} {'override':>9} {'class in page'}")
seen=set()
todo_formula=[]; keep_diagram=[]
for src,idx in rows:
    if idx not in broken: continue
    if src in seen: continue
    seen.add(src)
    c=cls_in_html(src)
    ov='YES' if src in have else '-'
    print(f"{src:16} {idx:>4} {ov:>9} {c}")
    if 'figure' in c:
        keep_diagram.append(src)
    elif c.startswith('NOT-IMG'):
        pass  # already converted
    elif src not in have:
        todo_formula.append(src)
print()
print('DIAGRAMS to keep as image:', ' '.join(keep_diagram) or '(none)')
print('FORMULAS still needing hand-authored override:', ' '.join(todo_formula) or '(none)')
print('count todo:', len(todo_formula))
