"""Estrae il testo dai documenti che ne contengono uno vero, senza OCR.

Un .pptx e' un archivio zip di XML: se il certificato e' stato composto in
PowerPoint, il testo c'e' davvero e non va indovinato. Stesso discorso per un PDF
che abbia uno strato di testo.
"""
import pathlib
import re
import zipfile

CARTELLA = pathlib.Path('privato/librettouniversitario')

print('=== .pptx: testo contenuto nelle diapositive ===')
pptx = next(CARTELLA.glob('*.pptx'), None)
if pptx:
    with zipfile.ZipFile(pptx) as z:
        diapo = sorted(n for n in z.namelist()
                       if re.match(r'ppt/slides/slide\d+\.xml$', n))
        print(f'{pptx.name}: {len(diapo)} diapositive')
        for n in diapo:
            xml = z.read(n).decode('utf-8', 'replace')
            testi = re.findall(r'<a:t>(.*?)</a:t>', xml, re.S)
            print(f'\n--- {n} ---')
            for t in testi:
                t = t.strip()
                if t:
                    print(f'   {t}')
else:
    print('nessun .pptx')

print('\n=== .pdf: c\'e uno strato di testo? ===')
pdf = next(CARTELLA.glob('*.pdf'), None)
if pdf:
    grezzo = pdf.read_bytes()
    print(f'{pdf.name}: {len(grezzo) // 1024} kB')
    print('  font incorporati :', len(re.findall(rb'/Font', grezzo)))
    print('  flussi di testo  :', len(re.findall(rb'BT\s', grezzo)))
    print('  immagini         :', len(re.findall(rb'/Subtype\s*/Image', grezzo)))
