'use strict';

/* Gerçek SW'ye küçük bir CacheStorage/HTTP benzetimi: başarılı ve kesilen kurulum. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const site = path.resolve(process.argv[2]);
const script = fs.readFileSync(path.join(site, 'sw.js'), 'utf8');
const buildId = JSON.parse(fs.readFileSync(path.join(site, 'data/catalog.json'), 'utf8')).buildId;
const scope = 'https://example.test/quran-offline-corpus/';
const marker = scope + '__offline_complete__';

function environment(options = {}) {
  const stores = new Map();
  const handlers = new Map();
  const messages = [];
  let manifestReads = 0;
  let networkDisabled = false;
  let oldPhase = false;
  const keyOf = key => typeof key === 'string' ? key : key.url || key.href;
  const cacheStorage = {
    async keys() { return [...stores.keys()]; },
    async delete(name) { return stores.delete(name); },
    async open(name) {
      if (!stores.has(name)) stores.set(name, new Map());
      const files = stores.get(name);
      return {
        async match(key, options = {}) {
          let url = keyOf(key);
          if (options.ignoreSearch) { const parsed = new URL(url); parsed.search = ''; url = parsed.href; }
          return files.get(url)?.clone();
        },
        async put(key, response) { files.set(keyOf(key), response.clone()); },
      };
    },
  };
  const context = vm.createContext({
    URL, Response, caches: cacheStorage,
    fetch: async value => {
      if (networkDisabled) throw new Error('İnternet kapalı');
      const url = keyOf(value);
      assert.ok(url.startsWith(scope), 'Host alt dizininin dışına çıkıldı');
      const relative = url.slice(scope.length);
      if (relative === 'manifest.json') {
        manifestReads++;
        const id = oldPhase ? 'old-complete' : options.swapManifest && manifestReads > 1 ? 'different-build' : buildId;
        return new Response(JSON.stringify({buildId: id,
          files: !oldPhase && options.unsafe ? ['../outside.txt'] : ['index.html', 'app.js', 'data/catalog.json', 'sw.js']}));
      }
      if (!oldPhase && options.failFile && relative === 'app.js') return new Response('Yok', {status: 404});
      return new Response(relative === '' ? oldPhase ? 'old-shell' : 'offline-shell' : `content:${relative}`);
    },
    self: {
      registration: {scope}, location: {origin: 'https://example.test'},
      clients: {async matchAll() { return [{postMessage(message) { messages.push(message); }}]; },
                async claim() {}},
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
  async function seedOld() {
    // Önceki sürüm de aynı gerçek kurulum akışından geçer; cache adı varsayılmaz.
    oldPhase = true;
    context.self.CORPUS_BUILD_ID = 'old-complete';
    await dispatch('install');
    assert.equal(stores.size, 1);
    const oldName = [...stores.keys()][0];
    oldPhase = false;
    context.self.CORPUS_BUILD_ID = buildId;
    manifestReads = 0;
    messages.length = 0;
    return oldName;
  }
  async function offlineFetch(relative, mode = 'cors') {
    networkDisabled = true;
    let promise;
    handlers.get('fetch')({request: {url: scope + relative, method: 'GET', mode},
                          respondWith(value) { promise = value; }});
    assert.ok(promise, 'Service worker isteği üstlenmedi');
    return (await promise).text();
  }
  return {stores, messages, dispatch, seedOld, offlineFetch};
}

(async () => {
  const success = environment();
  const oldName = await success.seedOld();
  await success.dispatch('install');
  const ready = [...success.stores.entries()].find(([name]) => name !== oldName)?.[1];
  assert.ok(ready, 'Yeni sürüm için ayrı bir önbellek oluşmadı');
  assert.ok(ready.has(marker), 'Eksiksiz kurulum tamamlandı diye işaretlenmedi');
  for (const relative of ['', 'manifest.json', 'index.html', 'app.js', 'data/catalog.json', 'sw.js']) {
    assert.ok(ready.has(scope + relative), `Önbellekte eksik dosya: ${relative}`);
  }
  assert.equal(await success.offlineFetch('app.js'), 'content:app.js');
  assert.equal(await success.offlineFetch('2/3', 'navigate'), 'offline-shell');
  await success.dispatch('activate');
  assert.ok(!success.stores.has(oldName), 'Eski sürüm aktivasyondan sonra temizlenmedi');

  for (const options of [{failFile: true}, {swapManifest: true}, {unsafe: true}]) {
    const failure = environment(options);
    const oldName = await failure.seedOld();
    await assert.rejects(failure.dispatch('install'), undefined,
                         `Eksik/karışık kurulum kabul edildi: ${JSON.stringify(options)}`);
    assert.ok(failure.stores.has(oldName), 'Başarısız güncelleme eski tamamlanmış kopyayı sildi');
    assert.equal(failure.stores.size, 1, 'Eksik sürüm görünür önbellekte kaldı');
    assert.ok(failure.messages.some(message => message.type === 'CACHE_ERROR'));
    assert.ok(!failure.messages.some(message => message.type === 'CACHE_READY'));
    assert.equal(await failure.offlineFetch('some-page', 'navigate'), 'old-shell');
  }
  process.stdout.write('Çevrimdışı worker: tam kurulum, ağsız okuma, kesilen güncelleme, kaynak değişimi ve alt dizin güvenliği doğrulandı.\n');
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
