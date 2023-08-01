// Web worker to cache assets
const CACHE_NAME = 'libre-chat-assets';

self.addEventListener('install', event => {
    console.log(`Caching`)
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            // Cache all stylesheets and scripts imported in the main HTML file
            const urlsToCache = [];
            const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
            const scripts = document.querySelectorAll('script[src]');

            stylesheets.forEach(link => urlsToCache.push(link.href));
            scripts.forEach(script => urlsToCache.push(script.src));
            console.log(`Caching ${urlsToCache}`)
            return cache.addAll(urlsToCache);
        })
    );
});
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
    );
});
