importScripts("https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js");

var CacheFirst = workbox.strategies.CacheFirst;
var StaleWhileRevalidate = workbox.strategies.StaleWhileRevalidate;
var CacheableResponse = workbox.cacheableResponse.CacheableResponse;
var registerRoute = workbox.routing.registerRoute;
var ExpirationPlugin = workbox.expiration.ExpirationPlugin;
var precacheAndRoute = workbox.precaching.precacheAndRoute;
var CacheableResponsePlugin = workbox.cacheableResponse.CacheableResponsePlugin;

workbox.setConfig({
  skipWaiting: true,
  clientsClaim: true,
});

// Cache images
registerRoute(
  /\.(?:png|gif|jpg|jpeg|webp|svg|ico)$/,
  new CacheFirst({
    cacheName: "images",
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 60 * 60 * 24 * 30,
      }),
    ],
  })
);

// Cache Google Fonts stylesheets
registerRoute(
  /^https:\/\/fonts\.googleapis\.com/,
  new StaleWhileRevalidate({
    cacheName: "google-fonts-stylesheets",
  })
);

// Cache Google Fonts webfont files
registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new CacheFirst({
    cacheName: "google-fonts-webfonts",
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60 * 24 * 365,
      }),
    ],
  })
);

// Cache js and css
registerRoute(/\.(?:js|css)$/, new StaleWhileRevalidate());

// Cache urls
precacheAndRoute(
  [
    {
      url: "/index.html",
      revision: "320ec9",
    },
  ],
  {
    cleanUrls: true,
  }
);