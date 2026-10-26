import { t, formatDate, languageConfig } from '/i18n.js';
// All notice/model strings become text nodes, never markup, links, or commands.
export function renderFields(data, text, cards, source, warnings, presentation = null) {
  cards.textContent = warnings.textContent = "";
  source.textContent = text;
  const code = presentation?.display_language || 'en';
  cards.lang = code;
  cards.dir = languageConfig(code).direction;
  // Each uncertainty is visible in its card; don't repeat the same list above it.
  const names = ['deadline', 'amount_due', 'required_action', 'contact', 'issuing_agency'];
  function showSource(field) {
    source.textContent = "";
    // Python offsets count Unicode code points; JS string indices count UTF-16.
    const chars = Array.from(text);
    const spans = [[field.source_start, field.source_end], [field.anchor_start, field.anchor_end]]
      .filter(([start, end]) => Number.isInteger(start) && Number.isInteger(end) && start >= 0 && end > start && end <= chars.length)
      .sort((a, b) => a[0] - b[0]);
    let cursor = 0;
    for (const [start, end] of spans) {
      if (start < cursor) continue;
      source.append(document.createTextNode(chars.slice(cursor, start).join("")));
      const mark = document.createElement("mark");
      mark.textContent = chars.slice(start, end).join("");
      source.append(mark);
      cursor = end;
    }
    source.append(document.createTextNode(chars.slice(cursor).join("")));
    const panel = source.closest?.('details');
    if (panel) panel.open = true;
    source.focus();
    source.querySelector("mark")?.scrollIntoView({ block: "nearest" });
  }
  for (const name of names) {
    const label = t(name);
    const field = data.fields[name];
    const card = document.createElement("article");
    card.className = `field-card ${field.status}`;
    const heading = document.createElement("h3");
    heading.lang = languageConfig().code;
    heading.textContent = label;
    const badge = document.createElement("span");
    badge.className = "field-badge";
    badge.lang = languageConfig().code;
    badge.textContent = t(field.status);
    const value = document.createElement("p");
    value.className = "field-value";
    if (presentation) value.textContent = presentation.localized.cards[name];
    else if (field.status !== "verified") value.textContent = t(`field_${field.status}`, { field: t(name, {}, 'en') }, 'en');
    else value.textContent = name === 'amount_due' ? `$${field.normalized_value}` : name === 'deadline' ? formatDate(field.normalized_value, 'en') : field.value;
    const prefix = `${t(name, {}, code)}: `;
    if (field.status !== 'verified' && value.textContent.startsWith(prefix)) value.textContent = value.textContent.slice(prefix.length);
    // The shared verification definition is shown once above the facts.
    card.append(heading, badge, value);
    if (field.status === "verified" && Number.isInteger(field.days_remaining)) {
      const days = document.createElement("p");
      days.textContent = t(field.days_remaining < 0 ? 'days_past' : field.days_remaining === 0 ? 'due_today' : 'days_remaining',
        { days: Math.abs(field.days_remaining), date: formatDate(data.today, code) });
      card.append(days);
    }
    const original = document.createElement('details');
    original.lang = languageConfig().code;
    const toggle = document.createElement('summary'); toggle.textContent = t('show_english');
    const snippet = document.createElement('pre'); snippet.lang = 'en'; snippet.dir = 'ltr';
    snippet.textContent = field.source_snippet || t('field_missing', { field: t(name, {}, 'en') }, 'en');
    original.append(toggle, snippet);
    if (Number.isInteger(field.source_start)) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "secondary";
      button.textContent = t('show_source');
      button.setAttribute('aria-label', t('show_source_for', { field: label }));
      button.addEventListener("click", () => showSource(field));
      original.append(button);
    }
    card.append(original);
    cards.append(card);
  }
}
