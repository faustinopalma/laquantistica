import pathlib
def mml(name):
    t = pathlib.Path(f'build/ch2_overrides/{name}.svg.mml').read_text(encoding='utf-8').strip()
    return t.replace('<math ', '<math display="block" ', 1)
html = ('<!doctype html><html lang="it"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="../../publish/leggi/assets/style.css">'
        '<style>body{background:#fff} .content{max-width:680px;margin:24px auto}</style></head>'
        '<body><main class="content">'
        '<p>Test barra di scorrimento (image120 e image108):</p>'
        '<div class="equation">' + mml('image120') + '</div>'
        '<div class="equation">' + mml('image108') + '</div>'
        '</main></body></html>')
out = pathlib.Path('build/ch2_scrolltest.html'); out.write_text(html, encoding='utf-8')
print('wrote', out)
