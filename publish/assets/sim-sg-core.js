/* Simulatore Stern-Gerlach — nucleo condiviso: helper SVG, disegno macchine, fisica, plotter.
   Ogni pagina esperimento usa questi helper e definisce il proprio apparato. */

var SVGNS = 'http://www.w3.org/2000/svg';
// palette "laboratorio di elettronica" (oscilloscopio): tracce fosforo su schermo scuro
var ACC = '#ffb000', BLU = '#35c8ff', INK = '#cfe0d6', DIM = '#4a6b59', PANEL = '#0d1a15';

function el(tag, attrs, parent) {
  var e = document.createElementNS(SVGNS, tag);
  for (var k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function txt(x, y, s, attrs, parent) {
  var t = el('text', Object.assign({ x: x, y: y }, attrs || {}), parent);
  t.textContent = s;
  return t;
}
function fmtPct(p) { return (Math.round(p * 1000) / 10) + '%'; }
function num(x) { var r = Math.round(x * 1000) / 1000; return (r === 0 ? 0 : r).toString(); }

/* ---- fasci ---- */
function beam(x1, y1, x2, y2, w, op, color, parent) {
  return el('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: color, 'stroke-width': w, opacity: op, 'stroke-linecap': 'round' }, parent);
}
// raccordo a S con tangenti orizzontali agli estremi
function curveBeam(x1, y1, x2, y2, w, op, color, parent) {
  var mx = (x1 + x2) / 2;
  var d = 'M' + x1 + ' ' + y1 + ' C ' + mx + ' ' + y1 + ' ' + mx + ' ' + y2 + ' ' + x2 + ' ' + y2;
  return el('path', { d: d, fill: 'none', stroke: color, 'stroke-width': w, opacity: op, 'stroke-linecap': 'round' }, parent);
}
function detector(x, y, col, parent) {
  el('circle', { cx: x, cy: y, r: 6, fill: col, stroke: '#111', 'stroke-width': 1 }, parent);
}
// fermo del fascio (tratteggiato), come nei disegni della tesi
function hatchStop(x, y, parent) {
  var g = el('g', {}, parent);
  el('rect', { x: x - 4, y: y - 15, width: 8, height: 30, fill: PANEL, stroke: INK, 'stroke-width': 1.4 }, g);
  for (var i = -13; i <= 13; i += 5) { el('line', { x1: x - 4, y1: y + i + 8, x2: x + 4, y2: y + i, stroke: INK, 'stroke-width': 1 }, g); }
  return g;
}

/* ---- macchina di Stern-Gerlach in SEZIONE TRASVERSALE ----
   polo superiore a lama (▽) + polo inferiore con gola (⊃), asse a tratto-punto,
   ruota di `angle` gradi; se angle≠0 disegna il riferimento verticale + arco dell'angolo. */
function sgMagnet(cx, cy, angle, label, parent) {
  var a = ((angle % 360) + 360) % 360;
  if (label) txt(cx, cy - 66, label, { 'text-anchor': 'middle', 'font-family': 'monospace', 'font-size': 11, fill: INK }, parent);
  if (a > 0.5 && a < 359.5) {
    el('line', { x1: cx, y1: cy - 52, x2: cx, y2: cy - 16, stroke: '#5a7d6a', 'stroke-width': 1, 'stroke-dasharray': '5 3 1 3' }, parent);
    var R = 30, rad = a * Math.PI / 180, x2 = cx + R * Math.sin(rad), y2 = cy - R * Math.cos(rad), sweep = a <= 180 ? 1 : 0;
    el('path', { d: 'M ' + cx + ' ' + (cy - R) + ' A ' + R + ' ' + R + ' 0 0 ' + sweep + ' ' + x2.toFixed(1) + ' ' + y2.toFixed(1), fill: 'none', stroke: '#5a7d6a', 'stroke-width': 1 }, parent);
  }
  var g = el('g', { transform: 'rotate(' + angle + ' ' + cx + ' ' + cy + ')' }, parent);
  var uw = 14;
  el('polygon', {
    points: (cx - uw) + ',' + (cy - 44) + ' ' + (cx + uw) + ',' + (cy - 44) + ' ' + (cx + uw) + ',' + (cy - 28) + ' ' + cx + ',' + (cy - 6) + ' ' + (cx - uw) + ',' + (cy - 28),
    fill: PANEL, stroke: INK, 'stroke-width': 1.6, 'stroke-linejoin': 'round'
  }, g);
  var lw = 17;
  var d = 'M' + (cx - lw) + ' ' + (cy + 40) + ' L' + (cx + lw) + ' ' + (cy + 40) + ' L' + (cx + lw) + ' ' + (cy + 8) +
    ' L' + (cx + 9) + ' ' + (cy + 8) + ' Q' + cx + ' ' + (cy + 20) + ' ' + (cx - 9) + ' ' + (cy + 8) + ' L' + (cx - lw) + ' ' + (cy + 8) + ' Z';
  el('path', { d: d, fill: PANEL, stroke: INK, 'stroke-width': 1.6, 'stroke-linejoin': 'round' }, g);
  el('line', { x1: cx, y1: cy - 52, x2: cx, y2: cy + 48, stroke: INK, 'stroke-width': 1, 'stroke-dasharray': '7 3 1.5 3' }, g);
  return g;
}

/* ---- fisica ---- */
function ketVec(theta, sign) {
  var t = theta * Math.PI / 360;
  return sign > 0 ? [Math.cos(t), Math.sin(t)] : [Math.sin(t), -Math.cos(t)];
}
function amp(state, phi, sign) {
  var p = phi * Math.PI / 360;
  return sign > 0 ? Math.cos(p) * state[0] + Math.sin(p) * state[1] : Math.sin(p) * state[0] - Math.cos(p) * state[1];
}

/* ---- plotter / registratore: registra punti di misura e traccia l'interpolante ---- */
function makePlotter(o) {
  var svg = document.getElementById(o.svg), stat = document.getElementById(o.stat),
    rec = document.getElementById(o.rec), fit = document.getElementById(o.fit);
  var BINS = 32, W = 660, H = 210, mL = 42, mR = 16, mT = 14, mB = 28;
  var data = {}, recTimer = null, curveDrawn = false, gDyn = null;
  function X(x) { return mL + (x - o.xmin) / (o.xmax - o.xmin) * (W - mL - mR); }
  function Y(p) { return H - mB - p * (H - mT - mB); }
  function full() { while (svg.firstChild) svg.removeChild(svg.firstChild); gDyn = el('g', {}, svg); curveDrawn = false; }
  function reset() { data = {}; full(); draw(); }
  function record(x) {
    var b = Math.round((x - o.xmin) / (o.xmax - o.xmin) * BINS);
    var y = o.fn(x) + (Math.random() - 0.5) * 0.03;
    data[b] = { x: x, y: Math.max(0, Math.min(1, y)) };
    if (rec) { rec.classList.add('on'); clearTimeout(recTimer); recTimer = setTimeout(function () { rec.classList.remove('on'); }, 340); }
    draw();
  }
  // crea la curva interpolante UNA VOLTA e la anima da sinistra a destra
  function drawCurveAnimated() {
    var d = '', i;
    for (i = 0; i <= 170; i++) { var xx = o.xmin + (o.xmax - o.xmin) * i / 170; d += (i ? 'L' : 'M') + X(xx).toFixed(1) + ' ' + Y(o.fn(xx)).toFixed(1) + ' '; }
    var path = el('path', { d: d, fill: 'none', stroke: o.color, 'stroke-width': 2, opacity: .95 }, svg); // sopra il layer dinamico
    path.style.filter = 'drop-shadow(0 0 3px ' + o.color + ')';
    try {
      var L = path.getTotalLength();
      if (L > 0) {
        path.style.strokeDasharray = L; path.style.strokeDashoffset = L;
        path.getBoundingClientRect(); // forza il reflow
        path.style.transition = 'stroke-dashoffset 1.15s cubic-bezier(.25,.72,.3,1)';
        path.style.strokeDashoffset = '0';
      }
    } catch (e) { }
  }
  function draw() {
    if (!gDyn) full();
    while (gDyn.firstChild) gDyn.removeChild(gDyn.firstChild);   // ridisegna solo griglia + punti
    var p, i;
    for (p = 0; p <= 1.0001; p += 0.25) {
      var gy = Y(p);
      el('line', { x1: mL, y1: gy, x2: W - mR, y2: gy, stroke: '#123026', 'stroke-width': 1 }, gDyn);
      txt(mL - 6, gy + 3, Math.round(p * 100) + '', { 'text-anchor': 'end', 'font-size': 9, fill: '#3e6b58', 'font-family': 'monospace' }, gDyn);
    }
    var span = o.xmax - o.xmin, step = span / 6;
    for (i = 0; i <= 6; i++) {
      var xv = o.xmin + step * i, gx = X(xv);
      el('line', { x1: gx, y1: mT, x2: gx, y2: H - mB, stroke: '#0d241b', 'stroke-width': 1 }, gDyn);
      txt(gx, H - mB + 14, Math.round(xv) + '', { 'text-anchor': 'middle', 'font-size': 9, fill: '#3e6b58', 'font-family': 'monospace' }, gDyn);
    }
    txt(mL - 30, Y(0.5), 'P', { 'font-size': 10, fill: '#57d98a', 'font-family': 'monospace' }, gDyn);
    txt(W - mR, H - 4, o.xlabel, { 'text-anchor': 'end', 'font-size': 9, fill: '#3e6b58', 'font-family': 'monospace' }, gDyn);
    var keys = Object.keys(data), cov = keys.length / (BINS + 1), done = cov >= 0.82;
    keys.forEach(function (k) {
      var pt = data[k], px = X(pt.x), py = Y(pt.y);
      el('line', { x1: px - 3, y1: py, x2: px + 3, y2: py, stroke: '#e6ece8', 'stroke-width': 1.2 }, gDyn);
      el('line', { x1: px, y1: py - 3, x2: px, y2: py + 3, stroke: '#e6ece8', 'stroke-width': 1.2 }, gDyn);
    });
    if (done && !curveDrawn) { drawCurveAnimated(); curveDrawn = true; }
    if (fit) fit.classList.toggle('on', curveDrawn);
    if (stat) stat.textContent = 'n = ' + keys.length + '   ·   ' + (curveDrawn ? 'interpolante tracciata' : 'copertura ' + Math.round(cov * 100) + '%');
  }
  return { record: record, reset: reset, draw: draw };
}

/* ---- back-link (?ret=) ---- */
function safeRet(v) {
  if (!v) return null;
  try { v = decodeURIComponent(v); } catch (e) { return null; }
  if (v.indexOf('..') !== -1 || v.indexOf('//') !== -1) return null;
  if (!/^[\w./#%-]+$/.test(v)) return null;
  return v;
}
function initBackLink(def) {
  var ret = safeRet(new URLSearchParams(location.search).get('ret')) || def;
  ['backTop', 'backBottom'].forEach(function (id) { var a = document.getElementById(id); if (a) a.setAttribute('href', ret); });
}
