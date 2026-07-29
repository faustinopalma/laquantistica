/* LaTeX -> HTML KaTeX per la pre-generazione delle formule del sito.
 *
 * Legge da stdin un JSON [{i, tex, display}] e scrive su stdout [{i, html, err}].
 * L'uscita comprende sia il disegno sia il MathML nascosto che i lettori di
 * schermo leggono: KaTeX li produce insieme, e servono entrambi.
 *
 * Uso:  node tools/katexgen/tex2katex.js < build/katexgen/05.in.json > build/katexgen/05.out.json
 */
const path = require('path');
const katex = require(path.join(__dirname, '..', '..', 'build', 'katexcheck', 'node_modules', 'katex'));

let raw = '';
process.stdin.on('data', (d) => (raw += d));
process.stdin.on('end', () => {
  const items = JSON.parse(raw);
  const out = items.map((it) => {
    try {
      const html = katex.renderToString(it.tex, {
        displayMode: !!it.display,
        throwOnError: true,
        strict: false,
        trust: false,
      });
      return { i: it.i, html };
    } catch (e) {
      return { i: it.i, err: String(e.message).slice(0, 200) };
    }
  });
  process.stdout.write(JSON.stringify(out));
});
