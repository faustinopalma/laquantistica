"""One-off repairs to build/mml/*.json so the native MathML is semantically
correct (meaning-identical to the original), keeping MathML on the site.
Idempotent-ish: guarded by length/content checks.
"""
import json
from pathlib import Path

MML = Path('build/mml')
XI = ('<math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow>'
      '<mstyle mathsize="12pt"><mi>ξ</mi></mstyle><mrow/></mrow></semantics></math>')


def load(k):
    return json.loads((MML / f'{k}.json').read_text(encoding='utf-8'))


def save(k, arr):
    (MML / f'{k}.json').write_text(json.dumps(arr, ensure_ascii=False), encoding='utf-8')


# --- Fix 1: ch6 alignment. 225 objects but 224 MathML: the lone 'ξ' at object
# index 104 was dropped, shifting everything after. Re-insert it. ------------
k = '06_ulteriori_sviluppi'
arr = load(k)
if len(arr) == 224 and 'ξ' not in ''.join(__import__('re').findall(r'>([^<>]+)<', arr[104])):
    arr.insert(104, XI)
    save(k, arr)
    print(f'{k}: inserted ξ at 104 -> len={len(arr)}')
else:
    print(f'{k}: no-op (len={len(arr)})')


# --- Fix 2: rewrite formulas whose LibreOffice MathML lost meaning (dropped the
# conjugate star *, leaked stray braces, or truncated a case/vector). We rebuild
# them from LaTeX (meaning-identical), keeping native MathML. -----------------
import re
import latex2mathml.converter as L

REPAIRS = {
    '04_diffrazione': {
        54: r'|u\rangle=\begin{pmatrix}u_1\\ u_2\end{pmatrix}\Rightarrow\langle u|=(u_1^{*},u_2^{*})=\begin{pmatrix}u_1\\ u_2\end{pmatrix}^{*t}=|u\rangle^{*t}',
        56: r'(*)',
        61: r'A^{*t}',
        62: r'A^{*t}',
        59: r'\langle u|=|u\rangle^{*t}=(A|v\rangle)^{*t}=|v\rangle^{*t}A^{*t}=\langle v|A^{*t}',
        60: r'|u\rangle=A|v\rangle\Leftrightarrow\langle u|=\langle v|A^{*t}',
        64: r'A^{*t}\equiv A^{+}',
        65: r'A=\begin{pmatrix}a_{11}&a_{12}\\ a_{21}&a_{22}\end{pmatrix}\Rightarrow A^{+}=A^{*t}=\begin{pmatrix}a_{11}^{*}&a_{21}^{*}\\ a_{12}^{*}&a_{22}^{*}\end{pmatrix}',
        81: r"-\delta'(x'-x)^{*t}=-\delta'(x'-x)^{t}=-\delta'(x-x')=\delta'(x'-x)",
        84: r'K^{+}=(iD)^{+}=i^{*}D^{+}=(-i)(-D)=iD=K',
        113: r'H^{+}=(iA)^{+}=i^{*}A^{+}=(-i)(-A)=iA=H',
        121: r"\langle x\rangle=\int p(x)x\,dx=\int\psi^{*}(x)x\psi(x)\,dx=\iint\psi^{*}(x)X(x,x')\psi(x)\,dx'\,dx=\langle\psi|X|\psi\rangle",
        207: r'p(x,t)\propto|\psi(x,t)|^{2}=\psi^{*}(x,t)\psi(x,t)=e^{-i\left(\frac{2\pi}{\lambda}x-c\frac{4\pi^{2}}{\lambda^{2}}t\right)}e^{i\left(\frac{2\pi}{\lambda}x-c\frac{4\pi^{2}}{\lambda^{2}}t\right)}=e^{0}=1\ \text{Costante.}',
    },
    '06_ulteriori_sviluppi': {
        41: r'\bar x,\bar y\text{ e }\bar z',
        50: r'\bar x,\bar y\text{ e }\bar z',
        59: r'p(\bar x)=\iint_{\text{Tutto il piano }\bar y\bar z}p(\bar x,\bar y,\bar z)\,d\bar y\,d\bar z',
        198: r'\begin{cases}L_x=(yp_z-zp_y)\\ L_y=(zp_x-xp_z)\\ L_z=(xp_y-yp_x)\end{cases}',
        215: r'\begin{cases}\langle L_x\rangle=\langle\psi|(YP_z-ZP_y)|\psi\rangle\\ \langle L_y\rangle=\langle\psi|(ZP_x-XP_z)|\psi\rangle\\ \langle L_z\rangle=\langle\psi|(XP_y-YP_x)|\psi\rangle\end{cases}',
    },
    '08_effetto_fotoelettrico': {
        20: r'\begin{cases}E=mc^{2}\\ p=mc\end{cases}\Rightarrow p=\dfrac{E}{c}',
    },
}


def to_mathml(latex):
    m = L.convert(latex)
    # drop the display attr so it matches the site's own styling hook
    m = re.sub(r'\s+display="[^"]*"', '', m, count=1)
    return m


for k, fixes in REPAIRS.items():
    arr = load(k)
    for idx, latex in fixes.items():
        arr[idx] = to_mathml(latex)
    save(k, arr)
    print(f'{k}: rewrote {len(fixes)} formule -> {sorted(fixes)}')

