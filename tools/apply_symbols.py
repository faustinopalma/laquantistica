import json, sys
path, data = sys.argv[1], sys.argv[2]
d = json.load(open(data, encoding='utf-8'))
t = open(path, encoding='utf-8').read()
missing = []
for old, new in d.get('once', []):
    if old in t:
        t = t.replace(old, new, 1)
    else:
        missing.append(old)
for old, new in d.get('all', []):
    if old in t:
        t = t.replace(old, new)
    else:
        missing.append('[all] ' + old)
open(path, 'w', encoding='utf-8').write(t)
print('done. missing:', len(missing))
for m in missing:
    print('   MISSING:', repr(m))
