import fitz, pathlib
doc = fitz.open('scansioni/02-stern-gerlach-cascata.pdf')
print('pages:', doc.page_count)
outdir = pathlib.Path('build/ch2_scan'); outdir.mkdir(exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=100)
    p = outdir / f'p{i+1:02}.png'
    pix.save(p)
print('rendered to', outdir)
