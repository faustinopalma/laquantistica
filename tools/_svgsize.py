import re, os
d = "publish/leggi/img/03_elettroni"
for f in ["FIG1", "FIG2", "FIG3", "FIG13"]:
    s = open(os.path.join(d, f + ".svg"), encoding="utf-8").read(800)
    w = re.search(r'<svg[^>]*?width="([^"]+)"', s)
    h = re.search(r'<svg[^>]*?height="([^"]+)"', s)
    vb = re.search(r'viewBox="([^"]+)"', s)
    print(f, "w=", w.group(1) if w else None, "h=", h.group(1) if h else None,
          "vb=", vb.group(1) if vb else None)
