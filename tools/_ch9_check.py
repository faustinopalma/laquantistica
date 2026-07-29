import re, pathlib
h = pathlib.Path('publish/09-spettri-atomici.html').read_text(encoding='utf-8')
bad = 0
for m in re.finditer(r'href="#fig-09_spettri_atomici-(\d+)" data-ref="fig-09_spettri_atomici-(\d+)">(\d+)</a>', h):
    a, b, c = m.groups()
    if not (a == b == c):
        print('MISMATCH', a, b, c); bad += 1
print('rimandi incoerenti:', bad)
print('n. rimandi totali:', len(re.findall(r'data-ref="fig-09_spettri_atomici-\d+"', h)))
print('caption Fig. count:', len(re.findall(r'<b>Fig\. \d+</b>', h)))
print('ids:', sorted(int(x) for x in re.findall(r'id="fig-09_spettri_atomici-(\d+)"', h)))
# plain-text figura N not inside a link
plains = []
for m in re.finditer(r'figura (\d+)', h):
    seg = h[m.start():m.start()+20]
    if '<a' not in seg:
        plains.append(seg)
print('figura N plain (senza link):', plains)
print('figure/chiusure:', h.count('<figure'), h.count('</figure>'))
