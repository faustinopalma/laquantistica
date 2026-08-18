# -*- coding: utf-8 -*-
"""Quarta passata: la proposta esatta come sarebbe scritta nel sorgente,
vista sia sull'angolo vero sia sulla lettura del goniometro della tesi."""
import math

RAD = math.pi / 180.0
TAB = [
    (0.0, 3059, 120), (2.5, 1736, 120), (5.0, 868, 120), (10.0, 84, 120),
    (15.0, 20, 125), (20.0, 20, 333), (25.0, 20, 526), (30.0, 20, 1000),
    (-1.2, 3201, 120), (-2.5, 3089, 120), (-5.0, 1796, 120), (-7.5, 873, 120),
    (-10.0, 268, 120), (-15.0, 50, 120), (-20.0, 20, 200), (-25.0, 20, 286),
    (-30.0, 20, 1053),
]

E0, THS = 5.486, 6.0


def rate(th, K0, A0, SGEO, SMS, slit=1, Ea=5.5):
    Kof = K0 * slit * (E0 / Ea) ** 2
    amp = A0 * slit
    sig = math.hypot(SGEO * slit ** 0.6, SMS)
    s = math.sin(th * RAD / 2) ** 2
    ss = math.sin(THS * RAD / 2) ** 2
    return amp * math.exp(-(th / sig) ** 2) + Kof / (s + ss) ** 2


OGGI = dict(K0=6.0e-5, A0=18.0, SGEO=4.0, SMS=0.0)
NUOVO = dict(K0=9.3e-5, A0=13.0, SGEO=4.0, SMS=3.9)

print('=== confronto sull ANGOLO VERO (lettura + 1,2) ===')
print(' vero   lett     tesi      oggi   r      nuovo   r')
for th, n, dt in sorted(TAB, key=lambda x: abs(x[0] + 1.2)):
    v, m = abs(th + 1.2), n / dt
    a, b = rate(v, **OGGI), rate(v, **NUOVO)
    print('%5.1f  %5.1f  %8.4f  %8.4f %5.2f  %8.4f %5.2f' % (v, th, m, a, a / m, b, b / m))

print('\n=== confronto sulla LETTURA del goniometro (quello del 17/08) ===')
print(' lett     tesi      oggi   r      nuovo   r')
for th, n, dt in sorted(TAB, key=lambda x: (abs(x[0]), x[0])):
    v, m = abs(th), n / dt
    a, b = rate(v, **OGGI), rate(v, **NUOVO)
    print('%5.1f  %8.4f  %8.4f %5.2f  %8.4f %5.2f' % (th, m, a, a / m, b, b / m))

print('\n=== tempi per venti impulsi (fenditura 1 mm, oro, 5,5 MeV) ===')
for th in (20.0, 25.0, 30.0):
    print(' ϑ=%2.0f  oggi %6.0f s   nuovo %6.0f s' % (th, 20 / rate(th, **OGGI), 20 / rate(th, **NUOVO)))
print(' tesi: 20 impulsi in 333 s (20 gradi), 526 s (25), 1000/1053 s (30)')

print('\n=== fascio a ϑ=0 ===')
for nome, p in (('oggi', OGGI), ('nuovo', NUOVO)):
    print(' %-6s %6.2f s^-1   (tesi: 25,5 letto a 0 gradi, 26,7 al massimo vero)'
          % (nome, rate(0.0, **p)))

print('\n=== fenditura 5 mm: la coda resta leggibile? ===')
for nome, p in (('oggi', OGGI), ('nuovo', NUOVO)):
    sig = math.hypot(p['SGEO'] * 5 ** 0.6, p['SMS'])
    for th in (25.0, 30.0):
        tot = rate(th, slit=5, **p)
        core = p['A0'] * 5 * math.exp(-(th / sig) ** 2)
        print('  %-6s ϑ=%2.0f  sig=%5.2f  totale=%.4f  di cui fascio %.4f (%.0f%%)'
              % (nome, th, sig, tot, core, 100 * core / tot))

print('\n=== stima di Z a 25 e 30 gradi (deve restare 79) ===')
for nome, p in (('oggi', OGGI), ('nuovo', NUOVO)):
    base = p['K0'] * 1 * (E0 / 5.5) ** 2
    for th in (25.0, 30.0):
        r = rate(th, **p)
        core = p['A0'] * math.exp(-(th / math.hypot(p['SGEO'], p['SMS'])) ** 2)
        s, ss = math.sin(th * RAD / 2) ** 2, math.sin(THS * RAD / 2) ** 2
        z = 79 * math.sqrt((r - core) * (s + ss) ** 2 / base)
        print('  %-6s ϑ=%2.0f  Z = %.2f' % (nome, th, z))

print('\n=== energia diversa: 4 e 7 MeV a 30 gradi (rapporto atteso (E0/E)^2) ===')
for Ea in (4.0, 5.5, 7.0):
    print('  E=%.1f MeV  nuovo N/dt(30) = %.4f' % (Ea, rate(30.0, Ea=Ea, **NUOVO)))
