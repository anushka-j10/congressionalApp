import { t } from '/i18n.js';
import { parkingData, parkingRoute, knownParkingState } from '/parking-data.js';

// State and issuer live only in this page's memory. Never inspect notice text,
// request location permission, send selections to a model, or attach ticket data to URLs.
let state = '';
let issuer = '';
const node = id => document.getElementById(id);
const allowedState = value => knownParkingState(value) || ['other', 'unsure'].includes(value);
export const hasParkingState = () => allowedState(state);
function option(value, label) {
  const element = document.createElement('option');
  element.value = value;
  element.textContent = label;
  return element;
}
function stateOptions(select) {
  select.replaceChildren(option('', t('state_choose')));
  for (const item of parkingData.states) select.append(option(item.code, item.name));
  select.append(option('other', t('state_other')), option('unsure', t('state_unsure')));
  select.value = state;
}
function paragraph(text, className = '') {
  const element = document.createElement('p');
  element.className = className;
  element.textContent = text;
  return element;
}
function officialLink(label, url, className = '') {
  const link = document.createElement('a');
  link.textContent = label;
  // URL arguments come exclusively from the bundled directory, not user input.
  link.href = url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.referrerPolicy = 'no-referrer';
  link.className = className;
  return link;
}
function renderGuidance() {
  const output = node('parking-guidance');
  output.replaceChildren();
  const route = parkingRoute(state, issuer);
  if (route) {
    const steps = document.createElement('ol');
    for (const key of ['parking_match', route.instruction_key, 'parking_check_options']) {
      const item = document.createElement('li');
      item.textContent = t(key);
      steps.append(item);
    }
    output.append(steps, officialLink(t(route.id === 'nj-municipal' ? 'parking_open_nj' : 'parking_open'), route.url, 'parking-link'),
      paragraph(new URL(route.url).hostname, 'parking-domain'),
      paragraph(t('parking_external'), 'hint'),
      officialLink(t('parking_source', { date: parkingData.checked_on }), route.source_url));
  } else {
    output.append(paragraph(t(!state ? 'state_choose' : !knownParkingState(state) ? 'parking_unsupported' : issuer ? 'parking_unlisted' : 'parking_select')));
    const directory = parkingData.directories[state];
    if (directory && issuer) output.append(officialLink(t('parking_directory'), directory));
  }
}
function renderParking() {
  for (const id of ['state-picker', 'parking-state-picker']) stateOptions(node(id));
  node('state-continue').disabled = !hasParkingState();
  const current = parkingData.states.find(item => item.code === state);
  node('parking-summary').textContent = current ? t('parking_summary', {state:current.name}) : t('parking_title');
  node('parking-issuer-control').hidden = !current;
  const picker = node('parking-issuer');
  picker.replaceChildren(option('', t('parking_choose_issuer')));
  for (const route of parkingData.routes.filter(route => route.state === state)) {
    picker.append(option(route.id, route.issuer.startsWith('parking_') ? t(route.issuer) : route.issuer));
  }
  picker.append(option('other', t('parking_other_issuer')));
  picker.value = issuer;
  renderGuidance();
}
export function initializeParking() {
  for (const id of ['state-picker', 'parking-state-picker']) {
    node(id).addEventListener('change', event => {
      const value = event.target.value;
      state = allowedState(value) ? value : '';
      issuer = ''; // A new state must never retain a previous payment destination.
      renderParking();
    });
  }
  node('parking-issuer').addEventListener('change', event => {
    const value = event.target.value;
    issuer = value === 'other' || parkingRoute(state, value) ? value : '';
    renderGuidance();
  });
  window.addEventListener('notice-language', renderParking);
  renderParking();
}
