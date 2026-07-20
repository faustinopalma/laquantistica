"""MTEF v3 (Microsoft Equation 3.0) -> LaTeX converter.
Based on the record structure of LibreOffice starmath/source/mathtype.cxx.
For MTEF v3 the CHAR record stores the Unicode codepoint directly, so no font
tables are needed; templates (fraction, root, scripts, fences, ...) are mapped
to LaTeX. Designed for the physics equations in this thesis.
"""
import struct, io
from collections import Counter

# record tags (tag & 0x0F)
END, LINE, CHAR, TMPL, PILE, MATRIX, EMBELL, RULER, FONT, SIZE = range(10)

# template selector enum order (from mathtype.hxx)
(tmANGLE, tmPAREN, tmBRACE, tmBRACK, tmBAR, tmDBAR, tmFLOOR, tmCEILING,
 tmLBLB, tmRBRB, tmRBLB, tmLBRP, tmLPRB, tmROOT, tmFRACT, tmSCRIPT, tmUBAR,
 tmOBAR, tmLARROW, tmRARROW, tmBARROW, tmSINT, tmDINT, tmTINT, tmSSINT,
 tmDSINT, tmTSINT, tmUHBRACE, tmLHBRACE, tmSUM, tmISUM, tmPROD, tmIPROD,
 tmCOPROD, tmICOPROD, tmUNION, tmIUNION, tmINTER, tmIINTER, tmLIM, tmLDIV,
 tmSLFRACT, tmINTOP, tmSUMOP, tmLSCRIPT, tmDIRAC, tmUARROW, tmOARROW,
 tmOARC) = range(49)

# Unicode -> LaTeX for characters MathJax needs help with; most Unicode passes through.
SPECIAL = {
    ord('{'): r'\{', ord('}'): r'\}', ord('%'): r'\%', ord('#'): r'\#',
    ord('&'): r'\&', ord('$'): r'\$', ord('_'): r'\_',
    0x00d7: r'\times ', 0x00b7: r'\cdot ', 0x2212: '-', 0x2013: '-', 0x2014: '-',
    0x2219: r'\cdot ', 0x2022: r'\cdot ', 0x00b0: r'^{\circ}',
    0x221a: r'\surd ', 0x2264: r'\le ', 0x2265: r'\ge ', 0x2260: r'\ne ',
    0x2192: r'\rightarrow ', 0x2190: r'\leftarrow ', 0x21d2: r'\Rightarrow ',
    0x21d4: r'\Leftrightarrow ', 0x2248: r'\approx ', 0x221e: r'\infty ',
    0x2211: r'\sum ', 0x220f: r'\prod ', 0x222b: r'\int ', 0x2202: r'\partial ',
    0x2207: r'\nabla ', 0x00b1: r'\pm ', 0x2213: r'\mp ', 0x00ac: r'\neg ',
    0x2261: r'\equiv ', 0x223c: r'\sim ', 0x221d: r'\propto ',
    0x27e8: r'\langle ', 0x27e9: r'\rangle ', 0x2220: r'\angle ',
    0x210f: r'\hbar ', 0x2205: r'\emptyset ', 0x2208: r'\in ',
    0x00a0: ' ', 0x2032: "'", 0x2033: "''",
}

_EMBEL = {
    0x02: r'\dot{%s}', 0x03: r'\ddot{%s}', 0x04: r'\dddot{%s}',
    0x08: r'\tilde{%s}', 0x09: r'\hat{%s}', 0x0b: r'\vec{%s}',
    0x11: r'\bar{%s}', 0x14: r'\breve{%s}', 0x10: r'\overline{%s}',
}


def apply_embellishment(e, base):
    if e in _EMBEL:
        return _EMBEL[e] % base
    if e == 0x05:
        return base + "'"
    if e == 0x06:
        return base + "''"
    if e == 0x12:
        return base + "'''"
    return base


def char_to_latex(ch, tface):
    if ch in SPECIAL:
        return SPECIAL[ch]
    if ch < 0x20:
        return ''
    # MathType private-use area: spacing / decorative glyphs -> drop (or space)
    if 0xE000 <= ch <= 0xF8FF:
        return ''
    if ch in (0xF8FF, 0xFEFF, 0x200B, 0x2061, 0x2062, 0x2063):
        return ''
    c = chr(ch)
    # Latin letters / digits / common operators pass through
    return c


