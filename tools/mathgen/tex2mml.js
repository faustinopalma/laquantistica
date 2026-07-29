/* LaTeX -> MathML per la conversione delle formule del sito.
 *
 * Legge da stdin un JSON [{i, tex, display}] e scrive su stdout [{i, mml, err}].
 * Usa lo stesso motore TeX di MathJax che rende le pagine, quindi il MathML
 * prodotto e' esattamente l'albero da cui MathJax genera l'SVG: la resa nel
 * sito non cambia rispetto a quella verificata nella pagina di confronto.
 *
 * Uso:  node tools/mathgen/tex2mml.js < build/mathgen/09.in.json > build/mathgen/09.out.json
 */
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
const { SerializedMmlVisitor } = require('mathjax-full/js/core/MmlTree/SerializedMmlVisitor.js');
const { STATE } = require('mathjax-full/js/core/MathItem.js');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');

RegisterHTMLHandler(liteAdaptor());

// bussproofs pretende un output jax con getBBox(): qui ci fermiamo al MathML.
const packages = AllPackages.filter((p) => p !== 'bussproofs');
// \oiint e \oiiint mancano dal repertorio di mathjax-full 3.2.2, su cui gira
// questo strumento: senza macro finirebbero in rosso (verificato). Il browser usa
// MathJax 4, che li conosce da se': la macro servira' finche' questo non passera'
// a @mathjax/src, dove mathjax-full e' proseguito.
const MACROS = { oiint: '∯', oiiint: '∰' };

const doc = mathjax.document('', { InputJax: new TeX({ packages, macros: MACROS }) });
const visitor = new SerializedMmlVisitor();

function convert(src, display) {
  const node = doc.convert(src, { display, end: STATE.CONVERT });
  return visitor.visitTree(node, doc);
}

let raw = '';
process.stdin.on('data', (d) => (raw += d));
process.stdin.on('end', () => {
  const items = JSON.parse(raw);
  const out = items.map((it) => {
    try {
      let mml = convert(it.tex, !!it.display);
      return { i: it.i, mml };
    } catch (e) {
      return { i: it.i, mml: '', err: String(e.message || e) };
    }
  });
  process.stdout.write(JSON.stringify(out));
});
