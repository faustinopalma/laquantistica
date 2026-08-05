"""Toglie la tilde dai nomi dei file immagine (erano nomi DOS 8.3) e aggiorna i richiami.

Rinomina in publish/img e riscrive i percorsi in sorgenti/*.html; poi va rieseguito
build/i18n/split.py per rigenerare publish/it e publish/en.
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
IMG = BASE / 'publish' / 'img'
SORGENTI = BASE / 'sorgenti'

NOMI = {
    '02_stern_gerlach_cascata': {
        'EVOLUZ~1.png': 'evoluzione.png',
    },
    '03_elettroni': {
        'APPARA~1.jpg': 'microscopio-e-lampada.jpg',
        'GOCCIO~1.jpg': 'goccioline-al-microscopio.jpg',
        'NEBULI~1.png': 'nebulizzatore.png',
    },
    '04_diffrazione': {
        'DIFFRA~1.png': 'diffrazione.png',
        'FIG1~1.png': 'schema-esperimento.png',
        'FIG1~1.svg': 'schema-esperimento.svg',
        'FIG2~1.png': 'struttura-cristallina.png',
        'FIG2~1.svg': 'struttura-cristallina.svg',
        'FIG3~1.png': 'previsione-classica.png',
        'FIG3~1.svg': 'previsione-classica.svg',
    },
    '05_rutherford': {
        'ASSEMB~1.jpg': 'camera-chiusa.jpg',
        'ATTRAV~1.png': 'lamina-trasparente.png',
        'ATTRAV~1.svg': 'lamina-trasparente.svg',
        'COMPON~1.jpg': 'camera-aperta.jpg',
        'ONDELA~1.png': 'onda-piana-e-sferica.png',
        'ONDEST~1.png': 'fascio-stretto.png',
        'PREPAR~1.jpg': 'preparato-am241.jpg',
        'RESIST~1.png': 'caduta-resistenza.png',
        'RESIST~1.svg': 'caduta-resistenza.svg',
    },
    '07_franck_hertz': {
        'AMPOLL~1.jpg': 'ampolla-neon.jpg',
        'AMPOLL~1.png': 'alimentazione-elettrodi.png',
        'AMPOLL~1.svg': 'alimentazione-elettrodi.svg',
        'APPARA~1.jpg': 'apparato-mercurio-1.jpg',
        'APPARA~2.jpg': 'apparato-mercurio-2.jpg',
        'APPARA~3.jpg': 'apparato-neon.jpg',
        'BANDED~1.png': 'zone-luminose.png',
        'DIAGRA~1.png': 'corrente-tensione.png',
        'DIAGRA~1.svg': 'corrente-tensione.svg',
        'DISPLA~1.jpg': 'oscilloscopio-neon.jpg',
        'DISPLA~2.jpg': 'oscilloscopio-mercurio.jpg',
    },
    '08_effetto_fotoelettrico': {
        'AMPOLL~1.jpg': 'ampolla-su-supporto.jpg',
        'AMPOLL~1.png': 'misura-energia.png',
        'AMPOLL~1.svg': 'misura-energia.svg',
        'AMPOLL~1-en.svg': 'misura-energia-en.svg',
        'AMPOLL~2.png': 'sistema-rilevazione.png',
        'AMPOLL~2.svg': 'sistema-rilevazione.svg',
        'AMPOLL~2-en.svg': 'sistema-rilevazione-en.svg',
        'BANCOO~1.jpg': 'banco-ottico.jpg',
        'EMISSI~1.png': 'emissione.png',
        'EMISSI~1.svg': 'emissione.svg',
        'EMISSI~1-en.svg': 'emissione-en.svg',
        'FILTRO~1.jpg': 'filtro-blu.jpg',
        'FILTRO~2.jpg': 'filtro-giallo.jpg',
        'LAMPAD~1.jpg': 'lampada-mercurio.jpg',
        'SEPARA~1.png': 'separatore-impedenza.png',
        'SEPARA~1.svg': 'separatore-impedenza.svg',
        'SEPARA~1-en.svg': 'separatore-impedenza-en.svg',
        'SOLOVO~1.png': 'solo-voltmetro.png',
        'SOLOVO~1.svg': 'solo-voltmetro.svg',
        'SOLOVO~1-en.svg': 'solo-voltmetro-en.svg',
    },
    '09_spettri_atomici': {
        'APPARA~1.jpg': 'apparato-1.jpg',
        'APPARA~2.jpg': 'apparato-2.jpg',
        'APPARA~3.jpg': 'banco-ottico.jpg',
        'IMMAGI~1.jpg': 'immagine-sullo-schermo.jpg',
        'LAMPAD~1.jpg': 'lampada-mercurio.jpg',
        'LAMPAD~1.png': 'lampada-balmer.png',
        'LAMPAD~2.png': 'lampada-balmer-2.png',
        'LAMPAD~3.png': 'lampada-balmer-3.png',
        'LUCIME~1.jpg': 'luce-mercurio.jpg',
        'NEONAC~1.jpg': 'neon-acceso.jpg',
        'RETICO~1.jpg': 'reticolo.jpg',
        'SPETTO~1.png': 'spettrometro.png',
    },
}

attesi = sorted(p for p in IMG.rglob('*') if '~' in p.name)
dichiarati = {(c, n) for c, m in NOMI.items() for n in m}
trovati = {(p.parent.name, p.name) for p in attesi}
if trovati != dichiarati:
    print('mancano dalla tabella:', sorted(trovati - dichiarati))
    print('nella tabella ma assenti:', sorted(dichiarati - trovati))
    sys.exit('tabella e cartella non coincidono')

rinominati = 0
for cartella, mappa in NOMI.items():
    for vecchio, nuovo in mappa.items():
        a = IMG / cartella / vecchio
        b = IMG / cartella / nuovo
        if b.exists():
            sys.exit(f'{b} esiste gia\'')
        a.rename(b)
        rinominati += 1

sostituzioni = 0
for f in sorted(SORGENTI.glob('*.html')):
    t = f.read_text(encoding='utf-8')
    originale = t
    for cartella, mappa in NOMI.items():
        for vecchio, nuovo in mappa.items():
            t, n = re.subn(re.escape(f'img/{cartella}/{vecchio}'), f'img/{cartella}/{nuovo}', t)
            sostituzioni += n
    if t != originale:
        f.write_text(t, encoding='utf-8')

resti = [p for p in IMG.rglob('*') if '~' in p.name]
resti += [f.name for f in SORGENTI.glob('*.html') if re.search(r'img/[^"]*~', f.read_text(encoding='utf-8'))]
print(f'file rinominati: {rinominati}')
print(f'richiami aggiornati: {sostituzioni}')
print(f'tilde rimaste: {len(resti)}')
for r in resti:
    print(f'  {r}')
