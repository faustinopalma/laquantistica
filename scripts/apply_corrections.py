"""Apply small, surgical corrections to the native MathML (build/mml/*.json) for
errors found during the physics review. Targeted string replacements only — the
original styling is preserved, only the wrong token is changed. Idempotent.

Corrections:
  ch8 obj9 : soglia fotoelettrica 4,0·10^(-14) Hz  ->  4,0·10^(14) Hz
  ch8 obj7 : pendenza  eVs^2 / Js^2  ->  eV·s / J·s   (unita' errata)
  ch8 obj8 : pendenza  Js^2         ->  J·s
  ch6 obj177/178 : (XPx - PxX) = -iℏI  ->  +iℏI   (segno del commutatore canonico)
"""
import json
import re
from pathlib import Path

MML = Path('build/mml')


def load(k):
    return json.loads((MML / f'{k}.json').read_text(encoding='utf-8'))


def save(k, arr):
    (MML / f'{k}.json').write_text(json.dumps(arr, ensure_ascii=False), encoding='utf-8')


def replace_in(arr, idx, old, new, label):
    s = arr[idx]
    if old not in s:
        if new in s:
            print(f'  [skip] {label}: already corrected')
        else:
            print(f'  [WARN] {label}: pattern NOT found at idx {idx}')
        return False
    n = s.count(old)
    arr[idx] = s.replace(old, new)
    print(f'  [ok]   {label}: {n} replacement(s) at idx {idx}')
    return True


# ---- ch8: effetto fotoelettrico ------------------------------------------------
k = '08_effetto_fotoelettrico'
a = load(k)
# soglia: rimuovi il segno meno nell'esponente 10^(-14) -> 10^(14)
replace_in(a, 9,
           '<mrow><mo stretchy="false">−</mo><mtext>14</mtext></mrow>',
           '<mtext>14</mtext>',
           'soglia 10^-14 -> 10^14')
# unita' pendenza: eVs^2 -> eV·s  e  Js^2 -> J·s
replace_in(a, 7,
           '<msup><mtext>eVs</mtext><mstyle mathsize="8pt"><mn>2</mn></mstyle></msup>',
           '<mtext>eV·s</mtext>',
           'unita eVs^2 -> eV·s')
replace_in(a, 7,
           '<msup><mtext>Js</mtext><mstyle mathsize="8pt"><mn>2</mn></mstyle></msup>',
           '<mtext>J·s</mtext>',
           'unita Js^2 -> J·s (obj7)')
replace_in(a, 8,
           '<msup><mtext>Js</mtext><mstyle mathsize="8pt"><mn>2</mn></mstyle></msup>',
           '<mtext>J·s</mtext>',
           'unita Js^2 -> J·s (obj8)')
save(k, a)

# ---- ch6: ulteriori sviluppi (segno del commutatore) ---------------------------
k = '06_ulteriori_sviluppi'
a = load(k)
# In arr[177] e arr[178] il termine "-i ℏ I": il "-i" e' <mo>−</mo><mi>i</mi>
# (seguito da uno o due </mrow> poi <mi>ℏ). Il "-" del prodotto XPx - PxX e'
# invece <mo>−</mo><msub><mi>P</mi>, quindi il pattern "<mo ...>−</mo><mi>i</mi>"
# che precede ℏ e' univoco per il segno da correggere.
sign_re = re.compile(
    r'(<mo stretchy="false">)−(</mo><mi>i</mi>(?:</mrow>)+<mi mathvariant="normal">ℏ</mi>)')
for idx in (177, 178):
    s = a[idx]
    s2, n = sign_re.subn(r'\g<1>+\g<2>', s)
    if n:
        a[idx] = s2
        print(f'  [ok]   segno -iℏ -> +iℏ (obj{idx}): {n} replacement(s)')
    elif '+</mo><mi>i</mi>' in s:
        print(f'  [skip] segno -iℏ -> +iℏ (obj{idx}): already corrected')
    else:
        print(f'  [WARN] segno -iℏ -> +iℏ (obj{idx}): pattern NOT found')
save(k, a)

print('done.')
