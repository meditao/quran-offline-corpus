'use strict';

/* Bağımlılıksız okuyucu. Korpus ve Markdown metinleri gösterilmeden önce kaçırılır. */
const state = { catalog: null, surahs: new Map(), documents: new Map(), verse: null, routeId: 0, worker: null, searchId: 0, pendingSearch: new Map(), selectedWord: null, panelReturnFocus: null };
const content = document.getElementById('content');
const wordPanel = document.getElementById('word-panel');
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const fmt = value => Number(value || 0).toLocaleString('tr-TR');
const verseRoute = (surah, ayah) => `#/ayet/${surah}/${ayah}`;
const searchRoute = (type, query, page = 1) => `#/arama?${new URLSearchParams({ type, q: query, page: String(page) })}`;
const documentRoute = id => `#/analiz/${encodeURIComponent(id)}`;
const docById = id => state.catalog.documents.find(doc => doc.id === id);
const rootByBW = bw => state.catalog.roots.find(root => root.bw === bw);
const ROOT_TYPES = new Set(['root', 'lemma', 'word', 'text', 'ref']);
// Yalnız insan tarafından okunabilen ad/başlık filtreleri; Buckwalter anahtarlarına uygulanmaz.
const humanFilterKey = value => String(value || '').toLocaleLowerCase('tr').normalize('NFD').replace(/\p{M}/gu, '').replace(/ı/g, 'i').replace(/[‘’'ʾʿ]/g, '').replace(/[–—]/g, '-');

async function readJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Veri dosyası açılamadı (${response.status}): ${url}`);
  return response.json();
}
async function loadSurah(id) {
  if (!state.surahs.has(id)) state.surahs.set(id, readJSON(`data/surahs/${String(id).padStart(3, '0')}.json`).catch(error => { state.surahs.delete(id); throw error; }));
  return state.surahs.get(id);
}
async function loadDocument(doc) {
  if (!state.documents.has(doc.id)) state.documents.set(doc.id, readJSON(doc.url).catch(error => { state.documents.delete(doc.id); throw error; }));
  return state.documents.get(doc.id);
}
function showError(title, message) {
  content.innerHTML = `<section class="error-view"><span class="eyebrow">ÇALIŞMA MASASI</span><h1>${escapeHTML(title)}</h1><p class="error-message">${escapeHTML(message)}</p><a href="${verseRoute(2, 2)}">Bakara 2:2’ye dön</a></section>`;
}
function renderSurahs() {
  const query = humanFilterKey(document.getElementById('surah-filter').value.trim());
  const list = state.catalog.surahs.filter(s => !query || String(s.id) === query || humanFilterKey(s.name).includes(query) || (s.arabicName || '').includes(query));
  document.getElementById('surah-list').innerHTML = list.length ? list.map(s => `<a class="surah-link${state.verse?.surah === s.id ? ' active' : ''}" href="${verseRoute(s.id, 1)}"${state.verse?.surah === s.id ? ' aria-current="page"' : ''}><span class="surah-number">${s.id}</span><span><span class="surah-name">${escapeHTML(s.name)}</span><span class="surah-meta">${s.verseCount} ayet${s.translatedCount ? ` · ${s.translatedCount} çalışma çevirisi` : ''}</span></span><span class="surah-arabic" lang="ar" dir="rtl">${escapeHTML(s.arabicName)}</span></a>`).join('') : '<p class="subtle">Bu filtreyle sûre bulunamadı.</p>';
  document.getElementById('surah-count').textContent = state.catalog.surahs.length;
}
function rootLabel(root) { return root ? `${root.latin || root.bw} · ${root.arabic || root.bw}` : ''; }
function rootLinks(roots) { return roots.map(bw => { const root = rootByBW(bw); return `<a class="root-chip" href="${escapeHTML(searchRoute('root', bw))}" title="${escapeHTML(bw)}">${escapeHTML(root?.latin || bw)} <span class="mono">${escapeHTML(bw)}</span></a>`; }).join('') || '<span class="subtle">Kök etiketi yok</span>'; }
function docLinks(ids) { return [...new Set(ids)].map(id => docById(id)).filter(Boolean).map(doc => `<a class="document-link" href="${documentRoute(doc.id)}">${escapeHTML(doc.title)}</a>`).join(''); }
function neighbouringVerse(surah, ayah, delta) {
  const s = state.catalog.surahs.find(item => item.id === surah);
  if (delta === -1) return ayah > 1 ? [surah, ayah - 1] : surah > 1 ? [surah - 1, state.catalog.surahs.find(item => item.id === surah - 1).verseCount] : null;
  return ayah < s.verseCount ? [surah, ayah + 1] : surah < 114 ? [surah + 1, 1] : null;
}
function navLink(label, pair) { return pair ? `<a href="${verseRoute(...pair)}">${label}</a>` : `<a aria-disabled="true" tabindex="-1">${label}</a>`; }
function renderVerse(surah, verse) {
  state.verse = verse;
  renderSurahs();
  const meta = state.catalog.surahs.find(item => item.id === surah.id);
  const tokens = verse.tokens || [];
  const arabic = tokens.length && tokens.map(t => t.text).join(' ') === verse.arabic ? tokens.map((token, index) => token.wordIds?.length ? `<button type="button" class="arabic-word" data-token="${index}" aria-label="${escapeHTML(token.text)} — kelime çözümlemesini aç">${escapeHTML(token.text)}</button>` : `<span class="arabic-unmapped" title="Bu metin birimi için güvenilir kelime eşleştirmesi yok">${escapeHTML(token.text)}</span>`).join(' ') : escapeHTML(verse.arabic);
  const relatedRoots = [...new Set((verse.words || []).flatMap(word => word.roots || []))];
  const relatedDocs = state.catalog.documents.filter(doc => (doc.roots || []).some(root => relatedRoots.includes(root))).map(doc => doc.id);
  const analysisIDs = [...new Set([...(verse.documentIds || []), ...relatedDocs])];
  const translation = verse.translation;
  document.title = `${meta.name} ${verse.ref} · Kur’an Araştırma Masası`;
  content.innerHTML = `<section aria-label="Ayet okuma"><div class="page-top"><div class="page-title"><span class="eyebrow">KUR’AN METNİ · SÛRE ${surah.id}</span><h1>${escapeHTML(meta.name)} <span class="surah-title-arabic" dir="rtl" lang="ar">${escapeHTML(meta.arabicName)}</span></h1><p class="subtle">${meta.verseCount} ayet · ${meta.translatedCount || 0} ayette çalışma çevirisi</p></div><form id="verse-jump" class="verse-controls"><label for="jump-surah">Sûre</label><input id="jump-surah" type="number" min="1" max="114" value="${surah.id}" required><label for="jump-ayah">Ayet</label><input id="jump-ayah" type="number" min="1" max="${meta.verseCount}" value="${verse.ayah}" required><button type="submit">Git</button></form></div><div class="verse-nav"><span class="verse-position">${escapeHTML(meta.name)} · ${verse.ref}</span><div class="nav-buttons">${navLink('← Önceki ayet', neighbouringVerse(surah.id, verse.ayah, -1))}${navLink('Sonraki ayet →', neighbouringVerse(surah.id, verse.ayah, 1))}</div></div><article class="verse-card"><section class="arabic-section"><div class="arabic-heading"><span class="section-label"><span class="label-tag">VERİ</span> TANZİL UTHMANI v1.1</span><span class="verse-ref">${verse.ref}</span></div><div class="arabic-text" dir="rtl" lang="ar">${arabic}</div><p class="arabic-hint">Kelimeye dokunarak QAC kök, lemma ve morfoloji bilgisini açın.</p>${verse.basmala ? '<p class="basmala-note">Bu sûrenin başındaki besmele Tanzil metninin içinde korunur; QAC ayet kelimelerinden ayrı gösterilir.</p>' : ''}</section><section class="reading-section"><span class="section-label"><span class="label-tag">AKTARIM</span> OKUNUŞ · TEZGAH</span><p class="reading-text">${escapeHTML(verse.reading || 'Bu ayet için okunuş verisi hazırlanmadı.')}</p>${verse.readingNotes?.length ? `<details class="reading-notes"><summary>Okunuş notları (${verse.readingNotes.length})</summary><ul>${verse.readingNotes.map(note => `<li>${escapeHTML(typeof note === 'string' ? note : JSON.stringify(note))}</li>`).join('')}</ul></details>` : ''}</section></article><article class="interpretation-card"><div class="interpretation-heading"><span class="section-label interpretation"><span class="label-tag">YORUM / TEFSİR</span> ÇALIŞMA ÇEVİRİSİ</span>${translation?.documentId ? `<a href="${documentRoute(translation.documentId)}">Araştırma dosyasını aç ↗</a>` : ''}</div>${translation ? `<section class="translation-section"><h2>Terimleri koruyan çeviri</h2><div class="translation-text">${renderInline(translation.terms || 'Bu ayet için terimleri koruyan çeviri bulunmuyor.', docById(translation.documentId))}</div></section><section class="translation-section tafsir"><h2>Tefsirli çeviri</h2><div class="translation-text">${renderInline(translation.tafsir || 'Bu ayet için tefsirli çeviri bulunmuyor.', docById(translation.documentId))}</div></section>` : '<p class="empty-translation">Bu ayet için depoda çalışma çevirisi bulunmuyor. Mevcut çeviriler ve analizler kaynak dosyalarından gösterilir.</p>'}</article><details class="support-box"><summary>Ayetin QAC kelimeleri · ${verse.words.length} kelime konumu</summary><p class="subtle" style="font-size:11px;margin:12px 0 0">QAC kelime listesi ve Tanzil metni ayrı kaynak katmanlarıdır. Eşleştirme durumu: ${escapeHTML(verse.alignmentStatus || 'belirtilmedi')}.</p><div class="word-grid">${verse.words.map(word => `<button type="button" class="qac-word-button" data-word="${word.id}"><span lang="ar" dir="rtl">${escapeHTML(word.form)}</span><small>${word.id}</small></button>`).join('')}</div></details><div class="content-footer"><span class="eyebrow">BAĞLANTILI ARAŞTIRMALAR</span>${analysisIDs.length ? `<div class="document-links">${docLinks(analysisIDs)}</div>` : '<p>Bu ayetle ilişkilendirilmiş bir araştırma dosyası bulunmuyor.</p>'}<p>Arapça metin: Tanzil Uthmani v1.1 · Kelime çözümlemesi: QAC v0.4 · Okunuş: mevcut tezgah kuralları.<br>Çeviri ve tefsirler araştırma yorumudur; Arapça metin ve morfoloji verisinden ayrı tutulur.</p></div></section>`;
  if (verse.basmala?.reading) content.querySelector('.reading-text').insertAdjacentHTML('beforebegin', `<p class="basmala-note">Sûre başı besmelesi: <span class="reading-text" style="font-size:14px">${escapeHTML(verse.basmala.reading)}</span></p>`);
  const jumpSurah = document.getElementById('jump-surah');
  jumpSurah.addEventListener('input', () => { const s = state.catalog.surahs.find(item => item.id === Number(jumpSurah.value)); document.getElementById('jump-ayah').max = s?.verseCount || 286; });
  document.getElementById('verse-jump').addEventListener('submit', event => { event.preventDefault(); const s = Number(jumpSurah.value); const a = Number(document.getElementById('jump-ayah').value); location.hash = verseRoute(s, a); });
}
function openWords(ids, trigger) {
  const words = ids.map(id => state.verse.words.find(word => word.id === id)).filter(Boolean);
  if (!words.length) return;
  state.panelReturnFocus = trigger;
  state.selectedWord = words[0].id;
  document.querySelectorAll('.arabic-word').forEach(button => { const token = state.verse.tokens[Number(button.dataset.token)]; button.classList.toggle('selected', token.wordIds.some(id => ids.includes(id))); });
  wordPanel.innerHTML = `<div class="panel-heading"><h2>Kelime çözümlemesi</h2><button id="close-word-panel" aria-label="Kelime panelini kapat">×</button></div><span class="section-label"><span class="label-tag">VERİ</span> QAC v0.4 · ${state.verse.ref}</span>${words.map(word => `<section><div class="word-detail-form" lang="ar" dir="rtl">${escapeHTML(word.form)}</div><p class="word-reading">${escapeHTML(word.reading || '')}</p><dl class="detail-definition"><dt>Konum</dt><dd>${state.verse.ref}:${word.id} · kelime konumu</dd><dt>Buckwalter</dt><dd class="mono">${escapeHTML(word.bw)}</dd><dt>Kök</dt><dd>${rootLinks(word.roots || [])}</dd><dt>Lemma</dt><dd>${(word.lemmas || []).map(lemma => `<a class="root-chip mono" href="${escapeHTML(searchRoute('lemma', lemma))}">${escapeHTML(lemma)}</a>`).join('') || '<span class="subtle">Lemma etiketi yok</span>'}</dd></dl>${word.alignmentNote ? `<p class="detail-note">${escapeHTML(word.alignmentNote)}</p>` : ''}<div class="table-scroll"><table><caption class="visually-hidden">${state.verse.ref}:${word.id} QAC segmentleri</caption><thead><tr><th>Segment</th><th>Biçim</th><th>Etiket</th><th>Tür</th></tr></thead><tbody>${(word.segments || []).map(segment => `<tr><td>${escapeHTML(segment.id)}</td><td dir="rtl" lang="ar">${escapeHTML(segment.form)}</td><td class="mono">${escapeHTML(segment.tag)}</td><td class="mono">${escapeHTML(segment.type || '—')}</td></tr><tr><td colspan="4"><div class="segment-features">${(segment.features || []).map(feature => `<span class="feature">${escapeHTML(feature)}</span>`).join('')}</div>${segment.root ? `Kök: <span class="mono">${escapeHTML(segment.root)}</span> ` : ''}${segment.lemma ? `Lemma: <span class="mono">${escapeHTML(segment.lemma)}</span>` : ''}</td></tr>`).join('')}</tbody></table></div></section>`).join('')}<section class="panel-section"><h3>Kaynak ve eşleştirme</h3><p>QAC kök ve lemma etiketleri kaynak dosyasında kayıtlı biçimleriyle gösterilir. Büyük ve küçük Buckwalter harfleri farklı Arapça harfleri temsil eder.</p><p>Tanzil eşleştirmesi: ${escapeHTML(state.verse.alignmentStatus || 'belirtilmedi')}. Metin ve morfoloji katmanları ayrı korunur.</p></section>`;
  const docs = state.catalog.documents.filter(doc => doc.roots?.some(root => words.some(word => word.roots?.includes(root))));
  if (docs.length) wordPanel.insertAdjacentHTML('beforeend', `<section class="panel-section"><h3>Yorum / kavram dosyaları</h3><div class="document-links">${docLinks(docs.map(doc => doc.id))}</div></section>`);
  wordPanel.hidden = false;
  document.getElementById('close-word-panel').addEventListener('click', closeWordPanel);
  document.getElementById('close-word-panel').focus({ preventScroll: true });
}
function closeWordPanel() {
  wordPanel.hidden = true;
  state.selectedWord = null;
  document.querySelectorAll('.arabic-word.selected').forEach(button => button.classList.remove('selected'));
  state.panelReturnFocus?.isConnected && state.panelReturnFocus.focus({ preventScroll: true });
  state.panelReturnFocus = null;
}

/* Ham HTML metin olarak gösterilir; bağlantılar yalnız bilinen dosyalara veya güvenli adreslere gider. */
function safeLink(target, doc) {
  const value = target.trim().replace(/^<|>$/g, '');
  if (/^https?:\/\//i.test(value)) { try { const url = new URL(value); return { href: url.href, external: true }; } catch { return null; } }
  if (/^#\/((ayet|analiz|arama|kaynaklar)(\/|\?|$))/.test(value)) return { href: value };
  if (value.startsWith('#')) return { href: value, anchor: true };
  if (/^[a-z][a-z\d+.-]*:/i.test(value) || value.startsWith('//')) return null;
  let normalized;
  try { normalized = decodeURIComponent(new URL(value.split('#')[0], `https://repo.invalid/${doc?.path || ''}`).pathname.slice(1)); } catch { return null; }
  const linkedDoc = state.catalog.documents.find(item => item.path.replace(/\\/g, '/') === normalized);
  if (linkedDoc) return { href: documentRoute(linkedDoc.id) };
  if (/^07_analyses\/.*\.(csv|tsv)$/i.test(normalized) && Object.hasOwn(state.catalog.sourceHashes || {}, normalized)) return { href:`sources/repository/${normalized}` };
  return null;
}
function localSourceLink(path) {
  if (typeof path !== 'string' || !path.startsWith('sources/') || path.includes('..') || /[?#\\]/.test(path)) return null;
  const repoPath = path.replace(/^sources\/repository\//, '');
  const doc = state.catalog.documents.find(item => item.path === repoPath);
  return doc ? documentRoute(doc.id) : path;
}
function renderInline(text, doc, depth = 0) {
  if (depth > 3) return escapeHTML(text);
  const pattern = /(`[^`\n]+`|!?\[[^\]\n]+\]\([^\)\n]+\)|\*\*[^*\n]+\*\*|__[^_\n]+__|(?<!\*)\*[^*\n]+\*(?!\*)|~~[^~\n]+~~)/g;
  let output = '', last = 0, match;
  while ((match = pattern.exec(String(text))) !== null) {
    output += escapeHTML(String(text).slice(last, match.index));
    const token = match[0];
    if (token.startsWith('`')) output += `<code>${escapeHTML(token.slice(1, -1))}</code>`;
    else if (token.startsWith('[') || token.startsWith('![')) {
      const parts = /^!?\[([^\]]+)\]\(([^)]+)\)$/.exec(token);
      const link = safeLink(parts[2], doc);
      const label = renderInline(parts[1], doc, depth + 1);
      if (token.startsWith('!')) output += `<span title="${escapeHTML(parts[2])}">[Görsel: ${label}]</span>`;
      else output += link ? `<a href="${escapeHTML(link.href)}"${link.external ? ' target="_blank" rel="noopener noreferrer"' : ''}${link.anchor ? ' data-doc-anchor="true"' : ''}>${label}</a>` : `<span title="Kaynak yolu: ${escapeHTML(parts[2])}">${label}</span>`;
    } else if (token.startsWith('**') || token.startsWith('__')) output += `<strong>${renderInline(token.slice(2, -2), doc, depth + 1)}</strong>`;
    else if (token.startsWith('~~')) output += `<del>${renderInline(token.slice(2, -2), doc, depth + 1)}</del>`;
    else output += `<em>${renderInline(token.slice(1, -1), doc, depth + 1)}</em>`;
    last = pattern.lastIndex;
  }
  return output + escapeHTML(String(text).slice(last));
}
function markdown(contentText, doc) {
  const lines = String(contentText).replace(/\r\n?/g, '\n').split('\n');
  const output = []; let paragraph = [], listType = null, inCode = false, code = [], quote = [];
  const flushParagraph = () => { if (paragraph.length) { output.push(`<p>${renderInline(paragraph.join('\n'), doc)}</p>`); paragraph = []; } };
  const closeList = () => { if (listType) { output.push(`</${listType}>`); listType = null; } };
  const flushQuote = () => { if (quote.length) { output.push(`<blockquote>${renderInline(quote.join('\n'), doc)}</blockquote>`); quote = []; } };
  const cells = row => { let value = row.trim(); if (value.startsWith('|')) value = value.slice(1); if (value.endsWith('|')) value = value.slice(0, -1); return value.split(/(?<!\\)\|/).map(cell => cell.trim().replace(/\\\|/g, '|')); };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*```/.test(line)) { flushParagraph(); closeList(); flushQuote(); if (inCode) { output.push(`<pre><code>${escapeHTML(code.join('\n'))}</code></pre>`); code = []; } inCode = !inCode; continue; }
    if (inCode) { code.push(line); continue; }
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(lines[i + 1])) {
      flushParagraph(); closeList(); flushQuote(); const headers = cells(line); i++; const rows = [];
      while (i + 1 < lines.length && lines[i + 1].includes('|') && lines[i + 1].trim()) rows.push(cells(lines[++i]));
      output.push(`<div class="table-scroll"><table><thead><tr>${headers.map(cell => `<th>${renderInline(cell, doc)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${renderInline(cell, doc)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`); continue;
    }
    const heading = /^(#{1,6})\s+(.+?)\s*#*$/.exec(line);
    if (heading) { flushParagraph(); closeList(); flushQuote(); const level = heading[1].length; const anchor = heading[2].toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s/g, '-'); output.push(`<h${level} id="${escapeHTML(anchor)}" class="route-anchor">${renderInline(heading[2], doc)}</h${level}>`); continue; }
    if (/^\s*([-*_])\s*\1\s*\1[\s\1]*$/.test(line)) { flushParagraph(); closeList(); flushQuote(); output.push('<hr>'); continue; }
    if (/^\s*>/.test(line)) { flushParagraph(); closeList(); quote.push(line.replace(/^\s*>\s?/, '')); continue; }
    flushQuote();
    const item = /^\s*(?:([-*+])|(\d+)\.)\s+(.+)$/.exec(line);
    if (item) { flushParagraph(); const type = item[2] ? 'ol' : 'ul'; if (listType !== type) { closeList(); output.push(`<${type}>`); listType = type; } output.push(`<li>${renderInline(item[3], doc)}</li>`); continue; }
    if (!line.trim()) { flushParagraph(); closeList(); continue; }
    closeList(); paragraph.push(line);
  }
  flushParagraph(); closeList(); flushQuote();
  if (code.length) output.push(`<pre><code>${escapeHTML(code.join('\n'))}</code></pre>`);
  return output.join('\n');
}
function renderDocument(doc, data) {
  document.title = `${doc.title} · Kur’an Araştırma Masası`;
  content.innerHTML = `<article class="document-layout"><span class="eyebrow">ARAŞTIRMA KÜTÜPHANESİ</span><h1>${escapeHTML(doc.title)}</h1><p class="subtle" style="font-size:11px">${escapeHTML(doc.path)}</p><div class="document-banner">YORUM / ARAŞTIRMA · Bu dosya depodaki çalışma metnidir. Çeviri, kavram tanımı ve yorumlar korpus verisinden ayrı değerlendirilir. Alıntılanan ayetleri metin ve morfoloji üzerinden inceleyebilirsiniz.</div>${doc.roots?.length ? `<div class="document-links">${rootLinks(doc.roots)}</div>` : ''}<div class="markdown">${markdown(data.content, doc)}</div></article>`;
}
function searchWorker() {
  if (!state.worker) {
    state.worker = new Worker('search-worker.js');
    state.worker.addEventListener('message', event => {
      const message = event.data;
      const pending = state.pendingSearch.get(message.id);
      if (!pending) return;
      state.pendingSearch.delete(message.id);
      message.type === 'error' ? pending.reject(new Error(message.message)) : pending.resolve(message);
    });
    state.worker.addEventListener('error', () => { state.pendingSearch.forEach(pending => pending.reject(new Error('Arama dizini açılamadı. Yerel sunucunun çalıştığını ve arama verisinin oluşturulduğunu kontrol edin.'))); state.pendingSearch.clear(); state.worker.terminate(); state.worker = null; });
  }
  return state.worker;
}
function performSearch(type, query, page) {
  return new Promise((resolve, reject) => { const id = ++state.searchId; state.pendingSearch.set(id, {resolve, reject}); searchWorker().postMessage({id, type:'search', searchType:type, query, page, pageSize:40}); });
}
function searchHelp(type) {
  if (type === 'root') return 'Kökü Arapça (<code>أ م ن</code>), tam Buckwalter (<code>Amn</code>) veya katalogdaki kayıpsız Latin gösterimle yazın. Buckwalter büyük/küçük harfe duyarlıdır: <code>Slw</code> ve <code>slw</code> ayrı köklerdir.';
  if (type === 'lemma') return 'QAC lemma etiketini tam Buckwalter biçiminde yazın. Ayetteki kelime panelinden lemma bağlantısına da tıklayabilirsiniz. Büyük/küçük harf ayrımı korunur.';
  if (type === 'word') return 'Arapça kelimeyi, tam Buckwalter biçimini veya okunuşunu yazın. Arapça aramada harekeler dikkate alınmaz. Sonuç birimi QAC kelime konumudur.';
  if (type === 'ref') return 'Sûre ve ayet numarasını <code>2:2</code> veya <code>10:109</code> biçiminde yazın.';
  return 'Arapça metin, okunuş, terimleri koruyan çeviri ve tefsirli çeviri içinde arayın. Sonuç birimi ayettir; çeviri ve tefsirler yorum katmanıdır.';
}
function searchForm(type, query) {
  return `<form id="page-search" class="search-form-large"><label class="visually-hidden" for="page-search-type">Arama türü</label><select id="page-search-type">${[['root','Kök'],['lemma','Lemma'],['word','Kelime'],['text','Metin'],['ref','Ayet']].map(([value,label]) => `<option value="${value}"${type === value ? ' selected' : ''}>${label}</option>`).join('')}</select><label class="visually-hidden" for="page-search-query">Aranacak ifade</label><input id="page-search-query" value="${escapeHTML(query)}" placeholder="Aranacak ifadeyi yazın…" maxlength="240" required><button>Ara</button></form>`;
}
function bindPageSearch() {
  document.getElementById('page-search').addEventListener('submit', event => { event.preventDefault(); location.hash = searchRoute(document.getElementById('page-search-type').value, document.getElementById('page-search-query').value.trim()); });
}
function provenanceLine() {
  const hashes = state.catalog.hashes || state.catalog.sourceHashes || {};
  const qac = hashes.qac || hashes.qacSha256 || Object.entries(hashes).find(([path]) => /qac\/quranic-corpus-morphology/.test(path))?.[1] || state.catalog.sources?.find(source => /QAC|Quranic Arabic Corpus/.test(source.name))?.sha256;
  return `Kaynak: QAC v0.4${qac ? ` · SHA-256 ${escapeHTML(String(qac).slice(0, 12))}…` : ''} · Tanzil Uthmani v1.1 · Derleme ${escapeHTML(state.catalog.buildId)}.`;
}
async function renderSearch(params, routeId) {
  const type = params.get('type') || 'root'; const query = (params.get('q') || '').trim(); const pageText = params.get('page') || '1'; const page = Number(pageText);
  if (!ROOT_TYPES.has(type) || !/^\d+$/.test(pageText) || page < 1 || !Number.isSafeInteger(page) || query.length > 240) throw new Error('Geçersiz arama bağlantısı. Arama türünü, ifadeyi ve sayfa numarasını kontrol edin.');
  state.verse = null; renderSurahs();
  document.title = `${query ? `${query} · ` : ''}Arama · Kur’an Araştırma Masası`;
  document.getElementById('search-type').value = type; document.getElementById('search-query').value = query;
  content.innerHTML = `<section><span class="eyebrow">KORPUS TARAMASI</span><h1>Metinden iz sür</h1>${searchForm(type, query)}<p class="search-help">${searchHelp(type)}</p><div id="search-results">${query ? '<p class="loading-line">Arama dizini taranıyor…</p>' : '<p class="loading-line">Arama yapmak için bir kök, kelime veya ifade yazın.</p>'}</div></section>`;
  bindPageSearch();
  if (!query) return;
  const result = await performSearch(type, query, page);
  if (routeId !== state.routeId) return;
  const unit = ['root', 'lemma', 'word'].includes(type) ? 'kelime konumu' : 'ayet';
  const root = result.resolvedRoot ? rootByBW(result.resolvedRoot) : null;
  const pages = Math.ceil(result.total / result.pageSize);
  const results = result.results.map(row => `<a class="result-card" href="${verseRoute(row.surah, row.ayah)}"><div class="result-head"><span class="verse-ref">${row.surah}:${row.ayah}</span><strong>${escapeHTML(state.catalog.surahs.find(s => s.id === row.surah)?.name)}</strong>${row.wordId ? `<span class="subtle">kelime ${row.wordId}</span>` : ''}</div><p class="result-arabic" dir="rtl" lang="ar">${escapeHTML(row.form || row.arabic)}</p><p class="result-text">${escapeHTML(row.reading || '')}</p>${row.terms ? `<p class="result-text"><small>Yorum / terimleri koruyan çeviri</small> · ${escapeHTML(row.terms)}</p>` : ''}<div class="result-metadata">${row.bw ? `<span class="mono">${escapeHTML(row.bw)}</span>` : ''}${row.roots?.map(bw => `<span>Kök ${escapeHTML(rootByBW(bw)?.latin || bw)} <span class="mono">${escapeHTML(bw)}</span></span>`).join('') || ''}${row.lemmas?.map(lemma => `<span>Lemma <span class="mono">${escapeHTML(lemma)}</span></span>`).join('') || ''}</div></a>`).join('');
  document.getElementById('search-results').innerHTML = `<div class="results-summary"><span><strong>${fmt(result.total)}</strong> ${unit} · ${fmt(result.verseCount)} ayet · ${fmt(result.surahCount)} sûre${root ? `<br><span class="subtle">${escapeHTML(rootLabel(root))} · <span class="mono">${escapeHTML(root.bw)}</span></span>` : ''}</span><span class="subtle">${result.total ? `${fmt((result.page - 1) * result.pageSize + 1)}–${fmt(Math.min(result.page * result.pageSize, result.total))}` : '0'} / ${fmt(result.total)}</span></div><p class="search-help" style="margin-top:12px">Sorgu: ${escapeHTML(type)} = <code>${escapeHTML(query)}</code> · Sayım: ${unit}; ayet ve sûre sayıları benzersiz konumlardır.<br>${provenanceLine()}</p>${root ? `<div class="document-links">${docLinks(state.catalog.documents.filter(doc => doc.roots?.includes(root.bw)).map(doc => doc.id))}</div>` : ''}<div class="result-list">${results || '<p class="loading-line">Bu sorguyla sonuç bulunamadı. Bu sonuç, kavramın Kur’an’da bulunmadığını göstermez.</p>'}</div>${pages > 1 ? `<nav class="pagination" aria-label="Arama sayfaları">${result.page > 1 ? `<a href="${escapeHTML(searchRoute(type, query, result.page - 1))}">← Önceki</a>` : ''}<span>Sayfa ${result.page} / ${fmt(pages)}</span>${result.page < pages ? `<a href="${escapeHTML(searchRoute(type, query, result.page + 1))}">Sonraki →</a>` : ''}</nav>` : ''}`;
}
function renderSources() {
  state.verse = null; renderSurahs(); document.title = 'Kaynaklar · Kur’an Araştırma Masası';
  const stats = state.catalog.stats;
  content.innerHTML = `<section><span class="eyebrow">ÇEVRİMDIŞI ARAŞTIRMA KÜTÜPHANESİ</span><h1>Kaynağa geri dön</h1><p class="subtle">Metin, morfoloji ve çalışma yorumları kendi kaynaklarıyla birlikte gösterilir.</p><div class="stats-row">${[['surahs','sûre'],['verses','ayet'],['words','QAC kelime konumu'],['segments','QAC segment'],['roots','QAC kök'],['translatedVerses','çalışma çevirili ayet']].map(([key,label]) => `<div class="stat-item"><strong>${fmt(stats[key])}</strong><span>${label}</span></div>`).join('')}</div><p class="search-help">${provenanceLine()}<br>Bu sayımlar uygulama derlemesinde korpus dosyalarından hesaplanmıştır; farklı sayım birimleri birbirine eklenmez.</p><div class="source-grid">${state.catalog.sources.map(source => `<section class="source-card"><h2>${escapeHTML(source.name)}</h2><p>${escapeHTML(source.note || '')}</p>${safeLink(source.url || '')?.external ? `<a href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">Kaynak sitesi ↗</a><small style="display:block;margin-top:7px">İnternet bağlantısı gerektirir.</small>` : ''}</section>`).join('')}</div><div class="document-banner">VERİ: Arapça Tanzil metni ve QAC morfoloji etiketleri. AKTARIM: tezgah okunuş kuralları. YORUM / TEFSİR: çalışma çevirileri, kavram kartları ve analiz dosyaları. Dış sözlükler ve ikincil okumalar, bulundukları araştırma dosyasındaki statüleriyle değerlendirilir.</div><h2>Araştırma ve yöntem dosyaları</h2><label class="visually-hidden" for="document-filter">Dosya filtrele</label><input id="document-filter" type="search" placeholder="Dosya adı, konu veya yol ara…" style="width:100%"><div id="document-catalog" class="catalog-list"></div><div class="content-footer"><p>Uygulama kendi veri dosyalarından çalışır. Yerel sunucu çalışırken internet bağlantısı gerekmez. Tarayıcıdaki çevrimdışı kopya tamamlandığında uygulama aynı adreste sunucu olmadan da açılabilir.</p><p>Derleme: <span class="mono">${escapeHTML(state.catalog.buildId)}</span></p><button id="check-update">Çevrimdışı kopyayı kontrol et</button></div></section>`;
  const filter = document.getElementById('document-filter');
  const sourceCards = [...content.querySelectorAll('.source-card')];
  state.catalog.sources.forEach((source, index) => {
    const card = sourceCards[index]; if (!card) return;
    const local = localSourceLink(source.localUrl), notice = localSourceLink(source.noticeUrl);
    if (local || notice) card.insertAdjacentHTML('beforeend', `<p class="source-local-links" style="margin-top:14px;margin-bottom:0">${local ? `<a href="${escapeHTML(local)}">Yerel kaynak dosyası</a>` : ''}${local && notice ? ' · ' : ''}${notice ? `<a href="${escapeHTML(notice)}">Lisans ve atıf metni</a>` : ''}</p>`);
    if (source.sha256) card.insertAdjacentHTML('beforeend', `<small class="mono" style="display:block;font-size:9px;margin-top:9px;overflow-wrap:anywhere">SHA-256 ${escapeHTML(source.sha256)}</small>`);
  });
  const notices = state.catalog.copyrightNotices || {};
  if (Object.keys(notices).length) {
    const catalog = document.getElementById('document-catalog');
    catalog.insertAdjacentHTML('afterend', `<section class="copyright-notices" style="margin-top:35px"><h2>Lisans ve kaynak atıfları</h2>${Object.entries(notices).map(([key, notice]) => `<details class="support-box"><summary>${escapeHTML(key === 'qac' ? 'QAC v0.4 — telif ve kullanım koşulları' : key === 'tanzil' ? 'Tanzil — telif ve kullanım koşulları' : key)}</summary><div class="markdown"><pre><code>${escapeHTML(notice)}</code></pre></div></details>`).join('')}</section>`);
  }
  const update = () => { const q = humanFilterKey(filter.value); const docs = state.catalog.documents.filter(doc => humanFilterKey(`${doc.title} ${doc.path}`).includes(q)); document.getElementById('document-catalog').innerHTML = docs.map(doc => `<a href="${documentRoute(doc.id)}"><span>${escapeHTML(doc.title)}</span><small>${escapeHTML(doc.path)}</small></a>`).join('') || '<p class="subtle">Bu filtreyle dosya bulunamadı.</p>'; };
  filter.addEventListener('input', update); update();
  document.getElementById('check-update').addEventListener('click', () => setupOffline(true));
}
async function route() {
  if (!state.catalog) return;
  const routeId = ++state.routeId;
  closeWordPanel();
  const hash = location.hash || verseRoute(2, 2);
  try {
    const verseMatch = /^#\/ayet\/(\d+)\/(\d+)$/.exec(hash);
    if (verseMatch) {
      const surah = Number(verseMatch[1]), ayah = Number(verseMatch[2]);
      const meta = state.catalog.surahs.find(s => s.id === surah);
      if (!meta || ayah < 1 || ayah > meta.verseCount) throw new Error('Bu sûre veya ayet numarası geçerli değil. Sûre 1–114 arasında; ayet sûrenin ayet sayısı içinde olmalı.');
      content.innerHTML = '<p class="loading-line">Ayet açılıyor…</p>';
      const data = await loadSurah(surah); if (routeId !== state.routeId) return;
      const verse = data.verses.find(v => v.ayah === ayah); if (!verse) throw new Error('Ayet, bu derlemenin veri dosyasında bulunamadı.');
      renderVerse(data, verse);
    } else if (hash.startsWith('#/analiz/')) {
      const id = decodeURIComponent(hash.slice('#/analiz/'.length)); const doc = docById(id);
      if (!doc) throw new Error('Bu araştırma dosyası katalogda bulunamadı. Kaynaklar sayfasından mevcut dosyaları açabilirsiniz.');
      state.verse = null; renderSurahs(); content.innerHTML = '<p class="loading-line">Araştırma dosyası açılıyor…</p>';
      const data = await loadDocument(doc); if (routeId !== state.routeId) return; renderDocument(doc, data);
    } else if (hash === '#/kaynaklar') renderSources();
    else if (hash === '#/arama' || hash.startsWith('#/arama?')) await renderSearch(new URLSearchParams(hash.split('?')[1] || ''), routeId);
    else throw new Error('Bu bağlantı tanınmadı. Bir sûre, ayet veya araştırma dosyası seçin.');
    if (routeId === state.routeId) window.scrollTo({top:0, behavior:'instant'});
  } catch (error) { if (routeId === state.routeId) showError('Sayfa açılamadı', error.message); }
}
let toastTimer;
function toast(message) { const element = document.getElementById('toast'); element.textContent = message; element.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(() => { element.hidden = true; }, 4500); }
function offlineMessage(message, className = '') { const badge = document.getElementById('offline-status'); badge.textContent = message; badge.className = `offline-badge ${className}`; badge.title = message; }
async function setupOffline(check = false) {
  if (!('serviceWorker' in navigator) || !window.isSecureContext) { offlineMessage('Yerel kullanım · sunucu gerekli'); return; }
  try {
    offlineMessage('Çevrimdışı kopya hazırlanıyor', 'pending');
    const registration = await navigator.serviceWorker.register('sw.js', {scope:'./', updateViaCache:'none'});
    if (check) await registration.update();
    if (registration.active) registration.active.postMessage({type:'CACHE_STATUS'});
    registration.addEventListener('updatefound', () => { const worker = registration.installing; worker?.addEventListener('statechange', () => { if (worker.state === 'redundant') offlineMessage('Kopya tamamlanamadı · yerel kullanım', 'error'); }); });
    if (check) toast('Çevrimdışı kopya ve sürüm kontrolü başlatıldı.');
  } catch { offlineMessage('Yerel kullanım · kopya tamamlanamadı', 'error'); }
}
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('message', event => { const message = event.data;
    if (message.type === 'CACHE_PROGRESS') offlineMessage(`Kopyalanıyor ${message.done}/${message.total}`, 'pending');
    if (message.type === 'CACHE_READY') { offlineMessage('Çevrimdışı kopya hazır'); if (state.catalog && message.buildId !== state.catalog.buildId) toast('Yeni çevrimdışı sürüm hazır. Sayfayı yenileyerek yeni sürümü açabilirsiniz.'); }
    if (message.type === 'CACHE_ERROR') { offlineMessage('Yerel kullanım · kopya tamamlanamadı', 'error'); toast('Tarayıcı kopyası tamamlanamadı. Yerel sunucu üzerinden internet olmadan çalışmaya devam edebilirsiniz.'); }
  });
  navigator.serviceWorker.addEventListener('controllerchange', () => navigator.serviceWorker.controller?.postMessage({type:'CACHE_STATUS'}));
}
content.addEventListener('click', event => {
  const tokenButton = event.target.closest('[data-token]'); if (tokenButton) openWords(state.verse.tokens[Number(tokenButton.dataset.token)].wordIds, tokenButton);
  const wordButton = event.target.closest('[data-word]'); if (wordButton) openWords([Number(wordButton.dataset.word)], wordButton);
  const anchor = event.target.closest('[data-doc-anchor]'); if (anchor) { event.preventDefault(); const id = decodeURIComponent(anchor.getAttribute('href').slice(1)); const heading = [...content.querySelectorAll('[id]')].find(node => node.id === id); if (heading) heading.scrollIntoView({block:'start'}); else toast('Bu başlık dosyada bulunamadı.'); }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !wordPanel.hidden) { closeWordPanel(); return; }
  if (!wordPanel.hidden && event.key === 'Tab') {
    const elements = [...wordPanel.querySelectorAll('button,a[href],input,select,[tabindex="0"]')].filter(element => !element.disabled);
    if (event.shiftKey && document.activeElement === elements[0]) { event.preventDefault(); elements.at(-1)?.focus(); }
    else if (!event.shiftKey && document.activeElement === elements.at(-1)) { event.preventDefault(); elements[0]?.focus(); }
  }
  if (event.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { event.preventDefault(); document.getElementById('search-query').focus(); }
});
document.getElementById('global-search').addEventListener('submit', event => { event.preventDefault(); const query = document.getElementById('search-query').value.trim(); if (query) location.hash = searchRoute(document.getElementById('search-type').value, query); });
document.getElementById('surah-filter').addEventListener('input', () => state.catalog && renderSurahs());
window.addEventListener('hashchange', route);
(async () => { try { state.catalog = await readJSON('data/catalog.json'); if (state.catalog.schemaVersion !== 1 || !Array.isArray(state.catalog.surahs) || !Array.isArray(state.catalog.documents)) throw new Error('Uygulama verisinin sürümü uyumlu değil. Veri derlemesini yeniden oluşturun.'); renderSurahs(); if (!location.hash) history.replaceState(null, '', verseRoute(2, 2)); await route(); setupOffline(); } catch(error) { showError('Veri kütüphanesi açılamadı', `${error.message} Başlatma komutuyla verileri oluşturup yerel sunucuyu açın.`); } })();
