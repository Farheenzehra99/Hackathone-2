// Service Worker for offline support

const CACHE_NAME = 'todo-app-v1';
const DATA_CACHE_NAME = 'todo-data-v1';

// URLs to cache for offline access
const staticAssets = [
  '/',
  '/dashboard',
  '/dashboard/tasks',
  '/auth/sign-in',
  '/auth/sign-up',
  '/_next/static/css/main.css',
  '/favicon.svg',
  '/manifest.json',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(staticAssets);
      })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== DATA_CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Handle API requests separately
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then((cache) => {
        return fetch(event.request)
          .then((networkResponse) => {
            // Update cache with fresh response
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          })
          .catch(() => {
            // Return cached response if network fails
            return cache.match(event.request);
          });
      })
    );
  } else {
    // Handle static assets
    event.respondWith(
      caches.match(event.request)
        .then((response) => {
          // Return cached version if available, otherwise fetch from network
          if (response) {
            return response;
          }
          return fetch(event.request);
        }
      )
    );
  }
});