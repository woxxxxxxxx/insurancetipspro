'use strict';
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

// ─── Config ───────────────────────────────────────────────────────────────────
const BASE_DIR = __dirname;
const TOPICS_FILE  = path.join(BASE_DIR, 'topics-used.json');
const INDEX_FILE   = path.join(BASE_DIR, 'index.html');
const SITEMAP_FILE = path.join(BASE_DIR, 'sitemap.xml');
const ARTICLES_DIR = path.join(BASE_DIR, 'articles');
const IMAGES_DIR   = path.join(BASE_DIR, 'images');

const DOMAIN     = 'https://insurancetipspro.com';
const SITE_NAME  = 'InsuranceTipsPro';
const GA_ID      = 'G-DQ4ZT8RD2R';
const ADSENSE    = 'ca-pub-1638874323475457';

// Read API key from env, .env file, or credentials file
function getApiKey() {
  if (process.env.ANTHROPIC_API_KEY) return process.env.ANTHROPIC_API_KEY;
  const envFile = path.join(BASE_DIR, '.env');
  if (fs.existsSync(envFile)) {
    const line = fs.readFileSync(envFile, 'utf8').split('\n')
      .find(l => l.startsWith('ANTHROPIC_API_KEY='));
    if (line) return line.split('=')[1].trim();
  }
  // Fall back to Claude Code OAuth token
  const creds = path.join(process.env.USERPROFILE || 'C:\\Users\\Administrator', '.claude', '.credentials.json');
  if (fs.existsSync(creds)) {
    const c = JSON.parse(fs.readFileSync(creds, 'utf8'));
    if (c.claudeAiOauth && c.claudeAiOauth.accessToken) return c.claudeAiOauth.accessToken;
  }
  throw new Error('No ANTHROPIC_API_KEY found. Set it in environment or .env file.');
}

const UNSPLASH_KEY = '5RQkzb688Ez9nXR-vzUbkXmxFaxQbLzEQUoyy8rogt4';

