'use strict';

let library;
const stripMarks = value => String(value || '').normalize('NFKC').replace(/[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed\u0640]/g, '');
// QAC kök alanındaki A, hemze/elif taşıyıcılarını tek etikette toplar (tezgah.veri.KOK_HEMZE).
const arabicRootKey = value => stripMarks(value).replace(/[ءأإآؤئاٱ]/g, 'ا').replace(/[\s\-–—·]/g, '');
const textKey = value => stripMarks(value).toLocaleLowerCase('tr').replace(/\s+/g, ' ').trim();
const latinRootKey = value => String(value || '').normalize('NFC').trim().replace(/\s+/g, '').replace(/[–—]/g, '-');
async function loadLibrary() {
  if (!library) library = Promise.all([fetch('data/search-index.json').then(response => { if (!response.ok) throw new Error('Arama dizini açılamadı.'); return response.json(); }), fetch('data/catalog.json').then(response => { if (!response.ok) throw new Error('Kök kataloğu açılamadı.'); return response.json(); })]).then(([index, catalog]) => {
    const verseMap = new Map(index.verses.map(row => [`${row[0]}:${row[1]}`, row]));
    return {index, catalog, verseMap};
  }).catch(error => { library = null; throw error; });
  return library;
}
function resolveRoot(query, roots) {
  /* Önce tam Buckwalter eşleşmesi; bu anahtarın büyük/küçük harf ayrımı korunur. */
  const exact = roots.find(root => root.bw === query);
  if (exact) return exact.bw;
  if (/[\u0600-\u06ff]/.test(query)) {
    const key = arabicRootKey(query);
    const matches = roots.filter(root => arabicRootKey(root.arabic) === key);
    if (matches.length === 1) return matches[0].bw;
    if (matches.length > 1) throw new Error('Bu Arapça kök gösterimi birden çok etiketle eşleşiyor. Tam Buckwalter biçimini kullanın.');
    return null;
  }
  const key = latinRootKey(query);
  const matches = roots.filter(root => root.latin && latinRootKey(root.latin) === key);
  if (matches.length === 1) return matches[0].bw;
  if (matches.length > 1) throw new Error('Bu Latin gösterimi tek bir köke karşılık gelmiyor. Arapça veya tam Buckwalter biçimini kullanın.');
  return null;
}
self.addEventListener('message', async event => {
  const request = event.data;
  if (request.type !== 'search') return;
  try {
    const query = String(request.query || '').trim();
    const pageSize = Math.min(100, Math.max(1, Number(request.pageSize) || 40));
    const requestedPage = Math.max(1, Math.floor(Number(request.page) || 1));
    if (!query) { self.postMessage({id:request.id,type:'results',total:0,verseCount:0,surahCount:0,results:[],page:1,pageSize}); return; }
    const {index, catalog, verseMap} = await loadLibrary();
    let rows = [], resolvedRoot = null;
    const wordSearch = ['root', 'lemma', 'word'].includes(request.searchType);
    if (request.searchType === 'root') { resolvedRoot = resolveRoot(query, catalog.roots); if (resolvedRoot) rows = index.words.filter(row => row[6].includes(resolvedRoot)); }
    else if (request.searchType === 'lemma') rows = index.words.filter(row => row[7].includes(query));
    else if (request.searchType === 'word') {
      const arabic = /[\u0600-\u06ff]/.test(query), key = arabic ? stripMarks(query).trim() : textKey(query);
      rows = index.words.filter(row => arabic ? stripMarks(row[3]).trim() === key : row[4] === query || textKey(row[5]).includes(key));
    } else if (request.searchType === 'text') { const key = textKey(query); rows = index.verses.filter(row => row.slice(2).some(value => textKey(value).includes(key))); }
    else if (request.searchType === 'ref') { const match = /^(\d{1,3})\s*[:/]\s*(\d{1,3})$/.exec(query); if (!match) throw new Error('Ayet aramasını sûre:ayet biçiminde yazın; örneğin 2:2.'); rows = index.verses.filter(row => row[0] === Number(match[1]) && row[1] === Number(match[2])); }
    else throw new Error('Bu arama türü desteklenmiyor.');
    const verses = new Set(rows.map(row => `${row[0]}:${row[1]}`)); const surahs = new Set(rows.map(row => row[0]));
    const page = Math.min(requestedPage, Math.max(1, Math.ceil(rows.length / pageSize)));
    const results = rows.slice((page - 1) * pageSize, page * pageSize).map(row => {
      if (wordSearch) { const verse = verseMap.get(`${row[0]}:${row[1]}`); return {surah:row[0],ayah:row[1],wordId:row[2],form:row[3],bw:row[4],reading:row[5],roots:row[6],lemmas:row[7],arabic:verse?.[2],terms:verse?.[4]}; }
      return {surah:row[0],ayah:row[1],arabic:row[2],reading:row[3],terms:row[4],tafsir:row[5]};
    });
    self.postMessage({id:request.id,type:'results',total:rows.length,verseCount:verses.size,surahCount:surahs.size,results,page,pageSize,resolvedRoot});
  } catch(error) { self.postMessage({id:request.id,type:'error',message:error.message || 'Arama tamamlanamadı.'}); }
});
