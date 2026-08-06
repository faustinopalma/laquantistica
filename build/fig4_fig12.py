"""Ridisegna la Fig.4 del Cap.4 (campana della previsione classica) e ritaglia la Fig.12."""
import math
import re
from pathlib import Path

IMG = Path("publish/img/04_diffrazione")

# --- Fig.4: campana ridisegnata, ritagliata, con assi e simboli ---------------
W, H = 1000, 560
X0, XPEAK = 500, 500          # asse P coincide con delta = 0
BASE, TOP = 470, 90           # linea di base e vertice della campana
SIGMA = 95.0

pts = []
x = XPEAK - 3.4 * SIGMA          # oltre 3.4 sigma la curva e' sull'asse: la tratterebbe due volte
while x <= XPEAK + 3.4 * SIGMA + 0.001:
    y = BASE - (BASE - TOP) * math.exp(-((x - XPEAK) ** 2) / (2 * SIGMA ** 2))
    pts.append(f"{x:.0f},{y:.1f}")
    x += 5
curva = "M " + " L ".join(pts)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="180mm" height="{180 * H / W:.1f}mm" viewBox="0 0 {W} {H}" role="img">
 <g fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round">
  <path stroke-width="5" d="M 40,{BASE} L 960,{BASE}"/>
  <path stroke-width="5" fill="#000" stroke="none" d="M 985,{BASE} L 953,{BASE - 11} L 953,{BASE + 11} Z"/>
  <path stroke-width="5" d="M {X0},{BASE + 20} L {X0},50"/>
  <path fill="#000" stroke="none" d="M {X0},25 L {X0 - 11},57 L {X0 + 11},57 Z"/>
  <path stroke-width="8" d="{curva}"/>
 </g>
 <g font-family="Times New Roman, Times, serif" font-size="46" font-style="italic" fill="#000">
  <text x="958" y="525">&#948;</text>
  <text x="470" y="70" text-anchor="end">P(&#948;)</text>
  <text x="484" y="518" text-anchor="end" font-style="normal">0</text>
 </g>
</svg>
'''
(IMG / "FIG4.svg").write_text(svg, encoding="utf-8")
print("FIG4.svg riscritta:", len(svg), "byte")

# --- Fig.12: stesso disegno, viewBox ridotta al contenuto --------------------
p12 = IMG / "FIG12.svg"
t = p12.read_text(encoding="utf-8")
bb = re.search(r'<rect class="BoundingBox"[^>]*x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', t)
bx, by, bw, bh = (int(v) for v in bb.groups())
pad = 90
vx, vy, vw, vh = bx - pad, by - pad, bw + 2 * pad, bh + 2 * pad
nuovo = f'width="{vw / 100:.1f}mm" height="{vh / 100:.1f}mm" viewBox="{vx} {vy} {vw} {vh}"'
t2, n = re.subn(r'width="215\.9mm" height="279\.4mm" viewBox="0 0 21590 27940"', nuovo, t, count=1)
if n:
    p12.write_text(t2, encoding="utf-8")
    print("FIG12.svg ritagliata:", nuovo)
else:
    print("FIG12.svg: gia' ritagliata, lasciata com'e'")