// Candidate topics — extend freely
const TOPIC_CANDIDATES = [
  { title: 'How to Read Your Insurance Policy',          slug: 'how-to-read-insurance-policy',          category: 'Fundamentals',    keyword: 'insurance policy document reading' },
  { title: 'What Is a Deductible in Insurance?',         slug: 'what-is-a-deductible-in-insurance',     category: 'Fundamentals',    keyword: 'insurance deductible explained' },
  { title: 'Types of Car Insurance Coverage Explained',  slug: 'types-of-car-insurance-coverage',       category: 'Auto Insurance',  keyword: 'car insurance coverage types' },
  { title: 'Medicare vs. Private Health Insurance',       slug: 'medicare-vs-private-health-insurance',  category: 'Health Insurance', keyword: 'medicare health insurance comparison' },
  { title: 'Homeowners Insurance vs. Home Warranty',     slug: 'homeowners-insurance-vs-home-warranty', category: 'Home Insurance',  keyword: 'home warranty vs insurance' },
  { title: 'Gap Insurance: What It Is and When You Need It', slug: 'gap-insurance-explained',           category: 'Auto Insurance',  keyword: 'gap insurance car loan' },
  { title: 'Life Insurance for Parents: Protecting Your Family', slug: 'life-insurance-for-parents',   category: 'Life Insurance',  keyword: 'family life insurance protection' },
  { title: 'Motorcycle Insurance: Coverage Options and Costs', slug: 'motorcycle-insurance-guide',     category: 'Auto Insurance',  keyword: 'motorcycle insurance coverage' },
  { title: 'Long-Term Care Insurance Explained',         slug: 'long-term-care-insurance-explained',    category: 'Specialty',       keyword: 'long term care insurance elderly' },
  { title: 'Cyber Insurance for Small Businesses',       slug: 'cyber-insurance-small-business',        category: 'Business',        keyword: 'cyber insurance business protection' },
  { title: 'How Insurance Premiums Are Calculated',      slug: 'how-insurance-premiums-are-calculated', category: 'Fundamentals',    keyword: 'insurance premium factors calculation' },
  { title: 'Boat and Watercraft Insurance Guide',        slug: 'boat-watercraft-insurance-guide',       category: 'Specialty',       keyword: 'boat insurance watercraft' },
  { title: 'SR-22 Insurance: What It Is and Who Needs It', slug: 'sr22-insurance-explained',           category: 'Auto Insurance',  keyword: 'sr22 insurance requirement' },
  { title: 'Renters vs. Homeowners Insurance: Key Differences', slug: 'renters-vs-homeowners-insurance', category: 'Home Insurance', keyword: 'renters vs homeowners insurance' },
  { title: 'How to Lower Your Homeowners Insurance Premium', slug: 'lower-homeowners-insurance-premium', category: 'Home Insurance', keyword: 'lower home insurance cost' },
  { title: 'Earthquake Insurance: What You Need to Know',    slug: 'earthquake-insurance-guide',         category: 'Home Insurance',  keyword: 'earthquake insurance coverage guide' },
  { title: 'Dental Insurance Explained: Plans and Coverage', slug: 'dental-insurance-explained',         category: 'Health Insurance', keyword: 'dental insurance plans explained' },
  { title: 'Vision Insurance Guide: Coverage and Costs',     slug: 'vision-insurance-guide',             category: 'Health Insurance', keyword: 'vision insurance coverage costs' },
  { title: 'Workers Compensation Insurance Guide',           slug: 'workers-compensation-guide',         category: 'Business',        keyword: 'workers compensation insurance' },
  { title: 'Professional Liability Insurance Explained',     slug: 'professional-liability-insurance',   category: 'Business',        keyword: 'professional liability insurance' },
  { title: 'Commercial Auto Insurance: A Complete Guide',    slug: 'commercial-auto-insurance',          category: 'Business',        keyword: 'commercial auto insurance coverage' },
  { title: 'Key Person Life Insurance for Businesses',       slug: 'key-person-life-insurance',          category: 'Business',        keyword: 'key person life insurance business' },
  { title: 'Supplemental Health Insurance: Do You Need It?', slug: 'supplemental-health-insurance',      category: 'Health Insurance', keyword: 'supplemental health insurance plans' },
  { title: 'Critical Illness Insurance: Is It Worth It?',    slug: 'critical-illness-insurance',         category: 'Health Insurance', keyword: 'critical illness insurance coverage' },
  { title: 'Accidental Death Insurance Explained',           slug: 'accidental-death-insurance',         category: 'Life Insurance',  keyword: 'accidental death insurance policy' },
  { title: 'Condo Insurance: What Your HOA Doesn\'t Cover',  slug: 'condo-insurance-guide',              category: 'Home Insurance',  keyword: 'condo insurance coverage guide' },
  { title: 'Landlord Insurance: Protecting Your Rental',     slug: 'landlord-insurance-guide',           category: 'Home Insurance',  keyword: 'landlord insurance rental property' },
  { title: 'Wedding Insurance: Protecting Your Big Day',     slug: 'wedding-insurance-guide',            category: 'Specialty',       keyword: 'wedding insurance coverage' },
  { title: 'Identity Theft Insurance: What It Covers',       slug: 'identity-theft-insurance',           category: 'Specialty',       keyword: 'identity theft insurance protection' },
  { title: 'Mobile Home Insurance Guide',                    slug: 'mobile-home-insurance',              category: 'Home Insurance',  keyword: 'mobile home insurance coverage' },
  { title: 'Excess Liability Insurance Explained',           slug: 'excess-liability-insurance',         category: 'Specialty',       keyword: 'excess liability umbrella insurance' },
  { title: 'Errors and Omissions Insurance Guide',           slug: 'errors-omissions-insurance',         category: 'Business',        keyword: 'errors omissions insurance E&O' },
  { title: 'Directors and Officers Insurance Explained',     slug: 'directors-officers-insurance',       category: 'Business',        keyword: 'directors officers D&O insurance' },
  { title: 'Commercial Property Insurance Guide',            slug: 'commercial-property-insurance',      category: 'Business',        keyword: 'commercial property insurance coverage' },
  { title: 'Builders Risk Insurance: Construction Coverage', slug: 'builders-risk-insurance',            category: 'Business',        keyword: 'builders risk insurance construction' },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────
function loadTopicsUsed() {
  if (!fs.existsSync(TOPICS_FILE)) return { used: [] };
  return JSON.parse(fs.readFileSync(TOPICS_FILE, 'utf8'));
}

function saveTopicsUsed(data) {
  fs.writeFileSync(TOPICS_FILE, JSON.stringify(data, null, 2));
}

function pickTopic(usedSlugs) {
  const available = TOPIC_CANDIDATES.filter(t => !usedSlugs.includes(t.slug));
  if (!available.length) throw new Error('All topics used! Add more to TOPIC_CANDIDATES.');
  return available[0];
}

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function todayDisplay() {
  return new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

function httpsGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const opts = new URL(url);
    const req = https.get({
      hostname: opts.hostname,
      path: opts.pathname + opts.search,
      headers: { 'User-Agent': 'InsuranceTipsPro-AutoPublish/1.0', ...headers },
    }, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, body: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Request timeout')); });
  });
}

