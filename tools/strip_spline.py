#!/usr/bin/env python3
"""Rimuove l'artefatto 'poligono di controllo' degli spline nelle SVG convertite da DWG.

Il convertitore rende alcune curve (linee di campo, grafici) come path FILL (C1) il cui
contorno = curva liscia (tanti micro-segmenti) + il poligono di controllo grossolano
(pochi segmenti grandi in coda). Il fill tra i due rende visibili ENTRAMBE le linee → la
'spezzata' sovrapposta. Qui, per i path fill con molti segmenti, si taglia la coda
grossolana (dal primo lineto grande nell'ultimo 40% fino alla fine), lasciando la curva liscia.

Usage: python tools/strip_spline.py <in.svg> [<out.svg>]   (default: in-place)
Opzioni via env: MINSEG (default 100), BIGMAG (default 30000), TAILFRAC (default 0.6)
Stampa quante code sono state rimosse.
"""
import re, sys, os

MINSEG = int(os.environ.get("MINSEG", "100"))
BIGMAG = int(os.environ.get("BIGMAG", "30000"))
TAILFRAC = float(os.environ.get("TAILFRAC", "0.6"))

def strip_tail(d):
    cmds = re.findall(r'([mMlLzZ])((?:\s+-?\d+\s+-?\d+)*)', d)
    flat = []
    for c, nums in cmds:
        pts = re.findall(r'(-?\d+)\s+(-?\d+)', nums)
        if not pts and c in 'zZ':
            flat.append((c, None, None))
        for a, b in pts:
            flat.append((c, int(a), int(b)))
    n = len(flat)
    cut = None
    for i in range(int(n * TAILFRAC), n):
        c, a, b = flat[i]
        if c in 'lL' and (abs(a) + abs(b)) > BIGMAG:
            cut = i
            break
    if cut is None:
        return d, 0
    kept = flat[:cut]
    out = []
    for c, a, b in kept:
        out.append('Z' if c in 'zZ' else f'{c} {a} {b}')
    return ' '.join(out), n - cut

def main():
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else path
    t = open(path, encoding='utf-8').read()
    report = []
    for m in list(re.finditer(r'<path d="([^"]+)" class="(C\d)"', t)):
        d, cls = m.group(1), m.group(2)
        nseg = len(re.findall(r'[lLmM]\s+-?\d+\s+-?\d+', d))
        if cls == 'C1' and nseg > MINSEG:
            nd, removed = strip_tail(d)
            if removed > 0:
                t = t.replace(f'<path d="{d}" class="{cls}"', f'<path d="{nd}" class="{cls}"')
                report.append((nseg, removed))
    open(out, 'w', encoding='utf-8').write(t)
    print(f'{os.path.basename(path)}: code rimosse da {len(report)} path fill -> {report}')

if __name__ == '__main__':
    main()
