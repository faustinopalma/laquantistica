"""Estrae le pagine di una scansione come immagini, per confrontarle col sito.

    python tools/scan_pagine.py scansioni/02-stern-gerlach-cascata.pdf 1 2 3
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

OUT = Path('build/ch2scan')

pdf = Path(sys.argv[1])
pagine = [int(a) for a in sys.argv[2:]]

doc = fitz.open(pdf)
OUT.mkdir(parents=True, exist_ok=True)
if not pagine:
    print(f'{pdf.name}: {doc.page_count} pagine')
    sys.exit()

for n in pagine:
    p = doc[n - 1]
    pix = p.get_pixmap(dpi=110)
    f = OUT / f'p{n:02d}.png'
    pix.save(f)
    print(f'  {f}  {pix.width}x{pix.height}')
