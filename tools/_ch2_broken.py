import pathlib, re
d = pathlib.Path('build/ch2_mml2')
broken=set()
for f in sorted(d.glob('*.mml')):
    t=f.read_text(encoding='utf-8')
    if '<mrow/><mo>)</mo>' in t or '<mo>|</mo><mrow/>' in t or re.search(r'<mtd><mrow><maligngroup/></mrow></mtd>', t):
        broken.add(int(f.stem))
# read final map
rows=[]
for ln in pathlib.Path('build/ch2_final_map.tsv').read_text(encoding='utf-8').splitlines():
    p=ln.split('\t')
    if len(p)>=3:
        src=p[0]; idx=int(p[2].replace('->','')); rows.append((src,idx,ln))
brk_imgs=[(src,idx) for src,idx,_ in rows if idx in broken]
print('broken vector formula indices ('+str(len(broken))+'):', ' '.join(f'{i:03}' for i in sorted(broken)))
print()
print('images mapped to broken formulas ('+str(len(brk_imgs))+'):')
for src,idx in brk_imgs: print(f'  {src} -> {idx:03}')
