"""
paginate.py — Splits insurancetipspro.com into 4 paginated pages.

Distribution: page1=1-6, page2=7-12, page3=13-18, page4=19-20.
Reads ALL items from existing index+page2+page3, then rebuilds all 4 pages.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, 'index.html')


# ── helpers ────────────────────────────────────────────────────────

def extract_list_items(html):
    """Return list of raw HTML strings, one per <div class="list-item"> block."""
    start_tag = '<div class="article-list">'
    end_tag   = '</div><!-- /article-list -->'
    s = html.find(start_tag)
    e = html.find(end_tag)
    if s == -1 or e == -1:
        return []
    section = html[s + len(start_tag):e]

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


def pagination_html(current, total=4):
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


def remove_old_pagination(html):
    """Remove existing pagination nav if present."""
    return re.sub(r'\n  <nav class="pagination".*?</nav>', '', html, count=1, flags=re.DOTALL)


def inject_pagination_after_list(html, pag_html):
    """Insert pagination block between </div><!-- /article-list --> and </div><!-- /section-alt -->."""
    marker = '</div><!-- /article-list -->\n  </div><!-- /section-alt -->'
    replacement = f'</div><!-- /article-list -->\n{pag_html}\n  </div><!-- /section-alt -->'
    return html.replace(marker, replacement, 1)


# ── page 1 (index.html) ────────────────────────────────────────────

def update_page1(html, items):
    page1_items = items[:6]
    html = remove_old_pagination(html)
    html = replace_article_list(html, items_html(page1_items))
    html = inject_pagination_after_list(html, pagination_html(1))
    return html


# ── pages 2 / 3 / 4 ───────────────────────────────────────────────

RANGES = {2: (6, 12), 3: (12, 18), 4: (18, 20)}
TOTAL_ARTICLES = 20
TITLES = {
    2: 'All Insurance Guides, Page 2 | InsuranceTipsPro',
    3: 'All Insurance Guides, Page 3 | InsuranceTipsPro',
    4: 'All Insurance Guides, Page 4 | InsuranceTipsPro',
}
DESCS = {
    2: 'Browse all insurance guides on InsuranceTipsPro — page 2 of 4.',
    3: 'Browse all insurance guides on InsuranceTipsPro — page 3 of 4.',
    4: 'Browse all insurance guides on InsuranceTipsPro — page 4 of 4.',
}
CANONICALS = {
    2: 'https://insurancetipspro.com/page2.html',
    3: 'https://insurancetipspro.com/page3.html',
    4: 'https://insurancetipspro.com/page4.html',
}


def build_page(base_html, page_num, items):
    lo, hi = RANGES[page_num]
    page_items = items[lo:hi]
    n_start, n_end = lo + 1, min(hi, TOTAL_ARTICLES)

    html = base_html

    # head: title
    html = re.sub(r'<title>.*?</title>',
                  f'<title>{TITLES[page_num]}</title>', html, count=1)

    # head: description
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{DESCS[page_num]}">',
                  html, count=1)

    # head: canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="{CANONICALS[page_num]}">',
                  html, count=1)

    # remove hero section
    html = re.sub(r'\n<!-- HERO -->\n<section class="hero">.*?</section>',
                  '', html, count=1, flags=re.DOTALL)

    # remove category nav
    html = re.sub(r'\n\n<!-- CATEGORY NAV -->\n<nav class="cat-nav".*?</nav>',
                  '', html, count=1, flags=re.DOTALL)

    # remove trust bar
    html = re.sub(r'\n\n<!-- TRUST BAR -->\n<div class="trust-bar">.*?</div>',
                  '', html, count=1, flags=re.DOTALL)

    # remove featured section (from <!-- FEATURED --> through end of featured-grid </div>)
    html = re.sub(r'\n\n  <!-- FEATURED -->.*?</div>\n\n  <!-- LATEST',
                  '\n\n  <!-- LATEST', html, count=1, flags=re.DOTALL)

    # remove why trust us section
    html = re.sub(r'\n\n  <!-- WHY TRUST US -->.*?</div>\n\n  <!-- NEWSLETTER',
                  '\n\n  <!-- NEWSLETTER', html, count=1, flags=re.DOTALL)

    # update section header
    html = html.replace(
        '<h2 class="section-title" id="latest" style="padding-top:32px;">Latest Articles</h2>',
        f'<p class="page-info">Showing articles {n_start}–{n_end} of {TOTAL_ARTICLES}</p>\n  '
        f'<h2 class="section-title" style="padding-top:16px;">All Guides — Page {page_num} of 4</h2>',
        1
    )

    # remove old pagination then replace article list and inject new pagination
    html = remove_old_pagination(html)
    html = replace_article_list(html, items_html(page_items))
    html = inject_pagination_after_list(html, pagination_html(page_num))

    return html


# ── main ───────────────────────────────────────────────────────────

def main():
    # Read current base (index.html before modification)
    with open(INDEX, 'r', encoding='utf-8') as f:
        base = f.read()

    # Collect ALL items from all existing pages
    all_items = extract_list_items(base)
    print(f'index.html: {len(all_items)} items')

    for pname in ['page2.html', 'page3.html']:
        fp = os.path.join(ROOT, pname)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                ph = f.read()
            extra = extract_list_items(ph)
            print(f'{pname}: {len(extra)} items')
            all_items.extend(extra)

    print(f'Total items collected: {len(all_items)}')

    if len(all_items) != 20:
        print(f'WARNING: expected 20 items, got {len(all_items)}')

    # Page 1 — update index.html in place (keep base pristine for page2-4 building)
    p1 = update_page1(base, all_items)
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(p1)
    print('Updated index.html (articles 1-6 + 4-page pagination)')

    # Pages 2-4 built from the original base
    for page_num in [2, 3, 4]:
        lo, hi = RANGES[page_num]
        phtml = build_page(base, page_num, all_items)
        out = os.path.join(ROOT, f'page{page_num}.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(phtml)
        actual_count = min(hi, len(all_items)) - lo
        print(f'Created page{page_num}.html (articles {lo+1}-{min(hi, len(all_items))}, {actual_count} items)')


if __name__ == '__main__':
    main()