async function fetchUnsplashImage(topic, slug) {
  const query = encodeURIComponent(topic.keyword || topic.title);
  const url = `https://api.unsplash.com/search/photos?query=${query}&per_page=3&orientation=landscape&client_id=${UNSPLASH_KEY}`;
  console.log('  Searching Unsplash for:', topic.keyword);

  const resp = await httpsGet(url);
  if (resp.status !== 200) {
    console.warn('  Unsplash API error:', resp.status);
    return null;
  }
  const data = JSON.parse(resp.body.toString());
  if (!data.results || !data.results.length) {
    console.warn('  No Unsplash images found for query:', topic.keyword);
    return null;
  }

  const photo = data.results[0];
  const imgUrl = photo.urls.regular;
  const photographer = photo.user.name;
  const photographerUrl = photo.user.links.html;

  // Download image
  const imgFilename = `img-${slug}.jpg`;
  const imgPath = path.join(IMAGES_DIR, imgFilename);
  console.log('  Downloading image from Unsplash...');
  const imgResp = await httpsGet(imgUrl);
  if (imgResp.status !== 200) {
    console.warn('  Image download failed:', imgResp.status);
    return null;
  }
  fs.writeFileSync(imgPath, imgResp.body);
  console.log('  Saved:', imgFilename);

  // Trigger Unsplash download tracking (required by their API guidelines)
  const trackUrl = photo.links.download_location + `?client_id=${UNSPLASH_KEY}`;
  httpsGet(trackUrl).catch(() => {});

  return { filename: imgFilename, photographer, photographerUrl };
}

