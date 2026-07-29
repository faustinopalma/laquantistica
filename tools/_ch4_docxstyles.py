import zipfile, re, pathlib
p = r'originale-docx/da-docx-originale/4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx'
z = zipfile.ZipFile(p)
doc = z.read('word/document.xml').decode('utf-8', 'replace')
# iterate paragraphs
paras = re.findall(r'<w:p[ >].*?</w:p>', doc, re.S)
from collections import Counter
styles = Counter()
print('--- paragraphs with a pStyle (style | text) ---')
for para in paras:
    st = re.search(r'<w:pStyle w:val="([^"]+)"', para)
    texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', para, re.S)
    txt = ''.join(texts).strip()
    if st:
        styles[st.group(1)] += 1
        if txt:
            print(f'[{st.group(1)}] {txt[:70]}')
print('--- style counts ---')
for s,c in styles.most_common():
    print(s, c)
