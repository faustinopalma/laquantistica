"""Divide le pagine bilingui in due alberi monolingui /it/ e /en/.

Principio: NON si rigenera nulla. Si rimuovono chirurgicamente gli elementi
dell'altra lingua dal file esistente e tutto il resto resta byte per byte
com'era. Cosi' il testo pubblicato non puo' cambiare per errore.
"""
import pathlib
import re
import shutil
import sys
from html.parser import HTMLParser

RADICE = pathlib.Path('publish')
USCITA = RADICE / 'v2'
BASE = 'https://laquantistica.com/v2'   # diventera' https://laquantistica.com al promuovere
ANTEPRIMA = True                        # mette noindex finche' e' una prova

VUOTI = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
         'link', 'meta', 'param', 'source', 'track', 'wbr'}

SALTA = {'_lab-index.html'}             # bozza locale, non pubblicata
MONOLINGUI = {'errata.html'}            # nessun marcatore di lingua: copiata tale e quale

# Titolo e descrizione per lingua. Le pagine assenti restano col titolo bilingue
# e vengono segnalate nel resoconto.
META = {
    'index.html': {
        'it': ('Esperimenti fondamentali della Meccanica Quantistica · La Quantistica', None),
        'en': ('Fundamental Experiments of Quantum Mechanics · La Quantistica', None),
    },
    '01-stern-gerlach.html': {
        'it': ('Esperimento di Stern-Gerlach · La Quantistica', None),
        'en': ('The Stern–Gerlach Experiment · La Quantistica', None),
    },
    'nota-01-stern-gerlach.html': {
        'it': ('Nota 01 · Dietro le quinte — Stern-Gerlach · La Quantistica', None),
        'en': ('Note 01 · Behind the scenes — Stern–Gerlach · La Quantistica',
               'An honest note: why for 27 years I never put this thesis on the Internet, '
               'and the true story of the cigar that made the Stern–Gerlach experiment visible.'),
    },
    'nota-tecnica-01-stern-gerlach.html': {
        'it': ("Nota tecnica · Dimensionamento dell'apparato di Stern-Gerlach · La Quantistica", None),
        'en': ('Technical note · Sizing the Stern–Gerlach apparatus · La Quantistica',
               'Technical note to Chapter 1: deflection, the air-gap/gradient trade-off, the '
               'short-magnet variant with a drift length, vacuum sizing, construction notes and detection.'),
    },
    'lab-01-stern-gerlach.html': {
        'it': ('Lab · Esperimento di Stern-Gerlach — La Quantistica', None),
        'en': ('Lab · The Stern–Gerlach Experiment — La Quantistica',
               'Simulated laboratory of Experiment 1 (Stern–Gerlach with silver): adjust pressure, '
               'temperature, collimation and magnet, and watch the deposit build up on the slide.'),
    },
}


class Potatore(HTMLParser):
    """Trova gli intervalli di testo occupati dagli elementi della lingua da togliere."""

    def __init__(self, testo, lingua_da_togliere):
        super().__init__(convert_charrefs=False)
        self.testo = testo
        self.togli = lingua_da_togliere
        self.inizi = [0]
        for riga in testo.splitlines(keepends=True):
            self.inizi.append(self.inizi[-1] + len(riga))
        self.pila = []
        self.intervalli = []
        self.inizio_taglio = None
        self.profondita_taglio = 0
        self.trovati = 0

    def _offset(self):
        r, c = self.getpos()
        return self.inizi[r - 1] + c

    def _fine_tag(self, inizio):
        i, apice = inizio, None
        while i < len(self.testo):
            ch = self.testo[i]
            if apice:
                if ch == apice:
                    apice = None
            elif ch in '"\'':
                apice = ch
            elif ch == '>':
                return i + 1
            i += 1
        raise ValueError(f'tag non chiuso a {inizio}')

    def _e_da_togliere(self, attrs):
        return self.togli in (dict(attrs).get('class') or '').split()

    def handle_starttag(self, tag, attrs):
        inizio = self._offset()
        da_togliere = self._e_da_togliere(attrs)
        if da_togliere:
            self.trovati += 1
        if tag in VUOTI:
            if da_togliere and self.inizio_taglio is None:
                self.intervalli.append((inizio, self._fine_tag(inizio)))
            return
        if da_togliere and self.inizio_taglio is None:
            self.inizio_taglio = inizio
            self.profondita_taglio = len(self.pila)
        self.pila.append(tag)

    def handle_startendtag(self, tag, attrs):
        inizio = self._offset()
        if self._e_da_togliere(attrs):
            self.trovati += 1
            if self.inizio_taglio is None:
                self.intervalli.append((inizio, self._fine_tag(inizio)))

    def handle_endtag(self, tag):
        if tag in VUOTI:
            return
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i] == tag:
                del self.pila[i:]
                break
        else:
            return
        if self.inizio_taglio is not None and len(self.pila) <= self.profondita_taglio:
            self.intervalli.append((self.inizio_taglio, self._fine_tag(self._offset())))
            self.inizio_taglio = None


