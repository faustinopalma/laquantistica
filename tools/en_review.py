import re, sys, glob, os
# Estrae il testo degli span EN e segnala possibili residui italiani / anomalie.
it_markers = re.compile(r'\b(della|degli|delle|dello|nella|nello|negli|perch\u00e9|perche|quindi|abbiamo|questo|questa|scheda|esperimento|grandezza|autostato|autovalore|sono|viene|essere|dalla|nell|dell|sull|misura|probabilit\u00e0|particella|quantistica|elettrone|energia|atomo|vettore|matrice|numero|figura|come|anche|molto|senza|dopo|sempre|ogni|questi|queste|cio\u00e8|oppure|inoltre|infatti|possiamo|dobbiamo|stato|stati|tutti|tutte)\b', re.I)
# parole che POSSONO essere legittime in EN, escludi dai falsi positivi note
allow = set()
rows = []
for path in sorted(glob.glob(sys.argv[1])):
    base = os.path.basename(path)
    t = open(path, encoding='utf-8').read()
    # tutti gli span/elementi con class contenente "en"
    for m in re.finditer(r'<span class="(?:ttl )?en">(.*?)</span>', t, re.S):
        inner = m.group(1)
        plain = re.sub(r'<[^>]+>', '', inner)
        plain = plain.replace('\u2019', "'")
        plain = ' '.join(plain.split())
        if not plain:
            continue
        hits = set(x.lower() for x in it_markers.findall(plain))
        if hits:
            rows.append((base, sorted(hits), plain[:150]))
print(f'FLAGGED EN spans: {len(rows)}')
for base, hits, txt in rows:
    print(f'[{base}] {",".join(hits)}  ::  {txt}')
