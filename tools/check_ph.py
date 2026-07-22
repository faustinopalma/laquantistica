import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
print('leftover placeholders:', re.findall(r'\{\d+\}', t)[:30])
print('fig-inline count:', t.count('class="fig-inline"'))
print('double class:', t.count('class="fig-inline" class='), t.count('fig-inline" class="fig-inline'))
print('span it:', t.count('<span class="it">'), 'span en:', t.count('<span class="en">'))
print('math count:', t.count('<math'))
