"""
paginate.py — Splits insurancetipspro.com homepage into 3 paginated pages.

Distribution: page 1 = articles 1-6, page 2 = 7-13, page 3 = 14-20.
Creates index.html (modified), page2.html, page3.html.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, 'index.html')


# ── helpers ────────────────────────────────────────────────────────

def extract_list_items(html):
    """Return list of raw HTML strings, one per <div class="list-item"> block."""
    start = html.find('<div class="article-list">') + len('<div class="article-list">')
    end   = html.find('</div><!-- /article-list -->')
    section = html[start:end]

    items, pos = [], 0
    while True:
        i0 = section.find('<div class="list-item"', pos)
        if i0 == -1:
            break
        depth, i = 0, i0
        while i < len(section):
            if section[i:i+4] == '<div':
                depth += 1; i += 4
            elif section[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    items.append(section[i0:i+6])
                    pos = i + 6
                    break
                i += 6
            else:
                i += 1
        else:
            break
    return items


def items_html(items):
    """Join list-item strings into article-list content."""
    return '\n\n    '.join([''] + items) + '\n\n  '


def pagination_html(current, total=3):
    """Build pagination <nav> block."""
    def page_href(p):
        return '/' if p == 1 else f'/page{p}.html'

    lines = ['  <nav class="pagination" aria-label="Page navigation">']

    # Prev
    if current == 1:
        lines.append('    <span class="page-link disabled">&larr; Prev</span>')
    else:
        lines.append(f'    <a href="{page_href(current-1)}" class="page-link prev">&larr; Prev</a>')

    # Numbered pages
    for p in range(1, total + 1):
        if p == current:
            lines.append(f'    <a href="{page_href(p)}" class="page-link active" aria-current="page">{p}</a>')
        else:
            lines.append(f'    <a href="{page_href(p)}" class="page-link">{p}</a>')

    # Next
    if current == total:
        lines.append('    <span class="page-link disabled">Next &rarr;</span>')
    else:
        lines.append(f'    <a href="{page_href(current+1)}" class="page-link next">Next &rarr;</a>')

    lines.append('  </nav>')
    return '\n'.join(lines)


def replace_article_list(html, new_items_html):
    """Replace everything between <div class="article-list"> and </div><!-- /article-list -->."""
    start_tag = '<div class="article-list">'
    end_tag   = '</div><!-- /article-list -->'
    s = html.find(start_tag) + len(start_tag)
    e = html.find(end_tag)
    return html[:s] + new_items_html + html[e:]


def inject_pagination_after_list(html, pag_html):
    """Insert pagination block between </div><!-- /article-list --> and </div><!-- /section-alt -->."""
    marker = '</div><!-- /article-list -->\n  </div><!-- /section-alt -->'
    replacement = f'</div><!-- /article-list -->\n{pag_html}\n  </div><!-- /section-alt -->'
    return html.replace(marker, replacement, 1)


# ── page 1 (index.html) ────────────────────────────────────────────

def update_page1(html, items):
    page1_items = items[:6]
    html = replace_article_list(html, items_html(page1_items))
    html = inject_pagination_after_list(html, pagination_html(1))
    return html


# ── page 2 / 3 ────────────────────────────────────────────────────

RANGES = {2: (6, 13), 3: (13, 20)}
TITLES = {
    2: 'All Insurance Guides, Page 2 | InsuranceTipsPro',
    3: 'All Insurance Guides, Page 3 | InsuranceTipsPro',
}
DESCS = {
    2: 'Browse all insurance guides on InsuranceTipsPro — page 2 of 3.',
    3: 'Browse all insurance guides on InsuranceTipsPro — page 3 of 3.',
}
CANONICALS = {
    2: 'https://insurancetipspro.com/page2.html',
    3: 'https://insurancetipspro.com/page3.html',
}


def build_page(base_html, page_num, items):
    lo, hi = RANGES[page_num]
    page_items = items[lo:hi]
    n_start, n_end = lo + 1, hi

    html = base_html

    # ── head: title
    html = re.sub(r'<title>.*?</title>',
                  f'<title>{TITLES[page_num]}</title>', html, count=1)

    # ── head: description
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{DESCS[page_num]}">',
                  html, count=1)

    # ── head: canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="{CANONICALS[page_num]}">',
                  html, count=1)

    # ── remove hero section
    html = re.sub(r'\n<!-- HERO -->\n<section class="hero">.*?</section>',
                  '', html, count=1, flags=re.DOTALL)

    # ── remove featured section (from <!-- FEATURED --> comment through end of featured-grid </div>)
    html = re.sub(r'\n\n  <!-- FEATURED -->.*?</div>\n\n  <!-- LATEST',
                  '\n\n  <!-- LATEST', html, count=1, flags=re.DOTALL)

    # ── remove why trust us section
    html = re.sub(r'\n\n  <!-- WHY TRUST US -->.*?</div>\n\n  <!-- NEWSLETTER',
                  '\n\n  <!-- NEWSLETTER', html, count=1, flags=re.DOTALL)

    # ── update section header
    html = html.replace(
        '<h2 class="section-title" id="latest" style="padding-top:32px;">Latest Articles</h2>',
        f'<p class="page-info">Showing articles {n_start}–{n_end} of 20</p>\n  '
        f'<h2 class="section-title" style="padding-top:16px;">All Guides — Page {page_num} of 3</h2>',
        1
    )

    # ── replace article list
    html = replace_article_list(html, items_html(page_items))

    # ── inject pagination
    html = inject_pagination_after_list(html, pagination_html(page_num))

    return html


# ── main ───────────────────────────────────────────────────────────

def main():
    with open(INDEX, 'r', encoding='utf-8') as f:
        base = f.read()

    items = extract_list_items(base)
    print(f'Extracted {len(items)} list items from index.html')

    # Page 1 — modify index.html in place
    p1 = update_page1(base, items)
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(p1)
    print('Updated index.html (articles 1-6 + pagination)')

    # Page 2
    p2 = build_page(base, 2, items)
    out2 = os.path.join(ROOT, 'page2.html')
    with open(out2, 'w', encoding='utf-8') as f:
        f.write(p2)
    print('Created page2.html (articles 7-13)')

    # Page 3
    p3 = build_page(base, 3, items)
    out3 = os.path.join(ROOT, 'page3.html')
    with open(out3, 'w', encoding='utf-8') as f:
        f.write(p3)
    print('Created page3.html (articles 14-20)')


if __name__ == '__main__':
    main()
