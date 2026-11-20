// Screenshots of harbour.html at t=0, 20, 40 and 60 seconds, saved next to this file.
// Run with: node shoot.js   (needs Playwright: npm install playwright && npx playwright install chromium)
const { chromium } = require('playwright');
const path = require('path');
const { pathToFileURL } = require('url');

(async () => {
  const page_url = pathToFileURL(path.join(__dirname, 'harbour.html')).href;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 960, height: 540 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  const shots = {};
  for (const t of [0, 20, 40, 60]) {
    await page.goto(`${page_url}?t=${t}`);
    await page.waitForTimeout(100);
    shots[t] = await page.screenshot({ path: path.join(__dirname, `t${t}.png`) });
  }
  console.log('errors:', errors);
  console.log('t0 == t60 (seamless loop):', Buffer.compare(shots[0], shots[60]) === 0);
  await browser.close();
})();
