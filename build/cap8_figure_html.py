"""Aggancia alla scheda 8 le figure con le scritte, una versione per lingua."""
from pathlib import Path

P = Path('sorgenti/08-effetto-fotoelettrico.html')
s = P.read_text(encoding='utf-8')

# nome del file: (alt italiano, alt inglese)
FIGURE = {
    'EMISSI~1.svg': ('L\u2019effetto fotoelettrico: la luce estrae elettroni dal metallo.',
                     'The photoelectric effect: light extracts electrons from the metal.'),
    'AMPOLL~2.svg': ('Sistema di rilevazione: catodo, anodo e corrente fotoelettrica.',
                     'Detection system: cathode, anode and photoelectric current.'),
    'AMPOLL~1.svg': ('Sistema per misurare l\u2019energia degli elettroni (condensatore).',
                     'System for measuring the energy of the electrons (capacitor).'),
    'SOLOVO~1.svg': ('Con un normale voltmetro la corrente fotoelettrica si richiude sul voltmetro.',
                     'With an ordinary voltmeter the photoelectric current closes through the voltmeter.'),
    'SEPARA~1.svg': ('Il separatore di impedenza per misurare la tensione.',
                     'The impedance buffer used to measure the voltage.'),
}

for nome, (alt_it, alt_en) in FIGURE.items():
    i = s.find('src="img/08_effetto_fotoelettrico/%s' % nome)
    assert i > 0, nome
    a = s.rfind('<img', 0, i)
    b = s.find('>', i) + 1
    en = nome.replace('.svg', '-en.svg')
    nuovo = ('<img class="it" loading="lazy" src="img/08_effetto_fotoelettrico/%s?v=3" alt="%s">'
             '<img class="en" loading="lazy" src="img/08_effetto_fotoelettrico/%s?v=1" alt="%s">'
             % (nome, alt_it, en, alt_en))
    s = s[:a] + nuovo + s[b:]

P.write_text(s, encoding='utf-8', newline='')
print(f'scheda 8: {len(FIGURE)} figure sdoppiate per lingua')
