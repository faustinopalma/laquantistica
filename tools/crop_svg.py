#!/usr/bin/env python
"""crop_svg.py — split a composite DWG-derived SVG into sub-figures by spatial clustering.

The DWG->SVG files are a flat list of <path d="..." class="Cx"/> with no grouping.
Sub-figures are separated by whitespace. This tool computes each path's bounding box,
clusters paths whose boxes are near each other (gap-based union-find), and can emit a
cropped SVG per cluster with its own viewBox.

Usage:
  python tools/crop_svg.py analyze <in.svg> [gap_frac]
      Print clusters: index, bbox (in user units), path count. gap_frac default 0.03.
  python tools/crop_svg.py extract <in.svg> <cluster_index> <out.svg> [gap_frac] [margin_frac]
      Write a cropped SVG containing only the paths of that cluster.

Notes:
- Coordinates are absolute user units of the source viewBox.
- margin_frac (default 0.04) pads the crop box by that fraction of the cluster's max side.
"""
import re
import sys

PATH_RE = re.compile(r'<path\b[^>]*\bd="([^"]*)"[^>]*>')
CLASS_RE = re.compile(r'class="([^"]*)"')
VIEWBOX_RE = re.compile(r'viewBox="([^"]*)"')
SVG_OPEN_RE = re.compile(r'<svg\b[^>]*>')
DEFS_RE = re.compile(r'<defs>.*?</defs>', re.S)
# tokenizer for path data: a command letter or a signed float number
TOK_RE = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)')


def path_points(d):
    """Yield (x, y) absolute points touched by the path d-string.

    Handles M/m L/l H/h V/v C/c S/s Q/q T/t Z/z. For curve commands we take the
    control points and endpoint (an over-estimate of the bbox, which is fine here).
    """
    toks = TOK_RE.findall(d)
    # flatten to a stream with type markers
    stream = []
    for cmd, num in toks:
        if cmd:
            stream.append(('c', cmd))
        else:
            stream.append(('n', float(num)))
    i = 0
    cx = cy = 0.0
    sx = sy = 0.0  # subpath start
    cur = None

    def nextnums(k):
        nonlocal i
        vals = []
        while len(vals) < k and i < len(stream) and stream[i][0] == 'n':
            vals.append(stream[i][1])
            i += 1
        return vals

    n = len(stream)
    while i < n:
        typ, val = stream[i]
        if typ == 'c':
            cur = val
            i += 1
        # implicit repeat: cur stays the same for following number runs
        if cur in ('M', 'L'):
            v = nextnums(2)
            if len(v) < 2:
                break
            cx, cy = v[0], v[1]
            if cur == 'M':
                sx, sy = cx, cy
                cur = 'L'  # subsequent pairs are lineto
            yield cx, cy
        elif cur in ('m', 'l'):
            v = nextnums(2)
            if len(v) < 2:
                break
            cx, cy = cx + v[0], cy + v[1]
            if cur == 'm':
                sx, sy = cx, cy
                cur = 'l'
            yield cx, cy
        elif cur == 'H':
            v = nextnums(1)
            if not v:
                break
            cx = v[0]
            yield cx, cy
        elif cur == 'h':
            v = nextnums(1)
            if not v:
                break
            cx += v[0]
            yield cx, cy
        elif cur == 'V':
            v = nextnums(1)
            if not v:
                break
            cy = v[0]
            yield cx, cy
        elif cur == 'v':
            v = nextnums(1)
            if not v:
                break
            cy += v[0]
            yield cx, cy
        elif cur in ('C', 'c'):
            v = nextnums(6)
            if len(v) < 6:
                break
            if cur == 'C':
                pts = [(v[0], v[1]), (v[2], v[3]), (v[4], v[5])]
            else:
                pts = [(cx + v[0], cy + v[1]), (cx + v[2], cy + v[3]), (cx + v[4], cy + v[5])]
            for px, py in pts:
                yield px, py
            cx, cy = pts[-1]
        elif cur in ('S', 's', 'Q', 'q'):
            v = nextnums(4)
            if len(v) < 4:
                break
            if cur.isupper():
                pts = [(v[0], v[1]), (v[2], v[3])]
            else:
                pts = [(cx + v[0], cy + v[1]), (cx + v[2], cy + v[3])]
            for px, py in pts:
                yield px, py
            cx, cy = pts[-1]
        elif cur in ('T', 't'):
            v = nextnums(2)
            if len(v) < 2:
                break
            if cur == 'T':
                cx, cy = v[0], v[1]
            else:
                cx, cy = cx + v[0], cy + v[1]
            yield cx, cy
        elif cur in ('A', 'a'):
            v = nextnums(7)
            if len(v) < 7:
                break
            if cur == 'A':
                cx, cy = v[5], v[6]
            else:
                cx, cy = cx + v[5], cy + v[6]
            yield cx, cy
        elif cur in ('Z', 'z'):
            cx, cy = sx, sy
        else:
            # unknown / stray number without command
            i += 1


