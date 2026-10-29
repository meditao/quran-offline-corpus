'use strict';

/* Sürüm ancak bütün dosyalar kopyalandığında yayımlanır; başarısız güncelleme eski sürümü korur. */
const CACHE_PREFIX = `quran-research-v1-${encodeURIComponent(self.registration.scope)}-`;
const MARKER = new URL('__offline_complete__', self.registration.scope).href;
let installationProgress = null;
async function broadcast(message) { const clients = await self.clients.matchAll({type:'window', includeUncontrolled:true}); clients.forEach(client => client.postMessage(message)); }
async function completeCache() {
  const keys = (await caches.keys()).filter(name => name.startsWith(CACHE_PREFIX));
  for (const key of keys.reverse()) {
    const cache = await caches.open(key); const marker = await cache.match(MARKER);
    if (marker) return {cache, key, marker:await marker.json()};
  }
  return null;
}
async function installCache() {
  let cacheName;
  try {
    const response = await fetch(new URL('manifest.json', self.registration.scope), {cache:'no-store'});
    if (!response.ok) throw new Error('Çevrimdışı dosya listesi açılamadı.');
    const manifest = await response.json();
    if (!manifest.buildId || !Array.isArray(manifest.files) || !manifest.files.length) throw new Error('Çevrimdışı dosya listesi geçersiz.');
    if (self.CORPUS_BUILD_ID && manifest.buildId !== self.CORPUS_BUILD_ID) throw new Error('Uygulama ve dosya listesi farklı derlemelerden; yeniden deneyin.');
    cacheName = `${CACHE_PREFIX}${manifest.buildId}`;
    const cache = await caches.open(cacheName);
    const marker = await cache.match(MARKER);
    if (marker) { await broadcast({type:'CACHE_READY',buildId:manifest.buildId}); return; }
    const urls = [...new Set(['./', 'manifest.json', ...manifest.files])].map(path => { const url = new URL(path, self.registration.scope); if (url.origin !== self.location.origin || !url.href.startsWith(self.registration.scope)) throw new Error('Çevrimdışı dosya liste yolu kapsam dışında.'); return url.href; });
    let done = 0;
    installationProgress = {type:'CACHE_PROGRESS',done,total:urls.length};
    await broadcast(installationProgress);
    let next = 0, cancelled = false;
    const downloads = await Promise.allSettled(Array.from({length:Math.min(5, urls.length)}, async () => {
      while (next < urls.length && !cancelled) {
        try {
          const url = urls[next++];
          const existing = await cache.match(url);
          if (!existing) { const file = await fetch(url, {cache:'no-store'}); if (!file.ok) throw new Error(`Dosya kopyalanamadı: ${url}`); if (cancelled) return; await cache.put(url, file); }
          if (cancelled) return;
          done++; installationProgress = {type:'CACHE_PROGRESS',done,total:urls.length};
          if (done % 5 === 0 || done === urls.length) await broadcast(installationProgress);
        } catch(error) { cancelled = true; throw error; }
      }
    }));
    const failed = downloads.find(result => result.status === 'rejected');
    if (failed) throw failed.reason;
    // Derleme dosyalar indirilirken değiştiyse karışık bir sürüm yayımlama.
    const latest = await fetch(new URL('manifest.json', self.registration.scope), {cache:'no-store'});
    if (!latest.ok || (await latest.json()).buildId !== manifest.buildId) throw new Error('Kopyalama sırasında derleme değişti; yeniden deneyin.');
    await cache.put(MARKER, new Response(JSON.stringify({buildId:manifest.buildId, completedAt:Date.now(), files:urls.length}), {headers:{'Content-Type':'application/json'}}));
    installationProgress = null;
    await broadcast({type:'CACHE_READY',buildId:manifest.buildId});
  } catch(error) {
    installationProgress = null;
    if (cacheName) { const cache = await caches.open(cacheName); if (!await cache.match(MARKER)) await caches.delete(cacheName); }
    await broadcast({type:'CACHE_ERROR',message:error.message});
    throw error;
  }
}
self.addEventListener('install', event => event.waitUntil(installCache().then(() => self.skipWaiting())));
self.addEventListener('activate', event => event.waitUntil((async () => {
  const complete = await completeCache();
  if (complete) { const keys = await caches.keys(); await Promise.all(keys.filter(key => key.startsWith(CACHE_PREFIX) && key !== complete.key).map(key => caches.delete(key))); }
  await self.clients.claim();
  if (complete) await broadcast({type:'CACHE_READY',buildId:complete.marker.buildId});
})()));
self.addEventListener('message', event => {
  if (event.data?.type === 'CACHE_STATUS') event.waitUntil((async () => {
    if (installationProgress) { event.source?.postMessage(installationProgress); return; }
    const complete = await completeCache();
    event.source?.postMessage(complete ? {type:'CACHE_READY',buildId:complete.marker.buildId} : {type:'CACHE_ERROR',message:'Çevrimdışı kopya henüz tamamlanmadı.'});
  })());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || !url.href.startsWith(self.registration.scope)) return;
  event.respondWith((async () => {
    const complete = await completeCache();
    if (complete) { const cached = await complete.cache.match(event.request, {ignoreSearch:true}); if (cached) return cached; if (event.request.mode === 'navigate') { const shell = await complete.cache.match(self.registration.scope); if (shell) return shell; } }
    return fetch(event.request);
  })());
});
