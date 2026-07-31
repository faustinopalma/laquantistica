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

RADICE = pathlib.Path('sorgenti')      # bilingui, NON pubblicati
USCITA = pathlib.Path('publish')       # sito generato: publish/it, publish/en
BASE = 'https://laquantistica.com'
ANTEPRIMA = False                      # True mette noindex (per le prove)

VUOTI = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
         'link', 'meta', 'param', 'source', 'track', 'wbr'}


def url_pubblico(lingua, file_):
    """Azure Static Web Apps risponde 301 da .html all'indirizzo senza estensione:
    canonical e hreflang devono dichiarare gia' quello finale."""
    if file_ == 'index.html':
        return f'{BASE}/{lingua}/'
    return f'{BASE}/{lingua}/{file_[:-5]}'

SALTA = ()                              # le bozze si riconoscono dal nome, vedi pagine()


def pagine():
    """I sorgenti da pubblicare: le bozze locali (_nome, game-*) restano fuori."""
    return [p for p in sorted(RADICE.glob('*.html'))
            if not p.name.startswith('_') and not p.name.startswith('game-')
            and p.name not in SALTA]

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
    '02-stern-gerlach-cascata.html': {
        'it': ('Esperimenti di Stern-Gerlach in cascata · La Quantistica', None),
        'en': ('Cascaded Stern–Gerlach Experiments · La Quantistica', None),
    },
    'nota-02-prodotto-scalare.html': {
        'it': ('Nota 02 · Conservazione del prodotto scalare — La Quantistica', None),
        'en': ('Note 02 · Conservation of the scalar product — La Quantistica',
               'Proof: time evolution preserves scalar products, from linear superposition and from '
               'conservation of the total (polarisation identity).'),
    },
    'lab-02a-sg-angolo-relativo.html': {
        'it': ('Lab · Stern-Gerlach in cascata: angolo relativo — La Quantistica', None),
        'en': ('Lab · Cascaded Stern–Gerlach: relative angle — La Quantistica',
               'Interactive simulator of Experiment 1 (cascaded Stern–Gerlach): two machines, the '
               'first selects the state, the second measures. cos²/sin² probabilities of the relative angle.'),
    },
    'lab-02b-sg-tre-macchine.html': {
        'it': ('Lab · Stern-Gerlach in cascata: tre macchine — La Quantistica', None),
        'en': ('Lab · Cascaded Stern–Gerlach: three machines — La Quantistica',
               'Interactive simulator of Experiment 2 (cascaded Stern–Gerlach): three machines. '
               'Rotating the first changes the intensity but not the ratio in which the third splits '
               'the beam: the state after the second machine is independent of the first.'),
    },
    'lab-02c-sg-ricombinazione.html': {
        'it': ('Lab · Stern-Gerlach in cascata: ricombinazione — La Quantistica', None),
        'en': ('Lab · Cascaded Stern–Gerlach: recombination — La Quantistica',
               'Interactive simulator of Experiment 3 (cascaded Stern–Gerlach): splitting and '
               'recombination. Blocking each branch in turn measures m₀; recombining both restores '
               'the state: probabilities do not add, amplitudes do.'),
    },
    'lab-02d-sg-sfasamento.html': {
        'it': ('Lab · Stern-Gerlach in cascata: sfasamento — La Quantistica', None),
        'en': ('Lab · Cascaded Stern–Gerlach: phase shift — La Quantistica',
               'Interactive simulator of Experiment 4 (cascaded Stern–Gerlach): phase shift between '
               'the two paths, built on the same base as Experiment 3.'),
    },
    '03-elettroni.html': {
        'it': ('Esperimenti con gli Elettroni · La Quantistica', None),
        'en': ('Experiments with Electrons · La Quantistica', None),
    },
    '04-diffrazione.html': {
        'it': ('Diffrazione degli Elettroni · La Quantistica', None),
        'en': ('Electron Diffraction · La Quantistica', None),
    },
    '05-rutherford.html': {
        'it': ('Esperimento di Rutherford · La Quantistica', None),
        'en': ('The Rutherford Experiment · La Quantistica', None),
    },
    '06-ulteriori-sviluppi.html': {
        'it': ('Ulteriori sviluppi della Teoria · La Quantistica', None),
        'en': ('Further Developments of the Theory · La Quantistica', None),
    },
    '07-franck-hertz.html': {
        'it': ('Esperimento di Franck-Hertz · La Quantistica', None),
        'en': ('The Franck–Hertz Experiment · La Quantistica', None),
    },
    '08-effetto-fotoelettrico.html': {
        'it': ('Effetto Fotoelettrico · La Quantistica', None),
        'en': ('The Photoelectric Effect · La Quantistica', None),
    },
    '09-spettri-atomici.html': {
        'it': ('Spettri atomici di emissione · La Quantistica', None),
        'en': ('Atomic Emission Spectra · La Quantistica', None),
    },
    'lab-03a-corrente-vuoto.html': {
        'it': ('Lab · Corrente nel vuoto — La Quantistica', None),
        'en': ('Lab · Current in a vacuum — La Quantistica',
               'Simulated laboratory of current in a vacuum: heat the filament, adjust the voltage '
               'between the electrodes and measure the current up to saturation.'),
    },
    'lab-03b-deflessione-em.html': {
        'it': ('Lab · Deflessione e/m — La Quantistica', None),
        'en': ('Lab · Beam deflection · e/m — La Quantistica',
               'Simulated laboratory of electron deflection: crossed electric and magnetic fields, '
               'measuring the ratio e/m between charge and mass.'),
    },
    'lab-03c-millikan.html': {
        'it': ('Lab · Goccia di Millikan — La Quantistica', None),
        'en': ('Lab · Millikan oil drop — La Quantistica',
               'Simulated Millikan experiment: suspend the oil drop in the electric field, measure '
               'the charges and discover that they are multiples of one elementary charge.'),
    },
    'lab-04-diffrazione.html': {
        'it': ('Lab · Diffrazione degli elettroni — La Quantistica', None),
        'en': ('Lab · Electron diffraction — La Quantistica',
               'Simulated laboratory of electron diffraction: let the rings build up on the screen, '
               'measure their radius and check the de Broglie wavelength.'),
    },
    'lab-05-rutherford.html': {
        'it': ('Lab · Esperimento di Rutherford — La Quantistica', None),
        'en': ('Lab · The Rutherford Experiment — La Quantistica',
               'Simulated Rutherford experiment: rotate the detector, count the pulses, build N(ϑ) '
               'and compare it with the 1/sin⁴(ϑ/2) law.'),
    },
    'lab-07-franck-hertz.html': {
        'it': ('Lab · Esperimento di Franck-Hertz — La Quantistica', None),
        'en': ('Lab · The Franck–Hertz Experiment — La Quantistica',
               'Simulated Franck–Hertz experiment: choose neon or mercury, sweep the voltage and '
               'watch the maxima and minima of the current and the glowing regions between the grids.'),
    },
    'lab-08-fotoelettrico.html': {
        'it': ('Lab · Effetto fotoelettrico — La Quantistica', None),
        'en': ('Lab · The photoelectric effect — La Quantistica',
               'Simulated laboratory of the photoelectric effect: mercury vapour lamp, iris '
               'diaphragm, interference filters, photocell and capacitor. Measure the stopping '
               'voltage against frequency and obtain h/e, the work function and the threshold frequency.'),
    },
    'lab-09-spettri.html': {
        'it': ('Lab · Spettri atomici di emissione — La Quantistica', None),
        'en': ('Lab · Atomic emission spectra — La Quantistica',
               'Simulated goniometer spectrometer: diffraction grating, rotating telescope, '
               'measurement of the angles of the emission lines of hydrogen, mercury, neon, argon '
               'and nitrogen. From the lines to the Rydberg constant and the levels of the hydrogen atom.'),
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
    rimosso = []
    ultimo = 0
    for a, b in sorted(p.intervalli):
        if a < ultimo:
            raise ValueError('intervalli sovrapposti')
        fuori.append(testo[ultimo:a])
        rimosso.append(testo[a:b])
        ultimo = b
    fuori.append(testo[ultimo:])
    return ''.join(fuori), p.trovati, len(p.intervalli), ''.join(rimosso)


class NodiTesto(HTMLParser):
    """Offset e contenuto dei soli nodi di testo veri.

    Serve per non toccare gli attributi: i tracciati SVG che KaTeX genera per le
    parentesi grandi sono pieni di coppie come `3,-2` e verrebbero corrotti.
    """

    SALTA = {'script', 'style', 'annotation'}

    def __init__(self, testo):
        super().__init__(convert_charrefs=False)
        self.testo = testo
        self.inizi = [0]
        for r in testo.splitlines(keepends=True):
            self.inizi.append(self.inizi[-1] + len(r))
        self.pila = []
        self.nodi = []

    def _off(self):
        r, c = self.getpos()
        return self.inizi[r - 1] + c

    def handle_starttag(self, tag, attrs):
        if tag not in VUOTI and tag not in ('path', 'use'):
            self.pila.append(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i] == tag:
                del self.pila[i:]
                return

    def handle_data(self, data):
        if not any(t in self.SALTA for t in self.pila):
            self.nodi.append((self._off(), data))


def separatore_decimale(testo, lingua):
    r"""Il separatore decimale segue la lingua: virgola in italiano, punto in inglese.
    Alcuni numeri (tabelle di dati, letture dei laboratori) sono condivisi fra le due
    versioni e sono scritti in una sola convenzione: qui si adeguano.
    I confini `(?<![\d.])` evitano di toccare cose come 3.2.2."""
    schema, rimpiazzo = ((r'(?<=\d),(?=\d)', '.') if lingua == 'en'
                         else (r'(?<![\d.])(\d+)\.(\d+)(?![\d.])', r'\1,\2'))
    p = NodiTesto(testo)
    p.feed(testo)
    p.close()
    pezzi, ultimo, n = [], 0, 0
    for off, dati in p.nodi:
        nuovo, k = re.subn(schema, rimpiazzo, dati)
        if k:
            pezzi.append(testo[ultimo:off])
            pezzi.append(nuovo)
            ultimo = off + len(dati)
            n += k
    pezzi.append(testo[ultimo:])
    return ''.join(pezzi), n


ATTR_LINGUA = re.compile(r'\s([\w-]+)-en="([^"]*)"')


def attributi_per_lingua(testo, lingua):
    """`alt-en="..."` diventa `alt="..."` nella versione inglese e sparisce in quella
    italiana. Serve per il testo che vive negli attributi (alt, aria-label): non
    essendo elementi, non si puo' sdoppiarlo con gli span."""
    n = 0

    def per_tag(m):
        nonlocal n
        tag = m.group(0)
        coppie = ATTR_LINGUA.findall(tag)
        if not coppie:
            return tag
        n += len(coppie)
        tag = ATTR_LINGUA.sub('', tag)
        if lingua == 'en':
            chiusura = '/>' if tag.rstrip('>').rstrip().endswith('/') else '>'
            corpo = tag.rstrip('>').rstrip().rstrip('/').rstrip()
            for nome, valore in coppie:
                corpo = re.sub(rf'\s{re.escape(nome)}="[^"]*"', '', corpo)
                corpo += f' {nome}="{valore}"'
            tag = corpo + chiusura
        return tag

    return re.sub(r'<[a-zA-Z][^>]*>', per_tag, testo), n


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
    testo, trovati, tolti, rimosso = pota(testo, altra)

    residui = re.findall(rf'class="{altra}"', re.sub(r'<script\b.*?</script>', '', testo, flags=re.S))
    if residui:
        avvisi.append(f'{lingua}/{file_}: {len(residui)} elementi "{altra}" non rimossi')

    # un id che viveva nell'altra lingua ma che lo script cerca: senza segnaposto
    # getElementById torna null e l'intero script si ferma (era il caso di lab-02d)
    script = ' '.join(re.findall(r'<script\b[^>]*>(.*?)</script>', testo, re.S))
    orfani = [i for i in re.findall(r'\sid="([^"]+)"', rimosso)
              if re.search(rf'''["']{re.escape(i)}["']''', script)]
    if orfani:
        # in apertura di <body>: gli script in linea girano durante l'analisi del documento,
        # quindi un segnaposto messo in fondo arriverebbe troppo tardi
        segnaposto = ''.join(f'<span id="{i}" hidden></span>' for i in orfani)
        testo = re.sub(r'(<body[^>]*>)', r'\1' + segnaposto, testo, count=1)
        avvisi.append(f'{lingua}/{file_}: segnaposto per {", ".join(orfani)}')

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

    testo, n_dec = separatore_decimale(testo, lingua)
    if n_dec:
        avvisi.append(f'{lingua}/{file_}: {n_dec} separatori decimali adeguati')

    testo, n_attr = attributi_per_lingua(testo, lingua)
    if n_attr:
        avvisi.append(f'{lingua}/{file_}: {n_attr} attributi per lingua risolti')

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
        testa.append(f'<link rel="alternate" hreflang="{l}" href="{url_pubblico(l, file_)}">')
    testa.append(f'<link rel="alternate" hreflang="x-default" href="{url_pubblico("en", file_)}">')
    if ANTEPRIMA:
        testa.append('<meta name="robots" content="noindex,nofollow">')
    testa.append('<link rel="stylesheet" href="/assets/lang-links.css?v=1">')
    testo = testo.replace('</head>', '\n'.join(testa) + '\n</head>', 1)

    nuovo_canonico = f'<link rel="canonical" href="{url_pubblico(lingua, file_)}">'
    if re.search(r'<link rel="canonical"[^>]*>', testo):
        testo = re.sub(r'<link rel="canonical"[^>]*>', nuovo_canonico, testo, count=1)
    else:
        testo = testo.replace('</head>', nuovo_canonico + '\n</head>', 1)

    return testo, trovati, tolti


def pagina_scelta():
    """Porta d'ingresso: manda alla lingua del browser, con entrambi i collegamenti
    visibili per chi ha JavaScript disattivato o vuole scegliere."""
    robots = '<meta name="robots" content="noindex,nofollow">\n' if ANTEPRIMA else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<link rel="canonical" href="{BASE}/">
<link rel="alternate" hreflang="it" href="{url_pubblico('it', 'index.html')}">
<link rel="alternate" hreflang="en" href="{url_pubblico('en', 'index.html')}">
<link rel="alternate" hreflang="x-default" href="{url_pubblico('en', 'index.html')}">
<title>La Quantistica</title>
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
  location.replace('/' + s + '/');
}})();
</script>
<style>
  body {{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:#f5f3ee; color:#1f2328; font-family:"Segoe UI",system-ui,sans-serif; }}
  .scelta {{ text-align:center; padding:2rem; }}
  .marchio {{ font-family:Georgia,"Times New Roman",serif; font-size:1.6rem; margin-bottom:1.4rem; }}
  .marchio .bk {{ color:#c98b83; }}
  a {{ display:inline-block; margin:0 .35rem; padding:.55rem 1.3rem; border:1px solid #7b2d26;
       border-radius:999px; color:#7b2d26; text-decoration:none; font-weight:600; }}
  a:hover {{ background:#7b2d26; color:#fff; }}
</style>
</head>
<body>
<div class="scelta">
  <p class="marchio"><span class="bk">⟨</span>ΛQ<span class="bk">⟩</span> La Quantistica</p>
  <a href="/it/" hreflang="it" lang="it">Italiano</a>
  <a href="/en/" hreflang="en" lang="en">English</a>
</div>
</body>
</html>
'''


def sitemap(nomi):
    righe = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for nome in nomi:
        for l in ('it', 'en'):
            righe.append('  <url>')
            righe.append(f'    <loc>{url_pubblico(l, nome)}</loc>')
            for a in ('it', 'en'):
                righe.append(f'    <xhtml:link rel="alternate" hreflang="{a}" '
                             f'href="{url_pubblico(a, nome)}"/>')
            righe.append(f'    <xhtml:link rel="alternate" hreflang="x-default" '
                         f'href="{url_pubblico("en", nome)}"/>')
            righe.append('  </url>')
    righe.append('</urlset>')
    return '\n'.join(righe) + '\n'


def main(solo=None):
    if not solo:
        for l in ('it', 'en'):
            cartella = USCITA / l
            if cartella.exists():
                shutil.rmtree(cartella)
            cartella.mkdir(parents=True)

    da_fare = pagine() if not solo else [RADICE / n for n in solo]
    avvisi = []
    print(f'{"pagina":<38} {"tolti it":>9} {"tolti en":>9}')
    for p in da_fare:
        testo = p.read_text(encoding='utf-8')
        conteggi = {}
        for l in ('it', 'en'):
            nuovo, trovati, tolti = trasforma(testo, l, p.name, avvisi)
            (USCITA / l / p.name).write_text(nuovo, encoding='utf-8')
            conteggi[l] = tolti
        print(f'{p.name:<38} {conteggi["it"]:>9} {conteggi["en"]:>9}')

    print(f'\npagine scritte: {len(list((USCITA / "it").glob("*.html")))} per lingua')
    if not solo:
        (USCITA / 'index.html').write_text(pagina_scelta(), encoding='utf-8')
        nomi = [p.name for p in pagine()]
        (USCITA / 'sitemap.xml').write_text(sitemap(nomi), encoding='utf-8')
        (USCITA / 'robots.txt').write_text(
            f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n', encoding='utf-8')
    da_curare = sorted({a.split(': ')[0].split('/')[1] for a in avvisi if 'titolo' in a})
    segnaposti = [a for a in avvisi if 'segnaposto' in a or 'separatori' in a or 'attributi' in a]
    veri_problemi = [a for a in avvisi
                     if not any(k in a for k in ('titolo', 'descrizione', 'segnaposto',
                                                'separatori', 'attributi'))]
    print(f'\ntitoli ancora da curare ({len(da_curare)}): {", ".join(da_curare) or "nessuno"}')
    for a in segnaposti:
        print(f'  ~  {a}')
    print(f'problemi strutturali: {len(veri_problemi)}')
    for a in veri_problemi:
        print(f'  !! {a}')
    return 1 if veri_problemi else 0


if __name__ == '__main__':
    argomenti = [a for a in sys.argv[1:] if not a.startswith('-')]
    sys.exit(main(argomenti or None))
