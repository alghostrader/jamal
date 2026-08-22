/* Support Replies — service worker, scoped to /replies only (never touches the rest of the dashboard). */
const V = 'replies-v1';
const SHELL = ['/replies', '/replies-icon-192.png', '/replies-icon-512.png', '/replies.webmanifest'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Cross-origin: only cache the immutable Firebase SDK from gstatic. Everything else (Firestore,
  // auth, Google APIs) passes straight through to the network — never cached, never intercepted.
  if (url.origin !== location.origin) {
    if (url.origin === 'https://www.gstatic.com') {
      e.respondWith(caches.open(V).then((c) =>
        c.match(req).then((hit) => hit || fetch(req).then((res) => {
          if (res && res.ok) c.put(req, res.clone());
          return res;
        }))
      ));
    }
    return;
  }

  // Same-origin page load -> network first (fresh), fall back to cached shell when offline.
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then((res) => { caches.open(V).then((c) => c.put('/replies', res.clone())); return res; })
        .catch(() => caches.match('/replies'))
    );
    return;
  }

  // Same-origin assets (icons, manifest) -> cache first.
  e.respondWith(caches.match(req).then((hit) => hit || fetch(req)));
});