// ─── Article Generation ───────────────────────────────────────────────────────
async function generateArticle(topic, imageFilename, today) {
  const prompt = `You are an expert insurance writer for InsuranceTipsPro.com. Write a comprehensive, SEO-optimized insurance article following the EXACT JSON structure below.

Topic: "${topic.title}"
Category: ${topic.category}
Target audience: US consumers, plain English, actionable advice
Date: ${today}
Image: /images/${imageFilename}

Return ONLY valid JSON (no markdown, no backticks) matching this schema exactly:
{
  "title": "Full article title (60-70 chars, include target keyword)",
  "metaDescription": "150-160 char meta description with keyword",
  "excerpt": "2 sentences for index page listing",
  "readTime": "X min read (integer only, 7-12 typical)",
  "keyTakeaways": ["5 bullet strings, each starting with a verb or noun phrase"],
  "tocItems": [
    { "id": "section-id", "label": "Section Title" }
  ],
  "intro": "Opening paragraph (80-120 words). Hook, state the problem, promise the solution.",
  "sections": [
    {
      "id": "section-id",
      "h2": "Section Heading",
      "content": "HTML content for this section. Use <p>, <ul><li>, <ol><li>, <h3>, <strong>. Add a <div class=\\"callout\\"><strong>Pro Tip:</strong> ...</div> in at least one section. Minimum 150 words per section."
    }
  ],
  "faqs": [
    { "question": "FAQ question?", "answer": "1-3 sentence answer." }
  ],
  "relatedArticles": [
    { "href": "/articles/slug.html", "title": "Article Title" }
  ],
  "imageAlt": "Descriptive alt text for the hero image, 8-12 words"
}

Requirements:
- 6-8 sections minimum
- 5 FAQs
- 5 related articles chosen from this list:
  /articles/how-much-car-insurance-do-i-need.html
  /articles/term-life-vs-whole-life-insurance.html
  /articles/what-does-homeowners-insurance-cover.html
  /articles/how-to-lower-car-insurance-premium.html
  /articles/best-health-insurance-for-self-employed.html
  /articles/what-is-liability-insurance.html
  /articles/how-to-file-insurance-claim.html
  /articles/life-insurance-for-young-adults.html
  /articles/renters-insurance-worth-it.html
  /articles/business-insurance-types.html
  /articles/how-much-life-insurance-do-i-need.html
  /articles/car-insurance-after-accident.html
  /articles/health-insurance-deductible-explained.html
  /articles/umbrella-insurance-explained.html
  /articles/disability-insurance-guide.html
  /articles/pet-insurance-worth-it.html
  /articles/travel-insurance-guide.html
  /articles/flood-insurance-vs-homeowners.html
  /articles/how-to-compare-insurance-quotes.html
  /articles/insurance-terms-glossary.html
- Include at least one link to https://coveragefixpro.com or a specific tool page there inside the article body
- Return ONLY the JSON object, no other text`;

  // Use claude CLI (already authenticated via Claude Code session)
  console.log('  Calling claude CLI...');

  return new Promise((resolve, reject) => {
    const { spawn } = require('child_process');
    const proc = spawn(
      'claude',
      [
        '-p', prompt,
        '--model', 'claude-sonnet-4-6',
        '--dangerously-skip-permissions',
        '--disallowed-tools', 'Bash,Edit,Write,Read,Glob,Grep,Agent,WebSearch,WebFetch',
        '--system-prompt', 'You are a JSON content generator for an insurance website. Return ONLY valid JSON. Never use tools, never create files, never run shell commands, never commit to git.',
      ],
      { cwd: BASE_DIR }
    );

    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', d => { stdout += d.toString(); });
    proc.stderr.on('data', d => { stderr += d.toString(); });

    proc.on('close', code => {
      if (code !== 0) {
        return reject(new Error('claude CLI failed (code ' + code + '): ' + stderr.slice(0, 400)));
      }
      const raw = stdout.trim();
      if (!raw) return reject(new Error('claude CLI returned empty output. stderr: ' + stderr.slice(0, 200)));

      // Strip markdown code fences if present
      const stripped = raw.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '').trim();
      try {
        resolve(JSON.parse(stripped));
      } catch (e) {
        const match = raw.match(/\{[\s\S]*\}/);
        if (match) {
          try { return resolve(JSON.parse(match[0])); } catch (e2) {}
        }
        reject(new Error('Failed to parse JSON: ' + e.message + '\nOutput start: ' + raw.slice(0, 400)));
      }
    });

    proc.on('error', err => reject(new Error('spawn error: ' + err.message)));

    // Timeout fallback (article generation can take 3-8 min for a full piece)
    const timer = setTimeout(() => {
      proc.kill();
      reject(new Error('claude CLI timed out after 600s'));
    }, 600000);
    proc.on('close', () => clearTimeout(timer));
  });
}

