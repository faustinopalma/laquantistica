import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

nome, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
righe = Path('sorgenti', nome).read_text(encoding='utf-8').split('\n')


def leggi(t):
    out, i = [], 0
    while i < len(t):
        if t.startswith('<span class="eq-inline', i) or t.startswith('<span class="eq-mml', i):
            j = t.find('data-tex="', i)
            k = t.find('"', j + 10)
            out.append(' $' + t[j + 10:k].replace('&amp;', '&') + '$ ')
            i = fine_span(t, i)
        elif t.startswith('<span class="en">', i):
            i = fine_span(t, i)
        elif t[i] == '<':
            j = t.find('>', i)
            i = len(t) if j < 0 else j + 1
        else:
            out.append(t[i]); i += 1
    return ''.join(out)


for n in range(a - 1, min(b, len(righe))):
    r = leggi(righe[n]).strip()
    if r:
        print(f'--- {n+1} ---')
        print(r)
