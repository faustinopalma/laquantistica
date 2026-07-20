"""Generate the static web site for the thesis.
Pipelines:
  - 'pandoc'  : ch1, ch2  -> use pandoc HTML, rewrite image src to converted PNG.
  - 'ole'     : intro, ch4..ch9 -> extracted text interleaved with the ORIGINAL
                Equation-Editor images (perfect-fidelity, correct position) plus a
                figure gallery from original images.
  - 'authored': ch3 -> hand-reconstructed content (from the PDF scan) in ch3_content.
"""
import re, html, json, shutil
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_content import doc_tokens

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT           # output dir (set per build)
MODE = 'svg'          # 'svg' or 'mathml'
MML = {}              # key -> list of <math> strings (mathml mode)
DOCX = ROOT / 'originale-docx'   # source .docx tree (new version)
EQ = ROOT / 'build' / 'eq'
EQSVG = ROOT / 'build' / 'eqsvg'
PANSVG = ROOT / 'build' / 'pandoc_svg'
MMLDIR = ROOT / 'build' / 'mml'


def load_mml():
    MML.clear()
    if MMLDIR.exists():
        for f in MMLDIR.glob('*.json'):
            MML[f.stem] = json.loads(f.read_text(encoding='utf-8'))

# The introduction is shown on the home page (index). Chapters = 9 single pages.
INTRO = dict(key='00_introduzione', title='Introduzione', src='Introduzione.docx')

CHAPTERS = [
    dict(n=1, slug='01-stern-gerlach', key='01_stern_gerlach', title='Esperimento di Stern-Gerlach',
         pipe='pandoc', htmlfile='ch1.html', media='pandoc_ch1', imgkey='01_stern_gerlach'),
    dict(n=2, slug='02-stern-gerlach-cascata', key='02_stern_gerlach_cascata',
         title='Esperimenti di Stern-Gerlach in cascata',
         pipe='pandoc', htmlfile='ch2.html', media='pandoc_ch2', imgkey='02_stern_gerlach_cascata'),
    dict(n=3, slug='03-elettroni', key='03_elettroni', title='Esperimenti con gli Elettroni',
         pipe='authored', imgkey='03_elettroni'),
    dict(n=4, slug='04-diffrazione', key='04_diffrazione', title='Diffrazione degli Elettroni',
         pipe='ole', src='4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx', imgkey='04_diffrazione'),
    dict(n=5, slug='05-rutherford', key='05_rutherford', title='Esperimento di Rutherford',
         pipe='ole', src='5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx', imgkey='05_rutherford'),
    dict(n=6, slug='06-ulteriori-sviluppi', key='06_ulteriori_sviluppi', title='Ulteriori sviluppi della Teoria',
         pipe='ole', src='6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx', imgkey='06_ulteriori_sviluppi'),
    dict(n=7, slug='07-franck-hertz', key='07_franck_hertz', title='Esperimento di Franck-Hertz',
         pipe='ole', src='7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx', imgkey='07_franck_hertz'),
    dict(n=8, slug='08-effetto-fotoelettrico', key='08_effetto_fotoelettrico', title='Effetto Fotoelettrico',
         pipe='ole', src='8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx', imgkey='08_effetto_fotoelettrico'),
    dict(n=9, slug='09-spettri-atomici', key='09_spettri_atomici', title='Spettri atomici di emissione',
         pipe='ole', src='9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx', imgkey='09_spettri_atomici'),
]


def load_equations(key):
    f = EQ / f'{key}.txt'
    if not f.exists():
        return []
    eqs = []
    for line in f.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\[\d+\]\s?(.*)', line)
        eqs.append(m.group(1) if m else line)
    return eqs


def esc(s):
    return html.escape(s, quote=False)


def build_nav():
    links = ['<a href="index.html"><span class="num"></span>Introduzione</a>']
    for c in CHAPTERS:
        links.append(
            f'<a href="{c["slug"]}.html"><span class="num">{c["n"]}</span>{esc(c["title"])}</a>')
    return '\n'.join(links)


# Display equations taller than this (inches) sitting alone on a line are centred
# as block images; the rest flow inline with the text.
EQ_SCALE = 1.15  # scale original physical size up slightly to match web body text
SENT = re.compile('\u0001IMG\u0001(\\d+)\u0001/IMG\u0001')