def path_bbox(d):
    xs0 = ys0 = 1e18
    xs1 = ys1 = -1e18
    for x, y in path_points(d):
        if x < xs0:
            xs0 = x
        if y < ys0:
            ys0 = y
        if x > xs1:
            xs1 = x
        if y > ys1:
            ys1 = y
    if xs1 < xs0:
        return None
    return (xs0, ys0, xs1, ys1)


def load_paths(svg):
    paths = []
    for m in PATH_RE.finditer(svg):
        d = m.group(1)
        bb = path_bbox(d)
        if bb is None:
            continue
        paths.append({'d': d, 'full': m.group(0), 'bbox': bb})
    return paths


def boxes_near(a, b, gap):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    # expand a by gap, test overlap with b
    return not (ax1 + gap < bx0 or bx1 + gap < ax0 or ay1 + gap < by0 or by1 + gap < ay0)


def cluster(paths, gap):
    n = len(paths)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # naive O(n^2); fine for a few thousand paths
    for i in range(n):
        for j in range(i + 1, n):
            if boxes_near(paths[i]['bbox'], paths[j]['bbox'], gap):
                union(i, j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    clusters = []
    for _, idxs in groups.items():
        x0 = min(paths[k]['bbox'][0] for k in idxs)
        y0 = min(paths[k]['bbox'][1] for k in idxs)
        x1 = max(paths[k]['bbox'][2] for k in idxs)
        y1 = max(paths[k]['bbox'][3] for k in idxs)
        clusters.append({'idxs': idxs, 'bbox': (x0, y0, x1, y1)})
    # order left-to-right, top-to-bottom (row-major with band tolerance)
    clusters.sort(key=lambda c: (round(c['bbox'][1] / 50000), c['bbox'][0]))
    return clusters


def get_viewbox(svg):
    m = VIEWBOX_RE.search(svg)
    if not m:
        return None
    return [float(v) for v in m.group(1).split()]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    inp = sys.argv[2]
    with open(inp, 'r', encoding='utf-8') as f:
        svg = f.read()
    vb = get_viewbox(svg)
    paths = load_paths(svg)
    if mode == 'analyze':
        gap_frac = float(sys.argv[3]) if len(sys.argv) > 3 else 0.03
        gap = gap_frac * (vb[2] if vb else 1000000)
        cl = cluster(paths, gap)
        print(f"viewBox: {vb}  paths: {len(paths)}  gap: {gap:.0f} ({gap_frac})")
        for i, c in enumerate(cl):
            x0, y0, x1, y1 = c['bbox']
            print(f"[{i}] paths={len(c['idxs']):4d}  bbox=({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})"
                  f"  size={x1-x0:.0f}x{y1-y0:.0f}")
        return
    if mode == 'extract':
        # cluster index may be a comma-separated list to merge several clusters
        idx_list = [int(v) for v in sys.argv[3].split(',')]
        out = sys.argv[4]
        gap_frac = float(sys.argv[5]) if len(sys.argv) > 5 else 0.03
        margin_frac = float(sys.argv[6]) if len(sys.argv) > 6 else 0.04
        gap = gap_frac * (vb[2] if vb else 1000000)
        cl = cluster(paths, gap)
        for ci in idx_list:
            if ci < 0 or ci >= len(cl):
                print(f"cluster index {ci} out of range 0..{len(cl)-1}")
                sys.exit(2)
        sel = []
        for ci in idx_list:
            sel.extend(cl[ci]['idxs'])
        x0 = min(paths[k]['bbox'][0] for k in sel)
        y0 = min(paths[k]['bbox'][1] for k in sel)
        x1 = max(paths[k]['bbox'][2] for k in sel)
        y1 = max(paths[k]['bbox'][3] for k in sel)
        c = {'idxs': sel, 'bbox': (x0, y0, x1, y1)}
        ci = idx_list
        w = x1 - x0
        h = y1 - y0
        margin = margin_frac * max(w, h)
        vx0, vy0 = x0 - margin, y0 - margin
        vw, vh = w + 2 * margin, h + 2 * margin
        defs = DEFS_RE.search(svg)
        defs_str = defs.group(0) if defs else ''
        # display size in mm proportional to source aspect
        wmm = 200.0
        hmm = wmm * vh / vw if vw else 100.0
        body = ''.join(paths[k]['full'] for k in c['idxs'])
        out_svg = (
            f"<?xml version='1.0' encoding='utf-8'?>\n"
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{wmm:.1f}mm" height="{hmm:.1f}mm" '
            f'viewBox="{vx0:.0f} {vy0:.0f} {vw:.0f} {vh:.0f}">'
            f'{defs_str}'
            f'<rect fill="#ffffff" x="{vx0:.0f}" y="{vy0:.0f}" width="{vw:.0f}" height="{vh:.0f}" fill-opacity="1.0" />'
            f'<g stroke-linecap="round" stroke-linejoin="round">{body}</g>'
            f'</svg>\n'
        )
        with open(out, 'w', encoding='utf-8') as f:
            f.write(out_svg)
        print(f"wrote {out}: cluster {ci} bbox=({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) "
              f"paths={len(c['idxs'])} viewBox=({vx0:.0f} {vy0:.0f} {vw:.0f} {vh:.0f})")
        return
    print("unknown mode", mode)
    sys.exit(1)


if __name__ == '__main__':
    main()
