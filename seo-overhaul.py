#!/usr/bin/env python3
"""
seo-overhaul.py — Full SEO overhaul for insurancetipspro.com

Applies to all 20 article pages + index.html:
  1. OG meta tags (og:type, og:title, og:description, og:url, og:image, og:site_name)
  2. Article + BreadcrumbList JSON-LD  (article pages)
  3. WebSite + ItemList JSON-LD         (index.html)
  4. Improved image alt text
  5. Contextual inline links in article body (2-3 internal + 1 CoverageFixPro per article)
"""
import os, re, json

ROOT       = os.path.dirname(os.path.abspath(__file__))
ARTS_DIR   = os.path.join(ROOT, 'articles')
BASE       = 'https://insurancetipspro.com'
PUB_NAME   = 'InsuranceTipsPro'
LOGO_URL   = f'{BASE}/logo.svg'
AUTHOR     = 'InsuranceTipsPro Editorial Team'

# ─── Per-article static data ──────────────────────────────────────────────────

ARTICLES = [
  {
    'slug': 'how-much-car-insurance-do-i-need',
    'title': 'How Much Car Insurance Do I Need?',
    'desc':  'Learn exactly how much car insurance you need — state minimums, liability limits, when to drop collision, and the right coverage for your situation.',
    'image': '/images/img-auto.png',
    'date':  '2025-06-05',
    'crumb': 'How Much Car Insurance Do I Need?',
    'alt_old': 'alt="Auto insurance guide"',
    'alt_new': 'alt="Car insurance guide showing state minimum requirements and recommended coverage limits"',
    'link_inserts': [
      # (find_text, replacement)
      (
        'pair it with a <strong>personal umbrella policy</strong>',
        'pair it with a <a href="/articles/umbrella-insurance-explained.html"><strong>personal umbrella policy</strong></a>'
      ),
      (
        'Use online comparison tools, contact independent agents who work with multiple carriers',
        'Use <a href="/articles/how-to-compare-insurance-quotes.html">online comparison tools</a>, contact independent agents who work with multiple carriers'
      ),
      (
        'Check your car\'s current value on Kelley Blue Book or Edmunds before every renewal.',
        'Check your car\'s current value on Kelley Blue Book or Edmunds before every renewal. Our <a href="https://coveragefixpro.com/tools/auto/deductible-optimizer.html" target="_blank" rel="noopener">free deductible optimizer</a> can also help you find the right balance between premium savings and out-of-pocket risk.'
      ),
    ],
  },
  {
    'slug': 'term-life-vs-whole-life-insurance',
    'title': 'Term Life vs. Whole Life Insurance: Which Is Right for You?',
    'desc':  'Compare term life vs whole life insurance — costs, cash value, pros and cons, and which policy fits your financial goals and family situation.',
    'image': '/images/img-life.png',
    'date':  '2025-06-04',
    'crumb': 'Term Life vs. Whole Life Insurance',
    'alt_old': 'alt="Life insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Term life vs whole life insurance comparison guide for families" class="article-hero-img"',
    'link_inserts': [
      (
        'Our related article on how much life insurance you need covers this in detail.',
        'Our related article on <a href="/articles/how-much-life-insurance-do-i-need.html">how much life insurance you need</a> covers this in detail.'
      ),
      (
        'Always work with a fee-only financial advisor before purchasing any permanent life insurance product.',
        'Always work with a fee-only financial advisor before purchasing any permanent life insurance product. Young buyers should also read why <a href="/articles/life-insurance-for-young-adults.html">life insurance is cheapest when you\'re young</a>.'
      ),
      (
        'The bottom line: for most Americans with dependents and a mortgage, a 20- or 30-year term policy',
        'The bottom line: for most Americans with dependents and a mortgage, a 20- or 30-year term policy'
      ),
    ],
  },
  {
    'slug': 'what-does-homeowners-insurance-cover',
    'title': 'What Does Homeowners Insurance Cover? A Complete Guide',
    'desc':  'Learn what homeowners insurance covers — dwelling, personal property, liability, loss of use — plus what\'s excluded and how much coverage you really need.',
    'image': '/images/img-home.png',
    'date':  '2025-06-03',
    'crumb': 'What Does Homeowners Insurance Cover?',
    'alt_old': 'alt="Home insurance guide"',
    'alt_new': 'alt="Homeowners insurance coverage areas including dwelling, personal property, and liability"',
    'link_inserts': [
      (
        '<strong>Floods:</strong> Flood damage is never covered under a standard homeowners policy. You need a separate flood insurance policy',
        '<strong>Floods:</strong> Flood damage is never covered under a standard homeowners policy. See our <a href="/articles/flood-insurance-vs-homeowners.html">flood insurance vs. homeowners insurance guide</a>. You need a separate flood insurance policy'
      ),
      (
        'many advisors recommend at least $300,000 and pairing it with a personal umbrella policy for additional protection.',
        'many advisors recommend at least $300,000 and pairing it with a <a href="/articles/umbrella-insurance-explained.html">personal umbrella policy</a> for additional protection.'
      ),
      (
        'Get your own repair estimates:</strong> Don\'t rely solely on the insurer\'s adjuster.',
        'Get your own repair estimates:</strong> Don\'t rely solely on the insurer\'s adjuster. Read our full guide on <a href="/articles/how-to-file-insurance-claim.html">how to file an insurance claim</a> for step-by-step advice.'
      ),
    ],
  },
  {
    'slug': 'how-to-lower-car-insurance-premium',
    'title': 'How to Lower Your Car Insurance Premium: 12 Proven Strategies',
    'desc':  'Discover 12 proven ways to lower your car insurance premium without sacrificing coverage. From bundling to usage-based programs, save hundreds per year.',
    'image': '/images/img-auto.png',
    'date':  '2025-06-02',
    'crumb': 'How to Lower Car Insurance Premium',
    'alt_old': 'alt="Auto insurance guide" class="article-hero-img"',
    'alt_new': 'alt="12 proven strategies to lower car insurance premium without reducing coverage" class="article-hero-img"',
    'link_inserts': [
      (
        'if your car is worth less than 10 times your annual collision/comprehensive premium, consider dropping those coverages.',
        'if your car is worth less than 10 times your annual collision/comprehensive premium, consider dropping those coverages. Our guide on <a href="/articles/how-much-car-insurance-do-i-need.html">how much car insurance you actually need</a> explains when dropping coverage makes financial sense.'
      ),
      (
        'For help estimating exactly how coverage level and deductible choices affect your costs, use our free calculators at CoverageFixPro.com.',
        'For help estimating exactly how coverage level and deductible choices affect your costs, use the <a href="https://coveragefixpro.com/tools/auto/bundling-discount-calculator.html" target="_blank" rel="noopener">free bundling discount calculator</a> and <a href="/articles/how-to-compare-insurance-quotes.html">learn how to compare insurance quotes</a> properly before you switch.'
      ),
    ],
  },
  {
    'slug': 'best-health-insurance-for-self-employed',
    'title': 'Best Health Insurance Options for the Self-Employed in 2025',
    'desc':  'Freelancers and self-employed workers have more health insurance options than ever. Compare ACA marketplace plans, HSAs, and more to find affordable coverage.',
    'image': '/images/img-health.png',
    'date':  '2025-06-01',
    'crumb': 'Best Health Insurance for Self-Employed',
    'alt_old': 'alt="Health insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Health insurance options for self-employed freelancers and independent contractors" class="article-hero-img"',
    'link_inserts': [
      (
        'HDHPs pair high deductibles ($1,600+ for individuals in 2025) with lower premiums.',
        'HDHPs pair high deductibles ($1,600+ for individuals in 2025) with lower premiums. To fully understand how deductibles, copays, and out-of-pocket maximums interact, read our <a href="/articles/health-insurance-deductible-explained.html">health insurance deductible explainer</a>.'
      ),
      (
        "Don't forget: as a self-employed individual, you can deduct 100% of your health insurance premiums",
        'Don\'t forget: as a self-employed individual, you can deduct 100% of your health insurance premiums'
      ),
      (
        'Freelancers Union, the National Association for the Self-Employed (NASE), and various industry associations negotiate group rates',
        'Freelancers Union, the National Association for the Self-Employed (NASE), and various industry associations negotiate group rates'
      ),
    ],
  },
  {
    'slug': 'what-is-liability-insurance',
    'title': 'What Is Liability Insurance? Everything You Need to Know',
    'desc':  'Liability insurance pays for damages you cause to others. Learn how it works, the different types, how much you need, and why it\'s essential coverage.',
    'image': '/images/img-business.png',
    'date':  '2025-05-31',
    'crumb': 'What Is Liability Insurance?',
    'alt_old': 'alt="Business insurance guide"',
    'alt_new': 'alt="Liability insurance protection against financial loss from accidents and lawsuits"',
    'link_inserts': [
      # already has inline links; add renters insurance one
      (
        'Included in standard homeowners and renters policies, this covers you if someone is injured',
        'Included in standard <a href="/articles/what-does-homeowners-insurance-cover.html">homeowners</a> and <a href="/articles/renters-insurance-worth-it.html">renters policies</a>, this covers you if someone is injured'
      ),
    ],
  },
  {
    'slug': 'car-insurance-after-accident',
    'title': 'Car Insurance After an Accident: What to Expect and What to Do',
    'desc':  'Learn exactly what to do after a car accident, when to file a claim, how rates are affected, how long surcharges last, and how to recover faster.',
    'image': '/images/img-auto.png',
    'date':  '2025-05-25',
    'crumb': 'Car Insurance After an Accident',
    'alt_old': 'alt="Auto insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Car insurance after accident guide covering claims process and rate impacts" class="article-hero-img"',
    'link_inserts': [
      (
        'Raising your deductible from $500 to $1,000 lowers your premium and demonstrates financial responsibility.',
        'Raising your deductible from $500 to $1,000 lowers your premium and demonstrates financial responsibility. See our full guide to <a href="/articles/how-to-lower-car-insurance-premium.html">lowering your car insurance premium</a>.'
      ),
      (
        'Get quotes from at least 5–6 insurers, including regional carriers',
        'Get quotes from at least 5–6 insurers — learn <a href="/articles/how-to-compare-insurance-quotes.html">how to compare insurance quotes the right way</a> — including regional carriers'
      ),
      (
        'Even saying "I\'m sorry" can be interpreted as an admission of liability.',
        'Even saying "I\'m sorry" can be interpreted as an admission of liability. Read our complete guide on <a href="/articles/how-to-file-insurance-claim.html">how to file an insurance claim</a> for the full process after you notify your insurer.'
      ),
    ],
  },
  {
    'slug': 'health-insurance-deductible-explained',
    'title': 'Health Insurance Deductible Explained: Deductibles, Copays & More',
    'desc':  'Understand health insurance deductibles, copays, coinsurance, out-of-pocket maximums, HDHPs, and HSAs. Learn how to choose the right plan for your needs.',
    'image': '/images/img-health.png',
    'date':  '2025-05-24',
    'crumb': 'Health Insurance Deductible Explained',
    'alt_old': 'alt="Health insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Health insurance deductible copay and coinsurance explained with real examples" class="article-hero-img"',
    'link_inserts': [
      (
        'The right deductible depends on your health status, financial situation, and risk tolerance:',
        'The right deductible depends on your health status, financial situation, and risk tolerance. Self-employed individuals should also see our guide to <a href="/articles/best-health-insurance-for-self-employed.html">health insurance options for freelancers</a>.'
      ),
      (
        'Understanding these terms transforms you from a passive consumer into an informed one.',
        'Understanding these terms transforms you from a passive consumer into an informed one. Brush up on more vocabulary in our <a href="/articles/insurance-terms-glossary.html">complete insurance terms glossary</a>. Use the <a href="https://coveragefixpro.com/tools/auto/deductible-optimizer.html" target="_blank" rel="noopener">free deductible optimizer</a> to model how different deductible levels affect your annual costs.'
      ),
    ],
  },
  {
    'slug': 'how-much-life-insurance-do-i-need',
    'title': 'How Much Life Insurance Do I Need?',
    'desc':  'Learn how to calculate exactly how much life insurance you need using the DIME formula, income replacement rule, and human life value approach.',
    'image': '/images/img-life.png',
    'date':  '2025-05-26',
    'crumb': 'How Much Life Insurance Do I Need?',
    'alt_old': 'alt="Life insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Life insurance needs calculator showing DIME formula and income replacement method" class="article-hero-img"',
    'link_inserts': [
      (
        'The bottom line: for most Americans with dependents and a mortgage, a 20- or 30-year term policy',
        # this text is in term-life article, not here
        'placeholder_skip'
      ),
      (
        'Getting the right amount of life insurance is less about finding a perfect formula',
        'Getting the right amount of life insurance is less about finding a perfect formula. Compare your options in our guide on <a href="/articles/term-life-vs-whole-life-insurance.html">term life vs. whole life insurance</a>. Also consider <a href="/articles/disability-insurance-guide.html">disability insurance</a> — your income needs protection even when you\'re alive but unable to work.'
      ),
      (
        'Employer group life coverage disappears if you change jobs or are laid off',
        'Employer group life coverage disappears if you change jobs or are laid off'
      ),
    ],
  },
  {
    'slug': 'pet-insurance-worth-it',
    'title': 'Is Pet Insurance Worth It? A Honest Cost-Benefit Analysis',
    'desc':  'Is pet insurance worth the monthly cost? We break down what pet insurance covers, real cost scenarios, and how to decide if it makes sense for your pet.',
    'image': '/images/img-health.png',
    'date':  '2025-05-21',
    'crumb': 'Is Pet Insurance Worth It?',
    'alt_old': 'alt="Health insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Pet insurance cost-benefit analysis for dogs and cats with premium examples" class="article-hero-img"',
    'link_inserts': [
      (
        'Veterinary care has become remarkably sophisticated—and expensive.',
        'Veterinary care has become remarkably sophisticated—and expensive. Just as with <a href="/articles/how-to-file-insurance-claim.html">filing any insurance claim</a>, having complete records of your pet\'s medical history speeds up reimbursement significantly.'
      ),
      (
        'The best time to enroll is when your pet is young and healthy.',
        'The best time to enroll is when your pet is young and healthy. When shopping policies, apply the same principles from our guide on <a href="/articles/how-to-compare-insurance-quotes.html">how to compare insurance quotes</a> — look beyond the headline premium to deductibles, limits, and exclusions.'
      ),
    ],
  },
  {
    'slug': 'how-to-compare-insurance-quotes',
    'title': 'How to Compare Insurance Quotes: The Right Way to Shop for Coverage',
    'desc':  'Comparing insurance quotes takes more than price. Learn how to shop for the best value coverage by comparing limits, deductibles, exclusions, and insurer quality.',
    'image': '/images/img-business.png',
    'date':  '2025-05-18',
    'crumb': 'How to Compare Insurance Quotes',
    'alt_old': 'alt="Business insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Comparing multiple insurance quotes to find the best value coverage" class="article-hero-img"',
    'link_inserts': [
      (
        'When comparing auto insurance quotes',
        'When comparing <a href="/articles/how-much-car-insurance-do-i-need.html">auto insurance</a> quotes'
      ),
      (
        'When comparing homeowners insurance quotes',
        'When comparing <a href="/articles/what-does-homeowners-insurance-cover.html">homeowners insurance</a> quotes'
      ),
    ],
  },
  {
    'slug': 'how-to-file-insurance-claim',
    'title': 'How to File an Insurance Claim: Step-by-Step Guide',
    'desc':  'Learn how to file an insurance claim the right way. Step-by-step guide covering documentation, working with adjusters, and getting a fair settlement.',
    'image': '/images/img-auto.png',
    'date':  '2025-05-30',
    'crumb': 'How to File an Insurance Claim',
    'alt_old': 'alt="Auto insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Step-by-step guide for filing an insurance claim with documentation tips" class="article-hero-img"',
    'link_inserts': [
      (
        'After an auto accident',
        'After an auto accident — read our full guide on <a href="/articles/car-insurance-after-accident.html">car insurance after an accident</a> —'
      ),
      (
        'For homeowners claims',
        'For <a href="/articles/what-does-homeowners-insurance-cover.html">homeowners</a> claims'
      ),
    ],
  },
  {
    'slug': 'insurance-terms-glossary',
    'title': 'Insurance Terms Glossary: 60+ Terms Explained in Plain English',
    'desc':  'Plain-English definitions of 60+ insurance terms — from deductible and premium to subrogation and indemnity. The complete insurance glossary for consumers.',
    'image': '/images/img-business.png',
    'date':  '2025-05-17',
    'crumb': 'Insurance Terms Glossary',
    'alt_old': 'alt="Business insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Insurance terms glossary with over 60 key terms defined in plain English" class="article-hero-img"',
    'link_inserts': [
      (
        'Deductible</strong>',
        'Deductible</strong>'  # skip - just add via related block
      ),
    ],
  },
  {
    'slug': 'life-insurance-for-young-adults',
    'title': 'Life Insurance for Young Adults: Why Buy Now and How to Start',
    'desc':  'Life insurance is cheapest when you\'re young and healthy. Learn why young adults should buy now, how much to get, and how term vs whole life compares.',
    'image': '/images/img-life.png',
    'date':  '2025-05-29',
    'crumb': 'Life Insurance for Young Adults',
    'alt_old': 'alt="Life insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Young adult reviewing affordable life insurance options and term policy quotes" class="article-hero-img"',
    'link_inserts': [
      (
        'the difference between term and whole life insurance',
        'the difference between <a href="/articles/term-life-vs-whole-life-insurance.html">term and whole life insurance</a>'
      ),
      (
        'calculate how much life insurance you need',
        'calculate <a href="/articles/how-much-life-insurance-do-i-need.html">how much life insurance you need</a>'
      ),
    ],
  },
  {
    'slug': 'renters-insurance-worth-it',
    'title': 'Is Renters Insurance Worth It? (Yes — Here\'s Why)',
    'desc':  'Renters insurance costs just $15–30/month and covers far more than most tenants realize. Learn what it covers, common myths, and how to get a policy.',
    'image': '/images/img-home.png',
    'date':  '2025-05-28',
    'crumb': 'Is Renters Insurance Worth It?',
    'alt_old': 'alt="Home insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Renters insurance protecting apartment belongings from theft, fire, and liability" class="article-hero-img"',
    'link_inserts': [
      (
        'personal liability coverage',
        '<a href="/articles/what-is-liability-insurance.html">personal liability coverage</a>'
      ),
      (
        'the same insurer for a multi-policy discount',
        'the same insurer for a multi-policy discount. Learn more strategies in our guide to <a href="/articles/how-to-compare-insurance-quotes.html">comparing insurance quotes</a>.'
      ),
    ],
  },
  {
    'slug': 'business-insurance-types',
    'title': 'Types of Business Insurance: Complete Guide for Business Owners',
    'desc':  'General liability, E&O, BOP, workers comp, cyber — a complete guide to business insurance types, what each covers, and what your business needs.',
    'image': '/images/img-business.png',
    'date':  '2025-05-27',
    'crumb': 'Types of Business Insurance',
    'alt_old': 'alt="Business insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Business insurance types including general liability, E&O, BOP, and workers comp" class="article-hero-img"',
    'link_inserts': [
      (
        'General liability',
        '<a href="/articles/what-is-liability-insurance.html">General liability</a>'
      ),
      (
        'umbrella policy',
        '<a href="/articles/umbrella-insurance-explained.html">umbrella policy</a>'
      ),
    ],
  },
  {
    'slug': 'disability-insurance-guide',
    'title': 'Disability Insurance: The Complete Guide to Protecting Your Income',
    'desc':  'Your income is your most valuable asset. Learn how disability insurance works, short vs long-term coverage, own-occupation definitions, and how much you need.',
    'image': '/images/img-life.png',
    'date':  '2025-05-22',
    'crumb': 'Disability Insurance Guide',
    'alt_old': 'alt="Life insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Disability insurance protecting income for workers unable to work due to illness or injury" class="article-hero-img"',
    'link_inserts': [
      (
        'life insurance',
        '<a href="/articles/term-life-vs-whole-life-insurance.html">life insurance</a>'
      ),
      (
        'how much coverage you need',
        '<a href="/articles/how-much-life-insurance-do-i-need.html">how much coverage you need</a>'
      ),
    ],
  },
  {
    'slug': 'flood-insurance-vs-homeowners',
    'title': 'Flood Insurance vs. Homeowners Insurance: Key Differences Explained',
    'desc':  'Standard homeowners insurance doesn\'t cover floods. Learn the critical difference, how NFIP flood insurance works, and whether you need separate flood coverage.',
    'image': '/images/img-home.png',
    'date':  '2025-05-19',
    'crumb': 'Flood Insurance vs. Homeowners Insurance',
    'alt_old': 'alt="Home insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Flood damage comparison showing what homeowners insurance covers versus NFIP flood insurance" class="article-hero-img"',
    'link_inserts': [
      (
        'standard homeowners insurance',
        '<a href="/articles/what-does-homeowners-insurance-cover.html">standard homeowners insurance</a>'
      ),
      (
        'how to file a flood insurance claim',
        '<a href="/articles/how-to-file-insurance-claim.html">how to file a flood insurance claim</a>'
      ),
    ],
  },
  {
    'slug': 'travel-insurance-guide',
    'title': 'Travel Insurance: Complete Guide to Coverage, Costs & When to Buy',
    'desc':  'Learn what travel insurance covers, what it costs, when it\'s worth buying, and how to choose the right policy for your trip. Complete 2025 guide.',
    'image': '/images/img-hero.png',
    'date':  '2025-05-20',
    'crumb': 'Travel Insurance Guide',
    'alt_old': 'alt="Insurance professional with documents" class="article-hero-img"',
    'alt_new': 'alt="Travel insurance guide covering trip cancellation, medical emergencies, and baggage loss" class="article-hero-img"',
    'link_inserts': [
      (
        'insurance terms',
        '<a href="/articles/insurance-terms-glossary.html">insurance terms</a>'
      ),
      (
        'compare quotes',
        '<a href="/articles/how-to-compare-insurance-quotes.html">compare quotes</a>'
      ),
    ],
  },
  {
    'slug': 'umbrella-insurance-explained',
    'title': 'Umbrella Insurance Explained: Extra Protection for Everything',
    'desc':  'Umbrella insurance adds $1M+ of extra liability coverage for just $150–300/year. Learn how it works, what it covers, and who needs it most.',
    'image': '/images/img-business.png',
    'date':  '2025-05-23',
    'crumb': 'Umbrella Insurance Explained',
    'alt_old': 'alt="Business insurance guide" class="article-hero-img"',
    'alt_new': 'alt="Umbrella insurance policy providing extra liability protection above auto and home limits" class="article-hero-img"',
    'link_inserts': [
      (
        'auto liability',
        '<a href="/articles/how-much-car-insurance-do-i-need.html">auto liability</a>'
      ),
      (
        'homeowners liability',
        '<a href="/articles/what-does-homeowners-insurance-cover.html">homeowners liability</a>'
      ),
      (
        'personal liability',
        '<a href="/articles/what-is-liability-insurance.html">personal liability</a>'
      ),
    ],
  },
]

