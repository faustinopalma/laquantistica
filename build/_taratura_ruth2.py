# -*- coding: utf-8 -*-
"""Taratura della coda di lab-05 sulla tabella del capitolo 5 — seconda passata.

Differenza dalla prima: il criterio non e' la verosimiglianza di Poisson (che e'
dominata dai tre punti da 3000 conteggi vicino allo zero e trascura la coda, dove
i punti valgono venti conteggi), ma l'accordo RELATIVO pesato con l'errore
statistico di ciascun punto:  chi2 = somma di [ln(lab/tesi) / (1/sqrt(N))]^2.
E' la stessa cosa nel limite gaussiano, ma tratta allo stesso modo un punto da
25 s^-1 e uno da 0,02 s^-1, che e' quello che chiediamo al laboratorio.
"""
import math

RAD = math.pi / 180.0

TAB = [
    (0.0, 3059, 120), (2.5, 1736, 120), (5.0, 868, 120), (10.0, 84, 120),
    (15.0, 20, 125), (20.0, 20, 333), (25.0, 20, 526), (30.0, 20, 1000),
    (-1.2, 3201, 120), (-2.5, 3089, 120), (-5.0, 1796, 120), (-7.5, 873, 120),
    (-10.0, 268, 120), (-15.0, 50, 120), (-20.0, 20, 200), (-25.0, 20, 286),
    (-30.0, 20, 1053),
]
OFF = 1.2

DAT = sorted((abs(th + OFF), n, dt, th) for th, n, dt in TAB)
# stessa tabella letta INGENUAMENTE, cioe' angolo = |lettura|, come nel confronto del 17/08
DAT_NAIVE = sorted((abs(th), n, dt, th) for th, n, dt in TAB)


def rate(th, p):
    K, ths, amp, sig = p
    core = amp * math.exp(-(th / sig) ** 2)
    s = math.sin(th * RAD / 2) ** 2
    ss = math.sin(ths * RAD / 2) ** 2
    return core + K / (s + ss) ** 2


def chi2(p, dat):
    if min(p) <= 0:
        return 1e30
    t = 0.0
    for th, n, dt, _ in dat:
        r = rate(th, p)
        if r <= 0:
            return 1e30
        t += (math.log(r / (n / dt)) * math.sqrt(n)) ** 2
    return t


def ottimizza(p0, liberi, dat):
    p = list(p0)
    passo = [0.15] * 4
    for _ in range(400):
        mosso = False
        for i in liberi:
            for seg in (1 + passo[i], 1 / (1 + passo[i])):
                q = list(p)
                q[i] *= seg
                if chi2(q, dat) < chi2(p, dat) - 1e-9:
                    p = q
                    mosso = True
        if not mosso:
            passo = [x / 2 for x in passo]
            if passo[0] < 1e-5:
                break
    return p, chi2(p, dat)


def mostra(nome, p, dat):
    print('\n--- %s ---' % nome)
    print('K = %.3e   THS = %.2f gradi   amp = %.2f   sig = %.2f   chi2 = %.1f (17 punti)'
          % (p[0], p[1], p[2], p[3], chi2(p, dat)))
    print(' vero   lett     tesi        lab     lab/tesi   err.stat.')
    peggio = 1.0
    for th, n, dt, letta in dat:
        mis, lab = n / dt, rate(th, p)
        r = lab / mis
        peggio = max(peggio, r, 1 / r)
        print('%5.1f  %5.1f  %9.4f  %9.4f     %5.2f      +-%2.0f%%'
              % (th, letta, mis, lab, r, 100 / math.sqrt(n)))
    print('scarto peggiore: %.0f%%' % ((peggio - 1) * 100))


ATT = [6.0e-5 * (5.486 / 5.5) ** 2, 6.0, 18.0, 4.0]

print('=== A. modello di oggi, confronto INGENUO (angolo = lettura) ===')
mostra('oggi, lettura', ATT, DAT_NAIVE)

print('\n\n=== B. modello di oggi, confronto sull\'ANGOLO VERO (lettura + 1,2 gradi) ===')
mostra('oggi, angolo vero', ATT, DAT)

print('\n\n=== C. solo K ritarato sull\'angolo vero ===')
p, _ = ottimizza(ATT, [0], DAT)
mostra('K libero', p, DAT)

print('\n\n=== D. K e THS ritarati sull\'angolo vero ===')
p, _ = ottimizza(ATT, [0, 1], DAT)
mostra('K, THS liberi', p, DAT)

print('\n\n=== E. tutti e quattro i parametri, angolo vero ===')
p, _ = ottimizza(ATT, [0, 1, 2, 3], DAT)
mostra('tutti liberi', p, DAT)
PFULL = p

print('\n\n=== F. lo stesso modello E, ma riletto ALL\'INGENUA ===')
mostra('tutti liberi, letto sulla lettura', PFULL, DAT_NAIVE)

print('\n\n=== G. quanto vale il fascio a 30 gradi: tempo per venti impulsi ===')
for nome, p in (('oggi', ATT), ('E (tutti liberi)', PFULL)):
    for th in (25.0, 30.0):
        print('%-18s  ϑ=%4.1f  N/dt=%.4f  ->  20 impulsi in %5.0f s' %
              (nome, th, rate(th, p), 20 / rate(th, p)))
print('%-18s  ϑ=30.0  tesi: 20 impulsi in 1000 s (+30) e 1053 s (-30)' % 'tabella')
