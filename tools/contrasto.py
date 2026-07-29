"""Misura il contrasto fra testo e sfondo sulle pagine del sito.

Le soglie sono quelle delle WCAG: 4,5 per il testo normale, 3 per quello grande
(da 24px, o da 18,66px se in grassetto) e per i bordi dei comandi.

Va usato con una pagina gia' aperta nel browser: qui c'e' solo il pezzo da
eseguire dentro la pagina, perche' il colore vero lo sa soltanto il browser
dopo aver applicato tutti i fogli di stile.

    node -e "..."   oppure incollato in run_playwright_code
"""

SCRIPT = r"""
(() => {
  const luminanza = (r, g, b) => {
    const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const rgb = s => (s.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
  const contrasto = (a, b) => {
    const [l1, l2] = [luminanza(...a), luminanza(...b)].sort((x, y) => y - x);
    return (l1 + 0.05) / (l2 + 0.05);
  };
  // lo sfondo vero: risalgo finche' non trovo un colore abbastanza opaco.
  // Un velo tipo rgba(255,255,255,.05) non copre nulla: contarlo come bianco
  // pieno fa bocciare testo chiaro che in realta' sta su fondo scuro.
  const sfondoDi = el => {
    for (let e = el; e; e = e.parentElement) {
      const c = getComputedStyle(e).backgroundColor;
      const n = (c.match(/[\d.]+/g) || []).map(Number);
      if (n.length === 3) return n;
      if (n.length === 4 && n[3] >= 0.5) return n.slice(0, 3);
    }
    return [255, 255, 255];
  };

  const esiti = [];
  const visti = new Set();
  for (const el of document.querySelectorAll('body *')) {
    if (!el.offsetParent && el.tagName !== 'BODY') continue;
    const testo = [...el.childNodes]
      .filter(n => n.nodeType === 3 && n.textContent.trim())
      .map(n => n.textContent.trim()).join(' ');
    if (!testo) continue;
    const st = getComputedStyle(el);
    const fg = rgb(st.color);
    const bg = sfondoDi(el);
    if (fg.length !== 3) continue;
    const px = parseFloat(st.fontSize);
    const grosso = px >= 24 || (px >= 18.66 && parseInt(st.fontWeight, 10) >= 700);
    const soglia = grosso ? 3 : 4.5;
    const c = contrasto(fg, bg);
    const chiave = `${st.color}|${bg.join(',')}|${Math.round(px)}`;
    if (visti.has(chiave)) continue;
    visti.add(chiave);
    esiti.push({
      passa: c >= soglia, rapporto: Math.round(c * 100) / 100, soglia,
      px: Math.round(px), colore: st.color, sfondo: `rgb(${bg.join(', ')})`,
      dove: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
      esempio: testo.slice(0, 40)
    });
  }
  return {
    combinazioni: esiti.length,
    bocciate: esiti.filter(e => !e.passa),
    peggiore: esiti.sort((a, b) => a.rapporto - b.rapporto)[0]
  };
})()
"""

if __name__ == '__main__':
    print(SCRIPT)
