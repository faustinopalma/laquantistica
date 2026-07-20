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


# --- Figure mapping (number -> file, caption) for the OLE chapters ------------
# Built by inspecting each image against the text so that numbered figures appear
# progressively in the text and references become hoverable.
FIGURES = {
    '04_diffrazione': {
        1: ('FIG1~1.png', 'Schema di principio dell’esperimento.'),
        2: ('FIG2~1.png', 'Struttura cristallina: reticolo tridimensionale di nuclei.'),
        3: ('FIG3~1.png', 'Previsione classica: deflessione dell’elettrone nel cristallo.'),
        5: ('IMG1.jpg', 'Foto dell’ampolla di vetro sotto vuoto.'),
        6: ('IMG2.jpg', 'Dettaglio del cannone elettronico.'),
        7: ('IMG3.jpg', 'Dettaglio del cannone elettronico.'),
        8: ('AMPOLLA1.png', 'Schema dell’ampolla con cannone e lamina.'),
        9: ('AMPOLLA2.png', 'Schema di alimentazione del sistema.'),
        10: ('IMG4.jpg', 'L’intero sistema alimentato.'),
        11: ('IMG5.jpg', 'Immagine ottenuta sullo schermo: punto centrale e due cerchi.'),
        14: ('GRAFITE1.png', 'Struttura cristallina piana della grafite.'),
        15: ('CERCHI1.png', 'Scomposizione del reticolo in sottoreticoli a linee parallele.'),
    },
    '05_rutherford': {
        1: ('PALLE.png', 'In un cristallo il volume di un atomo è quasi tutto vuoto; il nucleo sta al centro.'),
        2: ('APPARATO.png', 'Schema dell’apparato: sorgente, collimatore, lamina d’oro, rilevatore.'),
        3: ('PREPAR~1.jpg', 'Il preparato radioattivo Am241.'),
        4: ('LAMINA.jpg', 'La lamina d’oro con le fenditure di collimazione.'),
        5: ('AMPLIF.jpg', 'Il detector al silicio e l’amplificatore di misura.'),
        6: ('RESIST~1.png', 'Caduta della resistenza del detector al passaggio di una particella α.'),
        7: ('AMPLIF2.jpg', 'L’amplificatore dal lato dei morsetti di uscita.'),
        8: ('IMPULSO.png', 'L’impulso squadrato e la tensione di soglia U.'),
        9: ('INSIEME.jpg', 'L’intero apparato sperimentale.'),
        10: ('COMPON~1.jpg', 'La camera aperta con tutti i componenti.'),
        11: ('ASSEMB~1.jpg', 'La camera chiusa con il goniometro.'),
        13: ('IMPATTO.png', 'Urto contro atomi immaginati come sferette piene.'),
        14: ('ATTRAV~1.png', 'Con nuclei piccolissimi la lamina è quasi trasparente ai raggi α.'),
        15: ('DISTANZA.png', 'Geometria della diffusione.'),
        16: ('ONDELA~1.png', 'Onda piana incidente → onda piana più onda sferica divergente.'),
        17: ('ONDEST~1.png', 'Un fascio stretto: solo l’onda sferica raggiunge il detector.'),
        21: ('ANGOLO.png', 'Angolo solido del rivelatore.'),
    },
    '07_franck_hertz': {
        1: ('AMPOLLA.png', 'Ampolla con gli elettrodi.'),
        2: ('AMPOLL~1.png', 'Alimentazione degli elettrodi.'),
        3: ('AMPOLL~1.jpg', 'Foto dell’ampolla contenente il neon.'),
        4: ('APPARA~1.jpg', 'L’intero apparato sperimentale (neon).'),
        5: ('DISPLA~1.jpg', 'Schermo dell’oscilloscopio: diagramma tensione/corrente.'),
        6: ('DIAGRA~1.png', 'Corrente in funzione della tensione: massimi e minimi.'),
        7: ('BANDED~1.png', 'Le zone luminose tra le griglie (a 70 V).'),
        8: ('APPARA~2.jpg', 'Apparato sperimentale per il mercurio.'),
        9: ('APPARA~3.jpg', 'Apparato sperimentale per il mercurio.'),
        10: ('DISPLA~2.jpg', 'Grafico tensione/corrente per il mercurio: sei massimi.'),
    },
    '08_effetto_fotoelettrico': {
        1: ('EMISSI~1.png', 'L’effetto fotoelettrico: la luce estrae elettroni dal metallo.'),
        2: ('AMPOLL~2.png', 'Sistema di rilevazione: catodo, anodo e corrente I.'),
        3: ('AMPOLL~1.png', 'Sistema per misurare l’energia degli elettroni (condensatore).'),
        4: ('AMPOLLA.jpg', 'Foto dell’ampolla usata nell’esperimento.'),
        5: ('AMPOLL~1.jpg', 'L’ampolla montata sul supporto.'),
        6: ('LAMPAD~1.jpg', 'Lampada ai vapori di mercurio.'),
        7: ('FILTRO~1.jpg', 'Filtro interferometrico per il blu.'),
        8: ('FILTRO~2.jpg', 'Filtro interferometrico per il giallo.'),
        9: ('FILTRI.jpg', 'Supporto dei quattro filtri con diaframma a iride.'),
        10: ('BANCOO~1.jpg', 'Il banco ottico montato.'),
        11: ('APPARATO.jpg', 'L’intero apparato sperimentale in funzione.'),
        12: ('SOLOVO~1.png', 'Con un normale voltmetro la corrente fotoelettrica si richiude sul voltmetro.'),
        13: ('SEPARA~1.png', 'Il separatore di impedenza per misurare la tensione.'),
    },
    '09_spettri_atomici': {
        1: ('LIVELLI.png', 'Livelli energetici dell’atomo di idrogeno.'),
        2: ('SALTI.png', 'I possibili salti energetici tra i livelli.'),
        3: ('TUBI.jpg', 'Quattro tubicini con gas diversi (ossigeno, neon, argon, azoto).'),
        4: ('NEONAC~1.jpg', 'Il tubo contenente neon acceso.'),
        5: ('APPARA~3.jpg', 'Il banco ottico: tubo, lenti, reticolo e schermo.'),
        6: ('IMMAGI~1.jpg', 'L’immagine sullo schermo: le righe dei diversi colori.'),
        7: ('LAMPAD~1.jpg', 'Lampada ai vapori di mercurio.'),
        8: ('APPARA~1.jpg', 'Immagine spettrale della lampada al mercurio.'),
        9: ('APPARA~2.jpg', 'Immagine spettrale della lampada al mercurio.'),
        10: ('LUCIME~1.jpg', 'Immagine spettrale della lampada al mercurio.'),
        11: ('LAMPAD~1.png', 'Lampada di Balmer (idrogeno).'),
        12: ('SPETTO~1.png', 'Spettrometro a goniometro.'),
    },
}

