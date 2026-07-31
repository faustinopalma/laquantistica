"""Immagine di anteprima per la condivisione (Open Graph), 1200x630.

Riprende i colori e i caratteri del sito: fondo carta, marchio in serif,
accento amaranto. Una versione per lingua.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

USCITA = pathlib.Path('publish/img/social')
USCITA.mkdir(parents=True, exist_ok=True)

CARTA = (245, 243, 238)
INCHIOSTRO = (31, 35, 40)
TENUE = (74, 79, 87)
ACCENTO = (123, 45, 38)
ACCENTO_CHIARO = (201, 139, 131)
LINEA = (224, 220, 207)

SERIF = 'C:/Windows/Fonts/georgia.ttf'
SERIF_B = 'C:/Windows/Fonts/georgiab.ttf'
SANS = 'C:/Windows/Fonts/segoeui.ttf'

TESTI = {
    'it': ('Esperimenti fondamentali', 'della Meccanica Quantistica',
           'Dagli esperimenti all\u2019equazione di Schr\u00f6dinger \u00b7 Tesi di laurea, edizione web'),
    'en': ('Fundamental Experiments', 'of Quantum Mechanics',
           'From the experiments to Schr\u00f6dinger\u2019s equation \u00b7 Master\u2019s thesis, web edition'),
}


def bande(d, x, y, larghezza, altezza):
    """Richiamo grafico al vetrino di Stern-Gerlach: due bande separate."""
    for k in (0, 1):
        cy = y + k * (altezza + 26)
        for i in range(altezza):
            t = abs(i - altezza / 2) / (altezza / 2)
            v = int(255 - 150 * (1 - t * t))
            d.line([(x, cy + i), (x + larghezza, cy + i)], fill=(v, v - 6, v - 12))


def chevron(d, x, y, altezza, verso, colore):
    """Le parentesi angolari del marchio: Georgia non ha i caratteri, si disegnano."""
    meta = altezza / 2
    larghezza = altezza * 0.30
    punta = x if verso < 0 else x + larghezza
    base = x + larghezza if verso < 0 else x
    d.line([(base, y), (punta, y + meta), (base, y + altezza)], fill=colore, width=3, joint='curve')


for lingua, (riga1, riga2, sotto) in TESTI.items():
    im = Image.new('RGB', (1200, 630), CARTA)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, 1200, 8], fill=ACCENTO)
    bande(d, 980, 250, 150, 46)

    marchio = ImageFont.truetype(SERIF, 40)
    chevron(d, 80, 84, 40, -1, ACCENTO_CHIARO)
    d.text((104, 78), '\u039bQ', font=marchio, fill=INCHIOSTRO)
    chevron(d, 160, 84, 40, +1, ACCENTO_CHIARO)
    d.text((196, 88), 'La Quantistica', font=ImageFont.truetype(SANS, 26), fill=TENUE)

    titolo = ImageFont.truetype(SERIF_B, 58)
    d.text((80, 210), riga1, font=titolo, fill=INCHIOSTRO)
    d.text((80, 284), riga2, font=titolo, fill=INCHIOSTRO)

    d.line([(80, 396), (300, 396)], fill=ACCENTO, width=3)
    d.text((80, 428), sotto, font=ImageFont.truetype(SANS, 25), fill=TENUE)

    d.line([(80, 540), (1120, 540)], fill=LINEA, width=1)
    d.text((80, 562), 'laquantistica.com', font=ImageFont.truetype(SANS, 23), fill=ACCENTO)

    percorso = USCITA / f'copertina-{lingua}.png'
    im.save(percorso, optimize=True)
    print(f'{percorso}: {percorso.stat().st_size // 1024} kB')
