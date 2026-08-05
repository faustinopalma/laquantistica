"""I richiami alle note dicono cosa si trova dall'altra parte, non cosa qui manca."""
from pathlib import Path

L2 = 'nota-02-prodotto-scalare.html?ret=%s%%23nota-2'
L1 = 'nota-01-stern-gerlach.html?ret=01-stern-gerlach.html%23nota-1'

CAMBI = {
    '02-stern-gerlach-cascata.html': [(
        '<span class="it">Qui la propriet\u00e0 \u00e8 solo verificata su un esempio; per la '
        '<a href="%s">dimostrazione generale \u2192</a></span>'
        '<span class="en">Here the property is only checked on an example; for the '
        '<a href="%s">general proof \u2192</a></span>' % ((L2 % '02-stern-gerlach-cascata.html',) * 2),
        '<span class="it">La stessa propriet\u00e0 vale per qualunque coppia di stati: '
        '<a href="%s">la dimostrazione \u2192</a></span>'
        '<span class="en">The same property holds for any pair of states: '
        '<a href="%s">the proof \u2192</a></span>' % ((L2 % '02-stern-gerlach-cascata.html',) * 2))],

    '04-diffrazione.html': [(
        '<span class="it">La conservazione del prodotto scalare \u00e8 qui data per acquisita: per la '
        '<a href="%s">dimostrazione \u2192</a></span>'
        '<span class="en">Here the conservation of the scalar product is taken as known: for the '
        '<a href="%s">proof \u2192</a></span>' % ((L2 % '04-diffrazione.html',) * 2),
        '<span class="it">Come questa propriet\u00e0 discende dai principi: '
        '<a href="%s">la dimostrazione \u2192</a></span>'
        '<span class="en">How this property follows from the principles: '
        '<a href="%s">the proof \u2192</a></span>' % ((L2 % '04-diffrazione.html',) * 2))],

    '06-ulteriori-sviluppi.html': [(
        '<span class="it">Qui il teorema \u00e8 solo enunciato; per la '
        '<a href="%s">dimostrazione \u2192</a></span>'
        '<span class="en">Here the theorem is only stated; for the '
        '<a href="%s">proof \u2192</a></span>' % ((L2 % '06-ulteriori-sviluppi.html',) * 2),
        '<span class="it">Perch\u00e9 la matrice di evoluzione lascia invariati i prodotti scalari: '
        '<a href="%s">la dimostrazione \u2192</a></span>'
        '<span class="en">Why the time-evolution matrix leaves the scalar products unchanged: '
        '<a href="%s">the proof \u2192</a></span>' % ((L2 % '06-ulteriori-sviluppi.html',) * 2))],

    '01-stern-gerlach.html': [(
        '<span class="it">Una nota onesta a margine di questo capitolo. '
        '<a href="%s">Leggi \u2192</a></span>'
        '<span class="en">An honest note in the margin of this chapter. '
        '<a href="%s">Read \u2192</a></span>' % (L1, L1),
        '<span class="it">Avevo davvero provato a costruirlo, questo apparato: '
        '<a href="%s">com\u2019\u00e8 andata \u2192</a></span>'
        '<span class="en">I had really tried to build this apparatus: '
        '<a href="%s">how it went \u2192</a></span>' % (L1, L1))],
}

for nome, coppie in CAMBI.items():
    P = Path('sorgenti', nome)
    s = P.read_text(encoding='utf-8')
    for vecchio, nuovo in coppie:
        n = s.count(vecchio)
        assert n == 1, f'{nome}: {n} occorrenze'
        s = s.replace(vecchio, nuovo)
    assert s.count('<span') == s.count('</span>')
    P.write_text(s, encoding='utf-8', newline='')
    print(f'{nome}: richiamo riscritto')
