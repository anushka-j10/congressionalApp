// Exercise the actual app controller against delayed network responses. The small
// DOM/provider doubles make clear/navigation races deterministic without a model.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../frontend/app.js', import.meta.url), 'utf8')
  .replace(/^import .*;\n/gm, '');
const tick = () => new Promise(resolve => setImmediate(resolve));
const reading = { text: 'Synthetic notice. Deadline: 2026-10-29. Amount due: $45.00.',
  reader: 'preprocessed', doc_type: 'parking_ticket', doc_type_confidence: 0,
  warnings: [], signals: [] };
const response = data => ({ ok: true, json: async () => data });

class Element {
  value = ''; textContent = ''; hidden = true; disabled = false; checked = false;
  files = []; listeners = new Map();
  addEventListener(name, callback) { this.listeners.set(name, callback); }
  emit(name, event = {}) { return this.listeners.get(name)?.(event); }
  removeAttribute() {} focus() {} click() {} append() {}
}

async function setup() {
  const elements = new Map();
  function el(id) {
    if (!elements.has(id)) elements.set(id, new Element());
    return elements.get(id);
  }
  const pending = [];
  const window = new Element();
  window.isSecureContext = false;
  const context = vm.createContext({
    document: { querySelector: selector => el(selector.slice(1)), getElementById: el, createElement: () => new Element() },
    window, navigator: {}, AbortController, FormData, setTimeout, clearTimeout,
    URL: { createObjectURL: () => 'blob:synthetic', revokeObjectURL() {} },
    readerWarning: value => value, t: key => key, initializeLanguages: async () => true,
    setExplanationSource() {}, clearExplanation() {},
    preparePhoto: async () => new Blob(['synthetic photo'], { type: 'image/jpeg' }),
    renderReading: (text, reviews, primary, transcript) => { transcript.textContent = text; },
    renderFields: (data, text, cards, source) => { cards.textContent = 'verified synthetic cards'; source.textContent = text; },
    fetch: (url, options) => {
      if (url === '/api/health') return Promise.resolve(response({status:'ok'}));
      if (url === '/api/config') return Promise.resolve(response({reader:'preprocessed', external_processing:false, classifier_ready:false}));
      return new Promise(resolve => pending.push({url, options, resolve}));
    },
  });
  vm.runInContext(source, context);
  await tick();
  async function photo() {
    el('library-input').files = [new Blob(['synthetic'])];
    await el('library-input').emit('change', { target: el('library-input') });
  }
  async function read() {
    await photo();
    const task = el('read-photo').emit('click');
    pending.shift().resolve(response(reading));
    await task;
  }
  function extract() {
    el('text-checked').checked = true;
    el('text-checked').emit('change');
    return el('confirm-text').emit('click');
  }
  return {el, pending, window, photo, read, extract};
}

test('clear aborts reading and a late response cannot repopulate text', async () => {
  const app = await setup();
  await app.photo();
  const task = app.el('read-photo').emit('click');
  const pending = app.pending.shift();
  assert.equal(app.el('clear-photo').disabled, false);
  app.el('clear-photo').emit('click');
  assert.equal(pending.options.signal.aborted, true);
  pending.resolve(response(reading)); // Even a transport ignoring abort is safe.
  await task;
  assert.equal(app.el('results').hidden, true);
  assert.equal(app.el('confirmed-text').value, '');
  assert.equal(app.el('notice-text').textContent, '');
  assert.equal(app.el('read-photo').disabled, true);
});

test('late extraction cannot restore cleared cards or unlock a newer read', async () => {
  const app = await setup();
  await app.read();
  const oldTask = app.extract();
  const old = app.pending.shift();
  app.el('clear-photo').emit('click');
  assert.equal(old.options.signal.aborted, true);
  await app.photo();
  const newTask = app.el('read-photo').emit('click');
  const newer = app.pending.shift();
  old.resolve(response({fields:{}, warnings:[]}));
  await oldTask;
  assert.equal(app.el('field-results').hidden, true);
  assert.equal(app.el('field-cards').textContent, '');
  assert.equal(app.el('read-photo').disabled, true);
  assert.equal(app.el('take-photo').disabled, true);
  newer.resolve(response(reading));
  await newTask;
  assert.equal(app.el('confirmed-text').value, reading.text);
});

test('pagehide clears edited text and ignores in-flight extraction', async () => {
  const app = await setup();
  await app.read();
  const task = app.extract();
  const pending = app.pending.shift();
  app.window.emit('pagehide');
  pending.resolve(response({fields:{}, warnings:[]}));
  await task;
  assert.equal(app.el('confirmed-text').value, '');
  assert.equal(app.el('field-source').textContent, '');
  assert.equal(app.el('field-results').hidden, true);
});

test('editing confirmed text removes cards and requires a new confirmation', async () => {
  const app = await setup();
  await app.read();
  const task = app.extract();
  app.pending.shift().resolve(response({fields:{}, warnings:[]}));
  await task;
  assert.equal(app.el('field-cards').textContent, 'verified synthetic cards');
  app.el('confirmed-text').value += ' edited';
  app.el('confirmed-text').emit('input');
  assert.equal(app.el('text-checked').checked, false);
  assert.equal(app.el('confirm-text').disabled, true);
  assert.equal(app.el('field-results').hidden, true);
  assert.equal(app.el('field-cards').textContent, '');
});


test('language change refreshes dynamic statuses without restoring cleared messages', async () => {
  const app=await setup();await app.read();
  const task=app.extract();app.pending.shift().resolve(response({fields:{},today:'2026-10-23'}));await task;
  app.el('confirmation-status').textContent='previous-language';
  app.el('field-status').textContent='previous-language';
  app.window.emit('notice-language');
  assert.equal(app.el('confirmation-status').textContent,'confirmed');
  assert.equal(app.el('field-status').textContent,'extract_done');
  app.el('clear-photo').emit('click');app.window.emit('notice-language');
  assert.equal(app.el('confirmation-status').textContent,'');assert.equal(app.el('field-status').textContent,'');
});
