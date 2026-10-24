"use strict";
import { t, initializeLanguages, readerWarning } from "/i18n.js";
import { setExplanationSource, clearExplanation } from "/explanation.js";
import { preparePhoto } from "/image-prep.js";
import { renderFields } from "/field-cards.js";
import { renderReading } from "/token-review.js";

const messages = new Map();
function message(node, key, values = {}) {
  messages.set(node, { key, values });
  node.textContent = t(key, values);
}
const status = document.querySelector("#api-status");
const checkButton = document.querySelector("#check-connection");

async function checkConnection() {
  checkButton.disabled = true;
  message(status, "checking");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("/api/health", { cache: "no-store", signal: controller.signal });
    if (!response.ok) throw new Error("API unavailable");
    const data = await response.json();
    if (data.status !== "ok") throw new Error("Unexpected API response");
    message(status, "connected");
    await loadReaderConfig();
  } catch {
    message(status, "connection_error");
  } finally {
    clearTimeout(timeout);
    checkButton.disabled = false;
  }
}

checkButton.addEventListener("click", checkConnection);
window.addEventListener("online", checkConnection);
window.addEventListener("offline", () => {
  message(status, "offline");
});

const installStatus = document.querySelector("#install-status");
const offlineStatus = document.querySelector("#offline-status");
if (!window.isSecureContext) {
  message(installStatus, "https_required");
} else if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js").then(async () => {
    await navigator.serviceWorker.ready;
    message(offlineStatus, "shell_ready");
  }).catch(() => {
    message(offlineStatus, "shell_error");
  });
} else {
  message(installStatus, "no_install");
}

const camera = document.querySelector("#camera-input");
const library = document.querySelector("#library-input");
const takeButton = document.querySelector("#take-photo");
const chooseButton = document.querySelector("#choose-photo");
const readButton = document.querySelector("#read-photo");
const clearButton = document.querySelector("#clear-photo");
const preview = document.querySelector("#photo-preview");
const readStatus = document.querySelector("#read-status");
const readError = document.querySelector("#read-error");
const results = document.querySelector("#results");
const textEditor = document.querySelector("#confirmed-text");
const typeChoice = document.querySelector("#doc-type-choice");
const fieldResults = document.querySelector("#field-results");
const textChecked = document.querySelector("#text-checked");
const confirmButton = document.querySelector("#confirm-text");
let lastReading = null;
let confirmedText = null;
let preparedPhoto = null;
let previewUrl = null;
let config = null;
let busy = false;
let activeRequest = null;
let requestGeneration = 0;

function updateButtons() {
  takeButton.disabled = chooseButton.disabled = busy;
  textEditor.disabled = textChecked.disabled = typeChoice.disabled = busy;
  confirmButton.disabled = busy || !textChecked.checked || !textEditor.value.trim();
  readButton.disabled = busy || !preparedPhoto || !config;
  clearButton.disabled = !preparedPhoto && results.hidden;
}

async function loadReaderConfig() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("/api/config", { cache: "no-store", signal: controller.signal });
    if (!response.ok) throw new Error();
    config = await response.json();
    message(document.querySelector("#reader-note"), config.external_processing ? 'external_reader' : 'local_reader');
    message(document.querySelector("#classifier-note"), config.classifier_ready ? 'classifier_ready' : 'classifier_empty');
  } catch {
    config = null;
    message(document.querySelector("#reader-note"), "connection_error");
  } finally {
    clearTimeout(timeout);
    updateButtons();
  }
}

function clearResults() {
  lastReading = null;
  results.hidden = true;
  clearFields();
  typeChoice.value = "unknown";
  confirmedText = null;
  textEditor.value = "";
  textChecked.checked = false;
  document.querySelector("#confirmation-status").textContent = "";
  for (const id of ["notice-text", "doc-type", "confidence", "reader-used", "warnings", "signals", "token-reviews"]) {
    document.getElementById(id).textContent = "";
  }
  document.querySelector("#token-reviews").hidden = true;
}

function clearPhoto() {
  requestGeneration += 1;
  activeRequest?.abort();
  activeRequest = null;
  busy = false;
  preparedPhoto = null;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  preview.removeAttribute("src");
  preview.hidden = true;
  camera.value = library.value = "";
  document.querySelector("#photo-details").textContent = "";
  clearResults();
  readStatus.textContent = readError.textContent = "";
  updateButtons();
}

async function selectPhoto(event) {
  const file = event.target.files[0];
  if (!file) return;
  clearPhoto();
  const generation = requestGeneration;
  busy = true;
  updateButtons();
  message(readStatus, "preparing");
  let timeout;
  try {
    const prepared = await Promise.race([
      preparePhoto(file),
      new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error("Photo preparation took too long. Try a smaller photo.")), 30000); }),
    ]);
    if (generation !== requestGeneration) return;
    preparedPhoto = prepared;
    previewUrl = URL.createObjectURL(preparedPhoto);
    preview.src = previewUrl;
    preview.hidden = false;
    message(document.querySelector("#photo-details"), "photo_details", { kb: Math.ceil(preparedPhoto.size / 1024) });
    message(readStatus, "photo_ready");
  } catch (error) {
    if (generation !== requestGeneration) return;
    readStatus.textContent = "";
    message(readError, "prepare_error");
  } finally {
    clearTimeout(timeout);
    camera.value = library.value = "";
    if (generation === requestGeneration) {
      busy = false;
      updateButtons();
    }
  }
}

