import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const code=readFileSync(new URL('../frontend/field-cards.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
class Node {
  constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.events={};}
  append(...nodes){this.children.push(...nodes);}
  addEventListener(name,fn){this.events[name]=fn;}
  focus(){this.focused=true;}
  querySelector(){return {scrollIntoView(){}};}
}
test('compact cards retain warnings, literal snippets and an accessible full-source action',()=>{
  const context=vm.createContext({t:key=>key,formatDate:x=>x,languageConfig:()=>({direction:'ltr'}),
    document:{createElement:tag=>new Node(tag),createTextNode:text=>({textContent:text})}});
  vm.runInContext(code,context);
  const names=['issuing_agency','required_action','deadline','amount_due','contact'];
  const text='<script>not code</script> Due 2026-11-02';
  const fields=Object.fromEntries(names.map(name=>[name,{status:'verified',value:'Example',normalized_value:'2026-11-02',source_snippet:text,source_start:0,source_end:24}]));
  fields.contact={status:'missing',value:'DO NOT DISPLAY',source_snippet:null};
  const cards=new Node('div'),source=new Node('pre'),warnings=new Node('ul'),panel={open:false};
  source.closest=()=>panel;
  context.renderFields({fields,today:'2026-10-25'},text,cards,source,warnings);
  assert.deepEqual(cards.children.map(card=>card.children[0].textContent),['deadline','amount_due','required_action','contact','issuing_agency']);
  assert.equal(warnings.children.length,1);
  assert.equal(cards.children[3].children[2].textContent,'field_missing');
  const details=cards.children[0].children.at(-1);
  assert.equal(details.tag,'details');
  assert.equal(details.children[1].textContent,text);
  assert.equal(details.children[2].tag,'button');
  details.children[2].events.click();
  assert.equal(panel.open,true);
  assert.equal(source.focused,true);
  assert.equal(source.children.map(n=>n.textContent).join(''),text);
  assert.equal(source.children.some(n=>n.tag==='script'),false);
});
