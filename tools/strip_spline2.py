#!/usr/bin/env python3
"""Strip spline control-polygon artifact (v2, outlier-based, no vision needed).

Artifact: a path draws a smooth curve, then appends the curve's CONTROL POLYGON as
a few segments in the tail. The control polygon always STARTS with a huge 'jump-back'
lineto that is the single largest segment of the path and sits in its tail. We detect
that outlier and cut the path there.

Rule (per path): consider linetos (l/L) with |dx|+|dy|. If a path has >=MINSEG linetos,
find the largest lineto; if it lies in the tail (index >= TAILFRAC of the lineto
sequence), and its magnitude > ABS and > MULT * median(other linetos), cut the path
from that segment onward. Legit long edges live in tiny (2-seg) paths -> untouched.

Usage: python tools/strip_spline2.py <in.svg> [<out.svg>]   (default in-place)
Env: ABS (40000), MULT (3.0), MINSEG (6), TAILFRAC (0.5), BACKABS (10000)
BACKABS: after locating the largest lineto, walk backward while segments stay
above BACKABS so the WHOLE contiguous control-polygon run is removed, not just
from its peak (the polygon can have big segments before and after its max).
"""
import re, sys, os
from statistics import median

ABS = int(os.environ.get("ABS", "40000"))
MULT = float(os.environ.get("MULT", "3.0"))
MINSEG = int(os.environ.get("MINSEG", "6"))
TAILFRAC = float(os.environ.get("TAILFRAC", "0.5"))
BACKABS = int(os.environ.get("BACKABS", "10000"))

TOKEN = re.compile(r'([mMlLcCzZ])((?:\s*-?\d+){0,6})')


def parse(d):
    toks = []
    for c, nums in TOKEN.findall(d):
        vals = [int(x) for x in re.findall(r'-?\d+', nums)]
        toks.append((c, vals))
    return toks


def rebuild(toks):
    s = []
    for c, v in toks:
        if c in 'zZ':
            s.append('Z')
        else:
            s.append(c + ' ' + ' '.join(str(x) for x in v))
    return ' '.join(s).strip()


def cut(d):
    toks = parse(d)
    lines = [(i, abs(v[0]) + abs(v[1])) for i, (c, v) in enumerate(toks)
             if c in 'lL' and len(v) >= 2 and (abs(v[0]) + abs(v[1])) > 0]
    if len(lines) < MINSEG:
        return d, 0
    kmax = max(range(len(lines)), key=lambda k: lines[k][1])
    ti, mmax = lines[kmax]
    others = [m for k, (i, m) in enumerate(lines) if k != kmax]
    med = median(others) if others else 0
    if (kmax >= len(lines) * TAILFRAC and mmax > ABS and med > 0 and mmax > MULT * med):
        # walk backward to the start of the contiguous big-segment run (whole control polygon)
        start = kmax
        while start - 1 >= 0 and lines[start - 1][1] > BACKABS:
            start -= 1
        cut_ti = lines[start][0]
        removed = len(toks) - cut_ti
        return rebuild(toks[:cut_ti]), removed
    return d, 0


def main():
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else path
    t = open(path, encoding='utf-8').read()
    report = []
    for m in list(re.finditer(r'<path d="([^"]+)" class="(C\d)"', t)):
        d, cls = m.group(1), m.group(2)
        nd, removed = cut(d)
        if removed > 0:
            t = t.replace(f'<path d="{d}" class="{cls}"', f'<path d="{nd}" class="{cls}"')
            report.append((cls, removed))
    open(out, 'w', encoding='utf-8').write(t)
    print(f'{os.path.basename(path)}: tagliati {len(report)} path -> {report}')


if __name__ == '__main__':
    main()
