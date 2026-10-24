// Pour Decisions service worker.
// The page is network-first: online, you always get the latest version from the site;
// offline (or on a slow connection), the last saved copy opens instead.
// Bump VERSION when the list of app files below changes.
const VERSION = "v1";
const SHELL = `pd-shell-${VERSION}`;
const FONTS = "pd-fonts";
const SHELL_FILES = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon-32.png",
];
const NETWORK_TIMEOUT_MS = 3500;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(SHELL).then((c) => c.addAll(SHELL_FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== SHELL && k !== FONTS).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
      .then(() => { cacheThemeFonts(); }) // in the background; don't hold up activation
  );
});

// Save every theme's fonts (latin subset) so all themes look right offline,
// not just the ones already opened. The font list is read from the page itself.
async function cacheThemeFonts() {
  try {
    const cache = await caches.open(FONTS);
    const page = await (await caches.open(SHELL)).match("./index.html");
    if (!page) return;
    const href = ((await page.text()).match(/href="(https:\/\/fonts\.googleapis\.com\/css2[^"]+)"/) || [])[1];
    if (!href) return;
    const cssUrl = href.replace(/&amp;/g, "&");
    const res = await fetch(cssUrl);
    if (!res.ok) return;
    await cache.put(cssUrl, res.clone());
    const css = await res.text();
    const files = [...css.matchAll(/\/\* latin \*\/[^}]*?url\((https:[^)]+)\)/g)].map((m) => m[1]);
    for (const f of files) {
      if (!(await cache.match(f))) {
        try { const r = await fetch(f, { mode: "cors" }); if (r.ok) await cache.put(f, r); } catch { /* try again next time */ }
      }
    }
  } catch { /* offline right now; fonts still get saved as they're used */ }
}

// Network first, falling back to the cache. A slow network falls back after a timeout,
// while the fetch keeps going in the background and refreshes the cache for next time.
function networkFirst(request, cacheKey) {
  return caches.open(SHELL).then((cache) => {
    const fromNetwork = fetch(request, { cache: "no-cache" }).then((res) => {
      if (res.ok) cache.put(cacheKey || request, res.clone());
      return res;
    });
    const fallback = () => cache.match(cacheKey || request).then((hit) => hit || fromNetwork);
    const timer = new Promise((resolve) => setTimeout(resolve, NETWORK_TIMEOUT_MS)).then(() => cache.match(cacheKey || request));
    return Promise.race([fromNetwork.catch(fallback), timer.then((hit) => hit || fromNetwork)]).catch(fallback);
  });
}

// Serve from cache right away and refresh it in the background.
function staleWhileRevalidate(request, cacheName) {
  return caches.open(cacheName).then((cache) =>
    cache.match(request).then((hit) => {
      const update = fetch(request).then((res) => {
        if (res.ok || res.type === "opaque") cache.put(request, res.clone());
        return res;
      }).catch(() => hit);
      return hit || update;
    })
  );
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    event.respondWith(staleWhileRevalidate(req, FONTS));
    return;
  }
  if (url.origin !== self.location.origin) return;

  const scopePath = new URL(self.registration.scope).pathname;
  const isPage = req.mode === "navigate" || url.pathname === scopePath || url.pathname.endsWith("/index.html");
  if (isPage) {
    event.respondWith(networkFirst(req, "./index.html"));
  } else {
    event.respondWith(staleWhileRevalidate(req, SHELL));
  }
});