// ─── HTML Builder ─────────────────────────────────────────────────────────────
function buildArticleHTML(topic, article, imageFilename, photographer, photographerUrl, slug, today, todayFmt) {
  const canonicalUrl = `${DOMAIN}/articles/${slug}.html`;
  const imageUrl = `${DOMAIN}/images/${imageFilename}`;

  const tocHtml = article.tocItems.map(item =>
    `          <li><a href="#${item.id}">${item.label}</a></li>`
  ).join('\n');

  const takeawaysHtml = article.keyTakeaways.map(t =>
    `      <li>${t}</li>`
  ).join('\n');

  const sectionsHtml = article.sections.map(s =>
    `        <h2 id="${s.id}">${s.h2}</h2>\n        ${s.content}`
  ).join('\n\n');

  const faqsHtml = article.faqs.map(f => `        <div class="faq-item">
          <button class="faq-question">${f.question}</button>
          <div class="faq-answer"><p>${f.answer}</p></div>
        </div>`).join('\n');

  const relatedHtml = article.relatedArticles.slice(0, 5).map((r, i) =>
    `        <div class="related-post"><div class="related-num">${i + 1}</div><a href="${r.href}">${r.title}</a></div>`
  ).join('\n');

  const photoCredit = photographer
    ? `<!-- Photo by <a href="${photographerUrl}?utm_source=insurancetipspro&utm_medium=referral" target="_blank" rel="noopener">${photographer}</a> on <a href="https://unsplash.com/?utm_source=insurancetipspro&utm_medium=referral" target="_blank" rel="noopener">Unsplash</a> -->`
    : '';

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE}" crossorigin="anonymous"></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${article.title} | ${SITE_NAME}</title>
<meta name="description" content="${article.metaDescription}">
<link rel="canonical" href="${canonicalUrl}">
<meta property="og:type" content="article">
<meta property="og:title" content="${article.title}">
<meta property="og:description" content="${article.metaDescription}">
<meta property="og:url" content="${canonicalUrl}">
<meta property="og:image" content="${imageUrl}">
<meta property="og:site_name" content="${SITE_NAME}">
<link rel="stylesheet" href="../style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=${GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA_ID}');</script>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${article.title.replace(/"/g, '\\"')}",
  "description": "${article.metaDescription.replace(/"/g, '\\"')}",
  "image": "${imageUrl}",
  "datePublished": "${today}",
  "dateModified": "${today}",
  "author": {
    "@type": "Organization",
    "name": "${SITE_NAME} Editorial Team"
  },
  "publisher": {
    "@type": "Organization",
    "name": "${SITE_NAME}",
    "logo": {
      "@type": "ImageObject",
      "url": "${DOMAIN}/logo.svg"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "${canonicalUrl}"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "${DOMAIN}/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "${article.title.replace(/"/g, '\\"')}",
      "item": "${canonicalUrl}"
    }
  ]
}
</script>
</head>
<body>
<div id="read-progress"></div>

<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-logo"><img src="/logo.svg" alt="${SITE_NAME}" style="display:block;height:36px;width:auto;" loading="eager"></a>
    <nav class="site-nav" id="mainNav">
      <a href="/">Home</a><a href="/about.html">About</a><a href="/contact.html">Contact</a>
      <a href="https://coveragefixpro.com" target="_blank" rel="noopener">Calculators</a>
    </nav>
    <button class="nav-toggle" id="navToggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
  </div>
</header>

<main class="container main-content">
  <div class="breadcrumb"><a href="/">Home</a><span>›</span>${article.title}</div>
  <div class="content-grid">
    <article>
      <div class="article-header">
        <span class="category-tag">${topic.category}</span>
        <h1>${article.title}</h1>
        <div class="article-meta"><span class="author">By ${SITE_NAME} Editorial Team</span><span>${todayFmt}</span><span>${article.readTime}</span></div>
      </div>

      ${photoCredit}
      <img src="/images/${imageFilename}" alt="${article.imageAlt}" class="article-hero-img" loading="lazy">
<div class="ad-unit"><!-- AD_PLACEHOLDER --></div>
<div class="author-box">
  <div class="author-avatar-sm">IT</div>
  <div class="author-info">
    <strong>${SITE_NAME} Editorial Team</strong>
    <span>Last Updated: ${new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })} &bull; <span class="author-badge">Reviewed for accuracy</span></span>
  </div>