def pota(testo, lingua_da_togliere):
    p = Potatore(testo, lingua_da_togliere)
    p.feed(testo)
    p.close()
    if p.inizio_taglio is not None:
        raise ValueError('elemento di lingua mai chiuso')
    fuori = []
    ultimo = 0
    for a, b in sorted(p.intervalli):
        if a < ultimo:
            raise ValueError('intervalli sovrapposti')
        fuori.append(testo[ultimo:a])
        ultimo = b
    fuori.append(testo[ultimo:])
    return ''.join(fuori), p.trovati, len(p.intervalli)


SEL_LINGUA = re.compile(r'([ \t]*)<div class="langsw"[^>]*>.*?</div>', re.S)
NOMI = {'it': 'Italiano', 'en': 'English'}


def selettore(lingua, file_, rientro):
    voci = []
    for l in ('it', 'en'):
        corrente = ' aria-current="true"' if l == lingua else ''
        voci.append(f'{rientro}  <a class="langbtn" href="../{l}/{file_}" '
                    f'hreflang="{l}" lang="{l}"{corrente}>{NOMI[l]}</a>')
    return (f'{rientro}<div class="langsw" role="group" aria-label="Lingua / Language">\n'
            + '\n'.join(voci) + f'\n{rientro}</div>')


def pillola_mobile(lingua, file_):
    voci = []
    for l in ('it', 'en'):
        corrente = ' aria-current="true"' if l == lingua else ''
        voci.append(f'  <a class="langbtn" href="../{l}/{file_}" hreflang="{l}" '
                    f'lang="{l}"{corrente}>{NOMI[l]}</a>')
    return ('<div class="langsw-mobile" role="group" aria-label="Lingua / Language">\n'
            '  <span class="lg" aria-hidden="true">\U0001F310</span>\n'
            + '\n'.join(voci) + '\n</div>\n')


def trasforma(testo, lingua, file_, avvisi):
    altra = 'en' if lingua == 'it' else 'it'
    testo, trovati, tolti = pota(testo, altra)

    residui = re.findall(rf'class="{altra}"', re.sub(r'<script\b.*?</script>', '', testo, flags=re.S))
    if residui:
        avvisi.append(f'{lingua}/{file_}: {len(residui)} elementi "{altra}" non rimossi')

    testo = re.sub(r'<html[^>]*>', f'<html lang="{lingua}" data-lang="{lingua}">', testo, count=1)
    testo = re.sub(r'[ \t]*<script src="assets/lang\.js\?v=\d+"></script>\n?', '', testo)

    aveva_sidebar = 'class="sidebar"' in testo
    m = SEL_LINGUA.search(testo)
    if m:
        testo = testo[:m.start()] + selettore(lingua, file_, m.group(1)) + testo[m.end():]
    else:
        avvisi.append(f'{lingua}/{file_}: selettore di lingua non trovato')

    if aveva_sidebar:
        testo = testo.replace('</body>', pillola_mobile(lingua, file_) + '</body>', 1)

    # riferimenti agli asset: da relativi a radice del sito, cosi' non dipendono dalla cartella
    testo = re.sub(r'((?:src|href)=")(assets/|img/)', r'\1/\2', testo)

    meta = META.get(file_, {}).get(lingua)
    if meta:
        titolo, descr = meta
        testo = re.sub(r'<title>.*?</title>', f'<title>{titolo}</title>', testo, count=1, flags=re.S)
        if descr:
            if re.search(r'<meta\s+name="description"[^>]*>', testo):
                testo = re.sub(r'<meta\s+name="description"[^>]*>',
                               f'<meta name="description" content="{descr}">', testo, count=1)
            else:
                testo = testo.replace('<title>', f'<meta name="description" content="{descr}">\n<title>', 1)
    else:
        avvisi.append(f'{lingua}/{file_}: titolo non ancora curato')
        if lingua == 'en' and re.search(r'<meta\s+name="description"', testo):
            avvisi.append(f'{lingua}/{file_}: descrizione ancora in italiano')

    testa = []
    for l in ('it', 'en'):
        testa.append(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}/{file_}">')
    testa.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/{file_}">')
    if ANTEPRIMA:
        testa.append('<meta name="robots" content="noindex,nofollow">')
    testa.append('<link rel="stylesheet" href="/assets/lang-links.css?v=1">')
    testo = testo.replace('</head>', '\n'.join(testa) + '\n</head>', 1)

    nuovo_canonico = f'<link rel="canonical" href="{BASE}/{lingua}/{file_}">'
    if re.search(r'<link rel="canonical"[^>]*>', testo):
        testo = re.sub(r'<link rel="canonical"[^>]*>', nuovo_canonico, testo, count=1)
    else:
        testo = testo.replace('</head>', nuovo_canonico + '\n</head>', 1)

    return testo, trovati, tolti


