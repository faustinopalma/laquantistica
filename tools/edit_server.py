"""Server locale per modificare le pagine direttamente nel browser.

NON fa parte del sito pubblicato: e' uno strumento di lavoro che gira solo su
questa macchina. Serve la cartella publish/ e, quando l'indirizzo contiene
?edit=1, inietta lo script di modifica. Le pagine pubblicate restano intatte.

    python tools/edit_server.py
    poi apri  http://127.0.0.1:8790/06-ulteriori-sviluppi.html?edit=1

Principi:
- si modifica SOLO l'italiano e le formule; l'inglese resta come sta e viene
  allineato in un secondo momento, leggendo il registro delle modifiche;
- ogni salvataggio passa da una sostituzione a coordinate esatte nel sorgente,
  calcolate con un parser che tiene traccia delle posizioni: se qualcosa non
  torna il salvataggio viene RIFIUTATO invece di scrivere a caso;
- prima di scrivere si fa una copia in backups/edits/;
- ogni modifica viene annotata in build/edits/journal.jsonl con il testo prima
  e dopo e la corrispondente frase inglese, cosi' si puo' chiedere la revisione
  di tutto in un colpo solo.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
import webbrowser
from datetime import datetime
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
PUBLISH = ROOT / 'publish'
ASSETS = ROOT / 'tools' / 'edit_assets'
BACKUPS = ROOT / 'backups' / 'edits'
JOURNAL = ROOT / 'build' / 'edits' / 'journal.jsonl'
NODE_TEX2MML = ROOT / 'tools' / 'mathgen' / 'tex2mml.js'
PORT = 8790

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}

# Lingue del sito. La PRIMA e' quella che si modifica nel browser; le altre
# vengono soltanto registrate, per essere allineate in un secondo momento.
# Per aggiungerne una terza basta metterla qui (e insegnarla a lang.js/lang.css).
LANGS = ('it', 'en')
PRIMARY = LANGS[0]

INJECT = (
    '<link rel="stylesheet" href="/__edit/edit.css">\n'
    '<script src="/__edit/edit.js" data-file="{file}"></script>\n'
)

# LaTeX scritto a mano dentro il testo: \( ... \) in linea, \[ ... \] a blocco
INLINE_TEX = re.compile(r'\\\((.+?)\\\)|\\\[(.+?)\\\]', re.S)


# ---------------------------------------------------------------- indicizzatore

class Indexer(HTMLParser):
    """Trova, nel sorgente grezzo, dove cominciano e finiscono gli elementi che
    si possono modificare: le frasi di ogni lingua e le formule."""

    def __init__(self, src: str):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.starts = [0] + [m.end() for m in re.finditer('\n', src)]
        self.stack: list[dict] = []
        self.depth_main = 0
        self.lang: dict[str, list[dict]] = {c: [] for c in LANGS}
        self.tex: list[dict] = []
        self.feed(src)
        self.close()

    def _abs(self) -> int:
        ln, col = self.getpos()
        return self.starts[ln - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self._abs()
        raw = self.get_starttag_text() or ''
        cstart = start + len(raw)
        d = dict(attrs)
        refs = []
        if tag == 'main':
            self.depth_main += 1
        if self.depth_main:
            classes = (d.get('class') or '').split()
            for code in LANGS:
                if code in classes:
                    refs.append(('lang', code, len(self.lang[code])))
                    self.lang[code].append({'start': cstart, 'line': self.getpos()[0]})
                    break
            if 'data-tex' in d:
                k = raw.find('data-tex="')
                vs = start + k + len('data-tex="')
                ve = start + raw.index('"', k + len('data-tex="'))
                refs.append(('tex', None, len(self.tex)))
                self.tex.append({'start': cstart, 'line': self.getpos()[0],
                                 'attr': (vs, ve),
                                 'display': 'block' in (d.get('class') or '')})
        if tag not in VOID:
            self.stack.append({'tag': tag, 'refs': refs})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1]['tag'] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        end = self._abs()
        while self.stack:
            frame = self.stack.pop()
            if frame['tag'] == tag:
                for kind, code, i in frame['refs']:
                    rows = self.lang[code] if kind == 'lang' else self.tex
                    rows[i]['end'] = end
                break
        if tag == 'main':
            self.depth_main -= 1


def index_page(path: Path):
    src = path.read_text(encoding='utf-8')
    ix = Indexer(src)
    lang = {c: [r for r in rows if 'end' in r] for c, rows in ix.lang.items()}
    tex = [r for r in ix.tex if 'end' in r]
    for rows in list(lang.values()) + [tex]:
        for row in rows:
            row['raw'] = src[row['start']:row['end']]
    for row in tex:
        row['tex'] = html.unescape(src[row['attr'][0]:row['attr'][1]])
    return src, lang, tex


# ---------------------------------------------------------------- LaTeX -> MathML

def tex_to_mml(items: list[dict]) -> dict[int, str]:
    if not items:
        return {}
    payload = json.dumps([{'i': i, 'tex': it['tex'], 'display': it['display']}
                          for i, it in enumerate(items)])
    res = subprocess.run(['node', str(NODE_TEX2MML)], input=payload,
                         capture_output=True, text=True, encoding='utf-8',
                         cwd=str(ROOT))
    if res.returncode != 0:
        raise RuntimeError(f'tex2mml: {res.stderr.strip()[:300]}')
    out = {}
    for row in json.loads(res.stdout):
        if row.get('err'):
            raise RuntimeError(f'LaTeX non valido: {row["err"]}')
        if 'mathcolor="red"' in row['mml']:
            raise RuntimeError('LaTeX contiene un comando sconosciuto')
        out[row['i']] = re.sub(r'>\s+<', '><', row['mml']).strip()
    return out


def expand_inline_tex(fragment: str) -> str:
    """Trasforma il LaTeX scritto a mano dentro il testo in una vera formula."""
    found = []

    def grab(m):
        tex = (m.group(1) or m.group(2)).strip()
        found.append({'tex': tex, 'display': m.group(2) is not None})
        return f'\x00{len(found) - 1}\x00'

    marked = INLINE_TEX.sub(grab, fragment)
    if not found:
        return fragment
    mml = tex_to_mml(found)
    for i, f in enumerate(found):
        cls = 'eq-mml eq-mml-block' if f['display'] else 'eq-inline eq-mml'
        span = (f'<span class="{cls}" data-tex="{html.escape(f["tex"], quote=True)}">'
                f'{mml[i]}</span>')
        marked = marked.replace(f'\x00{i}\x00', span)
    return marked


# ---------------------------------------------------------------- salvataggio

def safe_page(name: str) -> Path:
    if not name or '/' in name or '\\' in name or not name.endswith('.html'):
        raise ValueError('nome di file non ammesso')
    p = (PUBLISH / name).resolve()
    if p.parent != PUBLISH.resolve() or not p.is_file():
        raise ValueError('file inesistente')
    return p


def apply_edits(name: str, edits: list[dict]) -> dict:
    path = safe_page(name)
    src, lang, tex = index_page(path)
    primary = lang[PRIMARY]

    pieces = []            # (inizio, fine, nuovo testo)
    entries = []           # righe del registro
    for e in edits:
        kind, i = e['kind'], int(e['index'])
        rows = primary if kind == 'text' else tex
        if i >= len(rows):
            raise ValueError(f'{kind}[{i}] non esiste piu\': ricarica la pagina')
        row = rows[i]
        if row['raw'] != e['old']:
            raise ValueError(
                f'{kind}[{i}] riga {row["line"]}: il file e\' cambiato sotto i piedi, '
                'ricarica la pagina prima di salvare')
        if kind == 'text':
            new = expand_inline_tex(e['html'])
            pieces.append((row['start'], row['end'], new))
            # le altre lingue non si toccano: si annotano per allinearle dopo
            others = {c: (lang[c][i]['raw'] if i < len(lang[c]) else None)
                      for c in LANGS if c != PRIMARY}
            entries.append({'kind': 'text', 'lang': PRIMARY, 'index': i,
                            'line': row['line'], 'before': row['raw'],
                            'after': new, 'others': others})
        else:
            mml = tex_to_mml([{'tex': e['tex'], 'display': row['display']}])[0]
            pieces.append((row['attr'][0], row['attr'][1],
                           html.escape(e['tex'], quote=True)))
            pieces.append((row['start'], row['end'], mml))
            entries.append({'kind': 'tex', 'lang': None, 'index': i,
                            'line': row['line'], 'before': row['tex'],
                            'after': e['tex'], 'others': {}})

    out = src
    for start, end, new in sorted(pieces, key=lambda p: -p[0]):
        out = out[:start] + new + out[end:]

    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    shutil.copy2(path, BACKUPS / f'{path.stem}.{stamp}.html')
    path.write_text(out, encoding='utf-8')

    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open('a', encoding='utf-8') as f:
        for en_ in entries:
            en_.update({'t': datetime.now().isoformat(timespec='seconds'),
                        'file': name, 'reviewed': False})
            f.write(json.dumps(en_, ensure_ascii=False) + '\n')

    return {'ok': True, 'saved': len(entries),
            'backup': str((BACKUPS / f'{path.stem}.{stamp}.html').relative_to(ROOT))}


def open_in_vscode(name: str, line: int) -> dict:
    path = safe_page(name)
    exe = shutil.which('code') or shutil.which('code.cmd')
    if not exe:
        return {'ok': False, 'error': 'comando "code" non trovato nel PATH'}
    subprocess.Popen([exe, '-g', f'{path}:{max(1, int(line))}'], shell=False)
    return {'ok': True}


# ---------------------------------------------------------------- server

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(PUBLISH), **kw)

    def log_message(self, fmt, *args):
        if '__edit' not in (args[0] if args else ''):
            super().log_message(fmt, *args)

    # -- utilita' --------------------------------------------------------------

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n) or b'{}')

    def _local(self) -> bool:
        return self.client_address[0] in ('127.0.0.1', '::1')

    # -- GET -------------------------------------------------------------------

    def do_GET(self):
        if not self._local():
            self.send_error(403)
            return
        u = urlparse(self.path)
        q = parse_qs(u.query)

        if u.path.startswith('/__edit/'):
            leaf = u.path[len('/__edit/'):]
            if leaf in ('edit.js', 'edit.css'):
                data = (ASSETS / leaf).read_bytes()
                self.send_response(200)
                self.send_header('Content-Type',
                                 'application/javascript' if leaf.endswith('.js')
                                 else 'text/css')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(data)
                return
            if leaf == 'spans':
                try:
                    _, lang, tex = index_page(safe_page(q.get('file', [''])[0]))
                except ValueError as e:
                    return self._json({'error': str(e)}, 400)
                keep = ('line', 'raw', 'tex', 'display')
                pick = lambda rows: [{k: r[k] for k in keep if k in r} for r in rows]
                return self._json({'langs': LANGS, 'primary': PRIMARY,
                                   'lang': {c: pick(rows) for c, rows in lang.items()},
                                   'tex': pick(tex)})
            self.send_error(404)
            return

        # pagina normale: se c'e' ?edit=1 inietto lo script di modifica
        if q.get('edit') == ['1'] and u.path.endswith('.html'):
            try:
                path = safe_page(u.path.lstrip('/'))
            except ValueError:
                self.send_error(404)
                return
            src = path.read_text(encoding='utf-8')
            tag = INJECT.format(file=path.name)
            src = src.replace('</body>', tag + '</body>', 1)
            data = src.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
            return

        super().do_GET()

    # -- POST ------------------------------------------------------------------

    def do_POST(self):
        if not self._local():
            self.send_error(403)
            return
        u = urlparse(self.path)
        try:
            body = self._body()
            if u.path == '/__edit/save':
                return self._json(apply_edits(body['file'], body['edits']))
            if u.path == '/__edit/open':
                return self._json(open_in_vscode(body['file'], body['line']))
            if u.path == '/__edit/preview':
                mml = tex_to_mml([{'tex': body['tex'], 'display': body.get('display', False)}])
                return self._json({'ok': True, 'mml': mml[0]})
        except Exception as e:                       # errore = rifiuto, mai scrittura a caso
            return self._json({'error': str(e)}, 400)
        self.send_error(404)


def main():
    page = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
    url = f'http://127.0.0.1:{PORT}/{page}?edit=1'
    print(f'Modifica locale attiva su {url}')
    print('Ctrl+C per fermare. Le pagine pubblicate non contengono nulla di tutto questo.')
    try:
        webbrowser.open(url)
    except Exception:
        pass
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()


if __name__ == '__main__':
    main()
