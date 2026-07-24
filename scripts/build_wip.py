#!/usr/bin/env python
"""Build the hidden WIP MathML site under publish/wip/.

- Reuses the current curated chapter <head>+sidebar (up-to-date chrome), rewriting
  asset/img paths to ../ so they resolve from publish/wip/.
- Converts a chapter's equation SVG images to inline/block MathML (from build/mml,
  the pandoc --mathml extraction of the docx), by occurrence-order alignment.
  Also emits a side-by-side verification page (SVG vs MathML) per formula.
- Other chapters become empty placeholders (filled later, one at a time).

Usage: python scripts/build_wip.py
"""
import re, json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / 'publish'
WIP = PUB / 'wip'
WIP.mkdir(exist_ok=True)

CHAPTERS = [
    ('index.html', 'Introduzione', None),
    ('01-stern-gerlach.html', 'Esperimento di Stern-Gerlach', None),
    ('02-stern-gerlach-cascata.html', 'Esperimenti di Stern-Gerlach in cascata', '02_stern_gerlach_cascata'),
    ('03-elettroni.html', 'Esperimenti con gli Elettroni', 'SKIP'),
    ('04-diffrazione.html', 'Diffrazione degli Elettroni', None),
    ('05-rutherford.html', 'Esperimento di Rutherford', None),
    ('06-ulteriori-sviluppi.html', 'Ulteriori sviluppi della Teoria', None),
    ('07-franck-hertz.html', 'Esperimento di Franck-Hertz', None),
    ('08-effetto-fotoelettrico.html', 'Effetto Fotoelettrico', None),
    ('09-spettri-atomici.html', 'Spettri atomici di emissione', None),
]

MMLDIR = ROOT / 'build' / 'mml'


def load_head_and_sidebar(sample_html):
    """Grab everything from <!DOCTYPE> up to and including the sidebar <aside>."""
    m = re.search(r'^(.*?</aside>)', sample_html, re.S)
    head = m.group(1)
    # rewrite asset/img paths for the wip/ subfolder
    head = head.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    head = head.replace('src="img/', 'src="../img/')
    # WIP badge in the brand subtitle
    head = head.replace('La Quantistica<small', 'La Quantistica · WIP<small')
    return head


def inject_display(mathml, disp):
    if re.search(r'<math\b[^>]*\bdisplay=', mathml):
        return re.sub(r'(<math\b[^>]*\bdisplay=")[^"]*(")', r'\g<1>%s\g<2>' % disp, mathml, count=1)
    return re.sub(r'<math\b', '<math display="%s"' % disp, mathml, count=1)


IMG_RE = re.compile(r'<img class="(eq-block|eq-inline eq-axis|eq-inline|eq-figure)"[^>]*?src="img/pandoc_ch2/(image\d+)\.svg[^"]*"[^>]*/?>')


def build_svg_to_math(curated_html, maths):
    """Occurrence-order alignment on the IT stream -> map svg-file -> mathml.
    Logs conflicts (a hint that alignment drifted)."""
    it_stream = re.sub(r'<span class="en">.*?</span>', '', curated_html, flags=re.S)
    occ = [m.group(2) for m in IMG_RE.finditer(it_stream)]
    mp, conflicts = {}, []
    for i, svg in enumerate(occ):
        if i >= len(maths):
            conflicts.append((i, svg, 'NO_MATH'))
            continue
        if svg in mp:
            # repeated formula: should match the earlier assignment; if not, drift
            continue
        mp[svg] = maths[i]
    return mp, occ, conflicts


def convert_chapter(curated_html, key):
    maths = json.loads((MMLDIR / (key + '.json')).read_text(encoding='utf-8'))
    mp, occ, conflicts = build_svg_to_math(curated_html, maths)

    def repl(m):
        cls, svg = m.group(1), m.group(2)
        ml = mp.get(svg)
        if not ml:
            return m.group(0)
        disp = 'block' if cls in ('eq-block', 'eq-figure') else 'inline'
        ml = inject_display(ml, disp)
        wrap_cls = 'mathml-block' if disp == 'block' else 'mathml-inline'
        return '<span class="%s">%s</span>' % (wrap_cls, ml)

    converted = IMG_RE.sub(repl, curated_html)
    return converted, mp, occ, conflicts


