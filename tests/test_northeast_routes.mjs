// Corpus-driven routing checks are independent of OCR/model extraction.
// A person must explicitly select the issuer; no city is inferred from a notice.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {parkingRoute, knownParkingState} from '../frontend/parking-data.js';
const dir = new URL('../eval/northeast_stress/corpus/',import.meta.url);
const manifest = JSON.parse(readFileSync(new URL('manifest.json',dir),'utf8'));
for (const name of manifest.cases) {
  const c=JSON.parse(readFileSync(new URL(name,dir),'utf8'));
  test(`stress ${c.id}: ${c.route_id ? 'explicit issuer route' : 'unlisted issuer abstains'}`,()=>{
    assert.equal(knownParkingState(c.state),true);
    assert.equal(parkingRoute(c.state,''),null);
    if (c.route_id) {
      const route=parkingRoute(c.state,c.route_id);
      assert.ok(route);
      assert.equal(new URL(route.url).protocol,'https:');
      for (const other of manifest.states.filter(s=>s!==c.state)) assert.equal(parkingRoute(other,c.route_id),null);
    } else {
      assert.equal(parkingRoute(c.state,'other'),null);
      assert.equal(parkingRoute(c.state,c.issuer),null);
    }
  });
}
