from pathlib import Path

p = Path('sorgenti/08-effetto-fotoelettrico.html')
s = p.read_text(encoding='utf-8')

coppie = [
    ('Se per caso la frequenza della luce \u00e8 troppo bassa',
     'Se la frequenza della luce \u00e8 troppo bassa'),
    ('If by chance the frequency of the light is too low',
     'If the frequency of the light is too low'),
    ('che lo lega al metallo ed, una volta fuori',
     'che lo lega al metallo e, una volta fuori'),
]
for vecchio, nuovo in coppie:
    n = s.count(vecchio)
    assert n == 1, f'{n} occorrenze di {vecchio[:50]!r}'
    s = s.replace(vecchio, nuovo)

assert s.count('<span') == s.count('</span>')
p.write_text(s, encoding='utf-8', newline='')
print(f'scheda 8: {len(coppie)} correzioni di testo')
