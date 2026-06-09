import os
import re

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'articles')
MARKER = '<!-- IMPROVE-2025 -->'

ARTICLE_DATA = {
    'how-much-car-insurance-do-i-need.html': {
        'img_keywords': 'car,driving,road',
        'img_alt': 'How much car insurance do I need',
        'takeaways': [
            'State minimums are often dangerously low — most drivers need 100/300/100 liability or higher.',
            'Collision and comprehensive coverage are worth it if your car is worth more than $4,000.',
            'Uninsured/underinsured motorist coverage protects you when the at-fault driver has no insurance.',
            'Your net worth determines how much liability coverage you actually need.',
            'Dropping coverage on older cars saves money only once the annual cost exceeds 10% of the car\'s value.',
        ]
    },
    'term-life-vs-whole-life-insurance.html': {
        'img_keywords': 'family,protection,future',
        'img_alt': 'Term life vs whole life insurance',
        'takeaways': [
            'Term life is 5–15x cheaper than whole life for the same death benefit.',
            'Most people need life insurance for 20–30 years — term coverage aligns with that window.',
            'Whole life\'s cash value grows slowly and the returns rarely beat a simple index fund.',
            'Buy term and invest the difference is the right strategy for most working families.',
            'If you need coverage beyond age 70 (e.g., estate planning), whole life may make sense.',
        ]
    },
    'what-does-homeowners-insurance-cover.html': {
        'img_keywords': 'house,home,neighborhood',
        'img_alt': 'What homeowners insurance covers',
        'takeaways': [
            'Standard policies cover your dwelling, personal property, liability, and additional living expenses.',
            'Floods and earthquakes are NOT covered — you need separate policies for both.',
            'Replacement cost coverage pays to rebuild at today\'s prices; actual cash value deducts depreciation.',
            'Personal liability covers lawsuits if someone is injured on your property.',
            'Keep a home inventory — it\'s the most important thing you can do to speed up a claim.',
        ]
    },
    'how-to-lower-car-insurance-premium.html': {
        'img_keywords': 'savings,money,piggybank',
        'img_alt': 'How to lower car insurance premium',
        'takeaways': [
            'Bundling auto and home insurance typically saves 10–25% on both policies.',
            'Raising your deductible from $500 to $1,000 can cut your premium by 15–30%.',
            'Good driver discounts can save 10–40% if you have a clean record for 3+ years.',
            'Shopping quotes every 6–12 months is the single fastest way to find savings.',
            'Usage-based programs can cut premiums up to 30% for low-mileage or careful drivers.',
        ]
    },
    'best-health-insurance-for-self-employed.html': {
        'img_keywords': 'health,medical,wellness',
        'img_alt': 'Best health insurance for self-employed',
        'takeaways': [
            'ACA marketplace plans offer subsidies if your income falls between 100–400% of the federal poverty level.',
            'HDHPs paired with an HSA let you save pre-tax money for medical expenses.',
            'Freelancer associations and professional groups sometimes offer group rate access.',
            'COBRA is an option after leaving a job, but it\'s typically the most expensive choice.',
            'Deducting 100% of your health insurance premiums as a self-employed person reduces your tax bill.',
        ]
    },
    'what-is-liability-insurance.html': {
        'img_keywords': 'business,handshake,legal',
        'img_alt': 'What is liability insurance',
        'takeaways': [
            'Liability insurance pays for damage or injury you cause to others — not to yourself.',
            'It appears in auto, home, business, and umbrella policies in different forms.',
            'General liability is the foundation of any business\'s insurance program.',
            'Professional liability (E&O) covers claims arising from mistakes in your work or advice.',
            'If your assets exceed your liability limits, you\'re personally exposed to lawsuits.',
        ]
    },
    'how-to-file-insurance-claim.html': {
        'img_keywords': 'paperwork,documents,form',
        'img_alt': 'How to file an insurance claim',
        'takeaways': [
            'Document everything immediately: photos, police reports, witness information.',
            'File your claim as soon as possible — most policies have a reporting deadline.',
            'Never admit fault at an accident scene before speaking with your insurer.',
            'Keep a written log of every call, email, and interaction with the claims adjuster.',
            'You can dispute a settlement offer — an independent appraiser or public adjuster can help.',
        ]
    },
    'life-insurance-for-young-adults.html': {
        'img_keywords': 'young,couple,lifestyle',
        'img_alt': 'Life insurance for young adults',
        'takeaways': [
            'Locking in a term policy in your 20s can cost as little as $15–$25/month for $500K coverage.',
            'Rates are based on age and health — every year you wait, premiums increase.',
            'You need life insurance if anyone financially depends on you or you have co-signed debts.',
            'A 20- or 30-year term policy covers most of your working and child-rearing years.',
            'Even if single and childless, life insurance can cover student loans or help aging parents.',
        ]
    },
    'renters-insurance-worth-it.html': {
        'img_keywords': 'apartment,living,home',
        'img_alt': 'Is renters insurance worth it',
        'takeaways': [
            'Renters insurance costs $15–$30/month and covers personal property, liability, and temporary housing.',
            'Your landlord\'s policy covers the building only — not a single item you own inside.',
            'Personal liability coverage protects you if a guest is injured in your rental.',
            'Off-premises coverage means your laptop is covered if stolen from a coffee shop.',
            'At under $20/month, renters insurance is one of the best-value insurance products available.',
        ]
    },
    'business-insurance-types.html': {
        'img_keywords': 'office,business,professional',
        'img_alt': 'Types of business insurance',
        'takeaways': [
            'A Business Owner\'s Policy (BOP) bundles general liability and property coverage at a discount.',
            'Professional liability (E&O) is essential for consultants, designers, and service providers.',
            'Workers\' compensation is legally required in most states as soon as you hire your first employee.',
            'Cyber liability insurance is increasingly critical as data breaches target small businesses.',
            'Commercial umbrella policies provide an extra layer of liability protection above your base policies.',
        ]
    },
    'how-much-life-insurance-do-i-need.html': {
        'img_keywords': 'family,children,home',
        'img_alt': 'How much life insurance do I need',
        'takeaways': [
            'The DIME formula (Debt + Income + Mortgage + Education) gives a solid starting estimate.',
            'Most experts recommend 10–12x your annual income as a coverage baseline.',
            'Replace income for the years your family would need financial support — usually until kids are grown.',
            'Include mortgage payoff in your coverage amount so your family keeps the house.',
            'Review your coverage after major life events: marriage, children, home purchase, divorce.',
        ]
    },
    'car-insurance-after-accident.html': {
        'img_keywords': 'car,accident,repair',
        'img_alt': 'Car insurance after an accident',
        'takeaways': [
            'At-fault accidents can raise your premium by 20–50% at renewal.',
            'Accident forgiveness programs (if you have one) waive the first rate increase.',
            'Not-at-fault accidents may still raise your rates in some states.',
            'Switching insurers after an accident doesn\'t erase it — it follows you via your driving record.',
            'Ask about diminishing deductible programs that reward claim-free years.',
        ]
    },
    'health-insurance-deductible-explained.html': {
        'img_keywords': 'health,insurance,doctor',
        'img_alt': 'Health insurance deductible explained',
        'takeaways': [
            'Your deductible is what you pay out of pocket before insurance starts covering costs.',
            'Copays and coinsurance still apply after you meet your deductible, until you hit the out-of-pocket max.',
            'HDHPs have higher deductibles but qualify you for a tax-advantaged Health Savings Account (HSA).',
            'The out-of-pocket maximum caps your total annual exposure — no matter how much care you need.',
            'Low-deductible plans cost more in premiums but are better if you expect high medical expenses.',
        ]
    },
    'umbrella-insurance-explained.html': {
        'img_keywords': 'umbrella,protection,rain',
        'img_alt': 'Umbrella insurance explained',
        'takeaways': [
            'Umbrella insurance kicks in after your auto or home liability limits are exhausted.',
            'A $1 million umbrella policy typically costs just $150–$300 per year.',
            'It also covers incidents your underlying policies might exclude, like libel or slander claims.',
            'Required by most lenders if you\'re renting out property or have significant assets to protect.',
            'You generally need at least $300K in auto liability before qualifying for an umbrella policy.',
        ]
    },
    'disability-insurance-guide.html': {
        'img_keywords': 'work,professional,income',
        'img_alt': 'Disability insurance guide',
        'takeaways': [
            'Your income is your most valuable asset — disability insurance replaces 60–70% of it if you can\'t work.',
            'Social Security disability is hard to qualify for and pays far less than most people expect.',
            'Short-term disability covers 3–6 months; long-term disability can cover you to retirement age.',
            'Own-occupation policies pay if you can\'t do YOUR specific job — not just any job.',
            'Buy disability insurance while you\'re healthy — pre-existing conditions can trigger exclusions.',
        ]
    },
    'pet-insurance-worth-it.html': {
        'img_keywords': 'dog,pet,veterinarian',
        'img_alt': 'Is pet insurance worth it',
        'takeaways': [
            'Emergency vet bills can run $3,000–$10,000+ — pet insurance protects against catastrophic costs.',
            'Premiums average $30–$50/month for dogs and $15–$25/month for cats.',
            'Pre-existing conditions are excluded, so buy while your pet is young and healthy.',
            'Accident-and-illness plans offer the best value versus accident-only plans.',
            'Compare reimbursement rates, annual limits, and deductible structures before choosing.',
        ]
    },
    'travel-insurance-guide.html': {
        'img_keywords': 'travel,airplane,vacation',
        'img_alt': 'Travel insurance guide',
        'takeaways': [
            'Cancel For Any Reason (CFAR) coverage is the most flexible but adds 40–50% to the cost.',
            'Travel medical insurance is essential when traveling internationally — your US health plan rarely covers you abroad.',
            'Trip cancellation insurance reimburses non-refundable trip costs if you cancel for a covered reason.',
            'Emergency evacuation coverage can be worth more than everything else combined if you need it.',
            'Credit cards often include limited travel insurance — check before buying a separate policy.',
        ]
    },
    'flood-insurance-vs-homeowners.html': {
        'img_keywords': 'flood,water,storm',
        'img_alt': 'Flood insurance vs homeowners insurance',
        'takeaways': [
            'Standard homeowners insurance never covers flood damage — it requires a separate policy.',
            'The National Flood Insurance Program (NFIP) offers federally-backed flood coverage up to $250K for the structure.',
            'Even 1 inch of water can cause $25,000+ in damage — flood risk extends well beyond 100-year floodplains.',
            'Private flood insurance often offers higher limits and broader coverage than the NFIP.',
            'Flood policies typically have a 30-day waiting period — don\'t wait until a storm is coming.',
        ]
    },
    'how-to-compare-insurance-quotes.html': {
        'img_keywords': 'comparison,laptop,research',
        'img_alt': 'How to compare insurance quotes',
        'takeaways': [
            'Get at least 3 quotes to ensure you\'re seeing competitive pricing across the market.',
            'Compare identical coverage levels — a lower price means nothing if the limits are also lower.',
            'Check insurer financial strength ratings (AM Best A or better) before buying.',
            'Read customer reviews specifically about the claims process, not just general satisfaction.',
            'Ask about every available discount upfront — many are not automatically applied.',
        ]
    },
    'insurance-terms-glossary.html': {
        'img_keywords': 'books,education,reading',
        'img_alt': 'Insurance terms glossary',
        'takeaways': [
            'Your premium is what you pay; your deductible is what you owe before coverage kicks in.',
            'Actual Cash Value (ACV) factors in depreciation; Replacement Cost Value (RCV) does not.',
            'Subrogation lets your insurer recover money from the at-fault party after paying your claim.',
            'Riders and endorsements customize your base policy — they can add or exclude specific coverage.',
            'Understanding your Declarations Page (Dec Page) is the fastest way to know what you\'re covered for.',
        ]
    },
}