def build_ole_body(src_rel, key, ch=None):
    src = DOCX / src_rel
    tokens = doc_tokens(src)
    sizes = _load_manifest(f'eq_{key}')
    maths = MML.get(key, [])

    def img_tag(idx, display):
        fn = f'obj{idx:03d}.png'
        w, h = sizes.get(fn, (0.3, 0.2))
        w *= EQ_SCALE
        h *= EQ_SCALE
        # MathML mode: emit inline <math> when available for this formula index.
        if MODE == 'mathml' and idx < len(maths) and maths[idx]:
            m = maths[idx]
            disp = 'block' if display else 'inline'
            m = re.sub(r'<math\b', f'<math display="{disp}"', m, count=1)
            return m
        src_attr = f'img/eq_{key}/obj{idx:03d}.svg'
        if display:
            return (f'<img class="eq-block" src="{src_attr}" '
                    f'style="width:{w:.3f}in;height:{h:.3f}in" alt="formula">')
        cls = 'eq-inline eq-axis' if h > 0.40 else 'eq-inline'
        return (f'<img class="{cls}" src="{src_attr}" '
                f'style="height:{h:.3f}in" alt="formula">')

    # Build a single stream: escaped text + image sentinels at object positions.
    parts = []
    oi = 0
    for typ, val in tokens:
        if typ == 'text':
            parts.append(esc(val))
        else:  # inline object -> its formula (svg image or inline MathML)
            if (EQSVG / key / f'obj{oi:03d}.svg').exists():
                parts.append(f'\u0001IMG\u0001{oi}\u0001/IMG\u0001')
            oi += 1
    full = ''.join(parts)
    raw_paras = [p.strip() for p in re.split(r'\n+', full) if p.strip()]

    html_paras = []
    for i, p in enumerate(raw_paras):
        if i == 0:
            continue  # chapter title handled separately
        # A paragraph made only of equation image(s) -> centred display equation.
        if SENT.search(p) and SENT.sub('', p).strip() == '':
            imgs = ''.join(img_tag(int(m), True) for m in SENT.findall(p))
            html_paras.append('<div class="equation">' + imgs + '</div>')
            continue
        p2 = SENT.sub(lambda m: img_tag(int(m.group(1)), False), p)
        if '\u0001' not in p and _looks_like_heading(p):
            html_paras.append('<h2>' + p2 + '</h2>')
        else:
            html_paras.append('<p>' + p2 + '</p>')
    body = '\n'.join(html_paras)
    if ch is not None:
        body += figure_gallery(ch)
    return body


def _looks_like_heading(p):
    # A short, title-like line with no math and mostly letters -> section heading.
    if '\\(' in p or len(p) > 55 or len(p) < 3:
        return False
    if p.endswith(('.', ',', ':', ';')):
        return False
    letters = sum(c.isalpha() for c in p)
    if letters < 0.6 * len(p):
        return False
    if not p[:1].isupper():
        return False
    return True


def figure_gallery(ch, exclude=None):
    if not ch.get('imgkey'):
        return ''
    d = SITE / 'img' / ch['imgkey']
    if not d.exists():
        return ''
    exts = {'.png', '.jpg', '.jpeg', '.gif'}
    files = sorted([f for f in d.iterdir() if f.suffix.lower() in exts])
    if not files:
        return ''
    cards = []
    for f in files:
        name = f.stem
        cards.append(
            f'<figure><img loading="lazy" src="img/{ch["imgkey"]}/{f.name}" alt="{esc(name)}">'
            f'<figcaption>{esc(name)}</figcaption></figure>')
    return ('\n<h2>Figure e immagini del capitolo</h2>\n'
            '<div class="gallery">\n' + '\n'.join(cards) + '\n</div>')


def _load_manifest(media):
    f = SITE / 'img' / media / 'manifest.csv'
    sizes = {}
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines()[1:]:
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    sizes[parts[0]] = (float(parts[1]), float(parts[2]))
                except ValueError:
                    pass
    return sizes


def build_pandoc_body(ch):
    htmlf = ROOT / 'build' / 'pandoc_test' / ch['htmlfile']
    txt = htmlf.read_text(encoding='utf-8', errors='replace')
    sizes = _load_manifest(ch['media'])
    # rewrite <img ...> to converted PNG and set the original physical size (inches)
    def repl(m):
        s = m.group(1)
        base = re.sub(r'.*/media/', '', s.replace('\\', '/'))
        base = re.sub(r'\.(wmf|emf|bmp|png|jpg|jpeg|gif)$', '', base, flags=re.I)
        png = f'{base}.png'
        wh = sizes.get(png)
        style = ''
        h = 0.0
        if wh:
            style = f' style="width:{wh[0]:.3f}in;height:{wh[1]:.3f}in"'
            h = wh[1]
        # prefer the vector SVG when we produced one for this media file
        fname = f'{base}.svg' if (PANSVG / ch['media'] / f'{base}.svg').exists() else png
        return f'<img data-h="{h:.3f}" src="img/{ch["media"]}/{fname}"{style} />'
    txt = re.sub(r'<img[^>]*src="([^"]+)"[^>]*/?>', repl, txt)
    # give inline equation images a baseline, and centre block equations/figures,
    # so the pandoc chapters match the look of the rest of the site.
    txt = _classify_pandoc_media(txt)
    txt = re.sub(r'\s*data-h="[\d.]+"', '', txt)  # strip the helper attribute
    # drop the first <h1> (title shown in header)
    txt = re.sub(r'<h1[^>]*>.*?</h1>', '', txt, count=1, flags=re.S)
    return txt


