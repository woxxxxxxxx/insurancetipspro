"""
apply-v3.py — V3 improvements for insurancetipspro.com
- Replaces SVG placeholder divs with Picsum Photos real images
- Adds favicon link to all pages
- Replaces text header logo with SVG img logo
- Updates title separators: ' - InsuranceTipsPro' -> ' | InsuranceTipsPro'
- Adds 'Was this helpful?' widget to all articles
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(ROOT, 'articles')
MARKER = '<!-- APPLY-V3 -->'

ARTICLE_PICSUM = {
    'how-much-car-insurance-do-i-need.html':        ('car',       'How Much Car Insurance Do I Need'),
    'term-life-vs-whole-life-insurance.html':        ('family',    'Term Life vs Whole Life Insurance'),
    'what-does-homeowners-insurance-cover.html':     ('house',     'What Does Homeowners Insurance Cover'),
    'how-to-lower-car-insurance-premium.html':       ('car',       'Lower Your Car Insurance Premium'),
    'best-health-insurance-for-self-employed.html':  ('health',    'Best Health Insurance for Self-Employed'),
    'what-is-liability-insurance.html':              ('office',    'What Is Liability Insurance'),
    'how-to-file-insurance-claim.html':              ('document',  'How to File an Insurance Claim'),
    'life-insurance-for-young-adults.html':          ('family',    'Life Insurance for Young Adults'),
    'renters-insurance-worth-it.html':               ('apartment', 'Is Renters Insurance Worth It'),
    'business-insurance-types.html':                 ('office',    'Types of Business Insurance'),
    'how-much-life-insurance-do-i-need.html':        ('family',    'How Much Life Insurance Do I Need'),
    'car-insurance-after-accident.html':             ('car',       'Car Insurance After an Accident'),
    'health-insurance-deductible-explained.html':    ('health',    'Health Insurance Deductible Explained'),
    'umbrella-insurance-explained.html':             ('rain',      'Umbrella Insurance Explained'),
    'disability-insurance-guide.html':               ('medical',   'Disability Insurance Guide'),
    'pet-insurance-worth-it.html':                   ('animals',   'Is Pet Insurance Worth It'),
    'travel-insurance-guide.html':                   ('travel',    'Travel Insurance Guide'),
    'flood-insurance-vs-homeowners.html':            ('water',     'Flood Insurance vs Homeowners Insurance'),
    'how-to-compare-insurance-quotes.html':          ('compare',   'How to Compare Insurance Quotes'),
    'insurance-terms-glossary.html':                 ('books',     'Insurance Terms Glossary'),
}

ARTICLE_IMG_RE = re.compile(r'<div class="article-image"[^>]*>.*?</div></div></div>', re.DOTALL)

HELPFUL_WIDGET = '''\n      <div class="helpful-widget">
        <p>Was this article helpful?</p>
        <div class="helpful-buttons">
          <button class="helpful-btn" onclick="helpfulVote(this)">&#128077; Yes, helpful</button>
          <button class="helpful-btn" onclick="helpfulVote(this)">&#128078; Not really</button>
        </div>
        <p class="helpful-msg" style="display:none;">Thanks for your feedback!</p>
      </div>
      <script>if(!window.helpfulVote)window.helpfulVote=function(b){document.querySelectorAll('.helpful-btn').forEach(function(x){x.classList.remove('voted');});b.classList.add('voted');b.closest('.helpful-widget').querySelector('.helpful-msg').style.display='block';};</script>'''

FAVICON_LINK = '<link rel="icon" type="image/svg+xml" href="/favicon.svg">'
LOGO_SRC = '<a href="/" class="site-logo"><img src="/logo.svg" alt="InsuranceTipsPro" style="display:block;height:36px;width:auto;" loading="eager"></a>'
LOGO_OLD = '<a href="/" class="site-logo">Insurance<span>Tips</span>Pro</a>'


def add_favicon(content):
    if 'favicon.svg' in content:
        return content, False
    return content.replace('</head>', f'{FAVICON_LINK}\n</head>', 1), True


def replace_logo(content):
    if 'logo.svg' in content:
        return content, False
    if LOGO_OLD not in content:
        return content, False
    return content.replace(LOGO_OLD, LOGO_SRC, 1), True


def fix_title(content):
    if ' - InsuranceTipsPro</title>' in content:
        return content.replace(' - InsuranceTipsPro</title>', ' | InsuranceTipsPro</title>'), True
    return content, False


def process_article(filename):
    fp = os.path.join(ARTICLES_DIR, filename)
    if not os.path.exists(fp):
        print(f'  MISSING: {filename}')
        return

    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print(f'  SKIP: {filename}')
        return

    seed, alt = ARTICLE_PICSUM[filename]
    img_tag = f'<img src="https://picsum.photos/seed/{seed}/720/300" alt="{alt}" class="article-hero-img" loading="lazy">'

    # Replace article-image div with Picsum img
    content, n = ARTICLE_IMG_RE.subn(img_tag, content, count=1)
    if not n:
        print(f'  WARNING: no article-image div found in {filename}')

    # Add helpful widget before </article>
    if '<!-- HELPFUL-WIDGET -->' not in content:
        content = content.replace('    </article>', HELPFUL_WIDGET + '\n    </article>', 1)

    content, _ = add_favicon(content)
    content, _ = replace_logo(content)
    content, _ = fix_title(content)

    # Add marker
    content = content.replace('<!-- IMPROVE-2025 -->', '<!-- IMPROVE-2025 -->\n' + MARKER, 1)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK: {filename}')


def process_index():
    fp = os.path.join(ROOT, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace featured-main article-image (first occurrence) → 800x400 insurance
    img_main = '<img src="https://picsum.photos/seed/insurance/800/400" alt="Insurance Guide" class="featured-img-real" loading="lazy">'
    img_life = '<img src="https://picsum.photos/seed/family/400/200" alt="Life Insurance" class="featured-small-img" loading="lazy">'
    img_health = '<img src="https://picsum.photos/seed/health/400/200" alt="Health Insurance" class="featured-small-img" loading="lazy">'

    replacements = [img_main, img_life, img_health]
    counter = [0]

    def replace_nth(m):
        idx = counter[0]
        counter[0] += 1
        if idx < len(replacements):
            return replacements[idx]
        return m.group(0)

    content, n = ARTICLE_IMG_RE.subn(replace_nth, content)
    content, _ = add_favicon(content)
    content, _ = replace_logo(content)
    content, _ = fix_title(content)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK (index.html, {n} images replaced)')


def process_about():
    fp = os.path.join(ROOT, 'about.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    img_team = '<img src="https://picsum.photos/seed/teamwork/800/300" alt="Our Editorial Team" class="team-photo" loading="lazy">'
    content, n = ARTICLE_IMG_RE.subn(img_team, content, count=1)
    content, _ = add_favicon(content)
    content, _ = replace_logo(content)
    content, _ = fix_title(content)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK (about.html, {n} images replaced)')


def process_contact():
    fp = os.path.join(ROOT, 'contact.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    content, _ = add_favicon(content)
    content, _ = replace_logo(content)
    content, _ = fix_title(content)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK (contact.html)')


def main():
    print('Applying V3 improvements...\n')
    for filename in ARTICLE_PICSUM:
        process_article(filename)
    process_index()
    process_about()
    process_contact()
    print('\nDone.')


if __name__ == '__main__':
    main()
