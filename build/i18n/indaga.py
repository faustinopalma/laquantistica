import pathlib
import re

print('=== residui class="en"/"it" nei lab: sono markup o stringhe JS? ===')
for n in ['lab-03c-millikan', 'lab-02c-sg-ricombinazione', 'lab-09-spettri']:
    t = (pathlib.Path('publish/v2/it') / f'{n}.html').read_text(encoding='utf-8')
    print(f'--- {n} (albero it, cerco "en") ---')
    for m in re.finditer(r'class="en"', t):
        riga = t[:m.start()].count('\n') + 1
        ctx = t[max(0, m.start() - 90):m.start() + 60].replace('\n', ' ')
        print(f'  riga {riga}: ...{ctx}...')

print('\n=== capitolo 6: elementi di lingua annidati ===')
t = pathlib.Path('publish/06-ulteriori-sviluppi.html').read_text(encoding='utf-8')
prof = 0
inizio = None
for m in re.finditer(r'<span\b[^>]*>|</span>', t):
    tag = m.group(0)
    if tag.startswith('</'):
        prof -= 1
        if inizio is not None and prof <= liv:
            inizio = None
    else:
        cl = re.search(r'class="([^"]*)"', tag)
        cls = (cl.group(1).split() if cl else [])
        if inizio is not None and ('it' in cls or 'en' in cls):
            print(f'  ANNIDATO a offset {m.start()}: esterno={esterno}')
            print(f'    ...{t[max(0,inizio-40):m.start()+150]}...')
            inizio = None
        elif 'it' in cls or 'en' in cls:
            inizio, liv, esterno = m.start(), prof, ('it' if 'it' in cls else 'en')
        prof += 1
