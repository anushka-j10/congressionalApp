import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const code=readFileSync(new URL('../frontend/field-cards.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
class Node {
  constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.events={};}
  append(...nodes){this.children.push(...nodes);}
  addEventListener(name,fn){this.events[name]=fn;}
  setAttribute(name,value){this[name]=value;}
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
  assert.equal(warnings.children.length,0); // uncertainty remains in the card, once
  assert.equal(cards.children[3].children[2].textContent,'field_missing');
  const details=cards.children[0].children.at(-1);
  assert.equal(details.tag,'details');
  assert.equal(details.children[1].textContent,text);
  assert.equal(details.children[2].tag,'button');
  assert.equal(details.children[2]['aria-label'],'show_source_for');
  details.children[2].events.click();
  assert.equal(panel.open,true);
  assert.equal(source.focused,true);
  assert.equal(source.children.map(n=>n.textContent).join(''),text);
  assert.equal(source.children.some(n=>n.tag==='script'),false);
});

test('English pending facts keep English field names while UI labels use the selected language',()=>{
  const catalogs=Object.fromEntries(['en','es'].map(lang=>[lang,JSON.parse(readFileSync(new URL(`../backend/languages/${lang}.json`,import.meta.url),'utf8'))]));
  const t=(key,values={},lang='es')=>Object.entries(values).reduce((text,[key,value])=>text.replaceAll(`{${key}}`,value),catalogs[lang].ui[key]);
  const context=vm.createContext({t,formatDate:x=>x,languageConfig:(lang='es')=>catalogs[lang],
    document:{createElement:tag=>new Node(tag),createTextNode:text=>({textContent:text})}});
  vm.runInContext(code,context);
  const fields=Object.fromEntries(['deadline','amount_due','required_action','contact','issuing_agency'].map(name=>[name,{status:'missing',value:null,source_snippet:null}]));
  fields.amount_due={status:'unverified',value:'PRIVATE-CANDIDATE',source_snippet:null};
  const cards=new Node('div');
  context.renderFields({fields,today:'2026-10-26'},'',cards,new Node('pre'),new Node('ul'));
  assert.equal(cards.lang,'en');
  assert.equal(cards.children[0].children[0].textContent,catalogs.es.ui.deadline);
  assert.equal(cards.children[0].children[0].lang,'es');
  assert.equal(cards.children[0].children[1].lang,'es');
  assert.equal(cards.children[0].children[2].textContent,t('field_missing',{field:'Deadline'},'en').slice('Deadline: '.length));
  assert.equal(cards.children[1].children[2].textContent.includes('PRIVATE-CANDIDATE'),false);
  assert.equal(cards.children[1].children.at(-1).lang,'es');
});
