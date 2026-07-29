import zipfile, re, pathlib, sys, unicodedata

CHAPTERS = {
 '05': (r'originale-docx/da-docx-originale/5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD.docx', 'publish/05-rutherford.html'),
 '06': (r'originale-docx/da-docx-originale/6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx', 'publish/06-ulteriori-sviluppi.html'),
 '07': (r'originale-docx/da-docx-originale/7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx', 'publish/07-franck-hertz.html'),
 '08': (r'originale-docx/da-docx-originale/8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx', 'publish/08-effetto-fotoelettrico.html'),
 '09': (r'originale-docx/da-docx-originale/9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx', 'publish/09-spettri-atomici.html'),
}
APPLY = '--apply' in sys.argv

# publish titles whose docx heading text was garbled during extraction
OVERRIDES = {
 'descrizionedellapparatosperimentaleperilneon': 2,  # ch07: docx had "...neon.Fig4"
}

def norm(s):
    s = re.sub(r'<[^>]*>', '', s)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

def docx_head_map(path):
    z = zipfile.ZipFile(path)
    doc = z.read('word/document.xml').decode('utf-8','replace')
    m = {}
    for para in re.findall(r'<w:p\b[^>]*>.*?</w:p>', doc, re.S):
        st = re.search(r'<w:pStyle w:val="(Heading[123])"', para)
        if not st: continue
        # text only from top-level runs; strip nested tags
        txt = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', para, re.S))
        txt = re.sub(r'<[^>]*>', '', txt)
        lvl = int(st.group(1)[-1])
        k = norm(txt)
        if k: m.setdefault(k, lvl)
    return m

def slug(it):
    s = it.lower().replace('\u2019','').replace("'",'').replace(',','')
    s = unicodedata.normalize('NFKD', s); s=''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9. ]+','',s); s=re.sub(r'\s+','-',s.strip())
    return 'sec-'+s

TITLE_P = re.compile(r'<p><span class="it">([^<]{4,90})</span><span class="en">([^<]{3,120})</span></p>')
for ch,(dp,hp) in CHAPTERS.items():
    hmap = docx_head_map(dp)
    html = pathlib.Path(hp).read_text(encoding='utf-8')
    conv=0; used=set()
    def repl(mm):
        global conv
        it, en = mm.group(1), mm.group(2)
        k = norm(it)
        if k in hmap or k in OVERRIDES:
            conv+=1; used.add(k); lvl=hmap.get(k, OVERRIDES.get(k))
            return f'<h{lvl} id="{slug(it)}"><span class="it">{it}</span><span class="en">{en}</span></h{lvl}>'
        return mm.group(0)
    newhtml = TITLE_P.sub(repl, html)
    print(f'\n== ch{ch}: docx headings={len(hmap)}, convertiti={conv} ==')
    missing = [k for k in hmap if k not in used]
    for k in missing: print('   NON abbinato (docx):', k[:50])
    if APPLY and conv>0:
        pathlib.Path(hp).write_text(newhtml, encoding='utf-8'); print('   scritto', hp)
