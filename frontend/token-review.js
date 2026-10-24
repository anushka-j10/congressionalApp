import { t } from '/i18n.js';
// Render only actual reader candidates; document text always stays inert text.
export function renderReading(text, reviews, primaryReader, transcript, panel) {
  transcript.textContent = "";
  panel.textContent = "";
  panel.hidden = reviews.length === 0;
  const chars = Array.from(text);
  const ranges = reviews.filter((review) => review.status === "disputed")
    .flatMap((review) => review.candidates)
    .filter((candidate) => candidate.reader === primaryReader &&
      chars.slice(candidate.start, candidate.end).join('') === candidate.value)
    ;
  // These literal markers indicate uncertainty; they are never auto-corrected.
  for (const match of text.matchAll(/\[unreadable\]|\uFFFD+/gi)) {
    const start = Array.from(text.slice(0, match.index)).length;
    ranges.push({ start, end: start + Array.from(match[0]).length });
  }
  ranges.sort((a, b) => a.start - b.start);
  let cursor = 0;
  for (const range of ranges) {
    if (range.start < cursor) continue;
    transcript.append(document.createTextNode(chars.slice(cursor, range.start).join('')));
    const mark = document.createElement("mark");
    mark.textContent = chars.slice(range.start, range.end).join('');
    mark.title = t('uncertain_reading');
    transcript.append(mark);
    cursor = range.end;
  }
  transcript.append(document.createTextNode(chars.slice(cursor).join('') || (!text ? t('empty_reading') : "")));
  if (!reviews.length) return;
  const heading = document.createElement("h3");
  heading.textContent = t('reader_reviews');
  const note = document.createElement("p");
  note.className = "hint";
  note.textContent = t('agreement_help');
  panel.append(heading, note);
  for (const review of reviews) {
    const card = document.createElement("div");
    card.className = `token-card ${review.status === "agreed" ? "agreed" : "disputed"}`;
    const label = document.createElement("strong");
    label.textContent = `${t('reader_' + review.kind)} · ${review.status === "agreed" ? t("agreed") : t("disputed")}`;
    card.append(label);
    for (const candidate of review.candidates) {
      const line = document.createElement("p");
      line.textContent = `${candidate.reader}: ${candidate.value}`;
      card.append(line);
    }
    panel.append(card);
  }
}
