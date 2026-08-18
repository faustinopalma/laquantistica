"""Divide le pagine bilingui in due alberi monolingui /it/ e /en/.

Principio: NON si rigenera nulla. Si rimuovono chirurgicamente gli elementi
dell'altra lingua dal file esistente e tutto il resto resta byte per byte
com'era. Cosi' il testo pubblicato non puo' cambiare per errore.
"""
import datetime
import html
import json
import pathlib
import re
import shutil
import subprocess
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

# Pagine pubblicate ma non collegate da nessuna parte: fuori dalla sitemap e con
# noindex, perche' sono proposte in attesa di giudizio, non parte del percorso.
BOZZE = {'bozza-matematica.html', 'nota-14-algebra-tre-dimensioni.html'}


def pagine():
    """I sorgenti da pubblicare: le bozze locali (_nome, game-*) restano fuori."""
    return [p for p in sorted(RADICE.glob('*.html'))
            if not p.name.startswith('_') and not p.name.startswith('game-')
            and p.name not in SALTA]


def collegamenti_canonici(testo):
    """Evita che i link interni passino dal redirect automatico .html di Azure."""
    pubbliche = {p.name for p in pagine()}

    def riscrivi(m):
        url = m.group(1)
        fine_percorso = min((i for i in (url.find('?'), url.find('#')) if i >= 0),
                            default=len(url))
        percorso, suffisso = url[:fine_percorso], url[fine_percorso:]
        nome = percorso.rsplit('/', 1)[-1]
        if nome not in pubbliche:
            return m.group(0)
        if nome == 'index.html':
            percorso = percorso[:-len(nome)] or './'
        else:
            percorso = percorso[:-5]
        return f'href="{percorso}{suffisso}"'

    return re.sub(r'href="([^"]+)"', riscrivi, testo)