def _classify_pandoc_media(html_txt):
    return re.sub(r'<p(?P<attr>[^>]*)>(?P<body>.*?)</p>', _para_wrap, html_txt, flags=re.S)


def _para_wrap(m):
    attr = m.group('attr')
    inner = m.group('body')
    if '<img' not in inner:
        return m.group(0)
    text = re.sub(r'<[^>]+>', '', inner).strip()
    if not text:
        block = re.sub(r'<img ', '<img class="eq-block" ', inner)
        return '<div class="equation">' + block + '</div>'

    def _mark_inline(im):
        tag = im.group(0)
        hm = re.search(r'data-h="([\d.]+)"', tag)
        h = float(hm.group(1)) if hm else 0.0
        if h > 0.9:
            cls = 'eq-figure'          # large image -> centred block, not inline
        elif h > 0.40:
            cls = 'eq-inline eq-axis'  # tall math -> align to the math axis
        else:
            cls = 'eq-inline'          # short symbol -> sit on the baseline
        return re.sub(r'<img ', f'<img class="{cls}" ', tag, count=1)

    return '<p' + attr + '>' + re.sub(r'<img [^>]*>', _mark_inline, inner) + '</p>'


def page_html(ch, body, prev_ch, next_ch):
    nav = build_nav()

    footer = []
    if prev_ch:
        footer.append(f'<a class="prev" href="{prev_ch["slug"]}.html"><span>Precedente</span>{esc(prev_ch["title"])}</a>')
    else:
        footer.append('<a class="prev" href="index.html"><span>Precedente</span>Introduzione</a>')
    if next_ch:
        footer.append(f'<a class="next" href="{next_ch["slug"]}.html"><span>Successivo</span>{esc(next_ch["title"])}</a>')
    chapter_nav = '<nav class="chapter-nav">' + ''.join(footer) + '</nav>'

    eyebrow = f'Capitolo {ch["n"]}'
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(ch["title"])} — Tesi di Laurea</title>
<link rel="stylesheet" href="assets/style.css">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'global' }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script defer src="assets/mathjax/tex-mml-svg.js"></script>
</head>
<body>
<button class="menu-toggle" aria-label="Menu">☰ Indice</button>
<div class="scrim"></div>
<div class="layout">
<aside class="sidebar">
  <a class="brand" href="index.html">Fisica Atomica<small>Esperimenti fondamentali di Meccanica Quantistica — Tesi di Laurea</small></a>
  <nav>{nav}</nav>
</aside>
<main class="content">
  <article class="page">
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="title">{esc(ch["title"])}</h1>
    {body}
    {chapter_nav}
  </article>
</main>
</div>
<script src="assets/app.js"></script>
</body>
</html>'''


def build_index(intro_body):
    cards = []
    for c in CHAPTERS:
        num = f'Capitolo {c["n"]}'
        cards.append(
            f'<a class="toc-card" href="{c["slug"]}.html"><span class="n">{num}</span>'
            f'<span class="t">{esc(c["title"])}</span></a>')
    toc = '\n'.join(cards)
    nav = build_nav()
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tesi di Laurea — Esperimenti fondamentali di Meccanica Quantistica</title>
<link rel="stylesheet" href="assets/style.css">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'global' }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script defer src="assets/mathjax/tex-mml-svg.js"></script>
</head>
<body>
<button class="menu-toggle" aria-label="Menu">☰ Indice</button>
<div class="scrim"></div>
<div class="layout">
<aside class="sidebar">
  <a class="brand" href="index.html">Fisica Atomica<small>Esperimenti fondamentali di Meccanica Quantistica — Tesi di Laurea</small></a>
  <nav>{nav}</nav>
</aside>
<main class="content">
  <article class="page cover">
    <p class="kicker">Tesi di Laurea</p>
    <h1>Esperimenti fondamentali della Meccanica Quantistica</h1>
    <p class="subtitle">Materiale didattico per la comprensione della fisica atomica e quantistica</p>
    <div class="toc-grid">{toc}</div>
  </article>
  <article class="page" id="introduzione">
    <p class="eyebrow">Introduzione</p>
    <h1 class="title">Introduzione</h1>
    {intro_body}
  </article>
</main>
</div>
<script src="assets/app.js"></script>
</body>
</html>'''