UNSPLASH_TEMPLATE = 'https://source.unsplash.com/720x300/?{keywords}'

BACK_TO_TOP_JS = '''<button id="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">&#8679;</button>
<script>window.addEventListener('scroll',function(){document.getElementById('back-to-top').classList.toggle('visible',window.scrollY>300);});</script>'''


def build_hero_img(keywords, alt):
    url = UNSPLASH_TEMPLATE.format(keywords=keywords)
    return f'<img src="{url}" alt="{alt}" class="article-hero-img" loading="lazy">\n'


def build_key_takeaways(points):
    items = '\n'.join(f'      <li>{p}</li>' for p in points)
    return (
        '<div class="key-takeaways">\n'
        '  <h4>Key Takeaways</h4>\n'
        '  <ul>\n'
        f'{items}\n'
        '  </ul>\n'
        '</div>\n'
    )


def process_file(filepath, filename, data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print(f'  SKIP (already done): {filename}')
        return False

    hero_img = build_hero_img(data['img_keywords'], data['img_alt'])
    takeaways = build_key_takeaways(data['takeaways'])

    # Insert hero image after </div> closing article-header, before <div class="author-box">
    hero_target = '<div class="author-box">'
    if hero_target in content:
        content = content.replace(hero_target, hero_img + hero_target, 1)
    else:
        print(f'  WARNING: author-box not found in {filename}')

    # Insert key takeaways before <div class="toc">
    toc_target = '<div class="toc">'
    if toc_target in content:
        content = content.replace(toc_target, takeaways + toc_target, 1)
    else:
        print(f'  WARNING: toc not found in {filename}')

    # Add back-to-top before </body>
    content = content.replace('</body>', BACK_TO_TOP_JS + '\n</body>', 1)

    # Add marker in <head>
    content = content.replace('<!-- REDESIGN-2025 -->', '<!-- REDESIGN-2025 -->\n<!-- IMPROVE-2025 -->', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'  OK: {filename}')
    return True


def main():
    modified = 0
    skipped = 0
    for filename, data in ARTICLE_DATA.items():
        filepath = os.path.join(ARTICLES_DIR, filename)
        if not os.path.exists(filepath):
            print(f'  MISSING: {filename}')
            continue
        result = process_file(filepath, filename, data)
        if result:
            modified += 1
        else:
            skipped += 1

    print(f'\nDone: {modified} modified, {skipped} skipped.')


if __name__ == '__main__':
    main()
