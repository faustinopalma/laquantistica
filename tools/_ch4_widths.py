import re, pathlib
d = pathlib.Path('publish/img/04_diffrazione')
figs = {'Fig1':'FIG1~1.svg','Fig2':'FIG2~1.svg','Fig3':'FIG3~1.svg','Fig8':'AMPOLLA1.svg','Fig9':'AMPOLLA2.svg','Fig12':'FIG12.svg','Fig13A':'FIG13A.svg','Fig13B':'FIG13B.svg','Fig14':'FIG14.svg','Fig15':'CERCHI1.svg','Fig16':'DIFFRA~1.svg','Fig17':'CERCHI2.svg','Fig18':'CERCHI3.svg'}
for n,f in figs.items():
    t=(d/f).read_text(encoding='utf-8',errors='replace')
    w=re.search(r'<svg[^>]*?width="([0-9.]+)mm"',t)
    mm=float(w.group(1)) if w else None
    px=round(mm*96/25.4) if mm else None
    print(f'{n:7} {f:14} width={mm}mm -> {px}px natural')
