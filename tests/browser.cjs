const { chromium }=require('playwright');
const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({headless:true,args:['--no-sandbox']});const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8765');await page.locator('#cases button').last().waitFor();assert.equal(await page.locator('#cases button').count(),10);
for(let i=0;i<10;i++){await page.locator('#cases button').nth(i).click();await page.locator('#simulate').click();await page.locator('#result:not([hidden])').waitFor();assert.match(await page.locator('#resultMode').innerText(),/SIMULAÇÃO/)}
await page.locator('#cases button').nth(1).click();await page.locator('#simulate').click();assert.match(await page.locator('#decision').innerText(),/Sugestão/);
await page.locator('#threshold').fill('0.95');await page.locator('#threshold').dispatchEvent('input');assert.match(await page.locator('#decision').innerText(),/Revisar/);
await page.locator('#state').fill('Texto novo');assert.equal(await page.locator('#simulate').isDisabled(),true);assert.equal(await page.locator('#result').isVisible(),false);
await page.locator('#reset').click();const download=page.waitForEvent('download');await page.locator('#download').click();assert.match((await download).suggestedFilename(),/request.json/);
await page.locator('#theme').click();assert.equal(await page.locator('body').evaluate(el=>el.classList.contains('light')),true);await page.reload();assert.equal(await page.locator('body').evaluate(el=>el.classList.contains('light')),true);await page.locator('#theme').click();
await page.locator('#calls').fill('1');await page.locator('#tokens').fill('10000');assert.match(await page.locator('#costTotal').innerText(),/0,00042/);await page.locator('#calls').fill('10000');
await page.locator('#cases button').nth(1).click();await page.locator('#simulate').click();await page.screenshot({path:'/home/nmaldaner/projetos/output/jev-verificacao/app-desktop.png',fullPage:true});
await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:'/home/nmaldaner/projetos/output/jev-verificacao/app-mobile.png',fullPage:true});
await page.goto('http://127.0.0.1:18766/guia/');await page.locator('img').first().waitFor();await page.screenshot({path:'/home/nmaldaner/projetos/output/jev-verificacao/guia-mobile.png',fullPage:true});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'/home/nmaldaner/projetos/output/jev-verificacao/guia-desktop.png',fullPage:true});
assert.deepEqual(errors,[]);await browser.close();console.log('OK: dez casos, política, edição, download, temas persistidos, custo, desktop/mobile sem overflow ou erros JS.');})().catch(e=>{console.error(e);process.exit(1)});
