import { t, languageCode, languageConfig, helpConfig } from '/i18n.js';
import { renderFields } from '/field-cards.js';
import { createSpeechController } from '/speech.js';
let extraction = null;
let sourceText = '';
let controller = null;
let generation = 0;
const section = document.querySelector('#explanation-results');
const speech = createSpeechController({ play: document.querySelector('#speech-play'),
  pause: document.querySelector('#speech-pause'), stop: document.querySelector('#speech-stop'),
  note: document.querySelector('#speech-note') }, t);

export function clearExplanation() {
  generation += 1;
  controller?.abort(); controller = null;
  extraction = null; sourceText = '';
  speech.clear(); section.hidden = true;
  for (const id of ['explanation-body', 'explanation-status', 'explanation-error', 'translation-note', 'help-contacts']) document.getElementById(id).textContent = '';
}

export function setExplanationSource(data, text) {
  clearExplanation();
  extraction = data; sourceText = text;
  generate();
}

function show(data) {
  const bundle = data.localized;
  const body = document.querySelector('#explanation-body');
  body.textContent = '';
  body.lang = data.display_language;
  body.dir = languageConfig(data.display_language).direction;
  const add = (tag, text) => { const node = document.createElement(tag); node.textContent = text; body.append(node); };
  add('p', bundle.summary);
  add('h3', t('what_happened')); add('p', bundle.what_happened);
  add('h3', t('what_to_do'));
  const steps = document.createElement('ol');
  for (const text of bundle.what_to_do) { const li = document.createElement('li'); li.textContent = text; steps.append(li); }
  body.append(steps);
  add('p', bundle.deadline_note); add('p', bundle.amount_note);
  add('h3', t('confidence_notes'));
  for (const text of bundle.confidence_notes) add('p', text);
  add('p', data.target_disclaimer);
  const translation = data.translation;
  document.querySelector('#translation-note').textContent = data.notice + ' ' +
    (translation.translation_confidence === 'low' ? t('confidence_low') : data.requested_language !== 'en' ? t('confidence_medium') : '');
  renderFields(extraction, sourceText, document.querySelector('#field-cards'), document.querySelector('#field-source'),
    document.querySelector('#field-warnings'), data);
  document.querySelector('#help-contacts').textContent = '';
  for (const entry of helpConfig().contacts) {
    // Contacts remain explicitly TODO until the student supplies real resources.
    const p = document.createElement('p'); p.textContent = entry.configured ? entry.name : t('help_todo');
    document.querySelector('#help-contacts').append(p);
  }
  speech.set([bundle.summary, bundle.deadline_note, bundle.amount_note, ...bundle.what_to_do].join('\n'), languageConfig(data.display_language));
}

async function generate() {
  if (!extraction) return;
  controller?.abort(); speech.clear();
  const version = ++generation;
  const data = extraction;
  const text = sourceText;
  const code = languageCode();
  controller = new AbortController();
  const localController = controller;
  const timeout = setTimeout(() => localController.abort(), 190000);
  section.hidden = false;
  document.querySelector('#explanation-body').textContent = '';
  document.querySelector('#translation-note').textContent = t('english_pending');
  document.querySelector('#explanation-error').textContent = '';
  document.querySelector('#explanation-status').textContent = t('explaining');
  document.querySelector('#help-contacts').textContent = t('help_todo');
  renderFields(data, text, document.querySelector('#field-cards'), document.querySelector('#field-source'), document.querySelector('#field-warnings'));
  try {
    const response = await fetch('/api/explain', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Notice-Language': code },
      body: JSON.stringify({ doc_type: data.doc_type, fields: data.fields, today: data.today, receipt: data.receipt, language: code }),
      signal: localController.signal, cache: 'no-store' });
    const result = await response.json();
    if (version !== generation) return;
    if (!response.ok) throw new Error(response.status === 409 ? 'receipt' : 'explain');
    show(result);
    document.querySelector('#explanation-status').textContent = '';
  } catch (error) {
    if (version !== generation) return;
    document.querySelector('#explanation-status').textContent = '';
    document.querySelector('#explanation-error').textContent = t(error.message === 'receipt' ? 'receipt_error' : 'explain_error');
    document.querySelector('#translation-note').textContent = t('english_pending');
  } finally {
    clearTimeout(timeout);
    if (version === generation) controller = null;
  }
}
window.addEventListener('notice-language', () => { if (extraction) generate(); });
window.addEventListener('pagehide', clearExplanation);
document.querySelector('#retry-explanation').addEventListener('click', generate);
