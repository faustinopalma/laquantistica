# -*- coding: utf-8 -*-
"""Terza passata: varianti VINCOLATE, per scegliere numeri difendibili.

La larghezza del fascio diretto viene separata in due contributi che si sommano
in quadratura: la divergenza geometrica del collimatore (4*slit^0.6 gradi, quella
di oggi) e l'allargamento per diffusione multipla nella lamina, che NON dipende
dalla fenditura. Per alfa da 5,5 MeV su 2 um d'oro la formula di Highland da'
theta_rms proiettato ~ 3,5 gradi.
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
DAT = sorted((abs(th + 1.2), n, dt, th) for th, n, dt in TAB)


def rate(th, K, ths, amp, sig):
    s = math.sin(th * RAD / 2) ** 2
    ss = math.sin(ths * RAD / 2) ** 2
    return amp * math.exp(-(th / sig) ** 2) + K / (s + ss) ** 2


def chi2(K, ths, amp, sig):
    t = 0.0
    for th, n, dt, _ in DAT:
        r = rate(th, K, ths, amp, sig)
        if r <= 0:
            return 1e30
        t += (math.log(r / (n / dt)) * math.sqrt(n)) ** 2
    return t


def ott(p, liberi):
    p = list(p)
    passo = 0.15
    while passo > 1e-5:
        mosso = False
        for i in liberi:
            for seg in (1 + passo, 1 / (1 + passo)):
                q = list(p)
                q[i] *= seg
                if chi2(*q) < chi2(*p) - 1e-9:
                    p, mosso = q, True
        if not mosso:
            passo /= 2
    return p


def riga(nome, p):
    peggio = max(max(rate(th, *p) / (n / dt), (n / dt) / rate(th, *p))
                 for th, n, dt, _ in DAT)
    r25, r30 = rate(25.0, *p), rate(30.0, *p)
    r0 = rate(0.0, *p)
    print('%-34s K=%.3e THS=%.2f amp=%.2f sig=%.2f | chi2=%6.1f peggio=%3.0f%% '
          '| 0gradi=%5.2f | 25gradi:%4.0fs 30gradi:%5.0fs'
          % (nome, p[0], p[1], p[2], p[3], chi2(*p), (peggio - 1) * 100, r0,
             20 / r25, 20 / r30))


ATT = [6.0e-5 * (5.486 / 5.5) ** 2, 6.0, 18.0, 4.0]
print('tesi: 0 gradi = 26,7 s^-1 | 25 gradi = 526 s | 30 gradi = 1000 s (+30) e 1053 s (-30)\n')
riga('oggi', ATT)
riga('tutti liberi', ott(ATT, [0, 1, 2, 3]))
riga('THS bloccato a 6', ott([1e-4, 6.0, 13.0, 5.6], [0, 2, 3]))
riga('THS=6, amp bloccata a 18', ott([1e-4, 6.0, 18.0, 5.6], [0, 3]))
riga('THS=6, sig bloccata a 4', ott([1e-4, 6.0, 13.0, 4.0], [0, 2]))

print('\nvalori arrotondati che si scriverebbero nel sorgente:')
for K, ths, amp, sig in [(9.3e-5, 6.0, 13.0, 5.6), (9.3e-5, 6.0, 12.8, 5.6),
                         (9.5e-5, 6.0, 13.0, 5.5), (9.0e-5, 6.0, 13.0, 5.6)]:
    riga('K0=%.1e amp=%.1f sig=%.1f' % (K, amp, sig), [K * (5.486 / 5.5) ** 2, ths, amp, sig])

P = [9.3e-5 * (5.486 / 5.5) ** 2, 6.0, 13.0, 5.6]
print('\n--- scelta proposta, punto per punto ---')
print(' vero   lett     tesi        lab     lab/tesi   err.stat.')
for th, n, dt, letta in DAT:
    print('%5.1f  %5.1f  %9.4f  %9.4f     %5.2f      +-%2.0f%%'
          % (th, letta, n / dt, rate(th, *P), rate(th, *P) / (n / dt), 100 / math.sqrt(n)))

print('\n--- larghezza del fascio: quadratura collimatore + diffusione multipla ---')
GEO = 4.0
sms = math.sqrt(5.6 ** 2 - GEO ** 2)
print('sig(slit=1) = 5.6 gradi  ->  parte da diffusione multipla = %.2f gradi' % sms)
print('(Highland per alfa 5,5 MeV su 2 um di Au: theta_rms proiettato ~ 3,5 gradi)')
for sl in (1, 5):
    geo = GEO * sl ** 0.6
    print('  fenditura %d mm: geometrica %.2f  ->  totale %.2f gradi  (oggi: %.2f)'
          % (sl, geo, math.hypot(geo, sms), geo))

print('\n--- fenditura 5 mm: la coda di Rutherford resta leggibile a 25-30 gradi? ---')
for nome, amp0, sigf in (('oggi', 18.0, lambda sl: 4.0 * sl ** 0.6),
                         ('proposta', 13.0, lambda sl: math.hypot(4.0 * sl ** 0.6, sms))):
    K0 = 6.0e-5 if nome == 'oggi' else 9.3e-5
    for sl in (1, 5):
        for th in (25.0, 30.0):
            core = amp0 * sl * math.exp(-(th / sigf(sl)) ** 2)
            s = math.sin(th * RAD / 2) ** 2
            ss = math.sin(6.0 * RAD / 2) ** 2
            tail = K0 * (5.486 / 5.5) ** 2 * sl / (s + ss) ** 2
            print('  %-9s fend.%dmm  ϑ=%2.0f  coda=%.4f  fascio=%.4f  fascio/coda=%.3f'
                  % (nome, sl, th, tail, core, core / tail))
