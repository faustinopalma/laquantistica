# Generate hand-authored MathML for image108 (5-line probability derivation) from ground truth.
import pathlib

phi='<mi>&#x3D5;</mi>'; th='<mi>&#x3D1;</mi>'; e='<mi>e</mi>'; ii='<mi>i</mi>'; k='<mi>k</mi>'
mn2='<mn>2</mn>'; mn4='<mn>4</mn>'
minus='<mo>&#8722;</mo>'; plus='<mo>+</mo>'; eq='<mo>=</mo>'; comma='<mo>,</mo>'
twoi=mn2+ii

def frac(n,d): return f'<mfrac><mrow>{n}</mrow><mrow>{d}</mrow></mfrac>'
def sup(b,x):  return f'<msup><mrow>{b}</mrow><mrow>{x}</mrow></msup>'
def sq(x):     return sup(x, mn2)
def cos(a):    return f'<mtext>cos</mtext>{a}'
def sen(a):    return f'<mtext>sen</mtext>{a}'
cos2=lambda a: f'<msup><mrow><mtext>cos</mtext></mrow><mrow>{mn2}</mrow></msup>{a}'

phih=frac(phi,mn2); thh=frac(th,mn2)
sumh=frac(phi+plus+th, mn2)     # (phi+theta)/2
diffh=frac(phi+minus+th, mn2)   # (phi-theta)/2

def E(sign, ang):  # e^{+/- i ang}
    return sup(e, (ii if sign=='+' else minus+ii)+ang)

def absn(x): return f'<mo stretchy="false">|</mo>{x}<mo stretchy="false">|</mo>'          # non-stretch bars
def absb(x): return f'<mrow><mo>|</mo>{x}<mo>|</mo></mrow>'                                 # stretchy bars

def msub_m(sub): return f'<msub><mrow><mi>m</mi></mrow><mrow>{sub}</mrow></msub>'
mfk = msub_m(phi)+'<mtext>=+</mtext>'+k    # m_phi=+k
mtk = msub_m(th) +'<mtext>=+</mtext>'+k    # m_theta=+k

braket = ('<mo stretchy="false">&#10216;</mo>'+mfk+'<mo stretchy="false">|</mo>'+mtk+'<mo stretchy="false">&#10217;</mo>')
row = '<mo stretchy="false">(</mo>'+cos(phih)+comma+sen(phih)+'<mo stretchy="false">)</mo>'
col = ('<mrow><mo>(</mo><mtable><mtr><mtd>'+cos(thh)+'</mtd></mtr>'
       '<mtr><mtd>'+sen(thh)+'</mtd></mtr></mtable><mo>)</mo></mrow>')

# line 1
L1 = eq + sq(absn(braket)) + eq + sq(absb(row+col)) + eq

# line 2: |  (e^{iφ/2}+e^{-iφ/2})/2 (e^{iϑ/2}+e^{-iϑ/2})/2  +  (e^{iφ/2}-e^{-iφ/2})/2i (e^{iϑ/2}-e^{-iϑ/2})/2i  |^2
cosphi = frac(E('+',phih)+plus+E('-',phih), mn2)
costh  = frac(E('+',thh) +plus+E('-',thh),  mn2)
senphi = frac(E('+',phih)+minus+E('-',phih), twoi)
senth  = frac(E('+',thh) +minus+E('-',thh),  twoi)
L2 = eq + sq(absb(cosphi+costh+plus+senphi+senth)) + eq

# line 3
num_plus = E('+',sumh)+plus+E('-',sumh)+plus+E('+',diffh)+plus+E('-',diffh)
num_minus= E('+',sumh)+plus+E('-',sumh)+minus+E('+',diffh)+minus+E('-',diffh)
L3 = eq + sq(absb(frac(num_plus, mn4)+minus+frac(num_minus, mn4))) + eq

# line 4
L4 = (eq + sq(absb(frac(mn2+E('+',diffh)+plus+mn2+E('-',diffh), mn4)))
      + eq + sq(absb(cos(diffh)))
      + eq + cos2(diffh))

rows = [('<mi>P</mi>', L1), ('', L2), ('', L3), ('', L4)]
body = ''.join(f'<mtr><mtd>{a}</mtd><mtd>{b}</mtd></mtr>' for a,b in rows)
mathml = ('<math xmlns="http://www.w3.org/1998/Math/MathML">'
          '<mtable columnalign="right left" rowspacing="0.45em">'+body+'</mtable></math>')

out = pathlib.Path('build/ch2_overrides/image108.svg.mml')
out.write_text(mathml, encoding='utf-8')
print('wrote', out, 'len', len(mathml))
# well-formedness check
import xml.etree.ElementTree as ET
ET.fromstring(mathml); print('well-formed OK')
