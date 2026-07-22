#!/usr/bin/env python3
"""Bilingualize a pandoc-produced chapter's body blocks.

Wraps <p>, <h2>, <figcaption> inner content in <span class="it">..</span><span class="en">..</span>.
Inline tokens (<math>..</math> and <a class="ref">..</a>) are extracted from the Italian
source in order; the English template references them as {0}, {1}, ... so they never need
to be re-typed and cannot drift.

Usage: python tools/bilingualize.py <html> <translations.json>

translations.json: a list of objects:
  {"it": "<leading plain-text of the Italian block>", "en": "<english with {0} {1} placeholders>"}
Blocks already containing class="it" are skipped. Figcaptions of the form
"Fig. N — desc" keep the bold label outside the language spans; provide the "it" key and the
"en" value as the DESCRIPTION only (without the "Fig. N — " prefix).
"""
import re, sys, json

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)

def norm(s):
    s = strip_tags(s)
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u00a0', ' ')
    return ' '.join(s.split())

def fill(en, inner):
    tokens = re.findall(r'<math.*?</math>|<a class="ref".*?</a>|<img[^>]*class="eq-[^"]*"[^>]*>', inner, re.S)
    for j, tok in enumerate(tokens):
        en = en.replace('{%d}' % j, tok)
    return en

def main():
    path, tjson = sys.argv[1], sys.argv[2]
    trans = json.load(open(tjson, encoding='utf-8'))
    for tr in trans:
        tr['_key'] = norm(tr['it'])
        tr['_used'] = False
    t = open(path, encoding='utf-8').read()
    fig_re = re.compile(r'^(Fig\.\s*\d+)\s*[\u2014-]\s*(.*)$', re.S)
    unmatched = []

    def find(plain):
        for tr in trans:
            if not tr['_used'] and plain.startswith(tr['_key']):
                return tr
        # exact-duplicate reuse: identical block text can reuse a used translation
        for tr in trans:
            if tr['_used'] and tr['_key'] == plain:
                return tr
        return None

    def repl(m):
        tag, attrs, inner = m.group(1), m.group(2) or '', m.group(3)
        if 'class="it"' in inner:
            return m.group(0)
        plain = norm(inner)
        if not plain:
            return m.group(0)
        if tag == 'figcaption':
            fm = fig_re.match(plain)
            if fm:
                label, desc = fm.group(1), fm.group(2).strip()
                tr = find(desc)
                if not tr:
                    unmatched.append('[cap] ' + plain[:70]); return m.group(0)
                tr['_used'] = True
                en = fill(tr['en'], inner)
                return f'<{tag}{attrs}><b>{label}</b> \u2014 <span class="it">{desc}</span><span class="en">{en}</span></{tag}>'
        tr = find(plain)
        if not tr:
            unmatched.append(f'[{tag}] ' + plain[:70]); return m.group(0)
        tr['_used'] = True
        en = fill(tr['en'], inner)
        return f'<{tag}{attrs}><span class="it">{inner}</span><span class="en">{en}</span></{tag}>'

    out = re.sub(r'<(p|h2|figcaption)((?:\s[^>]*)?)>(.*?)</\1>', repl, t, flags=re.S)
    open(path, 'w', encoding='utf-8').write(out)
    used = sum(1 for tr in trans if tr['_used'])
    print(f'applied {used}/{len(trans)} translations')
    unused = [tr['it'][:45] for tr in trans if not tr['_used']]
    if unused:
        print('UNUSED translations:', len(unused))
        for u in unused: print('   -', u)
    if unmatched:
        print('UNMATCHED blocks:', len(unmatched))
        for u in unmatched: print('   -', u)

if __name__ == '__main__':
    main()
