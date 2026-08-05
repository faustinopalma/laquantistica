"""Correzioni alla scheda 6: segno del commutatore, refusi nelle formule e nel testo,
carica del nucleo e simbolo del potenziale coulombiano."""
import json
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, 'build')
from prosa_inglese_persa import fine_span

P = Path('sorgenti/06-ulteriori-sviluppi.html')
s = P.read_text(encoding='utf-8')


# ---------------------------------------------------------------- testo
TESTO = [
    ('sia unico, il ch\u00e9 in generale', 'sia unico, il che in generale'),
    ('quadrato di ogni uno di questi', 'quadrato di ognuno di questi'),
    ('una delle possibili combinazione di valori', 'una delle possibili combinazioni di valori'),
    (', perch\u00e8 non \u00e8 possibile', ', perch\u00e9 non \u00e8 possibile'),
    ('\u201ccontiene in se\u201d', '\u201ccontiene in s\u00e9\u201d'),
    ('Prima di procedere con lo studio generalizzare al caso continuo la formula',
     'Prima di procedere con lo studio generalizziamo al caso continuo la formula'),
    ('un potenziale columbiano', 'un potenziale coulombiano'),
    ('un nucleo con carica pari a quella dell\u2019elettrone',
     'un nucleo con carica uguale e opposta a quella dell\u2019elettrone'),
    ('a nucleus with charge equal to that of the electron',
     'a nucleus with charge equal and opposite to that of the electron'),
]
for vecchio, nuovo in TESTO:
    n = s.count(vecchio)
    assert n == 1, f'{n} occorrenze di {vecchio[:50]!r}'
    s = s.replace(vecchio, nuovo)
print(f'testo: {len(TESTO)} correzioni')


# ---------------------------------------------------------------- formule
# frammenti da sostituire in qualunque formula li contenga
FRAMMENTI = [
    ('=-i\\hbar I', '=i\\hbar I'),
    ('-i\\hbar I|x,p_x,\\xi\\rangle', 'i\\hbar I|x,p_x,\\xi\\rangle'),
    ("|g'\\rangle=\\overline{g'}\\rangle", "|g'={\\overline{g}}'\\rangle"),
    ('\\Xi', '\\xi'),
    ('|p_x,\\varepsilon\\rangle', '|p_x,\\xi\\rangle'),
    ("\\int_\\xi^{\\xi'}d\\xi'", "\\int_\\xi d\\xi'"),
    ("\\int_\\xi^{\\:}d\\xi'", "\\int_\\xi d\\xi'"),
    ('\\int_\\xi d\\xi\\int_{-\\infty}', "\\int_\\xi d\\xi'\\int_{-\\infty}"),
    ('\\langle xp\\rangle_y', '\\langle xp_y\\rangle'),
    ('\\{\\overline{g_1}\\cdots\\overline{g_n}\\rangle',
     '\\{|\\overline{g}_1\\cdots\\overline{g}_n\\rangle\\}'),
    ("\\{p_x',\\xi'\\rangle\\}", "\\{|p_x',\\xi'\\rangle\\}"),
    ('dy\\:dz', 'd\\overline{y}\\:d\\overline{z}'),
    ('\\frac{1}{4\\pi\\varepsilon_0}\\frac{q}{r}', '\\frac{1}{4\\pi\\varepsilon_0}\\frac{e}{r}'),
]

# formule da sostituire per intero (un frammento sarebbe ambiguo)
RIGA_DOPPIA = ('&' ' =\\sum_{k_1\\dots k_n}|{\\overline{g}}_{k_1}\\dots{\\overline{g}}_{k_n}\\rangle'
               '\\langle{\\overline{g}}_{k_1}\\dots{\\overline{g}}_{k_n}|\\alpha\\rangle \\\\\n')
