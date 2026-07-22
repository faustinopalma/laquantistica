import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
def norm(s):
    s = re.sub(r'<math.*?</math>', ' \u25a1 ', s, flags=re.S)
    s = re.sub(r'<img[^>]*class="eq-[^"]*"[^>]*>', ' \u25a1 ', s)
    s = re.sub(r'<a class="ref".*?</a>', ' \u25a1 ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u00a0', ' ')
    s = s.replace('&apos;', "'")
    return ' '.join(s.split())
tok = re.compile(r'<math.*?</math>|<a class="ref".*?</a>|<img[^>]*class="eq-inline[^"]*"[^>]*>', re.S)
i = 0
for m in re.finditer(r'<(p|h2|figcaption)((?:\s[^>]*)?)>(.*?)</\1>', t, re.S):
    tag, inner = m.group(1), m.group(3)
    if 'class="it"' in inner:
        continue
    plain = norm(inner)
    if not plain:
        continue
    n = len(tok.findall(inner))
    print(f'--- [{i}] {tag} n={n} ---')
    print(plain)
    i += 1
