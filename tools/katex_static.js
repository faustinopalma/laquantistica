/**
 * Misura quanto peserebbero le pagine se le formule fossero generate con KaTeX
 * in fase di build invece che dal browser: nessun JavaScript da eseguire,
 * formule già impaginate nel sorgente.
 *
 *   node tools/katex_static.js publish/05-rutherford.html
 */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const katex = require(path.join(__dirname, '..', 'build', 'katexcheck', 'node_modules', 'katex'));

const decode = s => s
  .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
  .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&amp;/g, '&');

const gz = b => zlib.gzipSync(Buffer.from(b), { level: 9 }).length;
const kB = n => (n / 1024).toFixed(1).padStart(7);

for (const file of process.argv.slice(2)) {
  const html = fs.readFileSync(file, 'utf8');
  const tex = [...html.matchAll(/data-tex="([^"]*)"/g)].map(m => decode(m[1]));
  const mml = (html.match(/<math[\s\S]*?<\/math>/g) || []).join('');

  const t0 = Date.now();
  let out = '';
  for (const t of tex) out += katex.renderToString(t, { displayMode: true, throwOnError: false, strict: false });
  const ms = Date.now() - t0;

  console.log(`\n${path.basename(file)} — ${tex.length} formule`);
  console.log(`  generazione            ${ms} ms (una volta sola, in fase di build)`);
  console.log(`  MathML ora nel file   ${kB(mml.length)} kB ->${kB(gz(mml))} kB compresso`);
  console.log(`  KaTeX pre-generato    ${kB(out.length)} kB ->${kB(gz(out))} kB compresso`);
  console.log(`  pagina intera ora     ${kB(html.length)} kB ->${kB(gz(html))} kB compresso`);
}
