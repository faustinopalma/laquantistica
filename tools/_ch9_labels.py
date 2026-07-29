import re, pathlib, subprocess
D = pathlib.Path('publish/img/09_spettri_atomici')

# ---------- SALTO: hand-authored clean SVG ----------
salto = '''<?xml version='1.0' encoding='utf-8'?>
<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="52mm" viewBox="0 0 1150 400">
<defs><marker id="ar" markerWidth="12" markerHeight="12" refX="2" refY="6" orient="auto"><path d="M0,0 L10,6 L0,12 z" fill="#000"/></marker></defs>
<g fill="none" stroke="#000" stroke-width="5" stroke-linecap="round">
<line x1="120" y1="80" x2="380" y2="80"/>
<line x1="120" y1="320" x2="380" y2="320"/>
<line x1="180" y1="92" x2="180" y2="300" marker-end="url(#ar)"/>
</g>
<g font-family="Georgia,'Times New Roman',serif" fill="#000">
<text x="400" y="92" font-size="46">energia iniziale <tspan font-style="italic">E</tspan><tspan font-style="italic" font-size="32" dy="12">i</tspan></text>
<text x="400" y="332" font-size="46">energia finale <tspan font-style="italic">E</tspan><tspan font-style="italic" font-size="32" dy="12">f</tspan></text>
</g>
</svg>'''
(D/'SALTO.svg').write_text(salto, encoding='utf-8')
print('wrote SALTO.svg')

# ---------- helper to add text before </svg> ----------
def add_texts(fname, texts, viewbox=None, widthmm=None):
    p = D/fname
    t = p.read_text(encoding='utf-8')
    if viewbox:
        t = re.sub(r'viewBox="[^"]+"', f'viewBox="{viewbox}"', t, count=1)
    if widthmm:
        t = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+mm"', rf'\1 width="{widthmm}mm"', t, count=1)
    block = '<g font-family="Georgia,\'Times New Roman\',serif" fill="#000000">' + ''.join(texts) + '</g></svg>'
    t = t.replace('</svg>', block)
    p.write_text(t, encoding='utf-8')
    print('labeled', fname)

def txt(x, y, s, size, anchor='start', italic=False):
    st = ' font-style="italic"' if italic else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}"{st}>{s}</text>'

# ---------- LIVELLI (Fig.1) ----------
# levels y: 31176(0,n=inf) 52640(-0,9) 69054(-1,5,n=3) 117031(-3,4,n=2) 374596(-13,6,n=1)
FS=10500; off=3600
liv=[]
liv.append(txt(9000,-1500,'<tspan font-style="italic">E</tspan> (eV)',FS,'start'))
for y,val in [(31176,'0'),(52640,'\u22120,9'),(69054,'\u22121,5'),(117031,'\u22123,4'),(374596,'\u221213,6')]:
    liv.append(txt(-1500, y+off, val, 9500,'end'))
for y,n in [(31176,'n=\u221e'),(69054,'n=3'),(117031,'n=2'),(374596,'n=1')]:
    liv.append(txt(127000, y+off, n, FS,'start'))
add_texts('LIVELLI.svg', liv, viewbox='-30000 -15980 200000 431707', widthmm='255')

# ---------- SALTI (Fig.2) ----------
# same 5 levels; axis x=633418; levels x 649163..1000000
FS2=11000; off2=3800
sal=[]
sal.append(txt(641000,-1500,'<tspan font-style="italic">E</tspan> (eV)',FS2,'start'))
for y,val in [(31176,'0'),(52640,'\u22120,9'),(69054,'\u22121,5'),(117031,'\u22123,4'),(374596,'\u221213,6')]:
    sal.append(txt(630000, y+off2, val, 10000,'end'))
# series labels at bottom (first guess x-centers)
for xc,name in [(700000,'Serie di Lyman'),(830000,'Serie di Balmer'),(945000,'Serie di Paschen')]:
    sal.append(txt(xc, 405000, name, 11000,'middle'))
add_texts('SALTI.svg', sal, viewbox='603000 -15980 413000 440000', widthmm='206')

# render previews
out='build/ch9_labels_prev'
subprocess.run([r'C:\Program Files\LibreOffice\program\soffice.exe','--headless','--convert-to','png','--outdir',out,str(D/'SALTO.svg'),str(D/'LIVELLI.svg'),str(D/'SALTI.svg')],check=False)
print('rendered')
