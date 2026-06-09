"""
add-ad-placeholders.py — Insert <!-- AD_PLACEHOLDER --> at optimal positions.

Article pages (3 slots each):
  AD-1: after hero image, before author-box  (top of content, high visibility)
  AD-2: after article-body, before cta-section  (mid/end, highest intent)
  AD-3: sidebar, after Related Articles widget  (persistent sidebar)

Homepage index.html (1 slot):
  AD-HOME: between featured grid and Latest Articles list
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(ROOT, 'articles')

AD = '<div class="ad-unit"><!-- AD_PLACEHOLDER --></div>'


def process_article(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    if c.count('<!-- AD_PLACEHOLDER -->') >= 3:
        print(f'  SKIP (already done): {os.path.basename(fp)}')
        return

    original = c

    # AD-1: after article-hero-img tag, before author-box
    c = re.sub(
        r'(<img [^>]*class="article-hero-img"[^>]*>)\n(<div class="author-box">)',
        r'\1\n' + AD + r'\n\2',
        c, count=1
    )

    # AD-2: after article-body close, before cta-section
    c = c.replace(
        '      </div>\n\n      <div class="cta-section">',
        '      </div>\n\n      ' + AD + '\n\n      <div class="cta-section">',
        1
    )

    # AD-3: sidebar — after Related Articles widget, before sidebar-cta
    c = re.sub(
        r'([ \t]*</div>\n)([ \t]*<div class="sidebar-cta">)',
        r'\1      ' + AD + r'\n\2',
        c, count=1
    )

    if c != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        n = c.count('<!-- AD_PLACEHOLDER -->')
        print(f'  OK ({n} ads): {os.path.basename(fp)}')
    else:
        print(f'  WARN (no change): {os.path.basename(fp)}')


def process_index(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    if '<!-- AD_PLACEHOLDER -->' in c:
        print(f'  SKIP: {os.path.basename(fp)}')
        return

    # AD-HOME: after featured grid, before Latest Articles section
    marker = '  </div>\n\n  <!-- LATEST ARTICLES -->'
    replacement = '  </div>\n\n  ' + AD + '\n\n  <!-- LATEST ARTICLES -->'
    c = c.replace(marker, replacement, 1)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'  OK (1 ad): {os.path.basename(fp)}')


def main():
    print('Adding ad placeholders...\n')
    articles = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.html')))
    for fp in articles:
        process_article(fp)
    process_index(os.path.join(ROOT, 'index.html'))
    print('\nDone.')


if __name__ == '__main__':
    main()
