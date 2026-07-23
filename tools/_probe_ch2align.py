import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def strip(s):
    s = re.sub(r'<math\b.*?</math>', ' ', s, flags=re.DOTALL)
    s = re.sub(r'<img\b[^>]*>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()

svg = (ROOT / 'site/svg/02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
pub = (ROOT / 'publish/02-stern-gerlach-cascata.html').read_text(encoding='utf-8')

IMG = re.compile(r'<img class="eq-(?:inline|block)[^"]*"[^>]*>')
svg_imgs = []
for m in IMG.finditer(svg):
    ctx = strip(svg[max(0, m.start()-300):m.start()])[-40:]
    src = re.search(r'/([^/"]+)"', m.group(0)).group(1)
    svg_imgs.append((src, ctx))

MATH = re.compile(r'<math\b.*?</math>', re.DOTALL)
BLOCK = re.compile(r'<div class="equation">.*?</div>|<span class="it">.*?</span>|<span class="en">.*?</span>|<math\b.*?</math>', re.DOTALL)
slots = []
for m in BLOCK.finditer(pub):
    s = m.group(0)
    if s.startswith('<span class="en">'):
        continue
    if s.startswith('<span class="it">'):
        for mm in MATH.finditer(s):
            ctx = strip(s[:mm.start()])[-40:]
            slots.append(('inl', ctx))
    elif s.startswith('<div'):
        ctx = strip(pub[max(0, m.start()-400):m.start()])[-40:]
        for _ in MATH.finditer(s):
            slots.append(('blk', ctx))
    else:
        ctx = strip(pub[max(0, m.start()-400):m.start()])[-40:]
        slots.append(('std', ctx))

print(f'svg imgs={len(svg_imgs)}  pub slots={len(slots)}')
def fp(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())[-16:]
i = j = 0
while i < len(svg_imgs) or j < len(slots):
    a = svg_imgs[i] if i < len(svg_imgs) else ('--', '')
    b = slots[j] if j < len(slots) else ('--', '')
    match = (fp(a[1]) == fp(b[1])) and a[1] != ''
    flag = '' if match else '  <<<'
    print(f'{i:3}/{j:<3} | {a[0]:>10} | svg:...{a[1]:<40} | pub[{b[0]}]:...{b[1]:<40}{flag}')
    i += 1; j += 1
