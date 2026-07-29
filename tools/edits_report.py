"""Rilegge il registro delle modifiche fatte con lo strumento locale.

E' il ponte fra "io scrivo l'italiano" e "tu controlli e allinei le altre lingue":
mostra, raggruppate per pagina, tutte le modifiche non ancora riviste, con il
testo prima e dopo e la frase corrispondente nelle altre lingue, cosi' com'e'
adesso nel file.

    python tools/edits_report.py            # solo quelle da rivedere
    python tools/edits_report.py --all      # tutto lo storico
    python tools/edits_report.py --done     # segna come riviste
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

JOURNAL = Path('build/edits/journal.jsonl')
TAG = re.compile(r'<[^>]+>')


def load() -> list[dict]:
    if not JOURNAL.exists():
        return []
    rows = []
    for line in JOURNAL.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def plain(s: str | None, n: int = 400) -> str:
    if s is None:
        return '(manca)'
    t = TAG.sub('', s)
    t = re.sub(r'\s+', ' ', t).strip()
    return t if len(t) <= n else t[:n] + '…'


def show(rows: list[dict]) -> None:
    by_file: dict[str, list[dict]] = {}
    for r in rows:
        by_file.setdefault(r['file'], []).append(r)

    for f, items in sorted(by_file.items()):
        print(f'\n{"=" * 78}\n{f}  ({len(items)} modifiche)\n{"=" * 78}')
        for r in items:
            head = 'FORMULA' if r['kind'] == 'tex' else f'TESTO [{r.get("lang", "it")}]'
            print(f'\n  {head} · riga {r["line"]} · {r["t"]}')
            if r['kind'] == 'tex':
                print(f'    prima : {r["before"]}')
                print(f'    dopo  : {r["after"]}')
            else:
                print(f'    prima : {plain(r["before"])}')
                print(f'    dopo  : {plain(r["after"])}')
                for code, text in (r.get('others') or {}).items():
                    print(f'    [{code}] : {plain(text)}')


def mark_done(rows: list[dict]) -> int:
    n = 0
    for r in rows:
        if not r.get('reviewed'):
            r['reviewed'] = True
            n += 1
    JOURNAL.write_text(
        ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows),
        encoding='utf-8')
    return n


def main() -> None:
    rows = load()
    if '--done' in sys.argv:
        print(f'segnate come riviste: {mark_done(rows)}')
        return
    if '--all' not in sys.argv:
        rows = [r for r in rows if not r.get('reviewed')]
    if not rows:
        print('nessuna modifica da rivedere.')
        return
    show(rows)
    print(f'\n{len(rows)} modifiche da rivedere. '
          'Quando sono allineate: python tools/edits_report.py --done')


if __name__ == '__main__':
    main()