</div>
<div class="article-disclaimer">This article is for educational purposes. Rates and coverage vary by state and insurer. Consult a licensed insurance professional for personalized advice.</div>
<div class="key-takeaways">
  <h4>Key Takeaways</h4>
  <ul>
${takeawaysHtml}
  </ul>
</div>
<div class="toc">
        <h4>Table of Contents</h4>
        <ol>
${tocHtml}
        </ol>
      </div>

      <div class="article-body">
        <p>${article.intro}</p>

${sectionsHtml}
      </div>

      <div class="ad-unit"><!-- AD_PLACEHOLDER --></div>

      <div class="cta-section">
        <h3>Use Our Free Insurance Calculators</h3>
        <p>Get instant estimates and compare coverage options with our free tools.</p>
        <a href="https://coveragefixpro.com" target="_blank" rel="noopener" class="cta-btn">Visit CoverageFixPro.com &rarr;</a>
      </div>

      <div class="faq-section">
        <h2>Frequently Asked Questions</h2>
${faqsHtml}
      </div>

      <div class="author-bio">
        <div class="author-avatar">IT</div>
        <div><h4>${SITE_NAME} Editorial Team</h4><p>Our team of insurance researchers and writers provides unbiased, educational content to help consumers make smarter coverage decisions.</p></div>
      </div>

      <div class="helpful-widget">
        <p>Was this article helpful?</p>
        <div class="helpful-buttons">
          <button class="helpful-btn" onclick="helpfulVote(this)">&#128077; Yes, helpful</button>
          <button class="helpful-btn" onclick="helpfulVote(this)">&#128078; Not really</button>
        </div>
        <p class="helpful-msg" style="display:none;">Thanks for your feedback!</p>
      </div>
      <script>if(!window.helpfulVote)window.helpfulVote=function(b){document.querySelectorAll('.helpful-btn').forEach(function(x){x.classList.remove('voted');});b.classList.add('voted');b.closest('.helpful-widget').querySelector('.helpful-msg').style.display='block';};</script>
    </article>

    <aside class="sidebar"><div class="sidebar-sticky">
      <div class="sidebar-widget">
        <h3>Related Articles</h3>
${relatedHtml}
      </div>
      <div class="ad-unit"><!-- AD_PLACEHOLDER --></div>
      <div class="sidebar-cta">
  <h3>Free Quote Tools</h3>
  <p>Estimate your costs and find the right coverage options for free.</p>
  <a href="https://coveragefixpro.com" target="_blank" rel="noopener">Try Free Calculators &rarr;</a>
</div>
    </div></aside>
  </div>
</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand"><a href="/" class="site-logo" style="color:#fff;">Insurance<span style="color:#f59e0b;">Tips</span>Pro</a><p>Free insurance education for smarter coverage decisions.</p></div>
      <div class="footer-col"><h4>Auto Insurance</h4><ul>
        <li><a href="/articles/how-much-car-insurance-do-i-need.html">How Much Do I Need?</a></li>
        <li><a href="/articles/how-to-lower-car-insurance-premium.html">Lower Your Premium</a></li>
        <li><a href="/articles/car-insurance-after-accident.html">After an Accident</a></li>
      </ul></div>
      <div class="footer-col"><h4>Life &amp; Health</h4><ul>
        <li><a href="/articles/term-life-vs-whole-life-insurance.html">Term vs. Whole Life</a></li>
        <li><a href="/articles/how-much-life-insurance-do-i-need.html">How Much Life Insurance?</a></li>
        <li><a href="/articles/health-insurance-deductible-explained.html">Deductibles Explained</a></li>
      </ul></div>
      <div class="footer-col"><h4>Resources</h4><ul>
        <li><a href="/articles/insurance-terms-glossary.html">Insurance Glossary</a></li>
        <li><a href="/articles/how-to-compare-insurance-quotes.html">Compare Quotes</a></li>
        <li><a href="https://coveragefixpro.com" target="_blank" rel="noopener">Free Calculators</a></li>
      </ul></div>
    </div>
    <div class="footer-editorial">
  <p><strong>Editorial Independence:</strong> ${SITE_NAME} editorial content is not influenced by advertisers. Our guides are written independently to help consumers make informed decisions.</p>