# Un-numbered images that belong inline: placed right after the paragraph that
# contains the given text cue. (cue_substring, filename, caption)
INLINE_EXTRA = {
    '04_diffrazione': [
        ('cristalli orientati a caso', 'DIFFRA~1.png',
         'Formazione dei cerchi: diffrazione dal reticolo.'),
        ('costituita da alcuni punti', 'CERCHI2.png',
         'Immagine prodotta da un singolo cristallo.'),
        ('sovrapposizione di tante immagini', 'CERCHI3.png',
         'Sovrapposizione di cristalli orientati a caso: si formano i cerchi.'),
    ],
}


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

    imgkey = ch['imgkey'] if ch and ch.get('imgkey') else key
    figs = FIGURES.get(key, {})
    extras = INLINE_EXTRA.get(key, [])
    placed = set()
    used = set()

    html_paras = []
    for i, p in enumerate(raw_paras):
        if i == 0:
            continue  # chapter title handled separately
        # A paragraph made only of equation image(s) -> centred display equation.
        if SENT.search(p) and SENT.sub('', p).strip() == '':
            imgs = ''.join(img_tag(int(m), True) for m in SENT.findall(p))
            html_paras.append('<div class="equation">' + imgs + '</div>')
        else:
            p2 = SENT.sub(lambda m: img_tag(int(m.group(1)), False), p)
            if '\u0001' not in p and _looks_like_heading(p):
                html_paras.append('<h2>' + p2 + '</h2>')
            else:
                html_paras.append('<p>' + p2 + '</p>')
        # Progressive numbered figures: insert after the first paragraph that
        # references figure N (handles lists like "figure 6 e 7").
        refs_here = figs_referenced(p)
        for n in sorted(figs):
            if n in placed:
                continue
            if n in refs_here:
                fn, cap = figs[n]
                html_paras.append(figure_block(imgkey, n, fn, cap, key))
                placed.add(n)
                used.add(fn)
        # Un-numbered inline extras placed at their text cue.
        for cue, fn, cap in extras:
            if fn in used:
                continue
            if cue in p:
                html_paras.append(figure_block(imgkey, None, fn, cap, key))
                used.add(fn)

    # Figures referenced but never matched (or unreferenced) -> append in order.
    for n in sorted(figs):
        if n not in placed:
            fn, cap = figs[n]
            html_paras.append(figure_block(imgkey, n, fn, cap, key))
            placed.add(n)
            used.add(fn)

    body = '\n'.join(html_paras)
    if ch is not None:
        body += leftover_gallery(ch, used)
    return body


def references_fig(text, n):
    """True if the paragraph text refers to figure number n."""
    return re.search(rf'[Ff]ig(?:ur[ae])?\.?\s*(?:n\.?\s*)?0*{n}(?!\d)', text) is not None


