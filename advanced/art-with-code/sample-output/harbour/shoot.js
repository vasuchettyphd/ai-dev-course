const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const round = process.argv[2] || '1';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type()==='error' && errs.push(m.text()));
  const url = 'file://' + path.resolve('harbour.html');
  const bufs = {};
  for (const t of [0, 20, 40, 60]) {
    await p.goto(url + '?t=' + t);
    await p.waitForTimeout(100);
    const buf = await p.screenshot({ path: t < 60 ? `shot-r${round}-t${t}.png` : `seam-r${round}-t60.png` });
    bufs[t] = buf;
  }
  console.log('errors:', errs);
  console.log('t0 == t60 bytes identical:', Buffer.compare(bufs[0], bufs[60]) === 0);
  await b.close();
})();
