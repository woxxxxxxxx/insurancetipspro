"""
Batch-transform all article pages to the new editorial design.
Adds: progress bar, author box, disclaimer, inline CTA (via JS), sticky sidebar,
orange CTA widget, editorial independence footer note.
"""
import os, glob, re

ARTICLES_DIR = r'C:\Users\Administrator\insurancetipspro\articles'
MARKER = '<!-- REDESIGN-2025 -->'

AUTHOR_BOX = '''<div class="author-box">
  <div class="author-avatar-sm">IT</div>
  <div class="author-info">
    <strong>InsuranceTipsPro Editorial Team</strong>
    <span>Last Updated: June 2025 &bull; <span class="author-badge">Reviewed for accuracy</span></span>
  </div>
</div>
'''

DISCLAIMER = '''<div class="article-disclaimer">This article is for educational purposes. Rates and coverage vary by state and insurer. Consult a licensed insurance professional for personalized advice.</div>
'''

PROGRESS_BAR = '<div id="read-progress"></div>\n'

EDITORIAL_INDEPENDENCE = '''<div class="footer-editorial">
  <p><strong>Editorial Independence:</strong> InsuranceTipsPro editorial content is not influenced by advertisers. Our guides are written independently to help consumers make informed decisions.</p>
</div>
'''

INLINE_CTA_JS = '''<script>
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
</script>'''

PROGRESS_JS = '''<script>
(function(){
  var bar=document.getElementById('read-progress');
  if(!bar)return;
  function upd(){var s=document.documentElement;bar.style.width=Math.min(s.scrollTop/(s.scrollHeight-s.clientHeight)*100,100)+'%';}
  window.addEventListener('scroll',upd,{passive:true});
})();
</script>'''

files = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.html')))
modified = skipped = 0

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        skipped += 1
        continue

    # 1. Mark as redesigned (in <head>)
    content = content.replace('</head>', MARKER + '\n</head>', 1)

    # 2. Insert progress bar right after <body>
    content = content.replace('<body>', '<body>\n' + PROGRESS_BAR, 1)

    # 3. Insert author-box + disclaimer before <div class="toc"> or <div class="article-body">
    if '<div class="toc">' in content:
        content = content.replace(
            '<div class="toc">',
            AUTHOR_BOX + DISCLAIMER + '<div class="toc">',
            1
        )
    else:
        content = content.replace(
            '<div class="article-body">',
            AUTHOR_BOX + DISCLAIMER + '<div class="article-body">',
            1
        )

    # 4. Replace sidebar CTA widget (blue background) with orange sidebar-cta
    # Match the sidebar-widget with inline style background:#eff6ff
    content = re.sub(
        r'<div class="sidebar-widget" style="background:#eff6ff;">.*?</div>',
        '<div class="sidebar-cta">\n'
        '  <h3>Free Quote Tools</h3>\n'
        '  <p>Estimate your costs and find the right coverage options for free.</p>\n'
        '  <a href="https://coveragefixpro.com" target="_blank" rel="noopener">Try Free Calculators &rarr;</a>\n'
        '</div>',
        content,
        flags=re.DOTALL
    )

    # 5. Add sticky wrapper to sidebar
    content = content.replace(
        '<aside class="sidebar">',
        '<aside class="sidebar"><div class="sidebar-sticky">',
        1
    )
    # Close sticky wrapper before </aside>
    content = content.replace('</aside>', '</div></aside>', 1)

    # 6. Add editorial independence before footer-bottom div
    content = content.replace(
        '<div class="footer-bottom">',
        EDITORIAL_INDEPENDENCE + '<div class="footer-bottom">',
        1
    )

    # 7. Add scripts before </body>
    content = content.replace('</body>', INLINE_CTA_JS + '\n' + PROGRESS_JS + '\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    modified += 1
    print(f'  OK {fname}')

print(f'\nDone: {modified} modified, {skipped} already done.')
