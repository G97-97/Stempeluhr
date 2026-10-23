// Stempeluhr Offline-Cache (Version e282b49d32)
const CACHE = "stempeluhr-e282b49d32";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable.png", "apple-touch-icon.png", "fonts/f1.woff2", "fonts/f2.woff2", "fonts/f3.woff2", "fonts/f4.woff2", "fonts/f5.woff2", "fonts/f6.woff2"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request).catch(() => caches.match("index.html"))));
});
