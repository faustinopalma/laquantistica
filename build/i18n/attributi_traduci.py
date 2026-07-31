"""Traduzione del testo che vive negli attributi (alt delle figure, aria-label
degli schemi). Aggiunge accanto a ogni attributo italiano il gemello `-en`, che
lo splitter risolve generando l'albero inglese.

Le chiavi sono normalizzate sugli apostrofi: nel sorgente convivono ' e ’.
"""
import pathlib
import re

RADICE = pathlib.Path('sorgenti')
ATTRIBUTI = ('alt', 'aria-label', 'title', 'placeholder')


def chiave(s):
    return re.sub(r'\s+', ' ', s.replace('\u2019', "'")).strip()


TRAD = {
    # ---- Capitolo 1 ----
    "Un atomo come piccola calamita in un campo disuniforme.":
        "An atom as a tiny magnet in a non-uniform field.",
    "Il circuito magnetico che produce un campo disomogeneo nel traferro.":
        "The magnetic circuit that produces an inhomogeneous field in the gap.",
    "Il fascio di atomi attraverso il traferro sagomato.":
        "The beam of atoms through the shaped gap.",
    "Il percorso del fascio: fornetto, fenditure, vetrino.":
        "The path of the beam: oven, slits, glass slide.",
    "Camera di vaporizzazione e tubo con la prima fenditura di collimazione.":
        "Vaporisation chamber and tube with the first collimating slit.",
    "Apparato completo assemblato.":
        "The complete apparatus assembled.",
    "Il vetrino con due bande scure separate, e accanto il profilo di densità del deposito con due massimi.":
        "The slide with two separate dark bands, and beside it the density profile of the deposit with two maxima.",
    "Il deposito di argento fotografato al microscopio: a sinistra senza campo, una riga sola; a destra con il campo, la riga si apre al centro.":
        "The silver deposit photographed under the microscope: on the left without the field, a single line; on the right with the field, the line opens in the middle.",

    # ---- Capitolo 2 ----
    "Due macchine di Stern-Gerlach in cascata.":
        "Two cascaded Stern-Gerlach machines.",
    "Schema della disposizione delle macchine.":
        "Diagram of the arrangement of the machines.",
    "Seconda macchina verticale.":
        "Second machine vertical.",
    "Seconda macchina a novanta gradi.":
        "Second machine at ninety degrees.",
    "Entrambe le macchine inclinate.":
        "Both machines tilted.",
    "Tre macchine di Stern-Gerlach in cascata.":
        "Three cascaded Stern-Gerlach machines.",
    "Schema del primo esperimento.":
        "Diagram of the first experiment.",
    "Ricombinazione di due fasci.":
        "Recombination of two beams.",
    "Apparato dell'esperimento 3.":
        "Apparatus of experiment 3.",
    "I tre casi di misura.":
        "The three measurement cases.",
    "Apparato dell'esperimento 4.":
        "Apparatus of experiment 4.",
    "I due cammini con sfasamento.":
        "The two paths with a phase shift.",
    "La scatola con le macchine di Stern-Gerlach.":
        "The box containing the Stern-Gerlach machines.",

    # ---- Capitolo 3 ----
    "Fig. 1 \u2014 Ampolla di vetro con i due elettrodi A e B.":
        "Fig. 1 \u2014 Glass bulb with the two electrodes A and B.",
    "Fig. 2 \u2014 Circuito per rilevare la corrente nel vuoto.":
        "Fig. 2 \u2014 Circuit for detecting the current in a vacuum.",
    "Fig. 3 \u2014 Schema del cannone elettronico.":
        "Fig. 3 \u2014 Diagram of the electron gun.",
    "Fig. 4 \u2014 Schermo ai fosfori.":
        "Fig. 4 \u2014 Phosphor screen.",
    "Fig. 5 \u2014 Apparato per la deflessione mediante campo elettrico.":
        "Fig. 5 \u2014 Apparatus for deflection by an electric field.",
    "Fig. 6 \u2014 Deflessione del fascio mediante campo magnetico.":
        "Fig. 6 \u2014 Deflection of the beam by a magnetic field.",
    "Deflessione dovuta al campo elettrico.":
        "Deflection due to the electric field.",
    "Deflessione dovuta al campo magnetico.":
        "Deflection due to the magnetic field.",
    "Fig. 7 \u2014 Apparato per la separazione dell'atomo in ioni ed elettroni.":
        "Fig. 7 \u2014 Apparatus for separating the atom into ions and electrons.",
    "Fig. 8 \u2014 I due punti luminosi sugli schermi.":
        "Fig. 8 \u2014 The two bright spots on the screens.",
    "Fig. 9 \u2014 Deflessione dei fasci di ioni ed elettroni.":
        "Fig. 9 \u2014 Deflection of the ion and electron beams.",
    "Fig. 10 \u2014 Gli ioni positivi possono generare più punti luminosi.":
        "Fig. 10 \u2014 Positive ions can produce several bright spots.",
    "Fig. 11 \u2014 Foto dell'apparecchiatura di Millikan.":
        "Fig. 11 \u2014 Photograph of Millikan's apparatus.",
    "Fig. 12 \u2014 Microscopio (a sinistra) e lampada (a destra).":
        "Fig. 12 \u2014 Microscope (left) and lamp (right).",
    "Fig. 13 \u2014 Nebulizzatore per l'olio a effetto Venturi.":
        "Fig. 13 \u2014 Venturi-effect atomiser for the oil.",
    "Fig. 14 \u2014 Schema del nebulizzatore, del condensatore e delle goccioline.":
        "Fig. 14 \u2014 Diagram of the atomiser, the capacitor and the droplets.",
    "Fig. 15 \u2014 Foto del condensatore e della camera che lo racchiude.":
        "Fig. 15 \u2014 Photograph of the capacitor and the chamber enclosing it.",
    "Fig. 16 \u2014 Vista delle goccioline attraverso il microscopio.":
        "Fig. 16 \u2014 View of the droplets through the microscope.",
    "Fig. 17 \u2014 Le piastre del condensatore alimentate con la tensione V.":
        "Fig. 17 \u2014 The capacitor plates supplied with the voltage V.",
    "Istogramma delle frequenze delle misure di carica q (10^-19 C).":
        "Histogram of the measured charges q (10^-19 C).",

    # ---- Capitolo 4 ----
    "Schema di principio dell'esperimento.":
        "Schematic principle of the experiment.",
    "Struttura cristallina: reticolo tridimensionale di nuclei.":
        "Crystal structure: three-dimensional lattice of nuclei.",
    "Previsione classica: deflessione dell'elettrone nel cristallo.":
        "Classical prediction: deflection of the electron in the crystal.",
    "Previsione classica: distribuzione di probabilità a campana per l'angolo \u03b4.":
        "Classical prediction: bell-shaped probability distribution for the angle \u03b4.",
    "Foto dell'ampolla di vetro sotto vuoto.":
        "Photograph of the evacuated glass bulb.",
    "Dettaglio del cannone elettronico.":
        "Detail of the electron gun.",
    "Schema dell'ampolla con cannone e lamina.":
        "Diagram of the bulb with the gun and the foil.",
    "Schema di alimentazione del sistema.":
        "Wiring diagram of the system.",
    "L'intero sistema alimentato.":
        "The whole system powered up.",
    "Immagine ottenuta sullo schermo: punto centrale e due cerchi.":
        "Image obtained on the screen: central spot and two rings.",
    "La stessa immagine di diffrazione, in bianco e nero.":
        "The same diffraction image, in black and white.",
    "Relazione tra gli angoli di deflessione \u03b4\u2081, \u03b4\u2082 e i due cerchi concentrici.":
        "Relation between the deflection angles \u03b4\u2081, \u03b4\u2082 and the two concentric rings.",
    "Angoli \u03b4\u2081, \u03b4\u2082 in funzione della tensione V.":
        "Angles \u03b4\u2081, \u03b4\u2082 as a function of the voltage V.",
    "Angoli \u03b4\u2081, \u03b4\u2082 in funzione dell'inverso della radice della tensione.":
        "Angles \u03b4\u2081, \u03b4\u2082 as a function of the inverse square root of the voltage.",
    "Struttura cristallina piana della grafite.":
        "Planar crystal structure of graphite.",
    "Sottoreticoli a linee parallele individuati nel reticolo della grafite.":
        "Sub-lattices of parallel lines identified in the graphite lattice.",
    "Scomposizione del reticolo in reticoli a linee parallele.":
        "Decomposition of the lattice into lattices of parallel lines.",
    "Immagine prodotta da un singolo cristallo.":
        "Image produced by a single crystal.",
    "Sovrapposizione di cristalli orientati a caso: si formano i cerchi.":
        "Superposition of randomly oriented crystals: the rings appear.",

    # ---- Capitolo 5 ----
    "In un cristallo il volume di un atomo è quasi tutto vuoto; il nucleo sta al centro.":
        "In a crystal the volume of an atom is almost entirely empty; the nucleus sits at the centre.",
    "Schema dell'apparato: sorgente, collimatore, lamina d'oro, rilevatore.":
        "Diagram of the apparatus: source, collimator, gold foil, detector.",
    "Il preparato radioattivo Am241.":
        "The radioactive Am241 source.",
    "La lamina d'oro con le fenditure di collimazione.":
        "The gold foil with the collimating slits.",
    "Il detector al silicio e l'amplificatore di misura.":
        "The silicon detector and the measuring amplifier.",
    "Caduta della resistenza del detector al passaggio di una particella \u03b1.":
        "Drop in the detector resistance as an \u03b1 particle passes through.",
    "L'amplificatore dal lato dei morsetti di uscita.":
        "The amplifier seen from the output terminals.",
    "L'impulso squadrato e la tensione di soglia U.":
        "The squared pulse and the threshold voltage U.",
    "L'intero apparato sperimentale.":
        "The whole experimental apparatus.",
    "La camera aperta con tutti i componenti.":
        "The chamber open, with all the components.",
    "La camera chiusa con il goniometro.":
        "The chamber closed, with the goniometer.",
    "Dettaglio del goniometro con la scala graduata per l'angolo.":
        "Detail of the goniometer with the graduated scale for the angle.",
    "N/\u0394t in funzione dell'angolo \u03d1.":
        "N/\u0394t as a function of the angle \u03d1.",
    "Urto contro atomi immaginati come sferette piene.":
        "Collision with atoms imagined as solid little spheres.",
    "Con nuclei piccolissimi la lamina è quasi trasparente ai raggi \u03b1.":
        "With very small nuclei the foil is almost transparent to \u03b1 rays.",
    "Geometria della diffusione.":
        "Geometry of the scattering.",
    "Onda piana incidente \u2192 onda piana più onda sferica divergente.":
        "Incident plane wave \u2192 plane wave plus outgoing spherical wave.",
    "Un fascio stretto: solo l'onda sferica raggiunge il detector.":
        "A narrow beam: only the spherical wave reaches the detector.",
    "Confronto misure/teoria in scala lineare.":
        "Comparison of measurement and theory on a linear scale.",
    "Confronto misure/teoria in scala logaritmica.":
        "Comparison of measurement and theory on a logarithmic scale.",
    "Approssimazione della superficie con un cilindro.":
        "Approximation of the surface by a cylinder.",
    "Angolo solido del rivelatore.":
        "Solid angle of the detector.",
    "Confronto finale teoria/misure.":
        "Final comparison of theory and measurement.",

    # ---- Capitolo 7 ----
    "Ampolla con gli elettrodi.":
        "Bulb with the electrodes.",
    "Alimentazione degli elettrodi.":
        "Power supply to the electrodes.",
    "Foto dell'ampolla contenente il neon.":
        "Photograph of the bulb containing the neon.",
    "L'intero apparato sperimentale (neon).":
        "The whole experimental apparatus (neon).",
    "Schermo dell'oscilloscopio: diagramma tensione/corrente.":
        "Oscilloscope screen: voltage/current plot.",
    "Corrente in funzione della tensione: massimi e minimi.":
        "Current as a function of voltage: maxima and minima.",
    "Le zone luminose tra le griglie (a 70 V).":
        "The glowing regions between the grids (at 70 V).",
    "Apparato sperimentale per il mercurio.":
        "Experimental apparatus for mercury.",
    "Grafico tensione/corrente per il mercurio: sei massimi.":
        "Voltage/current plot for mercury: six maxima.",
    "Apparato Franck-Hertz con acquisizione della curva al computer.":
        "Franck-Hertz apparatus with the curve acquired by computer.",
    "Apparato Franck-Hertz con registrazione della curva tramite plotter.":
        "Franck-Hertz apparatus with the curve recorded by a plotter.",

    # ---- Capitolo 8 ----
    "L'effetto fotoelettrico: la luce estrae elettroni dal metallo.":
        "The photoelectric effect: light ejects electrons from the metal.",
    "Sistema di rilevazione: catodo, anodo e corrente I.":
        "Detection system: cathode, anode and current I.",
    "Sistema per misurare l'energia degli elettroni (condensatore).":
        "System for measuring the energy of the electrons (capacitor).",
    "Foto dell'ampolla usata nell'esperimento.":
        "Photograph of the bulb used in the experiment.",
    "L'ampolla montata sul supporto.":
        "The bulb mounted on its holder.",
    "Lampada ai vapori di mercurio.":
        "Mercury vapour lamp.",
    "Filtro interferometrico per il blu.":
        "Interference filter for blue.",
    "Filtro interferometrico per il giallo.":
        "Interference filter for yellow.",
    "Supporto dei quattro filtri con diaframma a iride.":
        "Holder for the four filters, with iris diaphragm.",
    "Il banco ottico montato.":
        "The optical bench assembled.",
    "L'intero apparato sperimentale in funzione.":
        "The whole experimental apparatus in operation.",
    "Con un normale voltmetro la corrente fotoelettrica si richiude sul voltmetro.":
        "With an ordinary voltmeter the photoelectric current flows back through the voltmeter.",
    "Il separatore di impedenza per misurare la tensione.":
        "The impedance buffer used to measure the voltage.",

    # ---- Capitolo 9 ----
    "Passaggio da uno stato di energia iniziale a uno finale.":
        "Transition from an initial energy state to a final one.",
    "Il reticolo di diffrazione.":
        "The diffraction grating.",
    "Livelli energetici dell'atomo di idrogeno.":
        "Energy levels of the hydrogen atom.",
    "I possibili salti energetici tra i livelli.":
        "The possible energy jumps between the levels.",
    "Quattro tubicini con gas diversi (ossigeno, neon, argon, azoto).":
        "Four small tubes with different gases (oxygen, neon, argon, nitrogen).",
    "Il tubo contenente neon acceso.":
        "The tube containing neon, lit.",
    "Il banco ottico: tubo, lenti, reticolo e schermo.":
        "The optical bench: tube, lenses, grating and screen.",
    "L'immagine sullo schermo: le righe dei diversi colori.":
        "The image on the screen: the lines of the different colours.",
    "Immagine spettrale della lampada al mercurio.":
        "Spectral image of the mercury lamp.",
    "Lampada di Balmer (idrogeno).":
        "Balmer lamp (hydrogen).",
    "Spettrometro a goniometro.":
        "Goniometer spectrometer.",

    # ---- Laboratori: descrizioni degli schemi per i lettori di schermo ----
    "Esperimento 1: due macchine di Stern-Gerlach in cascata":
        "Experiment 1: two cascaded Stern-Gerlach machines",
    "grafico delle misure":
        "chart of the measurements",
    "Esperimento 2: tre macchine di Stern-Gerlach in cascata":
        "Experiment 2: three cascaded Stern-Gerlach machines",
    "Esperimento 3: scomposizione e ricombinazione del fascio":
        "Experiment 3: splitting and recombination of the beam",
    "Esperimento 4: scomposizione e ricombinazione del fascio":
        "Experiment 4: splitting and recombination of the beam",
    "sfasamento \u03c6":
        "phase shift \u03c6",
    "curva P(m\u2080=\u2212k) in funzione di \u03c6":
        "curve P(m\u2080=\u2212k) as a function of \u03c6",
    "Ampolla con filamento A e anodo B":
        "Bulb with filament A and anode B",
    "grafico corrente-tensione":
        "current-voltage chart",
    "Cannone elettronico, piastre, bobine e schermo":
        "Electron gun, plates, coils and screen",
    "Apparato di Millikan: camera di spruzzo, condensatore, goccia e microscopio":
        "Millikan apparatus: spray chamber, capacitor, droplet and microscope",
    "Distribuzione delle cariche misurate: pila di misure e somma di gaussiane con picchi ai multipli interi di e":
        "Distribution of the measured charges: stack of measurements and sum of Gaussians with peaks at integer multiples of e",
    "Schema laterale: cannone elettronico, campione cristallino, raggi diffratti e schermo":
        "Side diagram: electron gun, crystalline sample, diffracted rays and screen",
    "Schermo di rivelazione: gli elettroni arrivano uno a uno e si accumulano formando anelli (policristallo) o punti (monocristallo)":
        "Detection screen: the electrons arrive one at a time and build up into rings (polycrystal) or spots (single crystal)",
    "Vista dall'alto dell'apparato: sorgente di americio, collimatore, lamina d'oro e rivelatore mobile sul goniometro; le particelle alfa attraversano la lamina e vengono diffuse.":
        "Top view of the apparatus: americium source, collimator, gold foil and detector movable on the goniometer; the alpha particles cross the foil and are scattered.",
    "Grafico del numero di impulsi al secondo in funzione dell'angolo, con la curva teorica di Rutherford.":
        "Chart of the number of pulses per second as a function of the angle, with Rutherford's theoretical curve.",
    "Sezione dell'ampolla: filamento A, griglie B e C, elettrodo D; tra le griglie compaiono le zone luminose dove gli elettroni cedono energia agli atomi.":
        "Section of the bulb: filament A, grids B and C, electrode D; between the grids appear the glowing regions where the electrons give up energy to the atoms.",
    "Schermo dell'oscilloscopio: corrente I in funzione della tensione VBC, con i massimi e i minimi caratteristici.":
        "Oscilloscope screen: current I as a function of the voltage VBC, with the characteristic maxima and minima.",
    "Banco ottico: lampada a vapori di mercurio, diaframma a iride, filtro interferenziale, ampolla fotocellula con anello anodico e catodo fotosensibile, condensatore, separatore di impedenza e voltmetro.":
        "Optical bench: mercury vapour lamp, iris diaphragm, interference filter, photocell bulb with anode ring and photosensitive cathode, capacitor, impedance buffer and voltmeter.",
    "A sinistra la carica del condensatore nel tempo; a destra la tensione di sbarramento in funzione della frequenza, con la retta dei minimi quadrati.":
        "On the left the charging of the capacitor over time; on the right the stopping voltage as a function of frequency, with the least-squares line.",
    "Banco ottico visto dall'alto: tubo a scarica, fenditura, due lenti convergenti, reticolo di diffrazione al centro di un cerchio graduato e cannocchiale girevole.":
        "Optical bench seen from above: discharge tube, slit, two converging lenses, diffraction grating at the centre of a graduated circle and rotating telescope.",
    "Campo del cannocchiale: le righe spettrali viste attraverso l'oculare, con il crocifilo al centro.":
        "Field of the telescope: the spectral lines seen through the eyepiece, with the crosshair at the centre.",
    "Spettro registrato in lunghezza d'onda e diagramma dei livelli dell'atomo di idrogeno con i salti misurati.":
        "Spectrum recorded against wavelength, and diagram of the hydrogen levels with the measured jumps.",
    "Angolo del cannocchiale":
        "Angle of the telescope",
}

