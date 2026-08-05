import re
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

PROMESSE = re.compile(
    r'\b\w{3,}remo\b|'                       # futuro, prima persona plurale
    r'\b(sar\u00e0|saranno|verr\u00e0|verranno)\s+\w+t[oaie]\b|'   # passivo al futuro
    r'scheda dedicata|scheda su[il]?\b|nota dedicata|nota su[il]?\b|'
    r'capitolo dedicat\w+|paragrafo dedicat\w+|prossima scheda|prossimo capitolo|'
    r'pi\u00f9 avanti|in seguito|successivamente|in un secondo momento|nel seguito|'
    r'per ora non|per il momento non|non ce ne (preoccupiamo|occupiamo)|'
    r'come vedremo|rimandiamo|rinviamo|approfondir\w+',
    re.I)


def prosa_it(s):
    """testo italiano con le formule ridotte a un segnaposto, tag rimossi"""
    fuori = []
    i = 0
    dentro_it = 0
    while i < len(s):
        if s.startswith('<span class="en">', i):
            i = fine_span(s, i)
        elif s.startswith('<span class="eq-inline', i) or s.startswith('<span class="eq-mml', i):
            fuori.append(' \u25ab ')
            i = fine_span(s, i)
        elif s.startswith('<table', i):
            i = s.find('</table>', i)
            i = len(s) if i < 0 else i + 8
        elif s[i] == '<':
            j = s.find('>', i)
            if s.startswith(('</p', '</h', '</li', '</div', '</figcaption'), i):
                fuori.append('\n')
            i = len(s) if j < 0 else j + 1
        else:
            fuori.append(s[i]); i += 1
    t = ''.join(fuori)
    t = t.replace('&nbsp;', ' ').replace('&rarr;', '\u2192').replace('&amp;', '&')
    return t


mirati = sys.argv[1:] or [p.name for p in sorted(Path('sorgenti').glob('*.html'))]
for nome in mirati:
    s = Path('sorgenti', nome).read_text(encoding='utf-8')
    testo = prosa_it(s)
    trovate = []
    for blocco in testo.split('\n'):
        blocco = re.sub(r'\s+', ' ', blocco).strip()
        if not blocco:
            continue
        for frase in re.split(r'(?<=[.;:!?])\s+', blocco):
            if PROMESSE.search(frase):
                trovate.append(frase.strip())
    if trovate:
        print(f'\n===== {nome} ({len(trovate)}) =====')
        for f in trovate:
            m = PROMESSE.search(f)
            print(f'  [{m.group(0)}] {f[:300]}')