function fillList(id, values) {
  const list = document.getElementById(id);
  list.textContent = "";
  for (const value of values) {
    const item = document.createElement("li");
    item.textContent = id === "warnings" ? readerWarning(value) : value;
    list.append(item);
  }
}

function showReading(data) {
    message(document.querySelector("#doc-type"), data.doc_type || 'unknown');
    document.querySelector("#confidence").textContent = `${Math.round(data.doc_type_confidence * 100)}% · ${t('heuristic')}`;
    document.querySelector("#reader-used").textContent = data.reader;
    renderReading(data.text, data.token_reviews || [], data.primary_reader || data.reader,
      document.querySelector("#notice-text"), document.querySelector("#token-reviews"));
    fillList("warnings", data.warnings);
    fillList("signals", data.signals.length ? data.signals : [t("no_signals")]);
}

readButton.addEventListener("click", async () => {
  if (!preparedPhoto || !config || busy) return;
  const generation = requestGeneration;
  busy = true;
  updateButtons();
  clearResults();
  readError.textContent = "";
  message(readStatus, "reading");
  const controller = new AbortController();
  activeRequest = controller;
  const timeout = setTimeout(() => controller.abort(), 75000);
  try {
    const body = new FormData();
    body.append("image", preparedPhoto, "notice.jpg");
    const response = await fetch("/api/read", { method: "POST", body, signal: controller.signal, cache: "no-store" });
    const data = await response.json();
    if (generation !== requestGeneration) return;
    if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "We could not read this photo. Please try again.");
    lastReading = data;
    showReading(data);
    textEditor.value = data.text;
    typeChoice.value = data.doc_type || "unknown";
    results.hidden = false;
    document.querySelector("#results-title").focus();
    message(readStatus, "read_done");
  } catch (error) {
    if (generation !== requestGeneration) return;
    readStatus.textContent = "";
    message(readError, error?.name === 'AbortError' ? 'read_timeout' : error instanceof TypeError ? 'connection_error' : 'read_error');
  } finally {
    clearTimeout(timeout);
    if (generation === requestGeneration) {
      activeRequest = null;
      busy = false;
      updateButtons();
    }
  }
});

function clearFields() {
  clearExplanation();
  fieldResults.hidden = true;
  for (const id of ["field-status", "field-error", "field-cards", "field-source", "field-warnings"]) {
    document.getElementById(id).textContent = "";
  }
}

function invalidateConfirmation() {
  clearFields();
  confirmedText = null;
  document.querySelector("#confirmation-status").textContent = "";
  updateButtons();
}
textEditor.addEventListener("input", () => {
  textChecked.checked = false;
  invalidateConfirmation();
});
textChecked.addEventListener("change", invalidateConfirmation);
typeChoice.addEventListener("change", () => {
  textChecked.checked = false;
  invalidateConfirmation();
});
confirmButton.addEventListener("click", async () => {
  if (busy || !textChecked.checked || !textEditor.value.trim()) return;
  const generation = requestGeneration;
  confirmedText = textEditor.value;
  const selectedType = typeChoice.value;
  clearFields();
  fieldResults.hidden = false;
  busy = true;
  updateButtons();
  message(document.querySelector("#confirmation-status"), "confirmed");
  message(document.querySelector("#field-status"), "extracting");
  const controller = new AbortController();
  activeRequest = controller;
  const timeout = setTimeout(() => controller.abort(), 100000);
  try {
    const response = await fetch("/api/extract", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: confirmedText, doc_type: selectedType, text_confirmed: true }),
      signal: controller.signal, cache: "no-store",
    });
    const data = await response.json();
    if (generation !== requestGeneration) return;
    if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Extraction could not finish. Try again.");
    renderFields(data, confirmedText, document.querySelector("#field-cards"),
      document.querySelector("#field-source"), document.querySelector("#field-warnings"));
    message(document.querySelector("#field-status"), selectedType === "unknown" ? "unknown_skipped" : "extract_done");
    document.querySelector("#fields-title").focus();
    setExplanationSource(data, confirmedText);
  } catch (error) {
    if (generation !== requestGeneration) return;
    document.querySelector("#field-status").textContent = "";
    // No partial cards remain after a timeout, provider error, or bad JSON.
    document.querySelector("#field-cards").textContent = "";
    message(document.querySelector("#field-error"), error?.name === 'AbortError' ? 'extract_timeout' : error instanceof TypeError ? 'connection_error' : 'extract_error');
  } finally {
    clearTimeout(timeout);
    if (generation === requestGeneration) {
      activeRequest = null;
      busy = false;
      updateButtons();
    }
  }
});

takeButton.addEventListener("click", () => camera.click());
chooseButton.addEventListener("click", () => library.click());
camera.addEventListener("change", selectPhoto);
library.addEventListener("change", selectPhoto);
clearButton.addEventListener("click", clearPhoto);
window.addEventListener("pagehide", clearPhoto);
window.addEventListener('notice-language', () => {
  for (const [node, entry] of messages) {
    if (node.textContent) node.textContent = t(entry.key, entry.values);
  }
  if (preparedPhoto) document.querySelector('#photo-details').textContent = t('photo_details', { kb: Math.ceil(preparedPhoto.size / 1024) });
  if (lastReading) { showReading(lastReading); readStatus.textContent = t('read_done'); }
  if (config) {
    message(document.querySelector('#reader-note'), config.external_processing ? 'external_reader' : 'local_reader');
    message(document.querySelector('#classifier-note'), config.classifier_ready ? 'classifier_ready' : 'classifier_empty');
  }
});
initializeLanguages().then((ready) => { if (ready) checkConnection(); });