# Titolo e descrizione per lingua. Le pagine assenti restano col titolo bilingue
# e vengono segnalate nel resoconto.
META = {
    'index.html': {
        'it': ('Esperimenti fondamentali della Meccanica Quantistica · La Quantistica',
               "Una tesi di laurea che ricava l'equazione di Schrödinger dagli esperimenti invece "
               'di postularla. Nove capitoli, laboratori simulati, testo integrale e gratuito.'),
        'en': ('Fundamental Experiments of Quantum Mechanics · La Quantistica',
               "A master's thesis that derives Schrödinger's equation from the experiments instead "
               'of postulating it. Nine chapters, simulated laboratories, full text, free.'),
    },
    '01-stern-gerlach.html': {
        'it': ('Esperimento di Stern-Gerlach · La Quantistica',
               "L'esperimento di Stern-Gerlach: perché il momento magnetico di un atomo d'argento "
               "si presenta in due sole direzioni. Con il laboratorio simulato dell'apparato."),
        'en': ('The Stern–Gerlach Experiment · La Quantistica',
               'The Stern–Gerlach experiment: why the magnetic moment of a silver atom shows up '
               'in two directions only. With a simulated laboratory of the apparatus.'),
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
        'it': ('Esperimenti di Stern-Gerlach in cascata · La Quantistica',
               'Stern-Gerlach in cascata: da qui nascono ampiezze, sovrapposizione e interferenza. '
               'Quattro esperimenti simulati con cui verificare ogni passaggio.'),
        'en': ('Cascaded Stern–Gerlach Experiments · La Quantistica',
               'Cascaded Stern–Gerlach: where amplitudes, superposition and interference come from. '
               'Four simulated experiments to check every step.'),
    },
    'nota-02-prodotto-scalare.html': {
        'it': ('Nota 02 · Conservazione del prodotto scalare — La Quantistica', None),
        'en': ('Note 02 · Conservation of the scalar product — La Quantistica',
               'Proof: time evolution preserves scalar products, from linear superposition and from '
               'conservation of the total (polarisation identity).'),
    },
    'nota-03-esperimenti-mentali.html': {
        'it': ('Nota 03 · Esperimenti mentali e realizzazione — La Quantistica', None),
        'en': ('Note 03 · Thought experiments and their realisation — La Quantistica',
               'The cascaded Stern–Gerlach experiments are thought experiments: recombining the '
               'separated beams is nearly impossible (the Humpty-Dumpty problem). Only recently did '
               "Folman's group achieve it with atom chips."),
    },
    'nota-04-i-principi.html': {
        'it': ('Nota 04 · I principi e la misura — La Quantistica', None),
        'en': ('Note 04 · The principles and measurement — La Quantistica',
               'The principles do not state the state in which a measurement leaves the system: not '
               'needed to derive the Schrödinger equation, but essential for cascaded apparatuses.'),
    },
    'nota-05-delta-dirac.html': {
        'it': ('Nota 05 · La δ di Dirac e la sua derivata — La Quantistica', None),
        'en': ('Note 05 · The Dirac δ and its derivative — La Quantistica',
               'The Dirac δ is not a function but a distribution: it is defined by how it acts '
               'under the integral sign. Its derivative is defined so that integration by parts '
               'keeps holding.'),
    },
    'nota-06-ehrenfest.html': {
        'it': ('Nota 06 · La media del campo e il campo nella posizione media — La Quantistica', None),
        'en': ('Note 06 · The mean of the field and the field at the mean position — La Quantistica',
               'Agreement with Newton is required on the mean of the field, not on the field at the '
               'mean position: the two coincide when the particle is well localised compared with '
               'the scale over which the field varies.'),
    },
    'nota-07-livelli-idrogeno.html': {
        'it': ('Nota 07 · I livelli energetici dell’atomo di idrogeno — La Quantistica', None),
        'en': ('Note 07 · The energy levels of the hydrogen atom — La Quantistica',
               'The hydrogen level formula derived from the eigenvalue problem: restriction to '
               'spherically symmetric states, the substitution u=rψ, a power series and the '
               'termination condition from which the integer n emerges.'),
    },
    'nota-08-matrici-hermitiane.html': {
        'it': ('Nota 08 · Perché preferiamo le matrici hermitiane — La Quantistica', None),
        'en': ('Note 08 · Why we prefer Hermitian matrices — La Quantistica',
               'Hermitian matrices are to real numbers what anti-Hermitian ones are to purely '
               'imaginary numbers: their eigenvalues are real, and real numbers are what a '
               'measurement returns. And what would have changed had we kept the anti-Hermitian matrix.'),
    },
    'nota-09-perche-numeri-complessi.html': {
        'it': ('Nota 09 · Perché scegliamo i numeri complessi? — La Quantistica',
               'Perché usiamo i numeri complessi: le quattro algebre di divisione normate, ampiezza '
               'e fase delle onde, il campo di Riemann-Silberstein e il ritorno alle soluzioni reali.'),
        'en': ('Note 09 · Why do we choose complex numbers? — La Quantistica',
               'Why we use complex numbers: the four normed division algebras, wave amplitude and '
               'phase, the Riemann-Silberstein field and the recovery of real solutions.'),
    },
    'nota-13-vettori-bra-ket.html': {
        'it': ('Nota 13 · Vettori, bra e ket — La Quantistica', None),
        'en': ('Note 13 · Vectors, bras and kets — La Quantistica',
               'A review of the algebra of complex vector spaces: the conjugate and the squared '
               'modulus, the dual vector, the bra and ket symbols, the scalar product and the '
               'decomposition of a vector on an orthogonal basis.'),
    },
    '04b-forma-evoluzione.html': {
        'it': ('La forma dell’equazione di evoluzione · La Quantistica',
               'Dalle ampiezze di probabilità alla forma generale della legge di evoluzione: stato '
               'come funzione complessa, algebra degli operatori, conservazione del prodotto scalare.'),
        'en': ('The Form of the Evolution Equation · La Quantistica',
               'From probability amplitudes to the general form of the law of evolution: the state '
               'as a complex function, the algebra of operators, conservation of the scalar product.'),
    },
    'bozza-matematica.html': {
        'it': ('Bozza · Numeri complessi e vettori di stato · La Quantistica', None),
        'en': ('Draft · Complex Numbers and State Vectors · La Quantistica', None),
    },
    'nota-14-algebra-tre-dimensioni.html': {
        'it': ('Nota 14 · Perché non un’algebra a tre dimensioni? — La Quantistica', None),
        'en': ('Note 14 · Why not a three-dimensional algebra? — La Quantistica', None),
    },
    '04c-hamiltoniana.html': {
        'it': ('L’hamiltoniana e l’equazione di Schrödinger · La Quantistica',
               'Determinazione della matrice hamiltoniana chiedendo l’accordo con l’equazione di '
               'Newton, e la costante fissata da una sola misura: la relazione di De Broglie.'),
        'en': ('The Hamiltonian and the Schrödinger Equation · La Quantistica',
               'Determining the Hamiltonian matrix by requiring agreement with Newton’s equation, '
               'and the constant fixed by a single measurement: the De Broglie relation.'),
    },
    '05b-diffusione.html': {
        'it': ('La formula di diffusione di Rutherford · La Quantistica',
               'L’equazione di Schrödinger in tre dimensioni, il flusso di probabilità e la formula '
               'di diffusione di Rutherford, confrontata con le misure dell’esperimento.'),
        'en': ('Rutherford’s Scattering Formula · La Quantistica',
               'The Schrödinger equation in three dimensions, the probability flux and Rutherford’s '
               'scattering formula, compared with the measurements from the experiment.'),
    },
    'nota-10-dimostrazione-commutatori.html': {
        'it': ('Nota 10 · Le formule sui commutatori — La Quantistica', None),
        'en': ('Note 10 · The commutator formulas — La Quantistica',
               'Proof by induction of the four commutator formulas used to determine the '
               'Hamiltonian matrix.'),
    },
    'nota-11-appendici-rutherford.html': {
        'it': ('Nota 11 · Le due appendici al calcolo della diffusione — La Quantistica', None),
        'en': ('Note 11 · The two appendices to the scattering calculation — La Quantistica',
               'General solution of the Helmholtz equation and the integral used in Rutherford’s '
               'scattering formula.'),
    },
    'nota-12-questa-edizione.html': {
        'it': ('Nota 12 · Che cosa è cambiato rispetto al 1999 — La Quantistica', None),
        'en': ('Note 12 · What has changed since 1999 — La Quantistica',
               'What sets this web edition apart from the 1999 thesis: the reading order, the '
               'splitting of the cards, and the original order with links to the pages.'),
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
        'it': ('Esperimenti con gli Elettroni · La Quantistica',
               "Corrente nel vuoto, rapporto e/m di Thomson ed esperimento di Millikan: come si è "
               'scoperto che la carica elettrica è fatta di quanti tutti uguali.'),
        'en': ('Experiments with Electrons · La Quantistica',
               "Current in a vacuum, Thomson's e/m ratio and Millikan's experiment: how it was "
               'discovered that electric charge comes in identical quanta.'),
    },
    '04-diffrazione.html': {
        'it': ('Diffrazione degli Elettroni · La Quantistica',
               "Gli elettroni diffratti da un cristallo formano anelli: la lunghezza d'onda di "
               "de Broglie misurata, e l'interpretazione probabilistica dell'ampiezza."),
        'en': ('Electron Diffraction · La Quantistica',
               "Electrons diffracted by a crystal form rings: de Broglie's wavelength measured, "
               'and the probabilistic interpretation of the amplitude.'),
    },
    '05-rutherford.html': {
        'it': ('Esperimento di Rutherford · La Quantistica',
               "L'esperimento di Rutherford e la legge 1/sin\u2074(\u03d1/2): dal conteggio delle particelle "
               'alfa alla scoperta del nucleo, con il calcolo completo della diffusione.'),
        'en': ('The Rutherford Experiment · La Quantistica',
               "Rutherford's experiment and the 1/sin\u2074(\u03d1/2) law: from counting alpha particles to "
               'the discovery of the nucleus, with the full scattering calculation.'),
    },
    '06-ulteriori-sviluppi.html': {
        'it': ('Ulteriori sviluppi della Teoria · La Quantistica',
               "Dai principi ricavati negli esperimenti all'equazione di Schrödinger: operatori, "
               'osservabili ed evoluzione temporale, dedotti passo per passo.'),
        'en': ('Further Developments of the Theory · La Quantistica',
               "From the principles obtained in the experiments to Schrödinger's equation: "
               'operators, observables and time evolution, derived step by step.'),
    },
    '07-franck-hertz.html': {
        'it': ('Esperimento di Franck-Hertz · La Quantistica',
               "L'esperimento di Franck-Hertz: gli atomi assorbono energia solo a pacchetti. "
               'I massimi e i minimi della corrente misurati su neon e mercurio.'),
        'en': ('The Franck–Hertz Experiment · La Quantistica',
               'The Franck–Hertz experiment: atoms absorb energy only in packets. The maxima and '
               'minima of the current measured on neon and mercury.'),
    },
    '08-effetto-fotoelettrico.html': {
        'it': ('Effetto Fotoelettrico · La Quantistica',
               "L'effetto fotoelettrico: la tensione di sbarramento in funzione della frequenza dà "
               'la costante di Planck e il lavoro di estrazione del metallo.'),
        'en': ('The Photoelectric Effect · La Quantistica',
               'The photoelectric effect: the stopping voltage against frequency gives Planck\u2019s '
               'constant and the work function of the metal.'),
    },
    '09-spettri-atomici.html': {
        'it': ('Spettri atomici di emissione · La Quantistica',
               'Gli spettri atomici di emissione: dalle righe misurate col goniometro alla costante '
               "di Rydberg e ai livelli energetici dell'atomo di idrogeno."),
        'en': ('Atomic Emission Spectra · La Quantistica',
               'Atomic emission spectra: from the lines measured with a goniometer to the Rydberg '
               'constant and the energy levels of the hydrogen atom.'),
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


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from ordine_schede import SCHEDE  # noqa: E402  (unica fonte dell'ordine di lettura)

CAPITOLI = [slug for slug, _, _ in SCHEDE]

AUTORE = {'@type': 'Person', 'name': 'Faustino Palma',
          'sameAs': 'https://www.linkedin.com/in/faustinopalma/'}

INSEGNA = {
    'it': ['Quantizzazione dello spin e esperimento di Stern-Gerlach',
           'Ampiezze di probabilita\u0300, sovrapposizione e interferenza',
           'Quantizzazione della carica elettrica',
           'Dualismo onda-particella e lunghezza d\u2019onda di de Broglie',
           'Struttura nucleare dell\u2019atomo e diffusione di Rutherford',
           'Operatori, osservabili ed equazione di Schr\u00f6dinger',
           'Quantizzazione dei livelli energetici atomici'],
    'en': ['Spin quantisation and the Stern\u2013Gerlach experiment',
           'Probability amplitudes, superposition and interference',
           'Quantisation of electric charge',
           'Wave\u2013particle duality and the de Broglie wavelength',
           'Nuclear structure of the atom and Rutherford scattering',
           'Operators, observables and the Schr\u00f6dinger equation',
           'Quantisation of atomic energy levels'],
}

SINTESI_CORSO = {
    'it': ('Un percorso completo che parte dagli esperimenti fondamentali e arriva a ricavare '
           'l\u2019equazione di Schr\u00f6dinger, invece di postularla. Chi lo segue fino in fondo, '
           'capitolo dopo capitolo e con i laboratori simulati, arriva a padroneggiare buona '
           'parte della meccanica quantistica non relativistica: quantizzazione, ampiezze di '
           'probabilit\u00e0, sovrapposizione e interferenza, operatori e osservabili, evoluzione '
           'temporale, struttura dell\u2019atomo e livelli energetici.'),
    'en': ('A complete path that starts from the fundamental experiments and ends by deriving '
           'the Schr\u00f6dinger equation instead of postulating it. Whoever follows it to the end, '
           'chapter after chapter and with the simulated laboratories, comes to master a good '
           'part of non-relativistic quantum mechanics: quantisation, probability amplitudes, '
           'superposition and interference, operators and observables, time evolution, the '
           'structure of the atom and its energy levels.'),
}


def dati_strutturati(lingua, file_, titolo, descrizione):
    """Dichiara a Google che l'opera e' un corso completo, non una pagina sciolta."""
    corso = {
        '@type': ['Course', 'LearningResource'],
        '@id': f'{BASE}/{lingua}/#corso',
        'name': META['index.html'][lingua][0].split(' \u00b7 ')[0],
        'description': SINTESI_CORSO[lingua],
        'url': url_pubblico(lingua, 'index.html'),
        'inLanguage': lingua,
        'isAccessibleForFree': True,
        'learningResourceType': 'corso completo' if lingua == 'it' else 'complete course',
        'educationalLevel': 'universitario' if lingua == 'it' else 'undergraduate',
        'teaches': INSEGNA[lingua],
        'about': {'@type': 'Thing',
                  'name': 'Meccanica quantistica' if lingua == 'it' else 'Quantum mechanics'},
        'author': AUTORE,
        'provider': {'@type': 'Organization', 'name': 'La Quantistica', 'url': f'{BASE}/'},
        'isBasedOn': {
            '@type': 'Thesis',
            'name': 'Esperimenti fondamentali della Meccanica Quantistica',
            'author': AUTORE,
            'datePublished': '1999',
            'inLanguage': 'it',
            'sourceOrganization': {'@type': 'CollegeOrUniversity',
                                   'name': 'Universit\u00e0 degli Studi di Napoli Federico II'},
        },
        'hasPart': [{'@type': 'LearningResource',
                     'name': META[c][lingua][0].split(' \u00b7 ')[0],
                     'url': url_pubblico(lingua, c),
                     'position': i + 1}
                    for i, c in enumerate(CAPITOLI)],
    }
    if file_ == 'index.html':
        dati = corso
    else:
        dati = {
            '@type': 'LearningResource',
            'name': titolo.split(' \u00b7 ')[0],
            'description': descrizione,
            'url': url_pubblico(lingua, file_),
            'inLanguage': lingua,
            'isAccessibleForFree': True,
            'position': CAPITOLI.index(file_) + 1,
            'author': AUTORE,
            'isPartOf': {'@type': 'Course', '@id': f'{BASE}/{lingua}/#corso',
                         'name': corso['name'], 'url': corso['url']},
        }
    dati['@context'] = 'https://schema.org'
    return ('<script type="application/ld+json">'
            + json.dumps(dati, ensure_ascii=False, separators=(',', ':'))
            + '</script>')


def anteprima_social(lingua, file_, titolo, descrizione):
    """Titolo, testo e immagine che compaiono quando il link viene condiviso."""
    pulito = re.split(r' [\u00b7\u2014] La Quantistica', titolo)[0]
    if len(descrizione) > 200:      # le piattaforme troncano: meglio tagliare fra due parole
        descrizione = descrizione[:197].rsplit(' ', 1)[0].rstrip(' ,;:') + '\u2026'
    voci = [
        ('og:type', 'article' if file_ != 'index.html' else 'website'),
        ('og:site_name', 'La Quantistica'),
        ('og:locale', 'it_IT' if lingua == 'it' else 'en_GB'),
        ('og:title', pulito),
        ('og:description', descrizione),
        ('og:url', url_pubblico(lingua, file_)),
        ('og:image', f'{BASE}/img/social/copertina-{lingua}.png'),
        ('og:image:width', '1200'),
        ('og:image:height', '630'),
        ('og:image:alt', pulito),
    ]
    testa = [f'<meta property="{k}" content="{html.escape(v, quote=True)}">' for k, v in voci]
    testa.append('<meta name="twitter:card" content="summary_large_image">')
    return '\n'.join(testa)


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
    testo = collegamenti_canonici(testo)

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

    m_tit = re.search(r'<title>(.*?)</title>', testo, re.S)
    m_des = re.search(r'<meta name="description" content="([^"]*)"', testo)
    titolo_pagina = html.unescape(m_tit.group(1).strip()) if m_tit else 'La Quantistica'
    descrizione = html.unescape(m_des.group(1)) if m_des else ''
    if descrizione:
        testa.append(anteprima_social(lingua, file_, titolo_pagina, descrizione))
    if file_ == 'index.html' or file_ in CAPITOLI:
        testa.append(dati_strutturati(lingua, file_, titolo_pagina, descrizione))
    if ANTEPRIMA or file_ in BOZZE:
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


def pagina_non_trovata():
    """Mostrata per qualunque indirizzo inesistente (con stato 404). Dice cosa e'
    successo invece di riportare in home di nascosto, e offre da dove ripartire."""
    return f'''<!DOCTYPE html>
<html lang="it" data-lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Pagina non trovata · Page not found · La Quantistica</title>
<link rel="stylesheet" href="/assets/style.css?v=20">
<link rel="stylesheet" href="/assets/lang.css?v=7">
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
  document.documentElement.setAttribute('lang', s);
  document.documentElement.setAttribute('data-lang', s);
}})();
</script>
<style>
  body {{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:var(--bg,#f5f3ee); color:var(--ink,#1f2328);
         font-family:"Segoe UI",system-ui,sans-serif; }}
  .avviso {{ max-width:34rem; padding:2rem 1.4rem; text-align:center; }}
  .marchio {{ font-family:Georgia,"Times New Roman",serif; font-size:1.35rem; margin-bottom:1.6rem; }}
  .marchio .bk {{ color:#c98b83; }}
  h1 {{ font-size:1.5rem; margin:.2rem 0 .7rem; }}
  p {{ line-height:1.6; color:#4a4f57; }}
  .vai {{ margin-top:1.6rem; }}
  .vai a {{ display:inline-block; margin:.25rem .3rem; padding:.55rem 1.2rem; border:1px solid #7b2d26;
            border-radius:999px; color:#7b2d26; text-decoration:none; font-weight:600; }}
  .vai a:hover {{ background:#7b2d26; color:#fff; }}
  .altra {{ margin-top:1.1rem; font-size:.86rem; }}
  .altra a {{ color:#4a4f57; }}
</style>
</head>
<body>
<div class="avviso">
  <p class="marchio"><span class="bk">\u27e8</span>\u039bQ<span class="bk">\u27e9</span> La Quantistica</p>
  <h1><span class="it">Pagina non trovata</span><span class="en">Page not found</span></h1>
  <p>
    <span class="it">L\u2019indirizzo che hai seguito non corrisponde a nessuna pagina del sito.
      Forse contiene un refuso, oppure la pagina \u00e8 stata spostata.</span>
    <span class="en">The address you followed does not match any page on this site.
      It may contain a typo, or the page may have been moved.</span>
  </p>
  <p class="vai">
    <a class="it" href="/it/" hreflang="it" lang="it">Vai all\u2019indice</a>
    <a class="en" href="/en/" hreflang="en" lang="en">Go to the contents</a>
  </p>
  <p class="altra">
    <span class="it"><a href="/en/" hreflang="en" lang="en">English</a></span>
    <span class="en"><a href="/it/" hreflang="it" lang="it">Italiano</a></span>
  </p>
</div>
</body>
</html>
'''


def date_modifica():
    """Data dell'ultimo commit che ha toccato ogni sorgente. E' cio' che serve a Google
    per capire *cosa* e' cambiato invece di riscandagliare tutto alla cieca.
    Se un file ha modifiche non ancora committate vale oggi."""
    date = {}
    try:
        registro = subprocess.run(
            ['git', 'log', '--format=%cs', '--name-only', '--', str(RADICE)],
            capture_output=True, text=True, encoding='utf-8', check=True).stdout
        corrente = None
        for riga in registro.splitlines():
            riga = riga.strip()
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', riga):
                corrente = riga
            elif riga.endswith('.html') and corrente:
                date.setdefault(pathlib.Path(riga).name, corrente)
        sporchi = subprocess.run(['git', 'status', '--porcelain', '--', str(RADICE)],
                                 capture_output=True, text=True, encoding='utf-8').stdout
        oggi = datetime.date.today().isoformat()
        for riga in sporchi.splitlines():
            date[pathlib.Path(riga[3:].strip().strip('"')).name] = oggi
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return date


def sitemap(nomi):
    quando = date_modifica()
    righe = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for nome in nomi:
        for l in ('it', 'en'):
            righe.append('  <url>')
            righe.append(f'    <loc>{url_pubblico(l, nome)}</loc>')
            if nome in quando:
                righe.append(f'    <lastmod>{quando[nome]}</lastmod>')
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
        (USCITA / '404.html').write_text(pagina_non_trovata(), encoding='utf-8')
        nomi = [p.name for p in pagine() if p.name not in BOZZE]
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
