import re, pathlib
d = pathlib.Path('publish/img/04_diffrazione')
figs = {
 'Fig1':'FIG1~1.svg','Fig2':'FIG2~1.svg','Fig3':'FIG3~1.svg',
 'Fig8':'AMPOLLA1.svg','Fig9':'AMPOLLA2.svg',
 'Fig12':'FIG12.svg','Fig13A':'FIG13A.svg','Fig13B':'FIG13B.svg',
 'Fig14':'FIG14.svg','Fig15':'CERCHI1.svg','Fig16':'DIFFRA~1.svg',
 'Fig17':'CERCHI2.svg','Fig18':'CERCHI3.svg',
}
for name,f in figs.items():
    t = (d/f).read_text(encoding='utf-8', errors='replace')
    vb = re.search(r'viewBox="([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)"', t)
    vbw = float(vb.group(3)) if vb else None
    sws = [float(x) for x in re.findall(r'stroke-width\s*[:=]\s*"?([0-9.]+)', t)]
    uniq = sorted(set(sws))
    ratios = [round(s/vbw*1000,3) for s in uniq] if vbw else []
    # dominant stroke-width = most common
    from collections import Counter
    dom = Counter(sws).most_common(1)[0] if sws else (None,0)
    domr = round(dom[0]/vbw*1000,3) if vbw and dom[0] else None
    print(f'{name:7} {f:14} vbw={vbw!s:>10}  n_sw={len(sws):3}  uniq={uniq}  dom={dom[0]}(x{dom[1]}) ratio‰(dom)={domr}')