def pagina_scelta():
    """Radice dei due alberi: manda alla lingua del browser, con entrambi i collegamenti visibili."""
    robots = '<meta name="robots" content="noindex,nofollow">\n' if ANTEPRIMA else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<link rel="alternate" hreflang="it" href="{BASE}/it/index.html">
<link rel="alternate" hreflang="en" href="{BASE}/en/index.html">
<link rel="alternate" hreflang="x-default" href="{BASE}/en/index.html">
<title>La Quantistica</title>
<link rel="stylesheet" href="/assets/style.css?v=17">
<script>
(function () {{
  var s = null;
  try {{ s = localStorage.getItem('site-lang'); }} catch (e) {{}}
  if (s !== 'it' && s !== 'en') {{
    var l = (navigator.languages && navigator.languages.length)
      ? navigator.languages : (navigator.language ? [navigator.language] : []);
    s = 'en';
    for (var i = 0; i < l.length; i++) {{
      var t = String(l[i]).toLowerCase().split('-')[0];
      if (t === 'it' || t === 'en') {{ s = t; break; }}
    }}
  }}
  location.replace(s + '/index.html');
}})();
</script>
</head>
<body>
<p style="font-family:system-ui;padding:2rem">
  <a href="it/index.html" hreflang="it" lang="it">Italiano</a> &middot;
  <a href="en/index.html" hreflang="en" lang="en">English</a>
</p>
</body>
</html>
'''


def main():
    if USCITA.exists():
        shutil.rmtree(USCITA)
    for l in ('it', 'en'):
        (USCITA / l).mkdir(parents=True)

    pagine = [p for p in sorted(RADICE.glob('*.html')) if p.name not in SALTA]
    avvisi = []
    print(f'{"pagina":<38} {"tolti it":>9} {"tolti en":>9}')
    for p in pagine:
        testo = p.read_text(encoding='utf-8')
        if p.name in MONOLINGUI:
            for l in ('it', 'en'):
                (USCITA / l / p.name).write_text(testo, encoding='utf-8')
            print(f'{p.name:<38} {"(monolingue, copiata)":>19}')
            continue
        conteggi = {}
        for l in ('it', 'en'):
            nuovo, trovati, tolti = trasforma(testo, l, p.name, avvisi)
            (USCITA / l / p.name).write_text(nuovo, encoding='utf-8')
            conteggi[l] = tolti
        print(f'{p.name:<38} {conteggi["it"]:>9} {conteggi["en"]:>9}')

    print(f'\npagine scritte: {len(list((USCITA / "it").glob("*.html")))} per lingua')
    (USCITA / 'index.html').write_text(pagina_scelta(), encoding='utf-8')
    da_curare = sorted({a.split(': ')[0].split('/')[1] for a in avvisi if 'titolo' in a})
    veri_problemi = [a for a in avvisi if 'titolo' not in a and 'descrizione' not in a]
    print(f'\ntitoli ancora da curare ({len(da_curare)}): {", ".join(da_curare) or "nessuno"}')
    print(f'problemi strutturali: {len(veri_problemi)}')
    for a in veri_problemi:
        print(f'  !! {a}')
    return 1 if veri_problemi else 0


if __name__ == '__main__':
    sys.exit(main())
