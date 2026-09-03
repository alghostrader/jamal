/* Deprecated: /replies is no longer a PWA. This stub self-unregisters and clears its caches. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    try { const ks = await caches.keys(); await Promise.all(ks.map((k) => caches.delete(k))); } catch (_) {}
    try { await self.registration.unregister(); } catch (_) {}
    const cs = await self.clients.matchAll();
    cs.forEach((c) => c.navigate(c.url));
  })());
});
self.addEventListener('fetch', () => {}); // passthrough
