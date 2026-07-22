import re, sys
d = open(sys.argv[1], encoding='utf-8').read()
print('len', len(d))
cls = set(re.findall(r'class="([^"]+)"', d))
print('classes:', cls)
paths = re.findall(r'<path\b[^>]*\bd="([^"]+)"', d)
print('num paths:', len(paths))
from collections import Counter
for i, pd in enumerate(paths):
    toks = re.findall(r'[mMlLcCzZ]', pd)
    c = Counter(toks)
    # tail preview
    print(f'path{i}: len={len(pd)} cmds={dict(c)}')
    if 'C' in c or 'c' in c:
        print('   head:', pd[:80])
        print('   tail:', pd[-120:])
