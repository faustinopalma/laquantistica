import re, sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
# paragraphs not starting with a language span and not pure image/figure
ps = re.findall(r'<p>(?!<span class="it")(?!<img)(?!<span class="mark").*?</p>', t)
ps = [x for x in ps if x.strip() not in ('<p></p>',)]
print('untranslated <p>:', len(ps))
for x in ps[:40]:
    print('   ', x[:90])
fcs = [m for m in re.findall(r'<figcaption>.*?</figcaption>', t) if 'class="it"' not in m]
print('untranslated figcaption:', len(fcs))
for f in fcs[:40]:
    print('   ', f[:90])
h2s = [m for m in re.findall(r'<h2[^>]*>.*?</h2>', t) if 'class="it"' not in m]
print('untranslated h2:', len(h2s))
for h in h2s[:40]:
    print('   ', h[:90])
print('garbled table leftover:', 'Colore\t' in t)
print('math count:', t.count('<math'))
print('span it:', t.count('<span class="it">'), ' span en:', t.count('<span class="en">'))
