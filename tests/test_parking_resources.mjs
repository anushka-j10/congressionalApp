import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {parkingData, parkingRoute, knownParkingState} from '../frontend/parking-data.js';
const read = path => readFileSync(new URL(path, import.meta.url), 'utf8');
const catalogs = Object.fromEntries(['en','es','tl'].map(code => [code, JSON.parse(read(`../backend/languages/${code}.json`))]));
class Element {
  value=''; textContent=''; children=[]; hidden=false; disabled=false; listeners={};
  constructor(tag='div'){this.tag=tag;}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=nodes;}
  addEventListener(key, fn){this.listeners[key]=fn;}
  change(value){this.value=value;this.listeners.change({target:this});}
}
function setup() {
  const nodes=new Map(), events=new Map();let lang='en';
  const node=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
  const ctx=vm.createContext({URL,parkingData,parkingRoute,knownParkingState,
    document:{getElementById:node,createElement:tag=>new Element(tag)},
    window:{addEventListener:(key,fn)=>events.set(key,fn)},
    t:(key,values={})=>Object.entries(values).reduce((text,[k,v])=>text.replaceAll(`{${k}}`,v),catalogs[lang].ui[key]||'')});
  vm.runInContext(read('../frontend/parking.js').replace(/^import .*;\n/gm,'').replace(/^export /gm,''),ctx);
  ctx.initializeParking();
  const all=el=>[el,...el.children.flatMap(all)];
  return {node,ctx,hasState:()=>vm.runInContext('hasParkingState()',ctx),language(code){lang=code;events.get('notice-language')();},
    links(){return all(node('parking-guidance')).filter(n=>n.tag==='a');},
    text(){return all(node('parking-guidance')).map(n=>n.textContent).join(' ');}};
}
test('nine researched Northeast states each have a specifically scoped source route',()=>{
 assert.deepEqual(parkingData.states.map(s=>s.code).sort(),['CT','MA','ME','NH','NJ','NY','PA','RI','VT']);
 assert.equal(new Set(parkingData.routes.map(r=>r.id)).size,parkingData.routes.length);
 for(const state of parkingData.states) assert.ok(parkingData.routes.some(r=>r.state===state.code));
 for(const r of parkingData.routes){
  for(const url of [r.url,r.source_url]) {const u=new URL(url);assert.equal(u.protocol,'https:');assert.equal(u.username,'');assert.equal(u.password,'');}
  assert.ok(new URL(r.source_url).hostname.endsWith('.gov') || new URL(r.source_url).hostname === 'www.hanovernh.org');
  for(const lang of ['en','es','tl']) assert.ok(catalogs[lang].ui[r.instruction_key]);
 }
});
test('no state-only routing and no NYC default for another New York issuer',()=>{
 for(const s of parkingData.states) assert.equal(parkingRoute(s.code,''),null);
 assert.equal(parkingRoute('NY','nyc').state,'NY');
 for(const input of ['albany','NYC','private','<script>','https://evil.example']) assert.equal(parkingRoute('NY',input),null);
 assert.equal(parkingRoute('NJ','nyc'),null);assert.equal(parkingRoute('CA','nyc'),null);
});
test('a fresh page requires an explicit choice, including unsure or another state',()=>{
 const a=setup();assert.equal(a.hasState(),false);assert.equal(a.node('state-continue').disabled,true);assert.equal(a.links().length,0);
 for(const value of ['unsure','other']){a.node('state-picker').change(value);assert.equal(a.hasState(),true);assert.equal(a.node('state-continue').disabled,false);assert.equal(a.links().length,0);assert.match(a.text(),/not researched/);}
 a.node('state-picker').change('CA');assert.equal(a.hasState(),false);assert.equal(a.links().length,0);
});
test('every configured issuer renders its own link and three directions, with no data in the URL',()=>{
 const a=setup();
 for(const r of parkingData.routes){
  a.node('state-picker').change(r.state);assert.equal(a.links().length,0);
  a.node('parking-issuer').change(r.id);
  assert.equal(a.links()[0].href,r.url);assert.equal(a.links()[1].href,r.source_url);
  assert.equal(a.node('parking-guidance').children[0].children.length,3);
  for(const link of a.links()){assert.equal(link.target,'_blank');assert.equal(link.rel,'noopener noreferrer');assert.equal(link.referrerPolicy,'no-referrer');}
 }
});
test('switching states clears the issuer and cannot retain or accept an old destination',()=>{
 const a=setup();a.node('state-picker').change('NJ');a.node('parking-issuer').change('nj-municipal');assert.equal(a.links().length,2);
 a.node('parking-state-picker').change('NY');assert.equal(a.node('state-picker').value,'NY');assert.equal(a.node('parking-issuer').value,'');assert.equal(a.links().length,0);
 a.node('parking-issuer').change('nj-municipal');assert.equal(a.links().length,0);
 a.node('parking-issuer').change('nyc');assert.match(a.links()[0].href,/nyc.gov/);
 a.node('parking-state-picker').change('other');assert.equal(a.links().length,0);
});
test('unlisted, private and campus issuers get contact guidance, never a guessed payment site',()=>{
 const a=setup();
 for(const s of parkingData.states){a.node('state-picker').change(s.code);a.node('parking-issuer').change('other');assert.match(a.text(),/not checked a payment link/);
  assert.ok(a.links().every(link=>link.href===parkingData.directories[s.code]));
 }
});
test('locale changes preserve selections while updating route directions and labels',()=>{
 const a=setup();a.node('state-picker').change('NJ');a.node('parking-issuer').change('nj-municipal');
 for(const lang of ['es','tl','en']){a.language(lang);assert.equal(a.node('state-picker').value,'NJ');assert.equal(a.node('parking-issuer').value,'nj-municipal');assert.ok(a.text().includes(catalogs[lang].ui.parking_route_nj));assert.equal(a.links()[0].textContent,catalogs[lang].ui.parking_open_nj);}
});
test('no notice extraction, location access, persistence or external requests in the directory controller',()=>{
 const source=read('../frontend/parking.js');
 for(const pattern of [/\bfetch\s*\(/,/localStorage/,/sessionStorage/,/geolocation/,/innerHTML/,/confirmed-text/,/source_snippet/]) assert.doesNotMatch(source,pattern);
 const a=setup();a.node('state-picker').change('NJ');assert.equal(setup().node('state-picker').value,'');
});
test('offline shell includes both resource modules and English includes all new UI copy',()=>{
 const sw=read('../frontend/sw.js');for(const file of ['/parking-data.js','/parking.js']) assert.ok(sw.includes(`"${file}"`));
 assert.deepEqual(JSON.parse(read('../frontend/en.json')),catalogs.en);
 for(const lang of ['es','tl'])for(const key of Object.keys(catalogs.en.ui).filter(k=>/^(parking_|state_)/.test(k)))assert.ok(catalogs[lang].ui[key],`${lang} ${key}`);
});
