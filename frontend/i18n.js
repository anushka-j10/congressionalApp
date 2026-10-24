// Only a language code is persisted. Notices, results and receipts stay in RAM.
let catalogs = {};
let current = 'en';
let help = { contacts: [] };
const storageKey = 'notice-decoder-language';
export const languageCode = () => current;
export const languageConfig = (code = current) => catalogs[code] || catalogs.en;
export const helpConfig = () => help;

export function t(key, values = {}, code = current) {
  let text = catalogs[code]?.ui[key] ?? catalogs.en?.ui[key] ?? '';
  for (const [name, value] of Object.entries(values)) text = text.replaceAll(`{${name}}`, String(value));
  return text;
}

export function formatDate(iso, code = current) {
  const cfg = languageConfig(code);
  const [year, month, day] = iso.split('-').map(Number);
  return cfg.date_format.replace('{day}', String(day)).replace('{month}', cfg.months[month - 1]).replace('{year}', String(year));
}

export function applyLanguage(code, remember = true) {
  current = catalogs[code] ? code : 'en';
  const cfg = languageConfig();
  document.documentElement.lang = current;
  document.documentElement.dir = cfg.direction;
  for (const node of document.querySelectorAll('[data-i18n]')) {
    const text = t(node.dataset.i18n);
    if (text) node.textContent = text;
  }
  for (const node of document.querySelectorAll('[data-i18n-aria]')) node.setAttribute('aria-label', t(node.dataset.i18nAria));
  for (const node of document.querySelectorAll('[data-i18n-alt]')) node.setAttribute('alt', t(node.dataset.i18nAlt));
  const picker = document.querySelector('#language-picker');
  if (picker) picker.value = current;
  if (remember) {
    try { localStorage.setItem(storageKey, current); } catch { /* private/offline browser */ }
  }
  window.dispatchEvent(new Event('notice-language'));
}

export async function initializeLanguages() {
  // Static English is part of the offline shell; all other language data is
  // discovered from backend configs. Adding a language needs no JS branching.
  try {
    const response = await fetch('/en.json', { cache: 'no-store' });
    const english = await response.json();
    catalogs.en = english;
  } catch { return false; }
  try {
    const response = await fetch('/api/languages', { cache: 'no-store' });
    if (response.ok) {
      const data = await response.json();
      catalogs = Object.fromEntries(data.languages.map(cfg => [cfg.code, cfg]));
      help = data.help;
    }
  } catch { /* English remains available offline. */ }
  const picker = document.querySelector('#language-picker');
  picker.textContent = '';
  for (const cfg of Object.values(catalogs)) {
    const option = document.createElement('option');
    option.value = cfg.code;
    option.textContent = cfg.display_name;
    picker.append(option);
  }
  let remembered;
  try { remembered = localStorage.getItem(storageKey); } catch { /* no storage */ }
  const preferred = (navigator.languages || [navigator.language || 'en']).map(value => value.toLowerCase().split('-')[0]);
  const match = Object.values(catalogs).find(cfg => preferred.includes(cfg.code) || (cfg.aliases || []).some(alias => preferred.includes(alias)));
  applyLanguage(catalogs[remembered] ? remembered : match?.code || 'en', false);
  picker.addEventListener('change', () => applyLanguage(picker.value));
  return true;
}

export function readerWarning(text) {
  const cfg = languageConfig();
  const rule = (cfg.reader_warning_patterns || []).find(item => new RegExp(item.pattern, 'i').test(text));
  return t(rule?.key || 'warning_review');
}
