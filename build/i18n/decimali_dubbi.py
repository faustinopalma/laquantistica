import html
import pathlib
import re

CAMPIONI = {
    '02-stern-gerlach-cascata.html': ['210,155', '10,310', '3,139'],
    '03-elettroni.html': ['142,137', '282,1185'],
    '05-rutherford.html': ['378,173', '0,0699'],
}

for nome, numeri in CAMPIONI.items():
    t = (pathlib.Path('sorgenti') / nome).read_text(encoding='utf-8')
    print(f'===== {nome} =====')
    for n in numeri:
        i = t.find(n)
        if i < 0:
            print(f'   {n}: non trovato')
            continue
        # se sta in un data-tex, mostro il LaTeX; altrimenti il contesto
        inizio = t.rfind('data-tex="', max(0, i - 2500), i)
        if inizio > 0 and t.find('"', inizio + 10) > i:
            tex = html.unescape(t[inizio + 10:t.find('"', inizio + 10)])
            j = tex.find(n)
            print(f'   {n}  [in formula] ...{tex[max(0, j - 70):j + 70]}...')
        else:
            print(f'   {n}  [in testo]   ...{t[max(0, i - 90):i + 60]}...'.replace('\n', ' '))
