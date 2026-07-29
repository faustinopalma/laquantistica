import zipfile, re, pathlib
p = r'originale-docx/da-docx-originale/5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD.docx'
z = zipfile.ZipFile(p)
doc = z.read('word/document.xml').decode('utf-8','replace')
rels = z.read('word/_rels/document.xml.rels').decode('utf-8','replace')
rid2 = {m.group(1): m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="(media/[^"]+)"', rels)}
print('=== media files ===')
for n in sorted(z.namelist()):
    if n.startswith('word/media'):
        print('  ', n, z.getinfo(n).file_size)
# walk: interleave images and 'Fig. N' captions
print('=== sequence: images (I) and Fig captions (F) ===')
toks=[]
for m in re.finditer(r'<a:blip[^>]*r:embed="(rId\d+)"|<w:t[^>]*>(.*?)</w:t>', doc):
    if m.group(1):
        toks.append(('I', rid2.get(m.group(1), m.group(1))))
    else:
        t=m.group(2)
        if t: toks.append(('T', t))
# join consecutive text
seq=[]
for typ,val in toks:
    if typ=='T' and seq and seq[-1][0]=='T': seq[-1][1]+=val
    else: seq.append([typ,val])
for typ,val in seq:
    if typ=='I':
        print('  I', val)
    else:
        for fm in re.finditer(r'Fig\.?\s*(\d{1,2})', val):
            print('     F', fm.group(1))
