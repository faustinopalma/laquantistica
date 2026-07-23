import re, os, pathlib
root = pathlib.Path('.')
src = (root/'build'/'ch2_from_docx.html').read_text(encoding='utf-8')
outdir = root/'build'/'ch2_mml'
outdir.mkdir(parents=True, exist_ok=True)
# clean old
for f in outdir.glob('*.mml'):
    f.unlink()
tag = re.compile(r'<math\b.*?</math>', re.DOTALL)
strip = re.compile(r'<[^>]+>')
ws = re.compile(r'\s+')
latexre = re.compile(r'<annotation encoding="application/x-tex">(.*?)</annotation>', re.DOTALL)
dispre = re.compile(r'display="(\w+)"')
rows = []
matches = list(tag.finditer(src))
for i, m in enumerate(matches, 1):
    block = m.group(0)
    (outdir/f'{i:03}.mml').write_text(block, encoding='utf-8')
    disp = dispre.search(block)
    disp = disp.group(1) if disp else '?'
    lx = latexre.search(block)
    lx = ws.sub(' ', lx.group(1)).strip() if lx else ''
    after = src[m.end():m.end()+80]
    after = ws.sub(' ', strip.sub('', after)).strip()[:50]
    before = src[max(0,m.start()-80):m.start()]
    before = ws.sub(' ', strip.sub('', before)).strip()[-50:]
    rows.append(f'{i:03}\t{disp}\t…{before} ⟦MATH⟧ {after}…\t{lx}')
(root/'build'/'ch2_index.tsv').write_text('\n'.join(rows), encoding='utf-8')
print(f'wrote {len(matches)} math blocks to {outdir}')
print('index -> build/ch2_index.tsv')
