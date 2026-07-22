"""Extract plain text (with figure references) from a .docx by reading word/document.xml.
Usage: python tools/_docxtext.py "<path.docx>"
Prints paragraphs; marks where images/drawings are embedded as [IMG].
"""
import sys, zipfile, re

path = sys.argv[1]
z = zipfile.ZipFile(path)
xml = z.read("word/document.xml").decode("utf-8", "replace")
# split into paragraphs
paras = re.split(r"</w:p>", xml)
out = []
for p in paras:
    # collect text runs
    texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)
    txt = "".join(texts)
    txt = re.sub(r"<[^>]+>", "", txt)
    has_img = ("<w:drawing" in p) or ("<w:pict" in p) or ("<v:imagedata" in p) or ("<pic:pic" in p)
    line = txt.strip()
    if has_img:
        out.append("    [IMG]" + ((" " + line) if line else ""))
    elif line:
        out.append(line)
for i, l in enumerate(out):
    print(f"{i:3d}| {l}")
