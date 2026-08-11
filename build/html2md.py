"""Converte una scheda pubblicata in italiano in markdown, per lavorarci a mano.

    python build/html2md.py 04-diffrazione 04b-forma-evoluzione

Scrive privato/bozze/<slug>.md. Le formule vengono ricostruite dagli attributi data-tex,
quindi il LaTeX torna identico a quello di partenza.
"""
import html
import re
import sys
from pathlib import Path


def _span_formule(s):
    """Sostituisce gli span con data-tex, contando gli span annidati del rendering."""
    fuori = []
    posizione = 0
    for avvio in [m.start() for m in re.finditer(r'<span[^>]*data-tex="', s)]:
        if avvio < posizione:
            continue
        apertura = re.match(r'<span[^>]*?class="([^"]*)"[^>]*?data-tex="([^"]*)"[^>]*>', s[avvio:])
        if not apertura:
            continue
        profondita = 0
        indice = avvio
        for tag in re.finditer(r'<span\b|</span>', s[avvio:]):
            profondita += 1 if tag.group(0) == '<span' else -1
            if profondita == 0:
                indice = avvio + tag.end()
                break
        tex = html.unescape(apertura.group(2))
        blocco = 'eq-mml-block' in apertura.group(1)
        fuori.append(s[posizione:avvio])
        fuori.append('\n\n$$%s$$\n\n' % tex if blocco else '$%s$' % tex)
        posizione = indice
    fuori.append(s[posizione:])
    return ''.join(fuori)


def testo(frammento):
    """Converte il contenuto di un blocco inline in markdown."""
    s = _span_formule(frammento)
    s = re.sub(r'<a class="ref"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S)
    s = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S)
    s = re.sub(r'</?(strong|b)>', '**', s)
    s = re.sub(r'</?(em|i)>', '*', s)
    s = re.sub(r'<br\s*/?>', '  \n', s)
    s = re.sub(r'<span class="it">|</span>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'(\w)\$', r'\1 $', s)
    return re.sub(r'[ \t]+', ' ', html.unescape(s)).strip()


def tabella(blocco):
    righe = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', blocco, re.S):
        celle = [testo(c) for _, c in re.findall(r'<(t[hd])[^>]*>(.*?)</\1>', tr, re.S)]
        righe.append('| ' + ' | '.join(celle) + ' |')
        if '<th' in tr and len(righe) == 1:
            righe.append('|' + '---|' * len(celle))
    return '\n'.join(righe)


def converti(slug):
    sorgente = Path('publish/it/%s.html' % slug).read_text(encoding='utf-8')
    corpo = re.search(r'<article[^>]*>(.*?)</article>', sorgente, re.S).group(1)
    corpo = re.split(r'<nav class="chapter-nav"', corpo)[0]

    pezzi = []
    modello = (r'<(h1|h2|h3|h4|p|figure|table|div|blockquote)\b[^>]*>(.*?)</\1>')
    for tag, contenuto in re.findall(modello, corpo, re.S):
        if tag == 'figure':
            src = re.search(r'src="([^"]*)"', contenuto)
            cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', contenuto, re.S)
            pezzi.append('![%s](%s)' % (testo(cap.group(1)) if cap else '', src.group(1) if src else ''))
        elif tag == 'div' and 'data-tex=' in contenuto:
            tex = re.search(r'data-tex="([^"]*)"', contenuto)
            pezzi.append('$$%s$$' % html.unescape(tex.group(1)))
        elif tag == 'table':
            pezzi.append(tabella(contenuto))
        elif tag in ('h1', 'h2', 'h3', 'h4'):
            pezzi.append('#' * int(tag[1]) + ' ' + testo(contenuto))
        else:
            t = testo(contenuto)
            if t:
                pezzi.append(t)

    fuori = Path('privato/bozze/%s.md' % slug)
    fuori.write_text('\n\n'.join(pezzi).replace('\n\n\n\n', '\n\n') + '\n',
                     encoding='utf-8', newline='\n')
    print('scritto', fuori, len(pezzi), 'blocchi')


for nome in sys.argv[1:]:
    converti(nome)