def figs_referenced(text):
    """Set of figure numbers referenced in the text (handles 'figure 6 e 7')."""
    out = set()
    for m in REF_RE.finditer(text):
        for tok in re.split(r'(?:e|,|-)', m.group(2)):
            tok = tok.strip()
            if tok.isdigit():
                out.add(int(tok))
    return out


def figure_block(imgkey, n, filename, caption, key):
    idattr = f' id="fig-{key}-{n}"' if n else ''
    if n:
        cap = f'<b>Fig. {n}</b> — {esc(caption)}' if caption else f'<b>Fig. {n}</b>'
        alt = caption or f'Figura {n}'
    else:
        cap = esc(caption)
        alt = caption
    return (f'<figure{idattr} class="fig-inline"><img loading="lazy" '
            f'src="img/{imgkey}/{filename}" alt="{esc(alt)}">'
            f'<figcaption>{cap}</figcaption></figure>')


# Reference pattern: "fig. 3", "figura 12", "figure 6 e 7", "Fig.3", ...
REF_RE = re.compile(r'([Ff]ig(?:ur[ae])?\.?\s*(?:n\.?\s*)?)(\d+(?:\s*(?:e|,|-)\s*\d+)*)')


def add_ref_system(body, key):
    """Assign ids to figures (from their 'Fig. N' caption) and turn textual
    references like 'figura 3' into hoverable anchors pointing at them."""
    # 1. Give every <figure> an id derived from its caption, if it lacks one.
    def assign(m):
        tag = m.group(0)
        if 'id="fig-' in tag:
            return tag
        cm = re.search(r'Fig(?:ur[ae])?\.?\s*(\d+)', m.group(1))
        if not cm:
            return tag
        return tag.replace('<figure', f'<figure id="fig-{key}-{int(cm.group(1))}"', 1)
    body = re.sub(r'<figure\b[^>]*>(.*?)</figure>', assign, body, flags=re.S)
    avail = set(int(x) for x in re.findall(rf'id="fig-{re.escape(key)}-(\d+)"', body))
    if not avail:
        return body
    # 2. Wrap references, but never inside the <figure> blocks themselves.
    blocks = []

    def stash(m):
        blocks.append(m.group(0))
        return f'\u0002{len(blocks)-1}\u0002'
    tmp = re.sub(r'<figure\b.*?</figure>', stash, body, flags=re.S)

    def wrap(m):
        kw, nums = m.group(1), m.group(2)

        def anc(tok):
            t = tok.strip()
            if t.isdigit() and int(t) in avail:
                n = int(t)
                return (f'<a class="ref" href="#fig-{key}-{n}" '
                        f'data-ref="fig-{key}-{n}">{tok}</a>')
            return tok
        parts = re.split(r'(\s*(?:e|,|-)\s*)', nums)
        return kw + ''.join(anc(t) for t in parts)
    tmp = REF_RE.sub(wrap, tmp)
    body = re.sub('\u0002(\\d+)\u0002', lambda m: blocks[int(m.group(1))], tmp)
    return body


def leftover_gallery(ch, used):
    """Gallery of chapter images that were not placed inline as numbered figures."""
    if not ch or not ch.get('imgkey'):
        return ''
    d = SITE / 'img' / ch['imgkey']
    if not d.exists():
        return ''
    exts = {'.png', '.jpg', '.jpeg', '.gif'}
    files = sorted([f for f in d.iterdir()
                    if f.suffix.lower() in exts and f.name not in used])
    if not files:
        return ''
    cards = []
    for f in files:
        cards.append(
            f'<figure class="plain"><img loading="lazy" src="img/{ch["imgkey"]}/{f.name}" '
            f'alt="{esc(f.stem)}"><figcaption>{esc(f.stem)}</figcaption></figure>')
    return ('\n<h2>Altre immagini del capitolo</h2>\n'
            '<div class="gallery">\n' + '\n'.join(cards) + '\n</div>')


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
  <article class="page" id="introduzione">
    <p class="kicker">Tesi di Laurea</p>
    <h1 class="cover-title">Esperimenti fondamentali della Meccanica Quantistica</h1>
    <p class="subtitle">Materiale didattico per la comprensione della fisica atomica e quantistica</p>
    <hr class="intro-sep">
    <p class="eyebrow">Introduzione</p>
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
            used = set(re.findall(r'img/[^/"]+/([^"]+)', b))
            body = b + leftover_gallery(ch, used)
        else:
            body = build_ole_body(ch['src'], ch['key'], ch)
        body = add_ref_system(body, ch['key'])
        (SITE / f'{ch["slug"]}.html').write_text(page_html(ch, body, prev_ch, next_ch), encoding='utf-8')
    intro_body = add_ref_system(build_ole_body(INTRO['src'], INTRO['key'], None), INTRO['key'])
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

