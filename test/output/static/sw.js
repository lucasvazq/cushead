importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
const {CacheFirst, StaleWhileRevalidate} = workbox.strategies;
const {CacheableResponse} = workbox.cacheableResponse;
const {registerRoute} = workbox.routing;
const {ExpirationPlugin} = workbox.expiration
const {precacheAndRoute} = workbox.precaching
const {CacheableResponsePlugin} = workbox.cacheableResponse
workbox.setConfig({
  skipWaiting: true,
  clientsClaim: true
});

// Cache not very dynamic images
registerRoute(
  /\.(?:png|gif|jpg|jpeg|webp|svg|ico)$/,
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60 // one month
      })
    ]
  })
);

// Cache Google Fonts stylesheets
registerRoute(
  /^https:\/\/fonts\.googleapis\.com/,
  new StaleWhileRevalidate({
    cacheName: 'google-fonts-stylesheets',
  })
);

// Cache Google Fonts webfont files
registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new CacheFirst({
    cacheName: 'google-fonts-webfonts',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60 * 24 * 365 // one year
      })
    ]
  })
);

// Cache js and css
registerRoute(/\.(?:js|css)$/, new StaleWhileRevalidate());

// Cache urls
precacheAndRoute([
  {url: "/index.html", revision: "f2c934"}
], {
  cleanUrls: true
});