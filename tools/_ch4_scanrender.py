import fitz, pathlib
src = pathlib.Path('scansioni/04-diffrazione.pdf')
out = pathlib.Path('build/ch4_scan'); out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(src)
print('pagine:', doc.page_count)
for i, pg in enumerate(doc):
    pix = pg.get_pixmap(dpi=100)
    pix.save(out / f'p{i+1:02d}.png')
print('reso in', out)