</div>
<div class="footer-bottom">
      <p>&copy; 2025 ${SITE_NAME}.com. All rights reserved.</p>
      <p class="footer-disclaimer">${SITE_NAME} provides educational content only. Consult a licensed insurance professional for advice.</p>
    </div>
  </div>
</footer>
<script>
document.getElementById('navToggle').addEventListener('click',()=>document.getElementById('mainNav').classList.toggle('open'));
document.querySelectorAll('.faq-question').forEach(btn=>{btn.addEventListener('click',()=>{btn.classList.toggle('open');btn.nextElementSibling.classList.toggle('open');});});
</script>
<script>
(function(){
  var body=document.querySelector('.article-body');
  if(!body)return;
  var paras=body.querySelectorAll('p');
  var target=paras.length>=3?paras[2]:paras[paras.length-1];
  if(!target)return;
  var cta=document.createElement('div');
  cta.className='inline-cta';
  cta.innerHTML='<div class="inline-cta-text"><strong>Need to compare insurance options?</strong><span>Use our free calculators to estimate costs and find the right coverage for your situation.</span></div><a href="https://coveragefixpro.com" target="_blank" rel="noopener" class="btn-orange-sm">Free Quote Tools &rarr;</a>';
  target.parentNode.insertBefore(cta,target.nextSibling);
})();
</script>
<script>
(function(){
  var bar=document.getElementById('read-progress');
  if(!bar)return;
  function upd(){var s=document.documentElement;bar.style.width=Math.min(s.scrollTop/(s.scrollHeight-s.clientHeight)*100,100)+'%';}
  window.addEventListener('scroll',upd,{passive:true});
})();
</script>
</body>
</html>`;
}

// ─── Index Update ─────────────────────────────────────────────────────────────
function updateIndexHTML(topic, article, slug, imageFilename, today, todayFmt) {
  let html = fs.readFileSync(INDEX_FILE, 'utf8');
  const articleUrl = `articles/${slug}.html`;
  const newListItem = `
    <div class="list-item" onclick="location.href='${articleUrl}';">
      <div class="list-num">1</div>
      <div class="list-body">
        <a href="${articleUrl}" class="cat-tag">${topic.category}</a>
        <h3><a href="${articleUrl}">${article.title}</a></h3>
        <p>${article.excerpt}</p>
        <div class="list-meta">${todayFmt} &middot; ${article.readTime}</div>
        <a href="${articleUrl}" class="read-link">Read article &rarr;</a>
      </div>
    </div>
