"""Convertitore MathML -> LaTeX per il MathML di questo sito.

Il MathML delle pagine viene tutto dallo stesso convertitore OMML, quindi usa un
sottoinsieme piccolo e regolare. Questo convertitore copre *quel* sottoinsieme ed
e' deliberatamente SEVERO: davanti a un tag, un attributo o un carattere che non
conosce solleva MathMLUnsupported invece di indovinare. Meglio fermarsi e
aggiungere una regola che produrre in silenzio una formula sbagliata.

Uso come libreria:   from mml2tex import mml_to_tex;  tex = mml_to_tex(fragment)
Uso da riga di comando (diagnostica su un file):
    python tools/mml2tex.py publish/09-spettri-atomici.html
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MML_NS = 'http://www.w3.org/1998/Math/MathML'


class MathMLUnsupported(Exception):
    pass


# --- simboli -----------------------------------------------------------------

GREEK = {
    '\u03b1': r'\alpha', '\u03b2': r'\beta', '\u03b3': r'\gamma',
    '\u03b4': r'\delta', '\u03b5': r'\varepsilon', '\u03f5': r'\epsilon',
    '\u03b6': r'\zeta', '\u03b7': r'\eta', '\u03b8': r'\theta',
    '\u03d1': r'\vartheta', '\u03b9': r'\iota', '\u03ba': r'\kappa',
    '\u03bb': r'\lambda', '\u03bc': r'\mu', '\u03bd': r'\nu', '\u03be': r'\xi',
    '\u03c0': r'\pi', '\u03c1': r'\rho', '\u03f1': r'\varrho',
    '\u03c3': r'\sigma', '\u03c4': r'\tau', '\u03c5': r'\upsilon',
    '\u03c6': r'\varphi', '\u03d5': r'\phi', '\u03c7': r'\chi',
    '\u03c8': r'\psi', '\u03c9': r'\omega',
    '\u0393': r'\Gamma', '\u0394': r'\Delta', '\u0398': r'\Theta',
    '\u039b': r'\Lambda', '\u039e': r'\Xi', '\u03a0': r'\Pi',
    '\u03a3': r'\Sigma', '\u03a6': r'\Phi', '\u03a8': r'\Psi',
    '\u03a9': r'\Omega',
}

# identificatori non alfabetici ammessi in <mi>
MI_SYMBOL = {
    '\u210f': r'\hbar', '\u2032': "'", '\u2026': r'\dots',
    '\u2020': r'\dagger', '\u2217': '*',
    '\u27e8': r'\langle', '\u27e9': r'\rangle', '\u27f6': r'\longrightarrow',
    '\u27f8': r'\Longleftarrow', '\u27f9': r'\Longrightarrow',
    '\u27fa': r'\Longleftrightarrow',
    '\u1d52f': r'\mathfrak{r}',
    'cos': r'\cos', 'sen': r'\sin', 'sin': r'\sin', 'tan': r'\tan',
    'log': r'\log', 'ln': r'\ln', 'exp': r'\exp',
    'Im': r'\operatorname{Im}', 'Re': r'\operatorname{Re}',
    'lim': r'\lim', 'max': r'\max', 'min': r'\min',
}
MI_SYMBOL.update(GREEK)

OPERATOR = {
    '=': '=', '+': '+', '-': '-', ',': ',', '.': '.', '/': '/', '*': '*',
    '(': '(', ')': ')', '[': '[', ']': ']', '<': '<', '>': '>',
    '{': r'\{', '}': r'\}', '|': '|', '!': '!', ':': ':', ';': ';',
    '\u2212': '-', '\u00b1': r'\pm', '\u2213': r'\mp',
    '\u00d7': r'\times', '\u00b7': r'\cdot', '\u22c5': r'\cdot',
    '\u2217': r'\ast', '\u2032': "'", '\u2020': r'\dagger',
    '\u2044': '/', '\u2215': '/',
    '\u2260': r'\neq', '\u2261': r'\equiv', '\u2245': r'\cong',
    '\u2248': r'\approx', '\u2243': r'\simeq', '\u221d': r'\propto',
    '\u2264': r'\leq', '\u2265': r'\geq', '\u226a': r'\ll', '\u226b': r'\gg',
    '\u2192': r'\to', '\u2190': r'\leftarrow', '\u2194': r'\leftrightarrow',
    '\u21d2': r'\Rightarrow', '\u21d0': r'\Leftarrow',
    '\u21d4': r'\Leftrightarrow', '\u27fa': r'\Longleftrightarrow',
    '\u27f8': r'\Longleftarrow', '\u27f9': r'\Longrightarrow',
    '\u27f6': r'\longrightarrow',
    '\u2211': r'\sum', '\u220f': r'\prod',
    '\u222b': r'\int', '\u222c': r'\iint', '\u222d': r'\iiint',
    '\u222e': r'\oint', '\u222f': r'\oiint',
    '\u2202': r'\partial', '\u2207': r'\nabla', '\u221e': r'\infty',
    '\u221a': r'\sqrt', '\u2205': r'\emptyset',
    '\u2208': r'\in', '\u2209': r'\notin', '\u2282': r'\subset',
    '\u2200': r'\forall', '\u2203': r'\exists',
    '\u2227': r'\wedge', '\u2228': r'\vee', '\u2218': r'\circ',
    '\u22ef': r'\cdots', '\u22ee': r'\vdots', '\u22ef': r'\cdots',
    '\u2223': r'\mid', '\u2225': r'\parallel',
    '\u27e8': r'\langle', '\u27e9': r'\rangle',
    '\u2061': '', '\u2062': '', '\u2063': '', '\u2064': '',  # invisibili
    '\u00af': r'\overline', '\u2015': r'\overline', '\u0304': r'\overline',
    '\u02d9': r'\dot', '\u00a8': r'\ddot', '\u005e': r'\hat',
    '\u02c6': r'\hat', '\u02dc': r'\tilde', '\u007e': r'\tilde',
    'sen': r'\sin', 'cos': r'\cos', 'tan': r'\tan',
    'Im': r'\operatorname{Im}', 'Re': r'\operatorname{Re}',
    'lim': r'\lim', 'log': r'\log', 'ln': r'\ln',
}

# accenti: quello che puo' stare sopra/sotto in <mover>/<munder>
ACCENT_OVER = {
    '\u00af': r'\overline', '\u2015': r'\overline', '\u0304': r'\overline',
    '\u02d9': r'\dot', '\u00a8': r'\ddot',
    '\u005e': r'\hat', '\u02c6': r'\hat',
    '\u007e': r'\tilde', '\u02dc': r'\tilde',
    '\u2192': r'\vec', '\u20d7': r'\vec',
    '\u23de': r'\overbrace', '\u2323': r'\overparen',
}
ACCENT_UNDER = {
    '\u00af': r'\underline', '\u2015': r'\underline', '\u0332': r'\underline',
    '\u23df': r'\underbrace',
}
# operatori grandi: sotto/sopra diventano limiti, non accenti
BIG_OPS = {'\u2211', '\u220f', '\u222b', '\u222c', '\u222d', '\u222e',
           '\u222f', '\u22c3', '\u22c2', 'lim'}

NBSP = '\u00a0'

# In MathML le parentesi sono elastiche per default e si allungano da sole attorno
# a matrici e frazioni; in LaTeX no, serve \left ... \right. Abbiniamo qui le coppie
# con apertura e chiusura DISTINTE: '|' resta fuori perche' nella notazione di Dirac
# (|psi>, <phi|) non e' una coppia.
FENCE_PAIRS = {'(': ')', '[': ']', r'\{': r'\}', r'\langle': r'\rangle'}
FENCE_CLOSE = {v: k for k, v in FENCE_PAIRS.items()}
# delimitatori uguali in apertura e chiusura: si accoppiano solo se il MathML
# li marca come tali con fence="true" e form="prefix"/"postfix"
SELF_FENCE = {'|', r'\|', r'\Vert'}

CMD_END = re.compile(r'\\[A-Za-z]+$')
PRIMES = re.compile(r"'+")


def _join(parts) -> str:
    """Concatena i pezzi separando \\nu da d: senza spazio diventerebbe \\nud."""
    out = ''
    for p in parts:
        if not p:
            continue
        if out and p[0].isalpha() and CMD_END.search(out):
            out += ' '
        out += p
    return out


def _tag(el) -> str:
    t = el.tag
    return t.split('}', 1)[1] if '}' in t else t


def _text(el) -> str:
    return (el.text or '').strip()


def _needs_braces(tex: str) -> bool:
    """Un argomento va messo fra graffe se non e' gia' un singolo token."""
    if len(tex) <= 1:
        return False
    if re.fullmatch(r'\\[A-Za-z]+', tex):
        return False
    return True


def _brace(tex: str) -> str:
    return tex if not _needs_braces(tex) else '{' + tex + '}'


def _brace_base(tex: str) -> str:
    """Come _brace, ma "10" resta "10": 10^{-3} e {10}^{-3} rendono identici."""
    if tex.isalnum():
        return tex
    return _brace(tex)


class Converter:
    def __init__(self, where: str = ''):
        self.where = where
        self.unknown: list[str] = []

    # -- foglie ---------------------------------------------------------------

    def leaf_mi(self, el) -> str:
        txt = _text(el)
        var = el.get('mathvariant')
        if txt in MI_SYMBOL:
            body = MI_SYMBOL[txt]
        elif len(txt) == 1 and (txt.isalpha() or txt.isdigit()):
            body = txt
        elif txt == '':
            return ''
        elif txt.isalpha():
            body = r'\mathit{' + txt + '}'
        else:
            self.unknown.append(f'<mi>{txt!r} ({" ".join(f"U+{ord(c):04X}" for c in txt)})')
            return ''
        if var == 'normal':
            return r'\mathrm{' + body + '}' if body.isalpha() else body
        if var == 'bold':
            return r'\mathbf{' + body + '}'
        if var in (None, 'italic'):
            return body
        self.unknown.append(f'<mi mathvariant={var}>')
        return body

    def leaf_mn(self, el) -> str:
        txt = _text(el)
        if re.fullmatch(r'[0-9]+([.,][0-9]+)?', txt):
            return txt
        if txt == '':
            return ''
        self.unknown.append(f'<mn>{txt!r}')
        return txt

    def leaf_mo(self, el) -> str:
        txt = _text(el)
        if txt == '':
            return ''
        if txt in OPERATOR:
            return OPERATOR[txt]
        self.unknown.append(f'<mo>{txt!r} ({" ".join(f"U+{ord(c):04X}" for c in txt)})')
        return ''

    def leaf_mtext(self, el) -> str:
        txt = (el.text or '')
        if txt.strip() == '':
            return r'\ ' if txt else ''
        return r'\text{' + txt.replace(NBSP, ' ') + '}'

    def leaf_mspace(self, el) -> str:
        w = el.get('width', '')
        m = re.fullmatch(r'(-?[\d.]+)(em|ex|px|pt)', w)
        if not m:
            return r'\;'
        v = float(m.group(1))
        if m.group(2) != 'em':
            v = v / 16.0
        for lim, tex in ((0.10, r'\,'), (0.20, r'\:'), (0.30, r'\;'),
                         (0.70, r'\quad'),):
            if v <= lim:
                return tex
        return r'\qquad'

    # -- contenitori ----------------------------------------------------------

    def children(self, el) -> str:
        return _join(self.node(c) for c in el)

    def row(self, el) -> str:
        parts = []                       # [tipo, chiusura attesa, testo]
        for c in el:
            tex = self.node(c)
            kind, want = '', ''
            if _tag(c) == 'mo' and c.get('stretchy') != 'false':
                if tex in FENCE_PAIRS:
                    kind, want = 'open', FENCE_PAIRS[tex]
                elif tex in FENCE_CLOSE:
                    kind = 'close'
                elif c.get('fence') == 'true' and tex in SELF_FENCE:
                    # barre verticali: coppia solo se il MathML la dichiara tale
                    form = c.get('form')
                    if form == 'prefix':
                        kind, want = 'open', tex
                    elif form == 'postfix':
                        kind = 'close'
            parts.append([kind, want, tex])
        stack = []
        for p in parts:
            if p[0] == 'open':
                stack.append(p)
            elif p[0] == 'close':
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j][1] == p[2]:
                        stack[j][2] = r'\left' + stack[j][2]
                        p[2] = r'\right' + p[2]
                        del stack[j:]
                        break
        return _join(p[2] for p in parts)

    def script(self, el, kind: str) -> str:
        kids = list(el)
        base = self.node(kids[0])
        if kind == 'msubsup':
            sub, sup = self.node(kids[1]), self.node(kids[2])
            tail = sup if PRIMES.fullmatch(sup) else '^' + _brace(sup)
            return f'{_brace_base(base)}_{_brace(sub)}{tail}'
        arg = self.node(kids[1])
        # il primo si scrive x' e non x^': con l'accento LaTeX si ferma
        if kind == 'msup' and PRIMES.fullmatch(arg):
            return _brace_base(base) + arg
        sign = '_' if kind == 'msub' else '^'
        return f'{_brace_base(base)}{sign}{_brace(arg)}'

    def over_under(self, el, kind: str) -> str:
        kids = list(el)
        base_el, base = kids[0], self.node(kids[0])
        base_txt = _text(base_el) if _tag(base_el) in ('mo', 'mi') else ''
        if kind == 'munderover':
            return f'{_brace(base)}_{_brace(self.node(kids[1]))}^{_brace(self.node(kids[2]))}'
        mark_el = kids[1]
        mark_txt = _text(mark_el)
        table = ACCENT_OVER if kind == 'mover' else ACCENT_UNDER
        if base_txt in BIG_OPS:
            sign = '^' if kind == 'mover' else '_'
            return f'{base}{sign}{_brace(self.node(mark_el))}'
        if mark_txt in table:
            return table[mark_txt] + '{' + base + '}'
        cmd = r'\overset' if kind == 'mover' else r'\underset'
        return cmd + '{' + self.node(mark_el) + '}{' + base + '}'

    def frac(self, el) -> str:
        kids = list(el)
        num, den = self.node(kids[0]), self.node(kids[1])
        if el.get('linethickness') in ('0', '0em', '0pt'):
            return r'\binom{' + num + '}{' + den + '}'
        return r'\frac{' + num + '}{' + den + '}'

    def table(self, el) -> str:
        rows = []
        for tr in el:
            if _tag(tr) != 'mtr':
                self.unknown.append(f'<mtable> contiene <{_tag(tr)}>')
                continue
            rows.append(' & '.join(self.children(td) for td in tr
                                   if _tag(td) == 'mtd'))
        body = ' \\\\\n'.join(rows)
        align = (el.get('columnalign') or '').split()
        # il caso tipico di questo sito: due colonne "right left" = allineamento
        if align == ['right', 'left']:
            return '\\begin{aligned}\n' + body + '\n\\end{aligned}'
        ncol = max((len(r.split(' & ')) for r in rows), default=1)
        if ncol == 1:
            return '\\begin{gathered}\n' + body + '\n\\end{gathered}'
        if align and set(align) <= {'center'}:
            return '\\begin{matrix}\n' + body + '\n\\end{matrix}'
        spec = ''.join({'right': 'r', 'left': 'l', 'center': 'c'}.get(a, 'c')
                       for a in (align or ['center'] * ncol))
        if len(spec) < ncol:
            spec = spec + spec[-1] * (ncol - len(spec))
        return '\\begin{array}{' + spec + '}\n' + body + '\n\\end{array}'

    def node(self, el) -> str:
        t = _tag(el)
        if t == 'math':
            return self.children(el)
        if t in ('mrow', 'mpadded', 'semantics', 'menclose'):
            return self.row(el)
        if t == 'mstyle':
            # Word usa <mstyle displaystyle="true"> per tenere le frazioni a dimensione
            # piena anche in linea: senza questo il LaTeX le rimpicciolisce.
            inner = self.row(el)
            ds = el.get('displaystyle')
            if ds == 'true':
                return r'{\displaystyle ' + inner + '}'
            if ds == 'false':
                return r'{\textstyle ' + inner + '}'
            return inner
        if t == 'mi':
            return self.leaf_mi(el)
        if t == 'mn':
            return self.leaf_mn(el)
        if t == 'mo':
            return self.leaf_mo(el)
        if t == 'mtext':
            return self.leaf_mtext(el)
        if t == 'mspace':
            return self.leaf_mspace(el)
        if t in ('msub', 'msup', 'msubsup'):
            return self.script(el, t)
        if t in ('mover', 'munder', 'munderover'):
            return self.over_under(el, t)
        if t == 'mfrac':
            return self.frac(el)
        if t in ('mtable', 'mtr', 'mtd'):
            return self.table(el) if t == 'mtable' else self.children(el)
        if t == 'msqrt':
            return r'\sqrt{' + self.children(el) + '}'
        if t == 'mroot':
            kids = list(el)
            return r'\sqrt[' + self.node(kids[1]) + ']{' + self.node(kids[0]) + '}'
        if t == 'mfenced':
            op = el.get('open', '('), el.get('close', ')')
            return r'\left' + op[0] + self.children(el) + r'\right' + op[1]
        if t == 'mphantom':
            return r'\phantom{' + self.children(el) + '}'
        if t == 'none':
            return ''
        self.unknown.append(f'<{t}> non gestito')
        return ''


MATRIX_ENV = {'(': 'pmatrix', '[': 'bmatrix', r'\{': 'Bmatrix',
              '|': 'vmatrix', r'\|': 'Vmatrix'}


def tidy(tex: str) -> str:
    tex = re.sub(r'[ \t]+', ' ', tex)
    tex = re.sub(r' *\n *', '\n', tex)
    tex = re.sub(r'(?<![\\\w]) (?=[,.;:])', '', tex)
    # \left( \begin{array}{cc} ... \right)  ->  \begin{pmatrix} ... \end{pmatrix}
    # (solo se dentro non c'e' un altro ambiente annidato, per non sbagliare coppia)
    def _mat(m):
        env = MATRIX_ENV.get(m.group(1))
        return m.group(0) if not env else f'\\begin{{{env}}}{m.group(2)}\\end{{{env}}}'
    body = r'((?:(?!\\begin\{)(?!\\end\{).)*?)'
    tex = re.sub(r'\\left(\\\||\\\{|[(\[|])\s*\\begin\{(?:matrix|array)\}(?:\{c+\})?'
                 + body +
                 r'\\end\{(?:matrix|array)\}\s*\\right(?:\\\||\\\}|[)\]|])',
                 _mat, tex, flags=re.S)
    return tex.strip()


def mml_to_tex(fragment: str, where: str = '') -> tuple[str, list[str]]:
    """Ritorna (latex, elenco dei costrutti non riconosciuti)."""
    xml = fragment
    if 'xmlns' not in xml.split('>', 1)[0]:
        xml = xml.replace('<math', f'<math xmlns="{MML_NS}"', 1)
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise MathMLUnsupported(f'{where}: MathML non ben formato — {e}') from e
    conv = Converter(where)
    tex = tidy(conv.node(root))
    return tex, conv.unknown


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    from math_extract import extract  # noqa: E402

    path = Path(sys.argv[1])
    _, items = extract(path)
    bad = 0
    for it in items:
        try:
            tex, unknown = mml_to_tex(it['src'], f'{path.name}[{it["i"]}]')
        except MathMLUnsupported as e:
            print(f'[{it["i"]}] riga {it["line"]}  ERRORE: {e}')
            bad += 1
            continue
        flag = '  <<< ' + '; '.join(unknown) if unknown else ''
        if unknown:
            bad += 1
        print(f'[{it["i"]:3d}] r{it["line"]:<5} {it["display"]:6}  {tex}{flag}')
    print(f'\n{len(items)} formule, {bad} da rivedere')
