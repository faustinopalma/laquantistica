import re, pathlib
c = pathlib.Path('publish/leggi/08-effetto-fotoelettrico.html').read_text(encoding='utf-8')
# spans/blocchi coperti
covered = []
for m in re.finditer(r'<div class="equation">.*?</div>|<span class="it">.*?</span>|<span class="en">.*?</span>', c, re.DOTALL):
    covered.append((m.start(), m.end()))
def is_cov(pos):
    return any(a<=pos<b for a,b in covered)
for m in re.finditer(r'<math\b.*?</math>', c, re.DOTALL):
    if not is_cov(m.start()):
        s = max(0, m.start()-70)
        print('--- MATH NON COPERTO @', m.start())
        print(repr(c[s:m.start()]))
        print('   >>>', m.group(0)[:80])
