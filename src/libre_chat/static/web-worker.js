// Add web worker to cache assets
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


// const urlsToCache = [
//     "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css",
// ];
// self.addEventListener('install', event => {
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//         .then(cache => cache.addAll(urlsToCache))
//     );
// });
// self.addEventListener('fetch', event => {
//     event.respondWith(
//         caches.match(event.request)
//         .then(response => {
//             return response || fetch(event.request);
//         })
//     );
// });
