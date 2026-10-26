"use strict";

const CACHE_NAME = "notice-decoder-shell-v13";
const SHELL = ["/", "/index.html", "/styles.css", "/app.js", "/image-prep.js", "/token-review.js", "/field-cards.js", "/i18n.js", "/explanation.js", "/speech.js", "/en.json", "/vendor/heic-to.js", "/manifest.webmanifest", "/icons/icon-192.png", "/icons/icon-512.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(
    keys.filter((key) => key.startsWith("notice-decoder-shell-") && key !== CACHE_NAME)
      .map((key) => caches.delete(key))
  )).then(() => self.clients.claim()));
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // Only cache the fixed shell allowlist. API responses and future uploads
  // must never enter this cache.
  if (event.request.method !== "GET" || url.origin !== self.location.origin || !SHELL.includes(url.pathname)) return;
  event.respondWith(fetch(event.request).catch(() => caches.match(url.pathname)));
});
