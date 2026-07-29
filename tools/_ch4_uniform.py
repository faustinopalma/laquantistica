import re, pathlib
d = pathlib.Path('publish/img/04_diffrazione')
# scale factor per figure to bring dominant stroke to Fig.16 on-screen weight
scale = {
 'FIG1~1.svg':0.1935, 'FIG2~1.svg':0.3996, 'FIG3~1.svg':1.3427,
 'AMPOLLA1.svg':0.8778, 'AMPOLLA2.svg':0.1903,
 'FIG12.svg':0.2831, 'FIG13A.svg':0.5619, 'FIG13B.svg':1.1639,
 'FIG14.svg':0.2066, 'CERCHI1.svg':2.657,
 'CERCHI2.svg':1.0227, 'CERCHI3.svg':1.1994,
}
def scale_strokes(text, f):
    def repl(m):
        return f'{m.group(1)}{round(float(m.group(2))*f,3)}'
    return re.sub(r'(stroke-width\s*[:=]\s*"?)([0-9.]+)', repl, text)
for name, f in scale.items():
    p = d/name
    t = p.read_text(encoding='utf-8', errors='replace')
    t2 = scale_strokes(t, f)
    p.write_text(t2, encoding='utf-8')
    print(f'{name:14} x{f}')
# Fig.16: remove control-line artifacts (stroke unchanged)
p16 = d/'DIFFRA~1.svg'
t = p16.read_text(encoding='utf-8', errors='replace')
for dd in ["M 522557 37039 l 321799 0","M 522557 105190 l 321799 0","M 522557 367426 l 321799 0","M 522557 435577 l 321799 0","M 792453 0 l 0 472616"]:
    t = t.replace(f'<path d="{dd}" class="C1" />','')
p16.write_text(t, encoding='utf-8')
print('DIFFRA~1.svg  artefatti rimossi')
