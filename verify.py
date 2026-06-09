import re
for fname in ['index.html','page2.html','page3.html']:
    with open(fname, encoding='utf-8') as f:
        c = f.read()
    items = len(re.findall(r'class="list-item"', c))
    pag_links = len(re.findall(r'class="page-link', c))
    has_hero = '<section class="hero">' in c
    has_feat = '<!-- FEATURED -->' in c
    has_pag = 'class="pagination"' in c
    print(f'{fname}: {items} articles, {pag_links} page-links, hero={has_hero}, featured={has_feat}, pagination={has_pag}')
