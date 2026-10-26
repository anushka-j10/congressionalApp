import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const code=readFileSync(new URL('../frontend/onboarding.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
function setup(hash='#welcome', reduced=false) {
  const nodes=new Map(), events=new Map();
  const node=id=>{if(!nodes.has(id))nodes.set(id,{hidden:id==='app-shell',dataset:{},listeners:{},textContent:'',focus(){this.focused=true;},addEventListener(k,v){this.listeners[k]=v;},showModal(){this.open=true;},close(){this.open=false;this.listeners.close();}});return nodes.get(id);};
  const timers=new Map(); let timerId=0;
  const win={location:{hash},addEventListener(k,v){events.set(k,v);},matchMedia:()=>({matches:reduced}),
    setTimeout(fn,delay){const id=++timerId;timers.set(id,{fn,delay});return id;},clearTimeout(id){timers.delete(id);}};
  const ctx=vm.createContext({document:{getElementById:node},window:win,t:(key,values={})=>key+JSON.stringify(values)});
  vm.runInContext(code,ctx);
  const click=id=>{node(id).listeners.click();events.get('hashchange')();};
  return {node,win,events,click,timers,runTimer(){const [id,timer]=timers.entries().next().value;timers.delete(id);timer.fn();}};
}
test('opening -> four tutorial steps -> reader exposes one screen at a time',()=>{
  const a=setup(); assert.equal(a.node('welcome-screen').hidden,false);assert.equal(a.node('notice-screen').hidden,true);
  a.click('get-started');
  for(let step=1;step<=4;step++){
    assert.equal(a.win.location.hash,`#tutorial/${step}`);
    assert.equal(a.node('tutorial-screen').hidden,false);assert.equal(a.node('welcome-screen').hidden,true);assert.equal(a.node('notice-screen').hidden,true);
    assert.equal(a.node('tutorial-title').textContent,`tutorial_${step}_title{}`);
    for(let i=1;i<=4;i++) assert.equal(a.node(`tutorial-art-${i}`).hidden,i!==step);
    a.click('tutorial-next');
  }
  assert.equal(a.win.location.hash,'#notice');assert.equal(a.node('notice-screen').hidden,false);assert.equal(a.node('tutorial-screen').hidden,true);assert.equal(a.node('reader-title').focused,true);
});
test('skip, back and browser navigation preserve the reader draft; replay begins at step one',()=>{
 const a=setup();a.node('confirmed-text').value='user correction';a.click('get-started');a.click('tutorial-next');a.click('tutorial-back');assert.equal(a.win.location.hash,'#tutorial/1');a.click('tutorial-back');assert.equal(a.node('welcome-screen').hidden,false);
 a.click('get-started');a.click('skip-tutorial');assert.equal(a.node('notice-screen').hidden,false);a.click('replay-tutorial');assert.equal(a.win.location.hash,'#tutorial/1');
 a.win.location.hash='#notice';a.events.get('hashchange')();assert.equal(a.node('notice-screen').hidden,false);assert.equal(a.node('confirmed-text').value,'user correction');
});
test('invalid routes return to welcome and language updates preserve tutorial position',()=>{
 const a=setup('#tutorial/99');assert.equal(a.node('welcome-screen').hidden,false);
 a.win.location.hash='#tutorial/3';a.events.get('hashchange')();a.events.get('notice-language')();assert.equal(a.node('tutorial-screen').dataset.step,'3');assert.equal(a.node('tutorial-title').textContent,'tutorial_3_title{}');
});
test('story uses a modal and returns focus to its opener on close',()=>{
 const a=setup();a.node('open-story').listeners.click();assert.equal(a.node('story-dialog').open,true);a.node('close-story').listeners.click();assert.equal(a.node('story-dialog').open,false);assert.equal(a.node('open-story').focused,true);
});


test('fresh launch holds the wordmark without scheduling any automatic advance',()=>{
 for(const reduced of [false,true]) {
  const a=setup('',reduced);assert.equal(a.node('app-shell').hidden,true);assert.equal(a.node('brand-intro').hidden,false);assert.equal(a.timers.size,0);
  a.events.get('notice-language')();assert.equal(a.node('app-shell').hidden,true);assert.equal(a.timers.size,0);
 }
});
test('Continue reveals welcome and returning through history does not replay the title',()=>{
 const a=setup('');a.node('skip-intro').listeners.click();assert.equal(a.node('brand-intro').hidden,true);assert.equal(a.node('app-shell').hidden,false);assert.equal(a.node('welcome-title').focused,true);
 a.click('get-started');a.click('tutorial-back');assert.equal(a.node('welcome-screen').hidden,false);assert.equal(a.node('brand-intro').hidden,true);assert.equal(a.timers.size,0);
});
test('leaving the page does not implicitly accept Continue',()=>{
 const a=setup('');a.events.get('pagehide')?.();assert.equal(a.node('brand-intro').hidden,false);assert.equal(a.node('app-shell').hidden,true);
});
test('direct screen navigation bypasses the title without a timer',()=>{
 const a=setup('#notice');assert.equal(a.node('brand-intro').hidden,true);assert.equal(a.node('notice-screen').hidden,false);assert.equal(a.timers.size,0);
 const b=setup('');b.win.location.hash='#tutorial/3';b.events.get('hashchange')();assert.equal(b.node('tutorial-screen').dataset.step,'3');assert.equal(b.node('brand-intro').hidden,true);
});