INTERE = {
    '\\varepsilon': '\\xi',
    'E=qV+\\frac{1}{2m}{\\overline{P}}^2': 'E=qV+\\frac{1}{2m}{\\overline{p}}^2',
    ('\\begin{aligned}\n\\langle E\\rangle & =\\left\\langle qV+\\frac{1}{2m}{\\overline{P}}^2'
     '\\right\\rangle \\\\\n& =q\\langle V\\rangle+\\frac{1}{2m}\\left\\langle{\\overline{P}}^2'
     '\\right\\rangle\n\\end{aligned}'):
        ('\\begin{aligned}\n\\langle E\\rangle & =\\left\\langle qV+\\frac{1}{2m}{\\overline{p}}^2'
         '\\right\\rangle \\\\\n& =q\\langle V\\rangle+\\frac{1}{2m}\\left\\langle{\\overline{p}}^2'
         '\\right\\rangle\n\\end{aligned}'),
}


def da_html(t):
    return t.replace('&#x27;', "'").replace('&amp;', '&')


def a_html(t):
    return t.replace('&', '&amp;').replace("'", '&#x27;')


def nuovo_tex(tex):
    if tex in INTERE:
        return INTERE[tex]
    t = tex
    for vecchio, nuovo in FRAMMENTI:
        t = t.replace(vecchio, nuovo)
    # la riga ripetuta nello sviluppo di |alpha>
    if t.count(RIGA_DOPPIA) == 2:
        t = t.replace(RIGA_DOPPIA * 2, RIGA_DOPPIA)
    return t


# raccogli le occorrenze da cambiare, con la posizione dello span che le contiene
cambi = []
i = 0
while True:
    i = s.find('data-tex="', i)
    if i < 0:
        break
    fine_attr = s.find('"', i + 10)
    tex = da_html(s[i + 10:fine_attr])
    t2 = nuovo_tex(tex)
    if t2 != tex:
        a = s.rfind('<span class="', 0, i)
        classe = s[a + 13:s.find('"', a + 13)]
        cambi.append((a, fine_span(s, a), tex, t2, 'eq-mml-block' in classe))
    i = fine_attr

print(f'formule da rigenerare: {len(cambi)}')
assert cambi, 'nessuna formula da cambiare'

richieste = [{'i': k, 'tex': t2, 'display': disp} for k, (_, _, _, t2, disp) in enumerate(cambi)]
r = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps(richieste), capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    raise SystemExit(r.stderr)
reso = {}
for x in json.loads(r.stdout):
    if 'err' in x:
        raise SystemExit('%s\n%s' % (richieste[x['i']]['tex'], x['err']))
    reso[x['i']] = x['html']

for k in range(len(cambi) - 1, -1, -1):          # dal fondo, per non spostare gli offset
    a, b, tex, t2, disp = cambi[k]
    apertura = s[a:s.find('>', a) + 1].replace(a_html(tex), a_html(t2))
    s = s[:a] + apertura + reso[k] + '</span>' + s[b:]

assert s.count('<span') == s.count('</span>'), 'span sbilanciati'


# ------------------------------------------- chi e' la carica nel potenziale
CHIARIMENTO = {
    'it': ', dove <em>e</em> \u00e8 la carica del nucleo, uguale e opposta alla carica '
          '<em>q</em> dell\u2019elettrone che compare in <em>H</em>.',
    'en': ', where <em>e</em> is the charge of the nucleus, equal and opposite to the charge '
          '<em>q</em> of the electron appearing in <em>H</em>.',
}
for lingua, coda in CHIARIMENTO.items():
    chiave = 'potenziale coulombiano' if lingua == 'it' else 'Coulomb potential'
    i = s.find(chiave)
    assert i > 0, chiave
    a = s.find('<span class="eq-inline', i)
    b = fine_span(s, a)
    assert s[b] == '.', repr(s[b:b + 20])
    s = s[:b] + coda + s[b + 1:]
print('chiarita la carica nel potenziale coulombiano')

P.write_text(s, encoding='utf-8', newline='')
print('scheda 6 riscritta')
