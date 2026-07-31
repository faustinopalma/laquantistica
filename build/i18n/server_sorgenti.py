"""Server d'appoggio per il confronto: serve sorgenti/ prendendo pero' assets e
immagini da publish/. Usato solo dai controlli, non fa parte del sito."""
import pathlib
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[2]


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = urlparse(path).path
        if p.startswith('/assets/') or p.startswith('/img/'):
            return str(ROOT / 'publish' / p.lstrip('/'))
        return super().translate_path(path)

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    server = ThreadingHTTPServer(
        ('127.0.0.1', 8792),
        partial(Handler, directory=str(ROOT / 'sorgenti')))
    print('sorgenti su http://127.0.0.1:8792')
    server.serve_forever()
