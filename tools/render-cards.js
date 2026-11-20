const {chromium}=require('playwright');const fs=require('fs');
const P=[
 {id:'izi-m',img:'izi.png',scale:128,cx:930,cy:385,title:'IZI M\n22.000 puffs',
  body:'- яркий экран: заряд и жидкость\n- режимы SOFT и BOOST\n- 22 мл жидкости\n- батарея 650 мАч',
  desc:'Одноразовая система IZI M: до 22 000 затяжек, большой цветной экран с уровнем заряда и жидкости, режимы SOFT и BOOST.',
  flavors:'Мята с двойным льдом',tags:'#izi #одноразка'},
 {id:'voopoo-vmate-pro-2',img:'pro2.png',scale:116,cx:950,cy:362,title:'VOOPOO\nVMATE PRO 2',
  body:'- батарея 1500 мАч\n- два картриджа 0.4 Ω и 0.7 Ω\n- верхняя заправка, 3 мл\n- зарядка Type-C',
  desc:'Многоразовая под-система VOOPOO VMATE PRO 2. В комплекте сразу два картриджа с верхней заправкой: 0.4 Ω и 0.7 Ω по 3 мл. Улучшены вкус, герметичность и ресурс (3X Upgrade).',
  flavors:'',tags:'#voopoo #vmate #подсистема'},
 {id:'voopoo-vmate-i3',img:'i3.png',scale:112,cx:950,cy:355,title:'VOOPOO\nVMATE i3',
  body:'- батарея 1500 мАч\n- картридж 0.7 Ω, 3 мл\n- верхняя заправка\n- подходят картриджи VMATE',
  desc:'Компактная под-система VOOPOO VMATE i3 в карбоновом корпусе. Картридж 0.7 Ω на 3 мл с верхней заправкой, подходят все картриджи семейства VMATE.',
  flavors:'',tags:'#voopoo #vmate #подсистема'}];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1400}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
for(const it of P){
 await p.goto('file:///home/user/tabachok-tgk/index.html');await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForTimeout(600);
 await p.fill('#fTitle',it.title);await p.fill('#fBody',it.body);await p.fill('#fLabel','Поступление');
 await p.fill('#pDesc',it.desc);await p.fill('#pFlavors',it.flavors);await p.fill('#pTags',it.tags);await p.fill('#pPrice','');await p.fill('#pWhere','');
 await p.setInputFiles('#fFile',it.img);await p.waitForTimeout(800);
 await p.evaluate(s=>{const e=document.getElementById('sScale');e.value=s;e.dispatchEvent(new Event('input'));},it.scale);
 // move product: drag from center
 const box=await p.locator('#card').boundingBox();const k=box.width/1280;
 await p.mouse.move(box.x+900*k,box.y+400*k);await p.mouse.down();await p.mouse.move(box.x+it.cx*k,box.y+it.cy*k,{steps:5});await p.mouse.up();
 await p.waitForTimeout(300);
 const url=await p.evaluate(()=>document.getElementById('card').toDataURL('image/png'));
 fs.writeFileSync(it.id+'.png',Buffer.from(url.split(',')[1],'base64'));
 fs.writeFileSync(it.id+'.txt',await p.inputValue('#postOut'));
}
console.log('errors',errs);await b.close();})();
