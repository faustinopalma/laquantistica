"""Controlli statici sui due alberi monolingui.

Indipendenti dallo splitter: rileggono i file prodotti e verificano testa,
collegamenti e presenza dei file richiamati. Esce con codice 1 se trova errori.
"""
import pathlib
import re
import sys
from urllib.parse import unquote, urlparse

SORGENTI = pathlib.Path('sorgenti')
RADICE = pathlib.Path('publish')       # radice del sito servito: qui stanno assets/ e img/
USCITA = RADICE
BASE = 'https://laquantistica.com'
LINGUE = ('it', 'en')

errori = []
avvisi = []


def url_pubblico(lingua, file_):
    if file_ == 'index.html':
        return f'{BASE}/{lingua}/'
    return f'{BASE}/{lingua}/{file_[:-5]}'


def err(pagina, msg):
    errori.append(f'{pagina}: {msg}')


def senza_script(t):
    return re.sub(r'<script\b.*?</script>', '', t, flags=re.S)


def risorsa_locale(base, url):
    percorso = unquote(urlparse(url).path)
    bersaglio = base / percorso
    candidati = (bersaglio, pathlib.Path(f'{bersaglio}.html'), bersaglio / 'index.html')
    return next((p for p in candidati if p.exists()), None)


def esiste_risorsa(url):
    return risorsa_locale(RADICE, unquote(urlparse(url).path).lstrip('/')) is not None


for lingua in LINGUE:
    altra = 'en' if lingua == 'it' else 'it'
    cartella = USCITA / lingua
    for f in sorted(cartella.glob('*.html')):
        nome = f'{lingua}/{f.name}'
        t = f.read_text(encoding='utf-8')
        orig = (SORGENTI / f.name).read_text(encoding='utf-8')
        monolingue = 'class="it"' not in orig and 'class="en"' not in orig

        m = re.search(r'<html[^>]*>', t)
        if not monolingue and (f'lang="{lingua}"' not in m.group(0)
                               or f'data-lang="{lingua}"' not in m.group(0)):
            err(nome, f'<html> non dichiara {lingua}: {m.group(0)}')

        if monolingue:
            continue

        can = re.findall(r'<link rel="canonical" href="([^"]*)"', t)
        atteso = url_pubblico(lingua, f.name)
        if can != [atteso]:
            err(nome, f'canonical {can} invece di [{atteso}]')

        alt = dict(re.findall(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"', t))
        for l in LINGUE:
            if alt.get(l) != url_pubblico(l, f.name):
                err(nome, f'hreflang {l} = {alt.get(l)}')
        if alt.get('x-default') != url_pubblico('en', f.name):
            err(nome, f'hreflang x-default = {alt.get("x-default")}')
        for l in LINGUE:
            gemella = USCITA / l / f.name
            if not gemella.exists():
                err(nome, f'manca la pagina gemella {l}/{f.name}')

        if re.search(r'src="[^"]*lang\.js', t):
            err(nome, 'lang.js ancora caricata')
        if 'lang.css' in orig and 'lang.css' not in t:
            err(nome, 'lang.css rimossa per sbaglio')
        if 'lang-links.css' not in t:
            err(nome, 'manca lang-links.css')

        residui = re.findall(rf'class="{altra}"', senza_script(t))
        if residui:
            err(nome, f'{len(residui)} elementi della lingua {altra} non rimossi')

        sel = re.search(r'<div class="langsw"[^>]*>(.*?)</div>', t, re.S)
        if not sel:
            err(nome, 'selettore di lingua assente')
        else:
            voci = re.findall(r'<a class="langbtn" href="\.\./(\w+)/([^"]*)"[^>]*?(aria-current)?>', sel.group(1))
            if len(voci) != 2:
                err(nome, f'il selettore ha {len(voci)} voci invece di 2')
            correnti = sel.group(1).count('aria-current="true"')
            if correnti != 1:
                err(nome, f'aria-current presente {correnti} volte invece di 1')
            destinazione = '' if f.name == 'index.html' else f.name[:-5]
            if f'href="../{lingua}/{destinazione}"' not in sel.group(1):
                err(nome, 'il selettore non punta a se stesso')
            if f'href="../{altra}/{destinazione}"' not in sel.group(1):
                err(nome, f'il selettore non punta a {altra}/{destinazione}')

        ha_sidebar = 'class="sidebar"' in t
        ha_pillola = 'langsw-mobile' in t
        if ha_sidebar != ha_pillola:
            err(nome, f'pillola mobile {"assente" if ha_sidebar else "di troppo"}')

        for m in re.finditer(r'(?:src|href)="([^"]+)"', t):
            u = m.group(1)
            if re.match(r'^(https?:|mailto:|#|data:|javascript:)', u):
                continue
            percorso = unquote(urlparse(u).path)
            nome_collegato = pathlib.PurePosixPath(percorso).name
            pubblicabile = (nome_collegato and not nome_collegato.startswith(('_', 'game-'))
                             and (SORGENTI / nome_collegato).exists())
            if percorso.endswith('.html') and pubblicabile:
                err(nome, f'collegamento interno non canonico: {u}')
            if u.startswith('/'):
                if not esiste_risorsa(u):
                    err(nome, f'risorsa mancante: {u}')
            elif u.startswith('../'):
                if not risorsa_locale(cartella, u):
                    err(nome, f'collegamento rotto: {u}')
            else:
                bersaglio = unquote(u.split('?')[0].split('#')[0])
                if bersaglio and not risorsa_locale(cartella, bersaglio):
                    # gia' rotto nel sito pubblicato: la pagina bersaglio non e' deployata
                    if bersaglio in orig and not (SORGENTI / bersaglio).exists() or bersaglio.startswith('_'):
                        avvisi.append(f'{nome}: collegamento gia' + "'" + f' rotto in produzione: {u}')
                    else:
                        err(nome, f'collegamento rotto: {u}')

        for m in re.finditer(r'href="[^"]*\?ret=([^"&\']+)"', t):
            bersaglio = unquote(m.group(1)).split('#')[0]
            if bersaglio and not (cartella / bersaglio).exists():
                err(nome, f'ritorno rotto: {m.group(1)}')

radice = USCITA / 'index.html'
if not radice.exists():
    errori.append('v2/index.html: assente')

n = sum(len(list((USCITA / l).glob('*.html'))) for l in LINGUE)
print(f'controllate {n} pagine ({n // 2} per lingua)')
print(f'errori: {len(errori)}')
for e in errori:
    print(f'  !! {e}')
for a in avvisi:
    print(f'  .  {a}')
sys.exit(1 if errori else 0)