class MTEF:
    def __init__(self, data, collect=None):
        self.s = io.BytesIO(data)
        self.collect = collect  # optional Counter for selectors

    def u8(self):
        b = self.s.read(1)
        return b[0] if b else None

    def u16(self):
        b = self.s.read(2)
        return struct.unpack('<H', b)[0] if len(b) == 2 else 0

    def n_slots(self, sel, var):
        if sel in (tmFRACT, tmSLFRACT, tmLSCRIPT, tmLDIV):
            return 2
        if sel == tmROOT:
            return 2  # radicand, index
        if sel == tmSCRIPT:
            return 2  # sub + sup slots (one may be empty), always present
        # Fence templates carry a trailing slot with the literal delimiter glyphs
        # that MathType stores but which must be skipped (LibreOffice does the same).
        if sel in (tmANGLE, tmPAREN, tmBRACE, tmBRACK, tmBAR, tmDBAR, tmFLOOR,
                   tmCEILING, tmLBLB, tmRBRB, tmRBLB, tmLBRP, tmLPRB, tmDIRAC):
            return 2
        if sel in (tmUBAR, tmOBAR, tmUHBRACE, tmLHBRACE, tmLARROW, tmRARROW,
                   tmBARROW, tmUARROW, tmOARROW, tmOARC):
            return 1
        if sel == tmLIM:
            return 2
        # n-ary operators with limits: variable -> read greedily
        return None

    def parse_expr(self):
        """Read one object-list (a slot) until its END; return latex string."""
        cur = []
        while True:
            tag = self.u8()
            if tag is None:
                break
            rec = tag & 0x0F
            if rec == END:
                break
            elif rec == LINE:
                # a LINE inside a slot: separator; render as space (rare at this level)
                if cur and not cur[-1].endswith(' '):
                    cur.append(' ')
            elif rec == CHAR:
                tface = self.u8()
                ch = self.u16()
                cur.append(char_to_latex(ch, tface))
            elif rec == TMPL:
                sel = self.u8(); var = self.u8(); opt = self.u8()
                if self.collect is not None:
                    self.collect[sel] += 1
                n = self.n_slots(sel, var)
                if n is None:
                    slots = self.read_variable_slots()
                else:
                    slots = [self.parse_expr() for _ in range(n)]
                cur.append(self.render_template(sel, var, slots))
            elif rec == PILE:
                self.u8(); self.u8()  # halign, valign
                lines = self.read_variable_slots()
                cur.append(self.render_pile(lines))
            elif rec == MATRIX:
                rows = self.u8(); cols = self.u8()
                self.u8(); self.u8()
                cells = self.read_variable_slots()
                cur.append(self.render_matrix(cells, rows, cols))
            elif rec == SIZE:
                t = self.u8()
                if t == 4:
                    self.u16(); self.u16()
            elif rec in (10, 11, 12, 13, 14):
                pass
            elif rec == FONT:
                self.u8(); self.u8()
                while True:
                    b = self.u8()
                    if b is None or b == 0:
                        break
            elif rec == EMBELL:
                # embellishments: a run of type bytes terminated by 0x00 (MTEF v3).
                embels = []
                while True:
                    b = self.u8()
                    if b is None or b == 0:
                        break
                    embels.append(b)
                if cur:
                    base = cur[-1]
                    for e in embels:
                        base = apply_embellishment(e, base)
                    cur[-1] = base
            elif rec == RULER:
                n = self.u8() or 0
                for _ in range(n):
                    self.u8(); self.u16()
            else:
                pass
        return ''.join(cur)

    def read_variable_slots(self, cap=32):
        """For PILE/MATRIX/n-ary: read slots until an empty terminating END."""
        slots = []
        while len(slots) < cap:
            pos = self.s.tell()
            peek = self.s.read(1)
            if not peek:
                break
            self.s.seek(pos)
            if (peek[0] & 0x0F) == END:
                self.u8()  # consume terminator
                break
            slots.append(self.parse_expr())
        return slots

    def parse_level(self):
        return [self.parse_expr()]

    def render_template(self, sel, var, sub):
        def g(i):
            return sub[i] if i < len(sub) else ''
        if sel == tmFRACT:
            return r'\frac{%s}{%s}' % (g(0), g(1))
        if sel == tmSLFRACT:
            return r'{%s}/{%s}' % (g(0), g(1))
        if sel == tmROOT:
            if g(1).strip():
                return r'\sqrt[%s]{%s}' % (g(1), g(0))
            return r'\sqrt{%s}' % g(0)
        if sel == tmSCRIPT:
            if var == 0:
                return r'^{%s}' % g(0)
            if var == 1:
                return r'_{%s}' % g(0)
            return r'_{%s}^{%s}' % (g(0), g(1))
        if sel == tmLSCRIPT:
            return r'{}_{%s}^{%s}' % (g(0), g(1))
        if sel == tmPAREN:
            return r'\left(%s\right)' % g(0)
        if sel == tmBRACK:
            return r'\left[%s\right]' % g(0)
        if sel == tmBRACE:
            return r'\left\{%s\right\}' % g(0)
        if sel in (tmBAR,):
            return r'\left|%s\right|' % g(0)
        if sel in (tmDBAR,):
            return r'\left\|%s\right\|' % g(0)
        if sel == tmANGLE:
            return r'\left\langle %s\right\rangle' % g(0)
        if sel == tmFLOOR:
            return r'\left\lfloor %s\right\rfloor' % g(0)
        if sel == tmCEILING:
            return r'\left\lceil %s\right\rceil' % g(0)
        if sel in (tmUARROW, tmOARROW, tmLARROW, tmRARROW, tmBARROW):
            return r'\vec{%s}' % g(0)
        if sel == tmOBAR:
            return r'\overline{%s}' % g(0)
        if sel == tmUBAR:
            return r'\underline{%s}' % g(0)
        if sel == tmUHBRACE:
            return r'\overbrace{%s}' % g(0)
        if sel == tmLHBRACE:
            return r'\underbrace{%s}' % g(0)
        if sel == tmDIRAC:
            return g(0)
        if sel in (tmLPRB, tmLBRP, tmLBLB, tmRBRB, tmRBLB, tmLPRB):
            return g(0)
        if sel in (tmSINT, tmDINT, tmTINT, tmINTOP):
            body = ''.join(sub)
            return r'\int %s' % body
        if sel in (tmSUM, tmISUM, tmSUMOP):
            return r'\sum %s' % ''.join(sub)
        if sel in (tmPROD, tmIPROD):
            return r'\prod %s' % ''.join(sub)
        if sel == tmLIM:
            return r'\lim %s' % ''.join(sub)
        if sel == tmLDIV:
            return r'\frac{%s}{%s}' % (g(0), g(1))
        # fallback: join slots
        return ''.join(sub)

    def render_pile(self, lines):
        lines = [l for l in lines if l.strip()]
        if not lines:
            return ''
        if len(lines) == 1:
            return lines[0]
        body = r' \\ '.join(lines)
        return r'\begin{aligned}%s\end{aligned}' % body

    def render_matrix(self, cells, rows, cols):
        cells = [c for c in cells]
        if not cells:
            return ''
        if cols and cols > 0:
            rows = [cells[i:i+cols] for i in range(0, len(cells), cols)]
        else:
            rows = [cells]
        body = r' \\ '.join(' & '.join(r) for r in rows)
        return r'\begin{matrix}%s\end{matrix}' % body