def _conv_latex(tex, disp):
    import latex2mathml.converter as L
    try:
        mm = L.convert(tex.strip())
    except Exception:
        return None
    return re.sub(r'display="[^"]*"', f'display="{disp}"', mm, count=1)


def ch3_to_mathml(body):
    """Convert the authored ch3 LaTeX (\\(..\\) inline, \\[..\\] block) to MathML."""
    def blk(m):
        r = _conv_latex(m.group(1), 'block')
        return r if r else m.group(0)

    def inl(m):
        r = _conv_latex(m.group(1), 'inline')
        return r if r else m.group(0)

    body = re.sub(r'\\\[(.+?)\\\]', blk, body, flags=re.S)
    body = re.sub(r'\\\((.+?)\\\)', inl, body, flags=re.S)
    return body


def _copy_assets(outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    # css/js/mathjax
    dst = outdir / 'assets'
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT / 'assets', dst)
    # all images (figure galleries + eq png+manifest + pandoc png+manifest)
    imgdst = outdir / 'img'
    if imgdst.exists():
        shutil.rmtree(imgdst)
    shutil.copytree(ROOT / 'img', imgdst)
    # overlay equation SVGs
    for kd in EQSVG.iterdir() if EQSVG.exists() else []:
        if kd.is_dir():
            d = imgdst / f'eq_{kd.name}'
            d.mkdir(parents=True, exist_ok=True)
            for svg in kd.glob('*.svg'):
                shutil.copy2(svg, d / svg.name)
    # overlay pandoc media SVGs
    for kd in PANSVG.iterdir() if PANSVG.exists() else []:
        if kd.is_dir():
            d = imgdst / kd.name
            d.mkdir(parents=True, exist_ok=True)
            for svg in kd.glob('*.svg'):
                shutil.copy2(svg, d / svg.name)


def build(outdir, mode):
    global SITE, MODE
    SITE = Path(outdir)
    MODE = mode
    load_mml()
    _copy_assets(SITE)
    from ch3_content import CH3_BODY
    for i, ch in enumerate(CHAPTERS):
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
        if ch['pipe'] == 'pandoc':
            body = build_pandoc_body(ch)
        elif ch['pipe'] == 'authored':
            b = ch3_to_mathml(CH3_BODY) if mode == 'mathml' else CH3_BODY
            body = b + figure_gallery(ch)
        else:
            body = build_ole_body(ch['src'], ch['key'], ch)
        (SITE / f'{ch["slug"]}.html').write_text(page_html(ch, body, prev_ch, next_ch), encoding='utf-8')
    intro_body = build_ole_body(INTRO['src'], INTRO['key'], None)
    (SITE / 'index.html').write_text(build_index(intro_body), encoding='utf-8')
    print(f'built {mode} -> {SITE}')


def build_chooser(site_dir):
    site_dir = Path(site_dir)
    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / 'index.html').write_text('''<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tesi di Laurea — scegli versione</title>
<style>
 body{margin:0;min-height:100vh;display:flex;flex-direction:column;align-items:center;
   justify-content:center;font-family:"Segoe UI",system-ui,sans-serif;background:#f5f3ee;color:#1f2328;gap:1.5rem}
 h1{font-weight:600;text-align:center;max-width:40rem;padding:0 1rem}
 .cards{display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center}
 a.card{display:block;width:16rem;padding:1.6rem 1.4rem;background:#fff;border:1px solid #e0dccf;
   border-radius:14px;text-decoration:none;color:inherit;box-shadow:0 8px 24px rgba(0,0,0,.06);transition:.15s}
 a.card:hover{transform:translateY(-3px);border-color:#a8443b}
 a.card h2{margin:.2rem 0 .5rem;color:#7b2d26}
 a.card p{margin:0;color:#4a4f57;font-size:.95rem;line-height:1.5}
</style></head>
<body>
 <h1>Esperimenti fondamentali della Meccanica Quantistica — Tesi di Laurea</h1>
 <div class="cards">
  <a class="card" href="svg/index.html"><h2>Versione SVG</h2>
    <p>Formule come immagini vettoriali fedeli all'originale (Equation Editor → SVG).</p></a>
  <a class="card" href="mathml/index.html"><h2>Versione MathML</h2>
    <p>Formule come MathML nativo, selezionabile e accessibile (via LibreOffice).</p></a>
 </div>
</body></html>''', encoding='utf-8')
    print(f'wrote chooser -> {site_dir / "index.html"}')


def main():
    build(ROOT / 'site' / 'svg', 'svg')
    build(ROOT / 'site' / 'mathml', 'mathml')
    build_chooser(ROOT / 'site')


if __name__ == '__main__':
    main()

