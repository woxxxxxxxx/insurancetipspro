'use strict';
const https = require('https');
const fs = require('fs');
const path = require('path');

const UNSPLASH_KEY = '5RQkzb688Ez9nXR-vzUbkXmxFaxQbLzEQUoyy8rogt4';
const IMAGES_DIR = path.join(__dirname, 'images');

const SVG_REPLACEMENTS = [
  { svg: 'img-hero.svg', query: 'insurance professional office', filename: 'img-hero.jpg' },
  { svg: 'img-auto.svg', query: 'car insurance driving', filename: 'img-auto.jpg' },
  { svg: 'img-life.svg', query: 'family life insurance protection', filename: 'img-life.jpg' },
  { svg: 'img-health.svg', query: 'health insurance medical', filename: 'img-health.jpg' },
  { svg: 'img-home.svg', query: 'home insurance house protection', filename: 'img-home.jpg' },
  { svg: 'img-business.svg', query: 'business insurance office', filename: 'img-business.jpg' },
  { svg: 'img-fundamentals.svg', query: 'insurance documents paperwork', filename: 'img-fundamentals.jpg' },
  { svg: 'img-umbrella.svg', query: 'umbrella insurance protection', filename: 'img-umbrella.jpg' },
  { svg: 'img-quotes.svg', query: 'insurance comparison quotes', filename: 'img-quotes.jpg' },
];

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': 'InsuranceTipsPro/1.0' } }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        httpsGet(res.headers.location).then(resolve).catch(reject);
        return;
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, body: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

async function downloadImage(query, filename) {
  const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=3&orientation=landscape&client_id=${UNSPLASH_KEY}`;
  console.log(`Searching: ${query}`);
  const resp = await httpsGet(url);
  if (resp.status !== 200) { console.warn('  API error:', resp.status); return false; }
  const data = JSON.parse(resp.body.toString());
  if (!data.results || !data.results.length) { console.warn('  No results'); return false; }
  const photo = data.results[0];
  const imgUrl = photo.urls.regular;
  console.log(`  Downloading from ${imgUrl.substring(0, 60)}...`);
  const imgResp = await httpsGet(imgUrl);
  if (imgResp.status !== 200) { console.warn('  Download failed:', imgResp.status); return false; }
  fs.writeFileSync(path.join(IMAGES_DIR, filename), imgResp.body);
  console.log(`  Saved: ${filename} (${(imgResp.body.length / 1024).toFixed(0)}KB)`);
  // Track download
  try {
    await httpsGet(photo.links.download_location + `?client_id=${UNSPLASH_KEY}`);
  } catch(e) {}
  return true;
}

function replaceInFiles(svgName, jpgName) {
  const htmlFiles = [];
  function scan(dir) {
    for (const f of fs.readdirSync(dir)) {
      const fp = path.join(dir, f);
      if (fs.statSync(fp).isDirectory() && !f.startsWith('.') && f !== 'node_modules') scan(fp);
      else if (f.endsWith('.html')) htmlFiles.push(fp);
    }
  }
  scan(__dirname);
  let count = 0;
  for (const fp of htmlFiles) {
    let content = fs.readFileSync(fp, 'utf8');
    if (content.includes(svgName)) {
      content = content.replace(new RegExp(svgName.replace('.', '\\.'), 'g'), jpgName);
      fs.writeFileSync(fp, content, 'utf8');
      count++;
      console.log(`  Replaced in: ${path.relative(__dirname, fp)}`);
    }
  }
  return count;
}

async function main() {
  for (const item of SVG_REPLACEMENTS) {
    console.log(`\n--- ${item.svg} -> ${item.filename} ---`);
    const ok = await downloadImage(item.query, item.filename);
    if (ok) {
      const n = replaceInFiles(item.svg, item.filename);
      console.log(`  Updated ${n} HTML files`);
      // Remove old SVG
      const svgPath = path.join(IMAGES_DIR, item.svg);
      if (fs.existsSync(svgPath)) { fs.unlinkSync(svgPath); console.log(`  Deleted ${item.svg}`); }
    }
    await new Promise(r => setTimeout(r, 500)); // rate limit
  }
  console.log('\nDone!');
}

main().catch(console.error);
