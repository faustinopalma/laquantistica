# La Quantistica — Fundamental Experiments of Quantum Mechanics

Digital edition of the 1999 degree thesis by **Faustino Palma**: an introductory
course in Quantum Mechanics that starts from the fundamental experiments and
**derives** the Schrödinger equation instead of postulating it.

> Work presented at the 85th National Congress of the **Italian Physical Society
> (SIF)**, Pavia, September 1999. LAFIDIN teaching laboratory — University of
> Naples «Federico II».

🌐 **Web edition (Italian and English):** [laquantistica.com](https://laquantistica.com)

---

## What it is

The thesis performs the historic experiments of atomic physics and, from their
analysis, builds a complete introduction to quantum theory, treated from the
outset with Dirac notation. The derivation of the Schrödinger equation does not
require Analytical Mechanics: it rests only on Newtonian mechanics and
electromagnetism.

To the 1999 text, the web edition adds twelve marginal notes, thirteen
interactive simulated laboratories — one for each experiment — and one card that
does not come from the thesis.

## The thirteen cards, in reading order

The experimental cards describe apparatus and measurements; the theoretical ones
build the theory starting from them.

1. Experiments with Electrons
2. Electron Diffraction
3. Complex Numbers and State Vectors
4. The Form of the Evolution Equation
5. The Hamiltonian and the Schrödinger Equation
6. The Rutherford Experiment
7. Rutherford’s Scattering Formula
8. The Franck–Hertz Experiment
9. The Photoelectric Effect
10. The Stern–Gerlach Experiment
11. Cascaded Stern–Gerlach Experiments
12. Further Developments of the Theory
13. Atomic Emission Spectra

## How this edition differs from the 1999 original

The text of the cards that come from the thesis is the 1999 text. What changed
is **the order in which the cards are read**, the fact that two of them have
been **split**, and one card that has been **added**. The contents and the
technical terminology have not been altered.

### The order

In the original, the path opened with the two Stern-Gerlach experiments, and
from them drew the principles on which everything else is built. That was
Feynman’s route, and the author had followed it: he had begun studying Quantum
Mechanics from the Feynman Lectures, knowing nothing of the subject, and wrote
the thesis in the order in which he had learned it.

Today that no longer convinces him. The cascaded Stern-Gerlach experiments are
thought experiments: at the time they were not feasible, and when they were
finally carried out — around 2019, on an atom chip — it was by methods that
require already knowing the theory they are supposed to ground. The premises
they rest on, such as the fact that the beams can be recombined leaving no trace
of the path taken, are not experimental data: they are a theoretical
requirement. Founding the theory on them asks the reader for a trust disguised
as proof.

Electron diffraction, on the other hand, was actually performed, with the tube
and the power supplies described in its card — and that card was already in the
original. So the path now starts from the electrons and builds the theory on an
experiment that was done. The four principles stay where they are, in the
introduction, but declared for what they are: premises. The two Stern-Gerlach
cards are at the end, where the reader has the means to judge them and where a
thought experiment is in its right place, because nobody is using it as proof
any more.

### The splits

In the original, the fourth and fifth cards held together the experiment and the
theory that follows from it, and the result was two very long chapters. They
have been split so that each card does one thing only: the fourth became three
cards, the fifth two. Nothing in the text has been moved or rewritten:
boundaries have been placed where the reasoning already paused. Two blocks of
pure calculation — the proofs of the commutator formulas and the two appendices
to the scattering calculation — have moved into notes; they remain readable in
full, but no longer interrupt the thread.

### The added card

The third card, *Complex Numbers and State Vectors*, is not in the thesis. In
1999 complex numbers and the algebra of complex vector spaces were taken as
known, and the reader met them scattered through the derivation. They are now
gathered before they are needed: why the probability amplitude is a complex
number, and the algebra of bras and kets used from that point on.

### The 1999 order

1. The Stern-Gerlach experiment
2. Cascaded Stern-Gerlach experiments
3. Experiments with electrons
4. Electron diffraction — *derivation of the Schrödinger equation* (now three cards)
5. The Rutherford experiment (now two cards)
6. Further developments of the theory
7. The Franck-Hertz experiment
8. The photoelectric effect
9. Atomic emission spectra

The same pages can still be read in this sequence; the site declares the change
in the note *[What has changed since 1999](https://laquantistica.com/en/nota-12-questa-edizione)*.

Apart from the reordering and the splits, the revision is limited to typos and
punctuation. The original, unrevised text is preserved in this repository in the
`originale-*` folders.

## Repository structure

| Folder | Contents |
|---|---|
| `originale-doc/` | The authentic 1999 original: legacy `.doc` files and technical drawings (`.DWG`/`.WMF`), kept as an archive |
| `originale-docx/` | Modern, openable `.docx` conversion of the thesis; the subfolders `da-doc-originale/` and `da-docx-originale/` record which source each conversion came from |
| `sorgenti/` | Bilingual source pages (Italian + English in one file); these are the ones you edit |
| `publish/` | The published site, generated from `sorgenti/`: `it/` and `en/`, one URL per language |
| `build/i18n/` | The generator: splits the bilingual sources into `it/` and `en/`, and checks the result |
| `img/` | Figures and images |
| `scripts/` | Site-generation tools |

The reading order lives in one place only, the `SCHEDE` list in
`build/ordine_schede.py`, which rewrites the chapter bar, the number in the
header and the previous/next links on every page.

## Editing a page

To revise the site you open a chapter in edit mode and correct it while looking
at it, without going through the code:

```powershell
.\modifica.ps1              # lists the chapters and asks which one
.\modifica.ps1 cascata      # opens the page whose name contains "cascata"
```

You edit the bilingual source in `sorgenti/`; on every save the two published
versions in `publish/it` and `publish/en` are regenerated on their own. To
rebuild the whole site:

```powershell
python build/i18n/split.py       # regenerates it/ and en/, sitemap and robots
python build/i18n/verifica.py    # checks language, canonical, hreflang, links
```

The browser opens on the real page. In there:

| gesture | effect |
|---|---|
| double-click on a sentence | correct it in place |
| double-click on a formula | edit the LaTeX, with preview |
| **↑ ↓** arrows to the left of a block | move it above or below |
| **Alt+click** | open that exact spot in VS Code |
| **Save** | write the text and formula corrections |

The arrows appear when hovering over a paragraph, a drawing or a formula, and
act **immediately**: reordering is judged by looking. Text corrections, instead,
accumulate until Save is pressed.

Every write leaves a backup in `backups/edits/` and a line in
`build/edits/journal.jsonl`, so it is always possible to go back and read what
was changed.

## License

- **Content** (thesis text, figures, teaching material): [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) — freely reusable with attribution to Faustino Palma.
- **Code** (scripts, site HTML/CSS/JavaScript): [MIT](LICENSE-CODE).

© 1999 Faustino Palma. Web edition 2026.
