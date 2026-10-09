'use strict';

/* Gerçek üretilmiş Yûnus JSON'u gerçek service worker üzerinden ağsız okunur. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const site = path.resolve(process.argv[2]);
const manifest = JSON.parse(fs.readFileSync(path.join(site, 'manifest.json'), 'utf8'));
const script = fs.readFileSync(path.join(site, 'sw.js'), 'utf8');
const scope = 'https://example.test/meal/';
const handlers = new Map();
const stores = new Map();
let networkDisabled = false;
const urlOf = value => typeof value === 'string' ? value : value.url || value.href;
const readerPaths = ['index.html', 'app.js', 'sw.js', 'data/reader/catalog.json', 'data/reader/010.json'];
for (const relative of readerPaths) assert.ok(manifest.files.includes(relative), `Manifestte eksik: ${relative}`);
const context = vm.createContext({
  URL, Response,
  caches: {
    async keys() { return [...stores.keys()]; },
    async delete(name) { return stores.delete(name); },
    async open(name) {
      if (!stores.has(name)) stores.set(name, new Map());
      const cache = stores.get(name);
      return {
        async match(request, options = {}) {
          let url = urlOf(request);
          if (options.ignoreSearch) { const parsed = new URL(url); parsed.search = ''; url = parsed.href; }
          return cache.get(url)?.clone();
        },
        async put(request, response) { cache.set(urlOf(request), response.clone()); },
      };
    },
  },
  fetch: async request => {
    assert.ok(!networkDisabled, 'Çevrimdışı okumada ağ istendi');
    const url = urlOf(request);
    assert.ok(url.startsWith(scope));
    const relative = url.slice(scope.length);
    if (relative === 'manifest.json') return new Response(JSON.stringify({buildId: manifest.buildId, files: readerPaths}));
    return new Response(fs.readFileSync(path.join(site, relative || 'index.html')));
  },
  self: {
    registration: {scope}, location: {origin: 'https://example.test'},
    clients: {async matchAll() { return []; }, async claim() {}},
    async skipWaiting() {},
    addEventListener(type, callback) { handlers.set(type, callback); },
  },
});
vm.runInContext(script, context, {filename: 'sw.js'});

async function dispatch(type) {
  let promise;
  handlers.get(type)({waitUntil(value) { promise = value; }});
  return promise;
}
async function readOffline(relative) {
  let promise;
  handlers.get('fetch')({request: {url: scope + relative, method: 'GET', mode: 'cors'},
                        respondWith(value) { promise = value; }});
  assert.ok(promise);
  return (await promise).json();
}

(async () => {
  await dispatch('install');
  await dispatch('activate');
  networkDisabled = true;
  const catalog = await readOffline('data/reader/catalog.json');
  const chapter = await readOffline('data/reader/010.json?offline=1');
  assert.equal(catalog.buildId, manifest.buildId);
  assert.deepEqual(catalog.surahs.filter(s => s.available).map(s => s.id), [10]);
  assert.equal(chapter.verses.length, 109);
  assert.equal(chapter.verses[108].ref, '10:109');
  assert.ok(chapter.verses.every(v => v.translations.length === 3 && v.reading));
  assert.ok(chapter.verses.every(v => v.translations.find(t => t.authorId === 'biz')?.text));
  process.stdout.write('Yûnus: 109 ayet ve üç çeviri satırı önbellekten ağsız okundu.\n');
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
