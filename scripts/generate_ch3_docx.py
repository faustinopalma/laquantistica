"""Regenerate the chapter-3 Word document (.docx) from the reconstructed content.
Converts the authored HTML body to Markdown (LaTeX math -> $..$), then uses pandoc
to produce a .docx with native Word (OMML) equations.
"""
import re, html, subprocess
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch3_content import CH3_BODY

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / '3. Esperimenti con gli Elettroni (ricostruito)'
IMGDIR = ROOT / 'img' / '03_elettroni'

def html_to_md(body):
    md = []
    # normalise
    s = body
    # figures -> markdown images
    def fig_repl(m):
        src = m.group('src'); cap = m.group('cap')
        name = Path(src).name
        return f'\n![{cap}]({IMGDIR / name})\n'
    s = re.sub(r'<figure><img[^>]*src="(?P<src>[^"]+)"[^>]*>\s*<figcaption>(?P<cap>.*?)</figcaption></figure>',
               fig_repl, s, flags=re.S)
    # tables
    def table_repl(m):
        rows = re.findall(r'<tr>(.*?)</tr>', m.group(0), flags=re.S)
        out = []
        for i, r in enumerate(rows):
            cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S)
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            cells = [html.unescape(c).replace('|', '\\|') for c in cells]
            out.append('| ' + ' | '.join(cells) + ' |')
            if i == 0:
                out.append('|' + '|'.join(['---'] * len(cells)) + '|')
        return '\n' + '\n'.join(out) + '\n'
    s = re.sub(r'<table[^>]*>.*?</table>', table_repl, s, flags=re.S)
    s = re.sub(r'</?div[^>]*>', '', s)

    # process block by block
    tokens = re.split(r'(?=<h2>|<p>|\n!\[)', s)
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok.startswith('<h2>'):
            t = re.sub(r'</?h2>', '', tok)
            md.append('\n## ' + clean_inline(t) + '\n')
        elif tok.startswith('<p>'):
            t = re.sub(r'</?p>', '', tok)
            # display equations inside paragraph
            md.append('\n' + clean_inline(t) + '\n')
        elif tok.startswith('!['):
            md.append('\n' + tok + '\n')
        else:
            md.append('\n' + clean_inline(tok) + '\n')
    text = ''.join(md)
    # LaTeX math delimiters -> markdown
    text = text.replace(r'\[', '\n$$').replace(r'\]', '$$\n')
    text = text.replace(r'\(', '$').replace(r'\)', '$')
    return text

def clean_inline(t):
    t = re.sub(r'<strong>(.*?)</strong>', r'**\1**', t, flags=re.S)
    t = re.sub(r'<em>(.*?)</em>', r'*\1*', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    return t.strip()

def main():
    md_body = html_to_md(CH3_BODY)
    md = '# Esperimenti con gli Elettroni\n' + md_body
    md_file = ROOT / 'build' / 'ch3.md'
    md_file.write_text(md, encoding='utf-8')
    out_docx = OUTDIR / 'Esperimenti con gli Elettroni.docx'
    cmd = ['pandoc', str(md_file), '-f', 'markdown+tex_math_dollars',
           '-o', str(out_docx), '--resource-path', str(IMGDIR)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        print('PANDOC ERROR:', r.stderr)
    else:
        print('wrote', out_docx, out_docx.stat().st_size, 'bytes')

if __name__ == '__main__':
    main()