def make_verify_page(occ, maths, mp):
    rows = []
    for i, svg in enumerate(occ):
        ml = maths[i] if i < len(maths) else '<b>—</b>'
        ml = inject_display(ml, 'inline')
        rows.append(
            '<tr><td class="n">%d</td><td class="s">%s</td>'
            '<td><img src="../img/pandoc_ch2/%s.svg?v=2" style="max-height:60px"></td>'
            '<td class="m">%s</td></tr>' % (i, svg, svg, ml))
    return ('<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<script>window.MathJax={tex:{},svg:{fontCache:"global"}};</script>'
            '<script defer src="../assets/mathjax/tex-mml-svg.js"></script>'
            '<style>body{font-family:sans-serif;margin:12px}table{border-collapse:collapse;width:100%}'
            'td{border:1px solid #ddd;padding:6px;vertical-align:middle}.n{color:#888;font:12px monospace}'
            '.s{font:12px monospace;color:#a33}td.m{background:#f7f7f2}</style></head><body>'
            '<h2>Verifica cap.2 — ordine documentale: SVG (originale) vs MathML</h2>'
            '<p>Colonna 3 = immagine SVG attuale; colonna 4 = MathML assegnato. Devono coincidere.</p>'
            '<table><tr><th>#</th><th>svg</th><th>SVG</th><th>MathML</th></tr>' + ''.join(rows) +
            '</table></body></html>')


PLACEHOLDER_BODY = ('<article class="page"><p class="eyebrow">{eyebrow}</p>'
                    '<h1 class="title">{title}</h1>'
                    '<p style="color:#8a6d3b;background:#fcf8e3;border:1px solid #e5dfc5;'
                    'padding:1rem;border-radius:6px"><b>Versione MathML in preparazione.</b> '
                    'Questo capitolo verrà ricreato in forma MathML. {extra}</p></article>')


def main():
    # up-to-date chrome from the current curated ch2
    sample = (PUB / '02-stern-gerlach-cascata.html').read_text(encoding='utf-8')
    head_side = load_head_and_sidebar(sample)
    # tail (after </main>) reused from sample for consistent scripts
    tail_m = re.search(r'(</main>.*</html>\s*)$', sample, re.S)
    tail = tail_m.group(1)
    tail = tail.replace('src="assets/', 'src="../assets/')

    for fname, title, key in CHAPTERS:
        if key and key not in ('SKIP',):
            curated = (PUB / fname).read_text(encoding='utf-8')
            converted, mp, occ, conflicts = convert_chapter(curated, key)
            # rewrite paths for wip and write
            out = converted.replace('href="assets/', 'href="../assets/') \
                           .replace('src="assets/', 'src="../assets/') \
                           .replace('src="img/', 'src="../img/') \
                           .replace('La Quantistica<small', 'La Quantistica · WIP<small')
            (WIP / fname).write_text(out, encoding='utf-8')
            (WIP / ('_verify-' + fname)).write_text(make_verify_page(occ, json.loads((MMLDIR / (key + '.json')).read_text(encoding='utf-8')), mp), encoding='utf-8')
            print('%s: mapped %d svgs, %d occurrences, %d conflicts' % (fname, len(mp), len(occ), len(conflicts)))
            for c in conflicts[:10]:
                print('   conflict', c)
        else:
            eyebrow = 'Introduzione' if fname == 'index.html' else 'Capitolo'
            extra = ('Già disponibile in MathML/MathJax nel sito live.' if key == 'SKIP'
                     else 'Sarà convertito prossimamente.')
            body = PLACEHOLDER_BODY.format(eyebrow=eyebrow, title=title, extra=extra)
            page = head_side + '\n<main class="content">\n' + body + '\n' + tail
            (WIP / fname).write_text(page, encoding='utf-8')
            print('%s: placeholder' % fname)


if __name__ == '__main__':
    main()