TRAD = {chiave(k): v for k, v in TRAD.items()}


def main():
    non_tradotti = []
    totale = 0
    for f in sorted(RADICE.glob('*.html')):
        t = f.read_text(encoding='utf-8')
        if 'class="it"' not in t:
            continue
        fatti = 0

        def per_tag(m):
            nonlocal fatti
            tag = m.group(0)
            if '-en="' in tag:
                return tag
            for a in ATTRIBUTI:
                mm = re.search(rf'\s{a}="([^"]*)"', tag)
                if not mm:
                    continue
                v = mm.group(1).strip()
                en = TRAD.get(chiave(v))
                if not v or en is None:
                    if v and chiave(v) not in ('Menu', 'Lingua / Language', 'Chiudi / Close'):
                        non_tradotti.append((f.name, a, v))
                    continue
                if en == v:
                    continue
                tag = tag[:mm.end()] + f' {a}-en="{en}"' + tag[mm.end():]
                fatti += 1
            return tag

        nuovo = re.sub(r'<[a-zA-Z][^>]*>', per_tag, t)
        if fatti:
            f.write_text(nuovo, encoding='utf-8')
            print(f'{f.name}: {fatti} attributi tradotti')
            totale += fatti

    print(f'\ntotale: {totale}')
    if non_tradotti:
        visti = set()
        print(f'\nsenza traduzione ({len(non_tradotti)}):')
        for nome, a, v in non_tradotti:
            if (a, v) in visti:
                continue
            visti.add((a, v))
            print(f'   [{nome}] {a}="{v[:80]}"')


if __name__ == '__main__':
    main()
