import zipfile, re, pathlib
p = r'originale-docx/da-docx-originale/4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx'
z = zipfile.ZipFile(p)
doc = z.read('word/document.xml').decode('utf-8', 'replace')
rels = z.read('word/_rels/document.xml.rels').decode('utf-8', 'replace')
# map rId -> media file
rid2media = {}
for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="(media/[^"]+)"', rels):
    rid2media[m.group(1)] = m.group(2)
# walk document: sequence of tokens = either image embed or 'Fig. N' caption text
# get text runs and blips in order
tokens = []
for m in re.finditer(r'<a:blip[^>]*r:embed="(rId\d+)"|<w:t[^>]*>(.*?)</w:t>', doc):
    if m.group(1):
        tokens.append(('IMG', rid2media.get(m.group(1), m.group(1))))
    else:
        t = m.group(2)
        if t:
            tokens.append(('T', t))
# reconstruct text stream, find 'Fig. N' and nearest preceding IMG
# Build a flat list; join consecutive T
seq = []
for typ,val in tokens:
    if typ=='T' and seq and seq[-1][0]=='T':
        seq[-1]=('T', seq[-1][1]+val)
    else:
        seq.append([typ,val])
for i,(typ,val) in enumerate(seq):
    if typ=='T' and re.search(r'Fig\.?\s*\d', val):
        # find nearest preceding IMG within 4 tokens
        prev=None
        for j in range(i-1, max(-1,i-6), -1):
            if seq[j][0]=='IMG':
                prev=seq[j][1]; break
        print(repr(val.strip()[:60]), '<-- IMG:', prev)
