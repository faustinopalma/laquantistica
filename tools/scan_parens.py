import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
# strip tags to inspect prose only, but keep offsets by working line by line on body
body = t
# find all '(' and show context; flag likely-corrupt (not followed by 'fig'/'Fig'/'1 '/'vedi'/'pressione'/'circa'/'10' digit start of real paren, and preceded by space+word)
for m in re.finditer(r'.{22}\(.{18}', body):
    s = m.group(0)
    # skip obvious real parentheses
    low = s[s.index('(')+1:].lower()
    if low.startswith(('fig','1 angstrom','vedi','pressione','gradi','t (','10','–','-','1,','2,','5,','7,','0,')):
        tag='real?'
    else:
        tag='CHK'
    print(tag, repr(s))
