/**
 * Prova a compilare con KaTeX tutte le formule del sito, per sapere quante
 * sopravviverebbero a una sostituzione di MathJax.
 *
 * Legge il LaTeX dagli attributi data-tex delle pagine pubblicate: è la
 * sorgente vera, quella da cui MathJax rigenera tutto.
 *
 *   node tools/katex_try.js
 */
const fs = require('fs');
const path = require('path');
const katex = require(path.join(__dirname, '..', 'build', 'katexcheck', 'node_modules', 'katex'));

const PUB = path.join(__dirname, '..', 'publish');
const files = fs.readdirSync(PUB).filter(f => f.endsWith('.html'));

const errori = new Map();   // messaggio -> [{pagina, tex}]
let tot = 0, ok = 0;

// data-tex contiene entità HTML: gli apici finiscono sempre in forma numerica
const decode = s => s
  .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
  .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
  .replace(/&amp;/g, '&');

for (const f of files) {
  const html = fs.readFileSync(path.join(PUB, f), 'utf8');
  const re = /data-tex="([^"]*)"/g;
  let m;
  while ((m = re.exec(html))) {
    const tex = decode(m[1]);
    tot++;
    try {
      katex.renderToString(tex, { displayMode: true, throwOnError: true, strict: false });
      ok++;
    } catch (e) {
      const msg = String(e.message).replace(/ at position \d+.*/, '').slice(0, 90);
      if (!errori.has(msg)) errori.set(msg, []);
      errori.get(msg).push({ pagina: f, tex: tex.slice(0, 70) });
    }
  }
}

console.log(`formule provate : ${tot}`);
console.log(`compilate       : ${ok}  (${(ok / tot * 100).toFixed(1)}%)`);
console.log(`fallite         : ${tot - ok}  (${((tot - ok) / tot * 100).toFixed(1)}%)\n`);

const ordinati = [...errori.entries()].sort((a, b) => b[1].length - a[1].length);
for (const [msg, casi] of ordinati) {
  console.log(`${String(casi.length).padStart(4)}x  ${msg}`);
  const pagine = [...new Set(casi.map(c => c.pagina))];
  console.log(`      pagine: ${pagine.join(', ')}`);
  console.log(`      es.: ${casi[0].tex.replace(/\n/g, ' ')}`);
}
