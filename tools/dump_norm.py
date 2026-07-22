import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u00a0', ' ')
    s = s.replace('&apos;', "'").replace('&amp;', '&')
    return ' '.join(s.split())
i = 0
for m in re.finditer(r'<(p|h2|figcaption)((?:\s[^>]*)?)>(.*?)</\1>', t, re.S):
    tag, inner = m.group(1), m.group(3)
    if 'class="it"' in inner:
        continue
    plain = norm(inner)
    if not plain:
        continue
    print(f'[{i}] {plain[:130]}')
    i += 1
