from pathlib import Path

root = Path(__file__).resolve().parent.parent

files = [
    "1. Esperimento di Stern-Gerlach/Esperimento di Stern-Gerlach.docx",
    "3. Esperimenti con gli Elettroni/ESPERIMENTI CON GLI ELETTRONI.docx",
    "3. Esperimenti con gli Elettroni/esperimenti_con_gli_elettroni_convertito.docx",
    "4. Diffrazione degli Elettroni/DIFFRAZIONE DEGLI ELETTRONI.docx",
    "5. Esperimento di Rutherford/ESPERIMENTO DI RUTHERFORD 2.docx",
    "6. Ulteriori sviluppi della Teoria/Ulteriori sviluppi della Teoria.docx",
    "7. Esperimento di Franck-Hertz/ESPERIMENTO DI FRANCK-HERTZ.docx",
    "8. Effetto Fotoelettrico/EFFETTO FOTOELETTRICO.docx",
    "9. Spettri atomici di emissione/SPETTRI ATOMICI DI EMISSIONE.docx",
    "Introduzione.docx",
]

sigs = {
    b"PK\x03\x04": "ZIP/OOXML (.docx)",
    b"\xd0\xcf\x11\xe0": "OLE2 (old .doc)",
    b"{\\rt": "RTF",
}

for f in files:
    p = root / f
    if not p.exists():
        print(f"MISSING  {f}")
        continue
    head = p.read_bytes()[:16]
    kind = "UNKNOWN"
    for sig, name in sigs.items():
        if head.startswith(sig):
            kind = name
            break
    print(f"{kind:20} {head.hex()[:24]}  {f}")
