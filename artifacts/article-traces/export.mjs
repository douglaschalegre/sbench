// Usage: node export.mjs [absolute path to playwright/index.mjs]
import { createRequire } from 'node:module';
import { readdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = process.argv[2]
  ? await import(pathToFileURL(process.argv[2]))
  : require('playwright');
const dir = dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const report = [];
try {
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
  for (const name of (await readdir(dir)).filter(n => /^0[1-4].*\.html$/.test(n)).sort()) {
    await page.goto(pathToFileURL(join(dir, name)).href);
    await page.locator('main').screenshot({ path: join(dir, name.replace('.html', '.png')) });
    await page.pdf({ path: join(dir, name.replace('.html', '.pdf')), width: '1100px', height: `${await page.locator('body').evaluate(e => e.scrollHeight) + 32}px`, printBackground: true, margin: { top: '16px', bottom: '16px', left: '16px', right: '16px' } });
    const desktopOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    await page.setViewportSize({ width: 390, height: 900 });
    const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    if (desktopOverflow || mobileOverflow) throw new Error(`Overflow in ${name}`);
    report.push({ name, desktopOverflow, mobileOverflow });
    await page.setViewportSize({ width: 1100, height: 900 });
  }
  await writeFile(join(dir, 'layout-check.json'), JSON.stringify(report, null, 2));
  console.log(`Exported and checked ${report.length} figures.`);
} finally {
  await browser.close();
}
