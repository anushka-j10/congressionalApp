// Actual explanation-controller and voice selection with deterministic transports.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { selectVoice } from '../frontend/speech.js';
const source=readFileSync(new URL('../frontend/explanation.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
const tick=()=>new Promise(resolve=>setImmediate(resolve));
class Element {
  textContent=''; hidden=true; children=[]; listeners=new Map();
  addEventListener(key,callback){this.listeners.set(key,callback);}
  emit(key){return this.listeners.get(key)?.();}
  append(...values){this.children.push(...values);}
}
function setup(){
  const nodes=new Map(), pending=[],shown=[],spoken=[];
  const node=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
  const events=new Element(); let code='es';
  const cfg={direction:'ltr',speech_synthesis_locale:'en-US'};
  const context=vm.createContext({
    document:{querySelector:s=>node(s.slice(1)),getElementById:node,createElement:()=>new Element()},
    window:events,AbortController,setTimeout,clearTimeout,
    t:key=>key,languageCode:()=>code,languageConfig:()=>cfg,helpConfig:()=>({contacts:[{configured:false}]}),
    createSpeechController:()=>({clear(){spoken.length=0;},set(text,configuration){spoken.push(text);}}),
    renderFields:(...args)=>{if(args[5])shown.push(args[5]);},
    fetch:(url,options)=>new Promise(resolve=>pending.push({options,resolve})),
  });
  vm.runInContext(source,context);
  const data={doc_type:'parking_ticket',fields:{},today:'2026-10-22',receipt:'synthetic-receipt'};
  const result=language=>({ok:true,json:async()=>({localized:{summary:'Synthetic '+language,what_happened:'Checked',what_to_do:['Check'],deadline_note:'Due',amount_note:'Amount',confidence_notes:['Double-check']},
    requested_language:language,display_language:language,translation:{translation_confidence:'medium'},notice:'Unreviewed',target_disclaimer:'No legal advice'})});
  return {nodes,node,pending,shown,spoken,events,data,result,context,setCode(value){code=value;}};
}

test('clear aborts and ignores a late explanation reply',async()=>{
  const app=setup(); app.context.setExplanationSource(app.data,'Synthetic original');
  const old=app.pending.shift(); app.context.clearExplanation();
  assert.equal(old.options.signal.aborted,true);
  old.resolve(app.result('es')); await tick();
  assert.equal(app.shown.length,0);assert.equal(app.node('explanation-results').hidden,true);
  assert.equal(app.spoken.length,0);
});

test('language change cannot display the preceding language response',async()=>{
  const app=setup(); app.context.setExplanationSource(app.data,'Synthetic original');
  const old=app.pending.shift(); app.setCode('tl');app.events.emit('notice-language');
  const current=app.pending.shift(); assert.equal(old.options.signal.aborted,true);
  old.resolve(app.result('es')); await tick(); assert.equal(app.shown.length,0);
  current.resolve(app.result('tl')); await tick();
  assert.equal(app.shown.length,1);assert.equal(app.shown[0].display_language,'tl');
});

test('page leave erases the explanation and prevents late speech',async()=>{
  const app=setup();app.context.setExplanationSource(app.data,'Synthetic original');
  const pending=app.pending.shift();app.events.emit('pagehide');pending.resolve(app.result('es'));await tick();
  assert.equal(app.shown.length,0);assert.equal(app.spoken.length,0);
});

test('a network failure never displays partial translated output',async()=>{
  const app=setup();app.context.setExplanationSource(app.data,'Synthetic original');
  app.pending.shift().resolve({ok:false,status:503,json:async()=>({detail:'synthetic error'})});await tick();
  assert.equal(app.shown.length,0);assert.equal(app.node('explanation-error').textContent,'explain_error');
});

test('voice selection refuses another language and supports configured aliases',()=>{
  const voices=[{lang:'en-US'},{lang:'es-MX'},{lang:'fil-PH'}];
  assert.equal(selectVoice({speech_synthesis_locale:'es-US'},voices),voices[1]);
  assert.equal(selectVoice({speech_synthesis_locale:'tl-PH',speech_aliases:['fil-PH']},voices),voices[2]);
  assert.equal(selectVoice({speech_synthesis_locale:'fr-FR'},voices),null);
});


test('OCR highlights use code-point offsets after a non-BMP character and keep markup inert',()=>{
  const module=readFileSync(new URL('../frontend/token-review.js',import.meta.url),'utf8')
    .replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
  const created=[];
  class Node extends Element { constructor(tag){super();this.tag=tag;} }
  const context=vm.createContext({t:key=>key,document:{
    createElement:tag=>{const node=new Node(tag);created.push(node);return node;},
    createTextNode:text=>({textContent:text})}});
  vm.runInContext(module,context);
  const transcript=new Node('pre'), panel=new Node('div');
  const text='😀 Due 2026-11-03 and [unreadable] <script>alert(1)</script>';
  context.renderReading(text,[{status:'disputed',kind:'date',candidates:[{reader:'local',start:6,end:16,value:'2026-11-03'}]}],
    'local',transcript,panel);
  assert.deepEqual(created.filter(node=>node.tag==='mark').map(node=>node.textContent),['2026-11-03','[unreadable]']);
  assert.equal(transcript.children.map(node=>node.textContent).join(''),text);
  assert.equal(created.some(node=>node.tag==='script'),false);
});

for (const failure of ['timeout','rate-limit','malformed-json']) {
  test(`${failure} leaves a fixed localized error and no partial explanation`,async()=>{
    const app=setup();app.context.setExplanationSource(app.data,'Synthetic original');
    const request=app.pending.shift();
    request.resolve(failure==='rate-limit'?{ok:false,status:429,json:async()=>({detail:'PRIVATE-STACK-PROVIDER'})}:
      {ok:true,json:async()=>{const error=new Error('PRIVATE-STACK-PROVIDER');error.name=failure==='timeout'?'AbortError':'SyntaxError';throw error;}});
    await tick();
    assert.equal(app.shown.length,0);
    assert.equal(app.node('explanation-error').textContent,'explain_error');
    assert.equal(app.node('explanation-error').textContent.includes('PRIVATE'),false);
    assert.equal(app.spoken.length,0);
  });
}
