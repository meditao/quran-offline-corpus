'use strict';

/* Gerçek tarayıcı worker kodu; veri ham kaynaklardan üretilen tam indekstir. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const site = path.resolve(process.argv[2]);
let handler;
const replies = new Map();
const fetches = [];
const context = vm.createContext({
  fetch: async url => {
    assert.ok(['data/search-index.json', 'data/catalog.json'].includes(url), `Beklenmeyen ağ isteği: ${url}`);
    fetches.push(url);
    return {ok: true, json: async () => JSON.parse(fs.readFileSync(path.join(site, url), 'utf8'))};
  },
  self: {
    addEventListener(type, callback) { assert.equal(type, 'message'); handler = callback; },
    postMessage(response) { replies.set(response.id, JSON.parse(JSON.stringify(response))); },
  },
});
vm.runInContext(fs.readFileSync(path.join(site, 'search-worker.js'), 'utf8'), context,
                {filename: 'search-worker.js'});

let id = 0;
async function search(query, searchType = 'root', page = 1, pageSize = 40) {
  const request = {id: ++id, type: 'search', query, searchType, page, pageSize};
  await handler({data: request});
  const response = replies.get(id);
  assert.ok(response, 'Worker yanıt vermedi');
  assert.equal(response.id, id);
  return response;
}

(async () => {
  let cases = 0;
  for (const [query, bw, words, verses, surahs] of [
    ['Slw', 'Slw', 99, 90, 37], ['slw', 'slw', 3, 3, 3],
    ['fTr', 'fTr', 20, 19, 17], ['ftr', 'ftr', 3, 3, 3],
    ['Amn', 'Amn', 879, 723, 77], ['امن', 'Amn', 879, 723, 77],
    ['أ م ن', 'Amn', 879, 723, 77], ['أمن', 'Amn', 879, 723, 77],
    ['ṣ-l-v', 'Slw', 99, 90, 37], ['s-l-v', 'slw', 3, 3, 3],
  ]) {
    const response = await search(query);
    assert.equal(response.type, 'results', query);
    assert.equal(response.resolvedRoot, bw, query);
    assert.equal(response.total, words, query);
    assert.equal(response.verseCount, verses, query);
    assert.equal(response.surahCount, surahs, query);
    assert.ok(response.results.every(row => row.roots.includes(bw)), query);
    cases++;
  }
  const wrongCase = await search('AMN');
  assert.equal(wrongCase.total, 0, 'Buckwalter büyük/küçük harf kayboldu');
  cases++;
  const page = await search('Amn', 'root', 999, 40);
  assert.equal(page.page, 22);
  assert.equal(page.total, 879);
  assert.equal(page.results.length, 39);
  cases++;
  const verse = await search('2:3', 'ref');
  assert.equal(verse.total, 1);
  assert.equal(verse.results[0].surah, 2);
  assert.equal(verse.results[0].ayah, 3);
  assert.ok(verse.results[0].terms);
  cases++;
  const invalid = await search('2:999', 'ref');
  assert.equal(invalid.total, 0);
  cases++;
  const word = await search('ٱلْحَمْدُ', 'word');
  assert.ok(word.results.some(row => row.surah === 1 && row.ayah === 2 && row.wordId === 1));
  cases++;
  const lemma = await search('{som', 'lemma');
  assert.ok(lemma.total > 0);
  assert.ok(lemma.results.every(row => row.lemmas.includes('{som')));
  cases++;
  assert.equal(fetches.length, 2, 'Her sorguda tüm veri yeniden yüklenmemeli');
  process.stdout.write(`Arama worker: ${cases} korpus sağlama örneği geçti.\n`);
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
