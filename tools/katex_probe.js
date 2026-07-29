/**
 * Verifica se KaTeX conosce davvero i costrutti su cui questo sito ha sofferto,
 * o se li accetta in silenzio rendendoli male.
 *
 *   node tools/katex_probe.js
 */
const path = require('path');
const katex = require(path.join(__dirname, '..', 'build', 'katexcheck', 'node_modules', 'katex'));

const prove = [
  ['integrale di superficie chiusa', '\\oiint_{\\Sigma_\\Omega} \\vec{J}\\cdot d\\vec{S}'],
  ['integrale di volume chiuso', '\\oiiint_\\Omega p\\:d\\Omega'],
  ['frazione a dimensione piena', '{\\displaystyle \\frac{\\hbar^2}{2m}}'],
  ['matrice fra parentesi', '\\begin{pmatrix} \\alpha_1 & \\alpha_2 \\\\ \\beta_1 & \\beta_2 \\end{pmatrix}'],
  ['gathered dentro parentesi', '\\left(\\begin{gathered}\\alpha_1\\\\\\alpha_2\\end{gathered}\\right)'],
  ['allineamento a più righe', '\\begin{aligned} a & = b \\\\ c & = d \\end{aligned}'],
  ['bra-ket', '\\langle\\alpha|\\beta\\rangle = \\alpha_1^*\\beta_1'],
  ['barra di Dirac elastica', '\\left|\\langle g\'|\\psi\\rangle\\right|^2'],
  ['primo su lettera greca', '\\alpha\' + \\beta\''],
  ['sopralineatura', '\\overline{g\'} \\quad \\overline{\\vec{r}}'],
  ['testo con accento', '\\text{unità di misura}'],
  ['quantificatore', '\\langle\\alpha_j|\\alpha_k\\rangle = 0 \\;\\forall j \\neq k'],
  ['sistema di equazioni', '\\begin{cases} x = 1 \\\\ y = 2 \\end{cases}'],
  ['array', '\\begin{array}{cc} a & b \\\\ c & d \\end{array}'],
  ['seno in tondo', '\\sin\\theta + \\cos\\theta'],
  ['sommatoria con limiti', '\\sum_{n=1}^{\\infty} \\frac{1}{n^2}'],
  ['implicazione doppia', 'a \\Longrightarrow b'],
  ['prodotto scalare puntato', '\\vec{a}\\cdot\\vec{b}'],
];

for (const [nome, tex] of prove) {
  let esito, dettaglio = '';
  try {
    const html = katex.renderToString(tex, { displayMode: true, throwOnError: true, strict: 'error' });
    // un comando ignorato non lascia traccia: cerchiamo il colore d'errore di KaTeX
    esito = /katex-error/.test(html) ? 'RESO MALE' : 'ok';
    const mml = (html.match(/<math[\s\S]*?<\/math>/) || [''])[0];
    dettaglio = `mathml ${mml ? mml.length + ' car.' : 'ASSENTE'}`;
  } catch (e) {
    esito = 'FALLITO';
    dettaglio = String(e.message).slice(0, 70);
  }
  console.log(`${esito.padEnd(10)} ${nome.padEnd(32)} ${dettaglio}`);
}
