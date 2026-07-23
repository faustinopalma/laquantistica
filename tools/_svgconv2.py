"""Converte publish/02 (bilingue, MathML) in SVG allineando PER-BLOCCO con
site/svg/02 (IT, SVG originali). I blocchi sono in corrispondenza 1:1, quindi
non c'e' deriva: per ogni blocco prendo le <img> SVG dal blocco svg e sostituisco
i <math> nel blocco publish (span it e span en riusano le stesse img).

Preserva il testo editoriale bilingue di publish; usa solo le IMMAGINI da site/svg.
Uso:  python tools/_svgconv2.py [--apply]
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
ch = '02-stern-gerlach-cascata'
IMG = re.compile(r'<img class="eq-(?:inline|block)[^"]*"[^>]*>')
MATH = re.compile(r'<math\b.*?</math>', re.DOTALL)
BLOCK = re.compile(r'<figure\b.*?</figure>|<div class="equation">.*?</div>|<p\b.*?</p>|<h2\b.*?</h2>|<h3\b.*?</h3>|<hr\b[^>]*/?>|<nav\b.*?</nav>', re.DOTALL)

svg = (ROOT/f'site/svg/{ch}.html').read_text(encoding='utf-8')
pub = (ROOT/f'publish/{ch}.html').read_text(encoding='utf-8')

def body(html):
    m = re.search(r'<article\b[^>]*>(.*)</article>', html, re.DOTALL)
    return m.group(1)

sb = BLOCK.findall(body(svg))
warn = []

def replace_span(span, imgs):
    cnt = [0]
    def r(mm):
        i = cnt[0]; cnt[0] += 1
        return imgs[i] if i < len(imgs) else '<img alt="MISS">'
    return MATH.sub(r, span)

def convert_block(sb_block, pb_block):
    if not MATH.search(pb_block):
        return pb_block
    imgs = IMG.findall(sb_block)
    it_m = len(MATH.findall(re.search(r'<span class="it">(.*?)</span>', pb_block, re.DOTALL).group(1))) if '<span class="it">' in pb_block else 0
    out = re.sub(r'<span class="(?:it|en)">.*?</span>',
                 lambda m: replace_span(m.group(0), imgs), pb_block, flags=re.DOTALL)
    if MATH.search(out):  # math fuori dagli span (div.equation ecc.)
        cnt = [0]
        def r2(mm):
            i = cnt[0]; cnt[0] += 1
            return imgs[i] if i < len(imgs) else '<img alt="MISS">'
        out = MATH.sub(r2, out)
    if it_m and len(imgs) != it_m:
        warn.append(f'blocco: it-math={it_m} svg-img={len(imgs)} :: {re.sub(chr(60)+"[^"+chr(62)+"]*"+chr(62)," ",pb_block)[:60].strip()}')
    return out

art = re.search(r'<article\b[^>]*>(.*)</article>', pub, re.DOTALL)
inner = art.group(1)
pb_blocks = BLOCK.findall(inner)
print(f'svg blocks={len(sb)}  pub blocks={len(pb_blocks)}')
if len(sb) != len(pb_blocks):
    print('!!! numero blocchi diverso, STOP'); sys.exit(1)

it = [0]
def sub(m):
    i = it[0]; it[0] += 1
    return convert_block(sb[i], m.group(0))
newinner = BLOCK.sub(sub, inner)

resid = len(MATH.findall(newinner))
miss = newinner.count('alt="MISS"')
print(f'math residui={resid}  MISS={miss}  avvisi_conteggio={len(warn)}')
for w in warn[:15]:
    print('  -', w)
ok = resid == 0 and miss == 0
print('OK =', ok)
if '--apply' in sys.argv and ok:
    newpub = pub[:art.start(1)] + newinner + pub[art.end(1):]
    (ROOT/f'publish/{ch}.html').write_text(newpub, encoding='utf-8')
    print('SCRITTO.')
elif '--apply' in sys.argv:
    print('NON scritto (controlli falliti).')
