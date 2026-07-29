import zipfile, re, pathlib, sys

CHAPTERS = {
 '05': (r'originale-docx/da-docx-originale/5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD.docx', 'publish/05-rutherford.html'),
 '06': (r'originale-docx/da-docx-originale/6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx', 'publish/06-ulteriori-sviluppi.html'),
 '07': (r'originale-docx/da-docx-originale/7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx', 'publish/07-franck-hertz.html'),
 '08': (r'originale-docx/da-docx-originale/8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx', 'publish/08-effetto-fotoelettrico.html'),
 '09': (r'originale-docx/da-docx-originale/9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx', 'publish/09-spettri-atomici.html'),
}

def docx_headings(path):
    z = zipfile.ZipFile(path)
    doc = z.read('word/document.xml').decode('utf-8','replace')
    out = []
    for para in re.findall(r'<w:p[ >].*?</w:p>', doc, re.S):
        st = re.search(r'<w:pStyle w:val="(Heading[123])"', para)
        if not st: continue
        txt = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', para, re.S)).strip()
        if txt:
            out.append((st.group(1), txt))
    return out

DRY = '--apply' not in sys.argv
for ch,(dp,hp) in CHAPTERS.items():
    print(f'\n==== chapter {ch} ====')
    heads = docx_headings(dp)
    html = pathlib.Path(hp).read_text(encoding='utf-8')
    for style,txt in heads:
        lvl = {'Heading1':1,'Heading2':2,'Heading3':3}[style]
        pat = re.compile(r'<p><span class="it">' + re.escape(txt) + r'</span><span class="en">(.*?)</span></p>')
        n = len(pat.findall(html))
        print(f'  [{style}] n={n}  {txt[:60]}')
