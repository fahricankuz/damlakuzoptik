// A4 HTML -> PDF (+ önizleme PNG): node araclar/a4-pdf.cjs <girdi.html> <cikti.pdf> [onizleme_klasoru]
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
(async () => {
  const [, , inp, out, prev] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto(pathToFileURL(require('path').resolve(inp)).href, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (prev) {
    const n = await p.locator('section.page').count();
    for (let i = 0; i < n; i++) await p.locator('section.page').nth(i).screenshot({ path: `${prev}/sayfa${i + 1}.png` });
  }
  await b.close();
})();
