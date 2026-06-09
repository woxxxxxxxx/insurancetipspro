import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Gradient color pairs per category
GRADIENTS = {
    'auto':      ('#1e40af', '#3b82f6'),
    'life':      ('#065f46', '#10b981'),
    'health':    ('#9f1239', '#f43f5e'),
    'home':      ('#92400e', '#f59e0b'),
    'business':  ('#4c1d95', '#8b5cf6'),
    'specialty': ('#164e63', '#06b6d4'),
    'team':      ('#1a2744', '#2563eb'),
}


def svg_div(icon, label, category, min_height='220px', extra_style=''):
    c1, c2 = GRADIENTS[category]
    return (
        f'<div class="article-image" style="background:linear-gradient(135deg,{c1},{c2});'
        f'display:flex;align-items:center;justify-content:center;'
        f'min-height:{min_height};border-radius:8px;{extra_style}">'
        f'<div style="text-align:center;color:white;">'
        f'<div style="font-size:48px;">{icon}</div>'
        f'<div style="font-size:16px;margin-top:8px;font-weight:600;">{label}</div>'
        f'</div></div>'
    )


# Per-file replacement specs:
#   key = relative path from ROOT
#   value = list of (old_img_tag, new_div) tuples
#   We match by class name so we don't need exact URL strings

ARTICLE_HEROES = {
    'articles/how-much-car-insurance-do-i-need.html':      ('🚗', 'Auto Insurance',      'auto'),
    'articles/term-life-vs-whole-life-insurance.html':      ('🛡️', 'Life Insurance',       'life'),
    'articles/what-does-homeowners-insurance-cover.html':   ('🏠', 'Home Insurance',       'home'),
    'articles/how-to-lower-car-insurance-premium.html':     ('🚗', 'Auto Insurance',       'auto'),
    'articles/best-health-insurance-for-self-employed.html':('❤️', 'Health Insurance',     'health'),
    'articles/what-is-liability-insurance.html':            ('⚖️', 'Liability Insurance',  'business'),
    'articles/how-to-file-insurance-claim.html':            ('📋', 'Insurance Claims',     'specialty'),
    'articles/life-insurance-for-young-adults.html':        ('🛡️', 'Life Insurance',       'life'),
    'articles/renters-insurance-worth-it.html':             ('🏠', 'Renters Insurance',    'home'),
    'articles/business-insurance-types.html':               ('💼', 'Business Insurance',   'business'),
    'articles/how-much-life-insurance-do-i-need.html':      ('🛡️', 'Life Insurance',       'life'),
    'articles/car-insurance-after-accident.html':           ('🚗', 'Auto Insurance',       'auto'),
    'articles/health-insurance-deductible-explained.html':  ('❤️', 'Health Insurance',     'health'),
    'articles/umbrella-insurance-explained.html':           ('☂️', 'Umbrella Insurance',   'specialty'),
    'articles/disability-insurance-guide.html':             ('🛡️', 'Disability Insurance', 'specialty'),
    'articles/pet-insurance-worth-it.html':                 ('🐾', 'Pet Insurance',        'life'),
    'articles/travel-insurance-guide.html':                 ('✈️', 'Travel Insurance',     'specialty'),
    'articles/flood-insurance-vs-homeowners.html':          ('💧', 'Flood Insurance',      'specialty'),
    'articles/how-to-compare-insurance-quotes.html':        ('📊', 'Compare Quotes',       'business'),
    'articles/insurance-terms-glossary.html':               ('📚', 'Insurance Glossary',   'specialty'),
}

# Regex to match any <img ... class="article-hero-img" ...> (single line)
IMG_HERO_RE = re.compile(r'<img\s[^>]*class="article-hero-img"[^>]*>', re.IGNORECASE)
IMG_FEATURED_MAIN_RE = re.compile(r'<img\s[^>]*class="featured-img-real"[^>]*>', re.IGNORECASE)
IMG_FEATURED_SMALL_RE = re.compile(r'<img\s[^>]*class="featured-small-img"[^>]*>', re.IGNORECASE)
IMG_TEAM_RE = re.compile(r'<img\s[^>]*class="team-photo"[^>]*>', re.IGNORECASE)


def process_articles():
    changed = 0
    for rel_path, (icon, label, cat) in ARTICLE_HEROES.items():
        fp = os.path.join(ROOT, rel_path.replace('/', os.sep))
        if not os.path.exists(fp):
            print(f'  MISSING: {rel_path}')
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        replacement = svg_div(icon, label, cat, min_height='220px', extra_style='margin-bottom:24px;')
        new_content, n = IMG_HERO_RE.subn(replacement, content)
        if n:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'  OK ({n} img replaced): {rel_path}')
            changed += 1
        else:
            print(f'  SKIP (no article-hero-img found): {rel_path}')
    return changed


def process_index():
    fp = os.path.join(ROOT, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    n_total = 0

    # Featured main: car insurance
    main_div = svg_div('🚗', 'Auto Insurance', 'auto', min_height='220px', extra_style='')
    content, n = IMG_FEATURED_MAIN_RE.subn(main_div, content)
    n_total += n

    # Featured small: life insurance (first occurrence)
    life_div = svg_div('🛡️', 'Life Insurance', 'life', min_height='160px', extra_style='border-radius:8px 8px 0 0;margin:-18px -18px 14px;width:calc(100% + 36px);box-sizing:content-box;')
    health_div = svg_div('❤️', 'Health Insurance', 'health', min_height='160px', extra_style='border-radius:8px 8px 0 0;margin:-18px -18px 14px;width:calc(100% + 36px);box-sizing:content-box;')

    # Replace first featured-small-img with life, second with health
    def replace_small(m):
        replace_small.count += 1
        return life_div if replace_small.count == 1 else health_div
    replace_small.count = 0

    content, n = IMG_FEATURED_SMALL_RE.subn(replace_small, content)
    n_total += n

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK ({n_total} img replaced): index.html')
    return 1


def process_about():
    fp = os.path.join(ROOT, 'about.html')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    team_div = svg_div('👥', 'Our Editorial Team', 'team', min_height='240px', extra_style='width:100%;border-radius:12px;margin-bottom:20px;')
    content, n = IMG_TEAM_RE.subn(team_div, content)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK ({n} img replaced): about.html')
    return 1


def main():
    print('Replacing Unsplash images with inline SVG placeholders...\n')
    a = process_articles()
    process_index()
    process_about()
    print(f'\nDone: {a} articles + index.html + about.html updated.')


if __name__ == '__main__':
    main()
