"""
use-local-images.py — Replace all Picsum Photos URLs with local /images/img-*.png paths.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(ROOT, 'articles')

# Article -> image category mapping
ARTICLE_IMG = {
    'how-much-car-insurance-do-i-need.html':        'auto',
    'how-to-lower-car-insurance-premium.html':      'auto',
    'car-insurance-after-accident.html':            'auto',
    'how-to-file-insurance-claim.html':             'auto',
    'term-life-vs-whole-life-insurance.html':       'life',
    'life-insurance-for-young-adults.html':         'life',
    'how-much-life-insurance-do-i-need.html':       'life',
    'disability-insurance-guide.html':              'life',
    'best-health-insurance-for-self-employed.html': 'health',
    'health-insurance-deductible-explained.html':   'health',
    'pet-insurance-worth-it.html':                  'health',
    'what-does-homeowners-insurance-cover.html':    'home',
    'renters-insurance-worth-it.html':              'home',
    'flood-insurance-vs-homeowners.html':           'home',
    'business-insurance-types.html':               'business',
    'what-is-liability-insurance.html':            'business',
    'how-to-compare-insurance-quotes.html':        'business',
    'umbrella-insurance-explained.html':           'business',
    'insurance-terms-glossary.html':               'business',
    'travel-insurance-guide.html':                 'hero',
}

ARTICLE_ALT = {
    'auto':     'Auto insurance guide',
    'life':     'Life insurance guide',
    'health':   'Health insurance guide',
    'home':     'Home insurance guide',
    'business': 'Business insurance guide',
    'hero':     'Insurance professional with documents',
}

PICSUM_RE = re.compile(r'<img src="https://picsum\.photos/[^"]*"[^>]*class="article-hero-img"[^>]*>')


def process_article(filename):
    fp = os.path.join(ARTICLES_DIR, filename)
    if not os.path.exists(fp):
        print(f'  MISSING: {filename}')
        return

    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    cat = ARTICLE_IMG[filename]
    alt = ARTICLE_ALT[cat]
    new_img = f'<img src="/images/img-{cat}.png" alt="{alt}" class="article-hero-img" loading="lazy">'

    new_content, n = PICSUM_RE.subn(new_img, content)
    if n == 0:
        # Already replaced or different pattern — check for any picsum reference
        if 'picsum.photos' in content:
            # Generic fallback: replace any remaining picsum img with article-hero-img class
            new_content = re.sub(
                r'<img src="https://picsum\.photos/[^"]*"[^>]*>',
                new_img, content, count=1
            )
            if new_content != content:
                print(f'  OK (fallback): {filename}')
            else:
                print(f'  SKIP (no match): {filename}')
                return
        else:
            print(f'  SKIP (no picsum): {filename}')
            return
    else:
        print(f'  OK: {filename}')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)


def process_index():
    fp = os.path.join(ROOT, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Featured main: seed=insurance -> img-auto.png
    content = content.replace(
        '<img src="https://picsum.photos/seed/insurance/800/400" alt="Insurance Guide" class="featured-img-real" loading="lazy">',
        '<img src="/images/img-auto.png" alt="Auto insurance featured guide" class="featured-img-real" loading="lazy">',
        1
    )
    # Featured small life: seed=family -> img-life.png
    content = content.replace(
        '<img src="https://picsum.photos/seed/family/400/200" alt="Life Insurance" class="featured-small-img" loading="lazy">',
        '<img src="/images/img-life.png" alt="Life insurance guide" class="featured-small-img" loading="lazy">',
        1
    )
    # Featured small health: seed=health -> img-health.png
    content = content.replace(
        '<img src="https://picsum.photos/seed/health/400/200" alt="Health Insurance" class="featured-small-img" loading="lazy">',
        '<img src="/images/img-health.png" alt="Health insurance guide" class="featured-small-img" loading="lazy">',
        1
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  OK: index.html (featured images)')


def process_page2_page3():
    for fname in ['page2.html', 'page3.html']:
        fp = os.path.join(ROOT, fname)
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        # These pages have no images currently; nothing to do
        print(f'  OK (no images): {fname}')


def process_about():
    fp = os.path.join(ROOT, 'about.html')
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(
        '<img src="https://picsum.photos/seed/teamwork/800/300" alt="Our Editorial Team" class="team-photo" loading="lazy">',
        '<img src="/images/img-hero.png" alt="Our Editorial Team" class="team-photo" loading="lazy">',
        1
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  OK: about.html')


def main():
    print('Replacing Picsum URLs with local images...\n')
    for filename in ARTICLE_IMG:
        process_article(filename)
    process_index()
    process_page2_page3()
    process_about()
    print('\nDone.')


if __name__ == '__main__':
    main()
