import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u00a0', ' ')
    return ' '.join(s.split())
tok = re.compile(r'<math.*?</math>|<a class="ref".*?</a>|<img[^>]*class="eq-[^"]*"[^>]*>', re.S)
for m in re.finditer(r'<(p|h2|figcaption)((?:\s[^>]*)?)>(.*?)</\1>', t, re.S):
    tag, attrs, inner = m.group(1), m.group(2) or '', m.group(3)
    if 'class="it"' in inner:
        continue
    plain = norm(inner)
    if not plain:
        continue
    n = len(tok.findall(inner))
    print(f'[{tag} n={n}] {plain[:75]}')
