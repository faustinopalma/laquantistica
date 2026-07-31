import pathlib

R = pathlib.Path('.')
print('staticwebapp.config.json:', [str(p) for p in R.rglob('staticwebapp.config.json')
                                    if '.git' not in str(p)] or 'ASSENTE')
print('robots.txt:', (R / 'publish/robots.txt').exists(),
      '| sitemap.xml:', (R / 'publish/sitemap.xml').exists())


def mb(files):
    return sum(f.stat().st_size for f in files) / 1024 / 1024


pub = R / 'publish'
sorgenti = list(pub.glob('*.html'))
v2 = [f for f in (pub / 'v2').rglob('*') if f.is_file()]
tutto = [f for f in pub.rglob('*') if f.is_file()]
print(f'sorgenti bilingui: {mb(sorgenti):.1f} MB ({len(sorgenti)} file)')
print(f'albero v2        : {mb(v2):.1f} MB ({len(v2)} file)')
print(f'publish totale   : {mb(tutto):.1f} MB')
print('workflow:', [p.name for p in (R / '.github/workflows').glob('*')] if (R / '.github/workflows').exists() else 'nessuno')
print('file html in publish/ non pubblicati (ignorati):',
      [f.name for f in sorgenti if f.name.startswith('_') or f.name.startswith('game-')])
