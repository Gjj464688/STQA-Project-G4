/** Recheck GUI/configuration/accessibility and Week 4 web cases on an isolated app.
 * npm install playwright, start run_isolated_server.py, then node this file.
 * Does not alter the application source or the user's normal database.
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.dirname(fileURLToPath(import.meta.url));
const webRoot=path.join(root,'..','04_Web_API');
const base=process.env.QA_BASE_URL||'http://127.0.0.1:5013';
const w3out=path.join(root,'evidence','verified');
const w4out=path.join(webRoot,'Evidence','verified');
for(const dir of [w3out,w4out])fs.mkdirSync(dir,{recursive:true});
const rows=[];const started=new Date().toISOString();
const assert=(ok,message)=>{if(!ok)throw new Error(message);};
let page,context,browser,engine='Edge';
async function launch(channel){
 const b=await chromium.launch({channel,headless:true,args:['--no-sandbox','--no-proxy-server']});
 const c=await b.newContext({viewport:{width:1280,height:900},timezoneId:'Asia/Singapore'});
 const p=await c.newPage();p.setDefaultTimeout(5000);return {b,c,p};
}
async function run(id,objective,expected,fn){
 const entry={case_id:id,objective,expected,browser:engine,version:browser.version(),viewport:page.viewportSize(),execution:'Agent-executed automated verification',started_utc:new Date().toISOString()};
 try{entry.actual=await fn();entry.status='Pass';}
 catch(e){entry.status='Fail';entry.actual=String(e.message);}
 const dir=id.startsWith('WEB-')?w4out:w3out;
 const filename=id+'.png';await page.screenshot({path:path.join(dir,filename),fullPage:true});
 entry.evidence=filename;rows.push(entry);console.log(id,entry.status,JSON.stringify(entry.actual));
}
async function register(username,password='TestPass123'){
 await page.goto(base+'/register');await page.locator('[name=username]').fill(username);await page.locator('[name=password]').fill(password);
 await page.getByRole('button',{name:'Register',exact:true}).click();await page.waitForLoadState('domcontentloaded');
}
async function login(username,password='TestPass123'){
 await page.goto(base+'/login');await page.locator('[name=username]').fill(username);await page.locator('[name=password]').fill(password);
 await page.getByRole('button',{name:'Log in',exact:true}).click();await page.waitForLoadState('domcontentloaded');
}
async function create(title,description='',category='None',date=''){
 await page.goto(base+'/tasks/new');await page.locator('[name=title]').fill(title);await page.locator('[name=description]').fill(description);
 await page.locator('[name=category_id]').selectOption({label:category});if(date)await page.locator('[name=due_date]').fill(date);
 await page.getByRole('button',{name:'Create Task',exact:true}).click();await page.waitForLoadState('domcontentloaded');
}
const taskRow=title=>page.locator('tbody tr').filter({has:page.locator('.title-cell',{hasText:title})});
async function filter(category='',status='',q=''){
 await page.goto(base+'/?'+new URLSearchParams({category,status,q}));
}
async function emptyValidation(){
 await page.goto(base+'/tasks/new');await page.getByRole('button',{name:'Create Task',exact:true}).click();
 const r=await page.locator('[name=title]').evaluate(e=>({valid:e.validity.valid,missing:e.validity.valueMissing,message:e.validationMessage}));
 assert(r.missing&&r.message&&page.url().endsWith('/tasks/new'),'Empty form was not blocked');return r;
}
async function deleteTask(title){
 let prompt='';page.once('dialog',async d=>{prompt=d.message();await d.accept();});
 await taskRow(title).getByRole('button',{name:'Delete',exact:true}).click();await page.waitForLoadState('domcontentloaded');
 assert(prompt==='Delete this task?','Missing confirmation');assert(await taskRow(title).count()===0,'Task not deleted');return {confirmation:prompt,removed:true};
}
function contrast(a,b){
 const lum=rgb=>rgb.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
 const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);
}
try{
 ({b:browser,c:context,p:page}=await launch('msedge'));
 await register('week3_verified');
 await run('GUI-TC-001','Empty New Task form','Required Title blocks submission',emptyValidation);
 await run('GUI-TC-002','Create no-date task','Title/category shown, no due date',async()=>{await create('Complete STQA Week 3','Perform GUI and usability testing','Study');const t=await taskRow('Complete STQA Week 3').innerText();assert(t.includes('Study')&&t.includes('No due date'),'Incorrect task fields');return t;});
 await run('GUI-TC-003','Create dated task','Selected date appears',async()=>{await create('Submit STQA Assignment','Week 3 report','Study','2099-11-30');const t=await taskRow('Submit STQA Assignment').innerText();assert(t.includes('2099-11-30')&&t.includes('Upcoming'),'Incorrect date');return t;});
 await run('GUI-TC-004','Edit existing task','Existing fields load and title/description changes persist',async()=>{await taskRow('Complete STQA Week 3').getByRole('link',{name:'Edit',exact:true}).click();assert(await page.locator('[name=description]').inputValue()==='Perform GUI and usability testing','Existing description missing');await page.locator('[name=title]').fill('Complete STQA Week 3 - Updated');await page.locator('[name=description]').fill('Complete GUI testing documentation');await page.getByRole('button',{name:'Save Changes',exact:true}).click();await taskRow('Complete STQA Week 3 - Updated').getByRole('link',{name:'Edit',exact:true}).click();const d=await page.locator('[name=description]').inputValue();assert(d==='Complete GUI testing documentation','Description not saved');await page.goto(base+'/');return {title:'Complete STQA Week 3 - Updated',description:d};});
 await run('GUI-TC-005','Delete with confirmation','Selected task removed after confirmation',()=>deleteTask('Submit STQA Assignment'));
 await run('GUI-TC-006','Category Study','Only Study task displayed',async()=>{await filter('Study');const t=await page.locator('tbody').innerText();assert(t.includes('Complete STQA')&&!t.includes('Submit STQA'),'Incorrect Study filter');return t;});
 await create('Buy groceries','','Personal');
 await run('GUI-TC-007','Sequential category filters','Study and Personal each exclude other categories',async()=>{await filter('Study');assert(await taskRow('Buy groceries').count()===0,'Personal task leaked into Study');await filter('Personal');assert(await taskRow('Buy groceries').count()===1&&await taskRow('Complete STQA').count()===0,'Incorrect Personal filter');return 'Study and Personal checked separately';});
 await run('GUI-TC-008','Open status filter','Both open tasks appear',async()=>{await filter('','open');assert(await page.locator('tbody .title-cell').count()===2,'Open task count mismatch');return await page.locator('tbody').innerText();});
 await filter();await taskRow('Complete STQA').locator('.check-btn').click();
 await run('GUI-TC-009','Done status filter','Only explicitly completed task appears',async()=>{await filter('','done');assert(await page.locator('tbody .title-cell').count()===1&&await page.locator('tr.done').count()===1,'Done filter mismatch');return await page.locator('tbody').innerText();});
 await run('GUI-TC-010','Search matching task','Only Buy groceries appears',async()=>{await filter('','','Buy groceries');assert(await page.locator('tbody .title-cell').count()===1,'Search count mismatch');return await page.locator('tbody').innerText();});
 await run('GUI-TC-011','Search missing task','Empty-state message appears',async()=>{await filter('','','Nonexistent Task 123');const t=await page.locator('tbody').innerText();assert(t.includes('No tasks match your filters'),'Missing empty-state feedback');return t;});
 await run('GUI-TC-012','Tasks Dashboard navigation','Both links open their respective pages',async()=>{await page.getByRole('link',{name:'Dashboard',exact:true}).click();assert(await page.locator('h1').innerText()==='Dashboard','Dashboard missing');await page.getByRole('link',{name:'Tasks',exact:true}).click();assert(await page.locator('h1').innerText()==='My Tasks','Tasks missing');return 'Dashboard and My Tasks both opened';});
 // Ensure completion precedes the dashboard timestamp boundary by at least one second.
 await page.waitForTimeout(1100);
 await run('GUI-TC-013','Dashboard counters','2 total, 1 open, 0 overdue, 0 due soon, 1 recent completion',async()=>{await page.goto(base+'/dashboard');const values=await page.locator('.stat-value').allTextContents();assert(JSON.stringify(values.map(x=>x.trim()))===JSON.stringify(['2','1','0','0','1']),'Dashboard counts: '+values);return values;});
 await run('GUI-TC-014','Logout session protection','Dashboard redirects to login',async()=>{await page.goto(base+'/logout');await page.goto(base+'/dashboard');assert(page.url().endsWith('/login'),'Unauthenticated dashboard accessible');return page.url();});
 await login('week3_verified');
 const edge=browser,edgeContext=context,edgePage=page;
 for(const channel of ['chrome','msedge']){
  if(channel==='chrome'){({b:browser,c:context,p:page}=await launch(channel));engine='Chrome';await login('week3_verified');}
  else{browser=edge;context=edgeContext;page=edgePage;engine='Edge';}
  const n=channel==='chrome'?1:3;
  await run(`COMP-TC-00${n}`,'Desktop display in '+engine,'Heading/table/buttons visible at 1280 x 900',async()=>{await page.goto(base+'/');assert(await page.locator('h1').isVisible()&&await page.locator('.task-table').isVisible(),'Missing controls');const metrics=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));assert(metrics.scrollWidth<=metrics.width,'Horizontal overflow');return metrics;});
  await run(`COMP-TC-00${n+1}`,'Task creation in '+engine,'Browser-created task appears',async()=>{await create(engine+' Compatibility Test','','Personal');assert(await taskRow(engine+' Compatibility Test').count()===1,'Task missing');return await taskRow(engine+' Compatibility Test').innerText();});
  if(channel==='chrome'){await browser.close();browser=edge;context=edgeContext;page=edgePage;engine='Edge';}
 }
 await run('COMP-TC-005','Desktop layout','No horizontal overflow at 1280 x 900',async()=>{await page.goto(base+'/');const x=await page.evaluate(()=>({width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth}));assert(x.scrollWidth<=x.width,'Desktop overflow');return x;});
 await page.setViewportSize({width:600,height:700});
 await run('COMP-TC-006','Narrow task list','Table and action controls fit horizontally at 600 x 700',async()=>{await page.goto(base+'/');const x=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,tableRight:document.querySelector('table').getBoundingClientRect().right}));assert(x.scrollWidth<=x.width&&x.tableRight<=x.width,'Horizontal overflow: '+JSON.stringify(x));return x;});
 await run('COMP-TC-007','Narrow task form','Fields/buttons fit at 600 x 700',async()=>{await page.goto(base+'/tasks/new');const x=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));assert(x.scrollWidth<=x.width,'Form horizontal overflow');assert(await page.getByRole('button',{name:'Create Task',exact:true}).isVisible(),'Create button missing');return x;});
 await page.setViewportSize({width:1280,height:900});
 await run('ACC-TC-001','Text legibility sample','Main heading/table text present and nonzero font size',async()=>{await page.goto(base+'/');const x=await page.locator('h1').evaluate(e=>({text:e.textContent,size:getComputedStyle(e).fontSize}));assert(parseFloat(x.size)>0,'Text hidden');return {...x,scope:'Mechanical sample; subjective readability retained in usability observations'};});
 await run('ACC-TC-002','Text contrast','Normal-size completed task text meets 4.5:1 contrast',async()=>{await page.goto(base+'/');const x=await page.locator('tr.done .title-cell').evaluate(e=>({color:getComputedStyle(e).color,size:getComputedStyle(e).fontSize,background:getComputedStyle(e.closest('table')).backgroundColor}));const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number);const ratio=contrast(rgb(x.color),rgb(x.background));assert(ratio>=4.5,'Completed title contrast '+ratio.toFixed(2)+':1 ('+x.color+' on '+x.background+'); below 4.5:1');return {ratio,...x};});
 await run('ACC-TC-003','Keyboard focus traversal','Keyboard reaches controls, visibly outlined, and activates New Task',async()=>{await page.goto(base+'/');const visited=[];let found=false;for(let i=0;i<18;i++){await page.keyboard.press('Tab');const f=await page.evaluate(()=>({tag:document.activeElement.tagName,text:document.activeElement.textContent.trim(),outline:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth}));visited.push(f);if(f.text==='+ New Task'){assert(f.outline!=='none'&&parseFloat(f.width)>0,'Focus outline missing');await page.keyboard.press('Enter');await page.waitForURL('**/tasks/new');found=true;break;}}assert(found&&page.url().includes('/tasks/new'),'Keyboard New Task activation failed');return visited;});
 await run('ACC-TC-004','Visible form labels','Title Description Category Due Date labels present',async()=>{await page.goto(base+'/tasks/new');const labels=await page.locator('label').allTextContents();assert(labels.length===4,'Missing visible labels');return {labels,scope:'Visible labels only; programmatic association assessed separately in ACC-TC-008'};});
 await run('ACC-TC-005','Validation feedback','Missing Title is focused and submission blocked',async()=>{const x=await emptyValidation();assert(await page.locator('[name=title]').evaluate(e=>e===document.activeElement),'Missing field not focused');return {...x,recommendation:'Optional clearer task-title wording; generic browser text alone is not a confirmed defect'};});
 await run('ACC-TC-006','Heading structure','Each inspected page has a descriptive h1',async()=>{const result=[];for(const url of ['/','/dashboard','/tasks/new']){await page.goto(base+url);const h=await page.locator('h1').allTextContents();assert(h.length===1&&h[0].trim(),'Missing unique h1');result.push({url,h});}return result;});
 await run('ACC-TC-007','Text action labels','Create Save Cancel links/buttons have descriptive visible text',async()=>{await page.goto(base+'/tasks/new');assert(await page.getByRole('button',{name:'Create Task',exact:true}).count()===1&&await page.getByRole('link',{name:'Cancel',exact:true}).count()===1,'Missing text actions');return 'Create Task and Cancel have descriptive text; icon-only completion control not assessed here';});
 await run('ACC-TC-008','Programmatic form labels','All four fields have associated labels or aria-label',async()=>{await page.goto(base+'/tasks/new');const x=await page.locator('.task-form input,.task-form textarea,.task-form select').evaluateAll(es=>es.map(e=>({name:e.name,labels:e.labels.length,aria:e.getAttribute('aria-label'),labelledby:e.getAttribute('aria-labelledby')})));assert(x.every(e=>e.labels||e.aria||e.labelledby),'Fields lack programmatic labels: '+JSON.stringify(x));return x;});
 await run('ACC-TC-009','Text enlargement','New Task controls remain available at 200% CSS zoom',async()=>{await page.goto(base+'/tasks/new');await page.evaluate(()=>document.body.style.zoom='2');const x=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,zoom:getComputedStyle(document.body).zoom}));assert(x.scrollWidth<=x.width,'200% zoom horizontal overflow');assert(await page.getByRole('button',{name:'Create Task',exact:true}).isVisible(),'Create button missing');return {...x,scope:'CSS zoom simulation; no physical-device or full reflow conformance claim'};});
 await page.evaluate(()=>document.body.style.zoom='1');
 await context.close();context=await browser.newContext({viewport:{width:1280,height:900},timezoneId:'Asia/Singapore'});page=await context.newPage();page.setDefaultTimeout(5000);
 const user='week4_web_verify';
 await run('WEB-01','Valid web registration','Redirect to task list',async()=>{await register(user);assert(page.url()===base+'/','Registration failed');return page.url();});
 await run('WEB-02','Duplicate web username','Reject duplicate registration (unconfirmed uniqueness assumption)',async()=>{await register(user);assert(page.url().includes('/register')&&await page.locator('.error').count()>0,'Duplicate registration accepted; username uniqueness requirement unconfirmed');return await page.locator('.error').innerText();});
 await run('WEB-03','Required registration fields','Native validation blocks empty registration',async()=>{await page.goto(base+'/register');await page.getByRole('button',{name:'Register',exact:true}).click();const x=await page.locator('[name=username]').evaluate(e=>({missing:e.validity.valueMissing,message:e.validationMessage}));assert(x.missing,'Empty registration not blocked');return x;});
 for(const [id,username,password,accepted] of [['WEB-04','w4_short','123',false],['WEB-05','w4_eight','Test1234',true],['WEB-06','w4_nine','Test12345',true],['WEB-07','ab','TestPass123',false],['WEB-08','web@test','TestPass123',false],['WEB-09','abcdefghijklmnopqrstuvwxyz','TestPass123',false]]){
  await run(id,'Registration boundary '+id,accepted?'Valid boundary accepted':'Invalid input rejected',async()=>{await register(username,password);const ok=page.url()===base+'/';const message=await page.locator('.error').allTextContents();assert(ok===accepted,'accepted='+ok+'; message='+message.join(' '));return {accepted:ok,message};});
 }
 await run('WEB-10','Valid web login','User reaches task list',async()=>{await page.goto(base+'/logout');await login(user);assert(page.url()===base+'/','Login failed');return page.url();});
 await run('WEB-11','Invalid web login','Error shown',async()=>{await page.goto(base+'/logout');await login(user,'WrongPassword');const t=await page.locator('.error').innerText();assert(t.includes('Invalid username or password'),'Wrong login accepted');return t;});
 await login(user);
 await run('WEB-12','Create task','New task listed',async()=>{await create('Prepare STQA Web Testing Report');assert(await taskRow('Prepare STQA').count()===1,'Task missing');return await taskRow('Prepare STQA').innerText();});
 await run('WEB-13','Complete task','Task changes to Done',async()=>{await taskRow('Prepare STQA').locator('.check-btn').click();assert(await page.locator('tr.done').count()===1,'Task not completed');return await page.locator('tr.done').innerText();});
 await run('WEB-14','Edit task','Updated title listed',async()=>{await taskRow('Prepare STQA').getByRole('link',{name:'Edit',exact:true}).click();await page.locator('[name=title]').fill('Prepare STQA Final Testing Report');await page.getByRole('button',{name:'Save Changes',exact:true}).click();assert(await taskRow('Prepare STQA Final').count()===1,'Edit not persisted');return await taskRow('Prepare STQA Final').innerText();});
 await run('WEB-15','Delete task','Task removed after confirmation',()=>deleteTask('Prepare STQA Final'));
 await create('Complete STQA Assignment');await create('Study Software Testing');
 await run('WEB-16','Search title','Only STQA match appears',async()=>{await filter('','','STQA');assert(await page.locator('tbody .title-cell').count()===1,'Search mismatch');return await page.locator('tbody').innerText();});
 await run('WEB-17','Done filter empty state','No completed tasks shown',async()=>{await filter('','done');assert(await page.locator('.empty').count()===1,'Unexpected completed tasks');return await page.locator('.empty').innerText();});
 await run('WEB-18','Dashboard data','2 total and 2 open',async()=>{await page.goto(base+'/dashboard');const values=await page.locator('.stat-value').allTextContents();assert(values[0].trim()==='2'&&values[1].trim()==='2','Counters mismatch');return values;});
 await run('WEB-19','Logout protects Tasks','Unauthenticated task page redirects to login',async()=>{await page.goto(base+'/logout');await page.goto(base+'/');assert(page.url().endsWith('/login'),'Unauthenticated access allowed');return page.url();});
 await login(user);await page.goto(base+'/');const editHref=await taskRow('Complete STQA Assignment').getByRole('link',{name:'Edit',exact:true}).getAttribute('href');
 await register('w4_other');
 await run('WEB-20','Cross-user edit protection','Another account cannot edit owner task',async()=>{await page.goto(base+editHref);assert(page.url()===base+'/','Other user edit page accessible');return {attempted:editHref,redirect:page.url()};});
}finally{
 if(browser)await browser.close();
 for(const [dir,predicate] of [[w3out,r=>!r.case_id.startsWith('WEB-')],[w4out,r=>r.case_id.startsWith('WEB-')]]){
  const results=rows.filter(predicate);const record={started_utc:started,source:'Unmodified original app; '+base+'; temporary DB',counts:{Pass:results.filter(x=>x.status==='Pass').length,Fail:results.filter(x=>x.status==='Fail').length},results};
  fs.writeFileSync(path.join(dir,'browser_results.json'),JSON.stringify(record,null,2));
 }
}
process.exitCode=rows.some(r=>r.status==='Fail')?1:0;
