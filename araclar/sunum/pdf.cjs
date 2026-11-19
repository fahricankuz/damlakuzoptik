// HTML slaytları PDF'e çevirir: node araclar/sunum/pdf.cjs <girdi.html> <cikti.pdf> [onizleme_klasoru]
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
(async () => {
  const [, , inp, out, prev] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto(pathToFileURL(inp).href, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  if (prev) {
    const n = await p.locator('section.s').count();
    for (let i = 0; i < n; i++) await p.locator('section.s').nth(i).screenshot({ path: `${prev}/s${String(i + 1).padStart(2, '0')}.png` });
  }
  await b.close();
})();
