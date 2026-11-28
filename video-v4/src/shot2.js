const {chromium}=require('playwright');
(async()=>{
const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:3});
p.on('dialog',d=>d.accept());
await p.goto('file:///mnt/project-files/kasrapi/Aplikasi-UMKM.html');await p.waitForTimeout(800);
const nav=async x=>{await p.evaluate(x=>document.querySelector('[data-nav="'+x+'"]').click(),x);await p.waitForTimeout(600);await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(200)};
await nav('pengaturan');await p.locator('[data-action="demo"]:visible').first().click();await p.waitForTimeout(1500);
await p.waitForTimeout(5000);await nav('beranda');await p.screenshot({path:'v_beranda.png'});

// list classes of bottom nav parent
console.log(await p.evaluate(()=>document.querySelector('.navbtn').parentElement.className));
const cards=async(pg)=>{await nav(pg);const n=await p.locator(`#page-${pg} .card:visible`).count();for(let i=0;i<n;i++){const c=p.locator(`#page-${pg} .card:visible`).nth(i);await c.scrollIntoViewIfNeeded();await c.screenshot({path:`c_${pg}_${i}.png`})}console.log(pg,n)};
await p.evaluate(()=>{const n=document.querySelector('.navbtn').parentElement;n.style.visibility='hidden'});
await cards('beranda');await cards('laporan');await cards('stok');await cards('transaksi');
await nav('stok');await p.screenshot({path:'v_stok.png'});
await nav('laporan');await p.screenshot({path:'v_laporan.png'});
await nav('beranda');
await p.evaluate(()=>{const n=document.querySelector('.navbtn').parentElement;n.style.visibility='visible'});
await p.locator('.fab').click();await p.waitForTimeout(800);
const opts=await p.$$eval('#fKanal option',o=>o.map(x=>x.textContent+'='+x.value));console.log(opts);
const sh=opts.find(o=>/Shopee/.test(o)).split('=')[1];
await p.selectOption('#fKanal',sh);await p.fill('#fQty','3');await p.locator('#fQty').dispatchEvent('input');await p.waitForTimeout(400);
await p.screenshot({path:'v_form.png'});
await p.locator('#fCalc').screenshot({path:'c_calc.png'});
await b.close();})();
