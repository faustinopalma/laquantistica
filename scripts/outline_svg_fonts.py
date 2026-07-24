#!/usr/bin/env python
"""Outline the font-dependent text in LibreOffice-exported equation SVGs.

Problem: these SVGs render some characters via *system* fonts (font-family
"Symbol", "MT Extra", ...). Those fonts exist on Windows desktop but NOT on
phones, so the glyphs break on mobile ("alcuni caratteri non riconosciuti").
LibreOffice embeds the fonts as SVG <font>/<glyph>, but browsers no longer
support SVG fonts, so the fallback is the (missing) system font.

Fix: replace each <text> that uses a NON-fallback embedded font (Symbol, MT
Extra, ...) with vector <path> outlines taken from the embedded <glyph> data,
positioned at the exact TextPosition coordinates. Text that already has a
generic fallback (e.g. "Times New Roman, serif") is LEFT as text — it renders
fine everywhere via the serif fallback and its width is pinned by textLength.

Usage:  python scripts/outline_svg_fonts.py <file-or-dir> [more...]
        (processes *.svg in place; originals are recoverable from git)
"""
import sys, os, glob
from lxml import etree

SVG = 'http://www.w3.org/2000/svg'

def qn(tag):
    return '{%s}%s' % (SVG, tag)

def fmt(v):
    return ('%.3f' % v).rstrip('0').rstrip('.')

def norm_family(f):
    fam = f.split(',')[0].strip().strip('"').strip("'")
    if fam.lower().endswith(' embedded'):
        fam = fam[:-len(' embedded')]
    return fam.strip().lower()

def has_generic_fallback(f):
    fl = f.lower()
    return 'serif' in fl or 'monospace' in fl or 'cursive' in fl

def collect_fonts(root):
    fonts = {}
    for font in root.iter(qn('font')):
        face = font.find(qn('font-face'))
        if face is None:
            continue
        fam = norm_family(face.get('font-family', ''))
        style = (face.get('font-style', 'normal') or 'normal').strip().lower()
        upm = float(face.get('units-per-em', '2048'))
        default_adv = float(font.get('horiz-adv-x', upm))
        entry = fonts.setdefault((fam, style), {'upm': upm, 'default_adv': default_adv, 'glyphs': {}})
        for g in font.findall(qn('glyph')):
            u = g.get('unicode')
            if not u:
                continue
            entry['glyphs'][u] = (float(g.get('horiz-adv-x', default_adv)), g.get('d', ''))
    return fonts

def font_tspans(text_el):
    return [t for t in text_el.iter(qn('tspan')) if t.get('font-family')]

def ancestor_xy(tspan):
    el, x, y = tspan, None, None
    while el is not None:
        if x is None and el.get('x') is not None:
            x = el.get('x')
        if y is None and el.get('y') is not None:
            y = el.get('y')
        if x is not None and y is not None:
            break
        el = el.getparent()
    fx = float(x.split()[0]) if x else 0.0
    fy = float(y.split()[0]) if y else 0.0
    return fx, fy

def process(path):
    parser = etree.XMLParser(resolve_entities=False, huge_tree=True)
    tree = etree.parse(path, parser)
    root = tree.getroot()
    fonts = collect_fonts(root)
    outlined = skipped_mixed = skipped_missing = 0

    for text_el in list(root.iter(qn('text'))):
        tspans = font_tspans(text_el)
        if not tspans:
            continue
        need = []
        for t in tspans:
            fam_attr = t.get('font-family', '')
            if has_generic_fallback(fam_attr):
                need.append(False)
            else:
                key = (norm_family(fam_attr), (t.get('font-style', 'normal') or 'normal').strip().lower())
                need.append(key in fonts or (norm_family(fam_attr), 'normal') in fonts)
        if not any(need):
            continue
        if not all(need):
            skipped_mixed += 1
            continue

        paths, ok = [], True
        for t in tspans:
            fam = norm_family(t.get('font-family', ''))
            style = (t.get('font-style', 'normal') or 'normal').strip().lower()
            entry = fonts.get((fam, style)) or fonts.get((fam, 'normal'))
            if entry is None:
                ok = False
                break
            upm, glyphs, dadv = entry['upm'], entry['glyphs'], entry['default_adv']
            fs = float(t.get('font-size', '0').replace('px', '').strip())
            s = fs / upm
            fill = t.get('fill', 'rgb(0,0,0)')
            x0, y0 = ancestor_xy(t)
            chars = t.text or ''
            advs = [(glyphs.get(ch, (dadv, ''))[0]) * s for ch in chars]
            nat = sum(advs)
            factor = 1.0
            tl = t.get('textLength')
            if tl:
                try:
                    tlf = float(tl)
                    if nat > 0:
                        factor = tlf / nat
                except ValueError:
                    pass
            penx = x0
            for ch, adv in zip(chars, advs):
                gd = glyphs.get(ch)
                if gd and gd[1]:
                    p = etree.Element(qn('path'))
                    p.set('d', gd[1])
                    p.set('transform', 'translate(%s,%s) scale(%s,%s)' % (fmt(penx), fmt(y0), fmt(s), fmt(-s)))
                    if fill and fill != 'none':
                        p.set('fill', fill)
                    p.set('stroke', 'none')
                    paths.append(p)
                penx += adv * factor
        if not ok:
            skipped_missing += 1
            continue

        g = etree.Element(qn('g'))
        g.set('class', 'OutlinedText')
        for p in paths:
            g.append(p)
        parent = text_el.getparent()
        idx = list(parent).index(text_el)
        parent.remove(text_el)
        parent.insert(idx, g)
        outlined += 1

    # Embedded SVG fonts are now unused (Symbol outlined; serif uses system font).
    for font in list(root.iter(qn('font'))):
        font.getparent().remove(font)

    tree.write(path, xml_declaration=True, encoding='UTF-8')
    return outlined, skipped_mixed, skipped_missing

def iter_files(args):
    for a in args:
        if os.path.isdir(a):
            for f in sorted(glob.glob(os.path.join(a, '**', '*.svg'), recursive=True)):
                yield f
        else:
            yield a

def main():
    if len(sys.argv) < 2:
        print('usage: outline_svg_fonts.py <file-or-dir> [...]')
        sys.exit(2)
    tot = tot_out = tot_mixed = tot_miss = 0
    changed = 0
    for f in iter_files(sys.argv[1:]):
        try:
            o, mx, ms = process(f)
        except Exception as e:
            print('ERROR %s: %s' % (f, e))
            continue
        tot += 1
        tot_out += o; tot_mixed += mx; tot_miss += ms
        if o or mx or ms:
            changed += 1
            print('%-48s outlined=%-3d mixed=%-2d missing=%-2d' % (os.path.basename(f), o, mx, ms))
    print('--- %d files, %d touched | outlined=%d mixed_skipped=%d missing_skipped=%d' %
          (tot, changed, tot_out, tot_mixed, tot_miss))

if __name__ == '__main__':
    main()
