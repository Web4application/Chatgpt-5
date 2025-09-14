self.addEventListener("install", event => {
  console.log("Service Worker: Installed");
});

self.addEventListener("activate", event => {
  console.log("Service Worker: Activated");
});

self.addEventListener("fetch", event => {
  // Network-first strategy
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});