# ─── Index ItemList entries ────────────────────────────────────────────────────
INDEX_ITEMS = [
    {'name': a['title'], 'url': f"{BASE}/articles/{a['slug']}.html"}
    for a in ARTICLES
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def og_block(og_type, title, desc, url, image):
    return (
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{BASE}{image}">\n'
        f'<meta property="og:site_name" content="{PUB_NAME}">\n'
    )


def article_schema(title, desc, url, image_url, date):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "image": image_url,
        "datePublished": date,
        "dateModified": date,
        "author": {
            "@type": "Organization",
            "name": AUTHOR
        },
        "publisher": {
            "@type": "Organization",
            "name": PUB_NAME,
            "logo": {
                "@type": "ImageObject",
                "url": LOGO_URL
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def breadcrumb_schema(article_title, article_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": article_title, "item": article_url}
        ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def website_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": PUB_NAME,
        "url": f"{BASE}/",
        "description": "Plain-English insurance guides reviewed by licensed professionals. Auto, life, health, home, and business insurance explained clearly.",
        "publisher": {
            "@type": "Organization",
            "name": PUB_NAME,
            "logo": {"@type": "ImageObject", "url": LOGO_URL}
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def itemlist_schema(items):
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Insurance Guides by InsuranceTipsPro",
        "description": "Expert insurance guides covering auto, life, health, home, and business insurance.",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": item['name'], "url": item['url']}
            for i, item in enumerate(items)
        ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def process_article(art):
    slug      = art['slug']
    fp        = os.path.join(ARTS_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        print(f'  SKIP (not found): {slug}.html')
        return

    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    orig = c

    # 1. OG tags — insert after <link rel="canonical" ...>
    if 'property="og:type"' not in c:
        canonical_url = f'{BASE}/articles/{slug}.html'
        og = og_block('article', art['title'], art['desc'], canonical_url, art['image'])
        # Insert after the canonical link tag
        c = re.sub(
            r'(<link rel="canonical"[^>]+>)',
            r'\1\n' + og.rstrip(),
            c, count=1
        )

    # 2. JSON-LD schemas — insert before </head>
    if 'application/ld+json' not in c:
        canonical_url = f'{BASE}/articles/{slug}.html'
        image_url     = f'{BASE}{art["image"]}'
        art_ld  = article_schema(art['title'], art['desc'], canonical_url, image_url, art['date'])
        crumb_ld = breadcrumb_schema(art['crumb'], canonical_url)
        insertion = f'\n{art_ld}\n{crumb_ld}\n'
        c = c.replace('</head>', insertion + '</head>', 1)

    # 3. Image alt text fix
    if art.get('alt_old') and art['alt_old'] in c:
        c = c.replace(art['alt_old'], art['alt_new'], 1)

    # 4. Inline link inserts
    for old_text, new_text in art.get('link_inserts', []):
        if new_text == 'placeholder_skip':
            continue
        if old_text in c and new_text not in c:
            c = c.replace(old_text, new_text, 1)

    if c != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'  OK: {slug}.html')
    else:
        print(f'  UNCHANGED: {slug}.html')


def process_index():
    fp = os.path.join(ROOT, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    orig = c

    # 1. OG tags
    if 'property="og:type"' not in c:
        desc = 'Plain-English insurance guides reviewed by licensed professionals. Auto, life, health, home, and business insurance explained clearly.'
        og = og_block('website', 'InsuranceTipsPro – Expert Insurance Guides', desc, f'{BASE}/', '/images/img-hero.png')
        c = re.sub(r'(<link rel="canonical"[^>]+>)', r'\1\n' + og.rstrip(), c, count=1)

    # 2. WebSite + ItemList JSON-LD
    if 'application/ld+json' not in c:
        ws_ld   = website_schema()
        il_ld   = itemlist_schema(INDEX_ITEMS)
        c = c.replace('</head>', f'\n{ws_ld}\n{il_ld}\n</head>', 1)

    if c != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print('  OK: index.html')
    else:
        print('  UNCHANGED: index.html')


def main():
    print('SEO Overhaul — InsuranceTipsPro\n')
    for art in ARTICLES:
        process_article(art)
    process_index()
    print('\nDone.')


if __name__ == '__main__':
    main()