`;

  // Insert after the opening of <div class="article-list">
  // Insert new item as first in list
  html = html.replace(
    /(<div class="article-list">)/,
    `$1${newListItem}`
  );

  // Renumber ALL list-num divs sequentially (1, 2, 3, ...)
  let seq = 0;
  html = html.replace(/<div class="list-num">\d+<\/div>/g, () => {
    return `<div class="list-num">${++seq}</div>`;
  });

  // Update ItemList JSON-LD: add new item at position 1
  const newItemListEntry = `    {
      "@type": "ListItem",
      "position": 1,
      "name": "${article.title.replace(/"/g, '\\"')}",
      "url": "${DOMAIN}/articles/${slug}.html"
    },`;

  // Insert after "itemListElement": [
  html = html.replace(
    /("itemListElement":\s*\[)/,
    `$1\n${newItemListEntry}`
  );

  // Renumber ALL "position": N sequentially in ItemList (1, 2, 3, ...)
  let posSeq = 0;
  html = html.replace(/"position":\s*\d+/g, () => `"position": ${++posSeq}`);

  // Update hero stat "20+ Expert Guides" if present
  html = html.replace(/<span>20\+<\/span>/, '<span>21+</span>');

  fs.writeFileSync(INDEX_FILE, html);
  console.log('  index.html updated');
}

// ─── Sitemap Update ───────────────────────────────────────────────────────────
function updateSitemap(slug, today) {
  let xml = fs.readFileSync(SITEMAP_FILE, 'utf8');
  const newEntry = `  <url><loc>${DOMAIN}/articles/${slug}.html</loc><lastmod>${today}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>`;
  xml = xml.replace('</urlset>', `${newEntry}\n</urlset>`);
  fs.writeFileSync(SITEMAP_FILE, xml);
  console.log('  sitemap.xml updated');
}

// ─── FTP Deploy ───────────────────────────────────────────────────────────────
function deploy() {
  console.log('\n[5/5] Deploying via FTP (node deploy-ftp.js)...');
  const result = spawnSync('node', [path.join(BASE_DIR, 'deploy-ftp.js')], {
    cwd: BASE_DIR,
    timeout: 600000,
    encoding: 'utf8',
    stdio: 'inherit',
  });
  if (result.status !== 0) {
    console.error('FTP deploy failed (status ' + result.status + ')');
  } else {
    console.log('  FTP deploy complete');
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const topicsData = loadTopicsUsed();
  const topic = pickTopic(topicsData.used);
  const today = todayISO();
  const todayFmt = todayDisplay();

  console.log(`\n=== Auto-Publishing: "${topic.title}" ===`);
  console.log('Slug:', topic.slug);
  console.log('Category:', topic.category);
  console.log('Date:', today);

  // Step 1: Fetch image
  console.log('\n[1/5] Fetching Unsplash image...');
  let imageFilename = 'img-auto.png'; // fallback
  let photographer = null;
  let photographerUrl = null;
  try {
    const img = await fetchUnsplashImage(topic, topic.slug);
    if (img) {
      imageFilename = img.filename;
      photographer = img.photographer;
      photographerUrl = img.photographerUrl;
    }
  } catch (e) {
    console.warn('  Image fetch failed:', e.message, '— using fallback image');
  }

  // Step 2: Generate article content
  console.log('\n[2/5] Generating article with Anthropic API...');
  const article = await generateArticle(topic, imageFilename, today);
  console.log('  Title:', article.title);
  console.log('  Sections:', article.sections.length);

  // Step 3: Build & write article HTML
  console.log('\n[3/5] Building article HTML...');
  const articleHtml = buildArticleHTML(
    topic, article, imageFilename, photographer, photographerUrl,
    topic.slug, today, todayFmt
  );
  const articlePath = path.join(ARTICLES_DIR, `${topic.slug}.html`);
  fs.writeFileSync(articlePath, articleHtml);
  console.log('  Written:', `articles/${topic.slug}.html`);

  // Step 4: Update index.html and sitemap.xml
  console.log('\n[4/5] Updating index.html and sitemap.xml...');
  updateIndexHTML(topic, article, topic.slug, imageFilename, today, todayFmt);
  updateSitemap(topic.slug, today);

  // Step 5: Deploy
  deploy();

  // Step 6: Save topic as used
  topicsData.used.push(topic.slug);
  saveTopicsUsed(topicsData);
  console.log('\n✓ topics-used.json updated');

  console.log('\n=== Done ===');
  console.log('New article:', `${DOMAIN}/articles/${topic.slug}.html`);
}

main().catch(err => {
  console.error('\nFATAL:', err.message);
  process.exit(1);
});
