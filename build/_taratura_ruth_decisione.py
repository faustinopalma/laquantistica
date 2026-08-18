# -*- coding: utf-8 -*-
"""Perche' la taratura di lab-05 NON va toccata.

Si legge la tabella del capitolo COME E' STAMPATA (angolo = lettura del goniometro),
che e' l'unica lettura legittima per un laboratorio allineato per costruzione:
lo spostamento di 1,2 gradi e' un difetto dell'apparato della tesi, non della fisica,
e non va ricostruito nel laboratorio.
"""
import math

RAD = math.pi / 180.0
K0 = 6.0e-5 * (5.486 / 5.5) ** 2
THS = 6.0

# (lettura, N, dt) — ramo positivo e ramo negativo della tabella del capitolo 5
PIU = [(0, 3059, 120), (2.5, 1736, 120), (5, 868, 120), (10, 84, 120),
       (15, 20, 125), (20, 20, 333), (25, 20, 526), (30, 20, 1000)]
MENO = [(1.2, 3201, 120), (2.5, 3089, 120), (5, 1796, 120), (7.5, 873, 120),
        (10, 268, 120), (15, 50, 120), (20, 20, 200), (25, 20, 286), (30, 20, 1053)]


def forma(th):
    """la legge del laboratorio a meno di K: coda di Rutherford vista con risoluzione THS"""
    return 1.0 / (math.sin(th * RAD / 2) ** 2 + math.sin(THS * RAD / 2) ** 2) ** 2


def lab(th):
    return 18 * math.exp(-(th / 4.0) ** 2) + K0 * forma(th)


print("=== 1. i due rami della tabella, alla stessa lettura ===")
print(" lett     ramo +     ramo -   rapporto")
for th in (5, 10, 15, 20, 25, 30):
    a = next(n / dt for t, n, dt in PIU if t == th)
    b = next(n / dt for t, n, dt in MENO if t == th)
    print("%5d  %9.4f  %9.4f      %.2f" % (th, a, b, max(a, b) / min(a, b)))
print("Il disaccordo INTERNO alla tabella arriva a 3,2. Uno scarto del laboratorio")
print("piu' piccolo di questo sta sotto il rumore del dato di riferimento.")

print("\n=== 2. il ramo + non e' una curva a K costante ===")
print(" lett     N/dt      K = (N/dt)/forma(th)   err.stat.")
for th, n, dt in PIU:
    if th < 10:
        continue
    print("%5d  %8.4f        %.3e          +-%2.0f%%"
          % (th, n / dt, (n / dt) / forma(th), 100 / math.sqrt(n)))
print("K sale di un fattore 2,2 fra 10 e 30 gradi DENTRO lo stesso ramo:")
print("nessun modello a K unico puo' riprodurre tutto il ramo. Si sceglie dove starci.")

print("\n=== 3. dove sta oggi K0: e' la massima verosimiglianza del ramo + ===")
for soglia in (10, 15, 20, 25):
    dati = [(t, n, dt) for t, n, dt in PIU if t >= soglia]
    sn = sum(n for _, n, dt in dati)
    sd = sum(dt * forma(t) for t, n, dt in dati)
    print("  ramo +, th >= %2d gradi : K = %.3e  (oggi %.3e, x%.2f)  [%4d conteggi, +-%.0f%%]"
          % (soglia, sn / sd, K0, (sn / sd) / K0, sn, 100 / math.sqrt(sn)))

print("\n=== 4. quanto vale lo scarto residuo, punto per punto ===")
print(" lett     tesi        lab     lab/tesi   err.stat.   scarto")
for th, n, dt in PIU:
    if th < 10:
        continue
    mis, sim = n / dt, lab(th)
    s = 100 / math.sqrt(n)
    print("%5d  %8.4f  %9.4f     %5.2f     +-%2.0f%%     %4.1f sigma"
          % (th, mis, sim, sim / mis, s, abs(math.log(sim / mis)) / (s / 100)))

print("\n=== 5. e se si alzasse K0 per prendere i due punti a 25-30 gradi? ===")
for f in (1.0, 1.6):
    print("  K0 x%.1f :" % f, end=" ")
    for th in (10, 15, 20, 25, 30):
        mis = next(n / dt for t, n, dt in PIU if t == th)
        sim = 18 * math.exp(-(th / 4.0) ** 2) + K0 * f * forma(th)
        print("%2d: %.2f |" % (th, sim / mis), end=" ")
    print("  picco a 0 gradi = %.1f s^-1 (tesi 25,5)" % (18 + K0 * f * forma(0.0)))
print("Guadagnare due punti da venti conteggi al prezzo di tre punti che oggi tornano,")
print("e di un picco sbagliato del 20%, non e' un miglioramento.")

print("\n=== 6. tempo per venti impulsi, come lo dice la pagina ===")
for th in (25, 30):
    print("  th=%2d  lab: %.0f s = %.1f min" % (th, 20 / lab(th), 20 / lab(th) / 60))
print("  la pagina dice \"a 30 gradi ci vuole piu' di mezz'ora\": sono 27 minuti.")
