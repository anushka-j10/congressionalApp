import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const code=readFileSync(new URL('../frontend/onboarding.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
function setup(hash='') {
  const nodes=new Map(), events=new Map();
  const node=id=>{if(!nodes.has(id))nodes.set(id,{hidden:false,dataset:{},listeners:{},textContent:'',focus(){this.focused=true;},addEventListener(k,v){this.listeners[k]=v;},showModal(){this.open=true;},close(){this.open=false;this.listeners.close();}});return nodes.get(id);};
  const win={location:{hash},addEventListener(k,v){events.set(k,v);}};
  const ctx=vm.createContext({document:{getElementById:node},window:win,t:(key,values={})=>key+JSON.stringify(values)});
  vm.runInContext(code,ctx);
  const click=id=>{node(id).listeners.click();events.get('hashchange')();};
  return {node,win,events,click};
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