def mtef_from_eqnstream(data):
    """Strip the 28-byte OLE equation header, return MTEF bytes (skip 5-byte MTEF header)."""
    cbHdr = struct.unpack_from('<H', data, 0)[0]
    mtef = data[cbHdr:]
    # skip 5-byte MTEF header
    return mtef[5:]


def convert(data, collect=None):
    body = mtef_from_eqnstream(data)
    m = MTEF(body, collect=collect)
    latex = m.parse_expr()
    latex = latex.replace('  ', ' ').strip()
    return latex


if __name__ == '__main__':
    import sys
    from pathlib import Path
    import olefile
    root = Path(__file__).resolve().parent.parent
    rel = sys.argv[1] if len(sys.argv) > 1 else '9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx'
    p = root / rel
    ole = olefile.OleFileIO(str(p))
    eqs = []
    for e in ole.listdir(streams=True):
        if len(e) >= 3 and e[0] == 'ObjectPool' and e[-1] == 'Equation Native':
            eqs.append((e[1], ole.openstream(e).read()))
    ole.close()
    eqs.sort(key=lambda t: t[0])
    sel_hist = Counter()
    print(f'{rel}: {len(eqs)} equations')
    for i, (name, data) in enumerate(eqs):
        try:
            latex = convert(data, collect=sel_hist)
        except Exception as ex:
            latex = f'<ERR {type(ex).__name__}: {ex}>'
        print(f'[{i:03d}] {latex}')
    print('--- template selector histogram ---')
    names = {globals()[k]: k for k in list(globals()) if k.startswith('tm')}
    for sel, cnt in sel_hist.most_common():
        print(f'  {names.get(sel, sel)}: {cnt}')
