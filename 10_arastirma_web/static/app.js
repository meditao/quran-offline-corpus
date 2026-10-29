'use strict';

const AUTHOR_ORDER = ['okuyan', 'aktas', 'biz'];
const AUTHOR_NAMES = {okuyan:'Mehmet Okuyan', aktas:'Erhan Aktaş', biz:'Bizim tefsirli çevirimiz'};
const state = {catalog:null, surah:null, renderedSurah:null, routeVersion:0, cacheBuild:null, largeText:false};
const surahCache = new Map();
const content = document.getElementById('content');
const select = document.getElementById('surah-select');
const jumpForm = document.getElementById('verse-jump');
const jumpInput = document.getElementById('ayah-number');
const statusBadge = document.getElementById('offline-status');
const backToTop = document.getElementById('back-to-top');

// Kaynak metinlerini HTML olarak işlemeyerek çevirilerin aynen görünmesini sağla.
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}

// Yalnız bizim tefsirdeki vurguları göster; kaynak metni ve diğer çevirileri değiştirme.
function appendTranslationText(container, value, emphasis = false) {
  const text = String(value);
  if (!emphasis) {
    container.append(document.createTextNode(text));
    return;
  }
  const pattern = /\*\*([^\n]+?)\*\*|\*([^*\n]+)\*/g;
  let end = 0;
  for (const match of text.matchAll(pattern)) {
    container.append(document.createTextNode(text.slice(end, match.index)));
    const body = match[1] ?? match[2];
    if (body.trim()) {
      const node = element(match[1] !== undefined ? 'strong' : 'em');
      appendTranslationText(node, body, match[1] !== undefined);
      container.append(node);
    } else container.append(document.createTextNode(match[0]));
    end = match.index + match[0].length;
  }
  container.append(document.createTextNode(text.slice(end)));
}

async function readJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error('Dosya okunamadı.');
  return response.json();
}

function currentRoute() {
  const hash = window.location.hash;
  let match = hash.match(/^#\/sure\/(\d+)(?:\/ayet\/(\d+))?$/);
  if (match) return {surah:Number(match[1]), ayah:match[2] ? Number(match[2]) : null};
  match = hash.match(/^#\/ayet\/(\d+)\/(\d+)$/);
  if (match) return {surah:Number(match[1]), ayah:Number(match[2])};
  match = hash.match(/^#ayet-(\d+)$/);
  if (match) return {surah:state.surah || 10, ayah:Number(match[1])};
  return {surah:10, ayah:null};
}

function goToSurah(id) {
  const hash = `#/sure/${id}`;
  if (window.location.hash === hash) window.scrollTo({top:0, behavior:'smooth'});
  else window.location.hash = hash;
}

function noteText(note) {
  if (typeof note === 'string') return note;
  return String(note?.text ?? note?.message ?? '');
}

function safeLink(url) {
  if (typeof url !== 'string' || !url.trim()) return null;
  try {
    const parsed = new URL(url, window.location.href);
    return ['https:', 'http:'].includes(parsed.protocol) ? parsed.href : null;
  } catch { return null; }
}

function makeNoteButton(note, noteIndex, author, ref, panelId) {
  const button = element('button', 'note-reference', note.label || '*');
  button.type = 'button';
  button.setAttribute('aria-label', `${author}, ${ref}: açıklama ${noteIndex + 1}`);
  button.setAttribute('aria-expanded', 'false');
  button.setAttribute('aria-controls', panelId);
  button.title = `Açıklama ${noteIndex + 1}`;
  button.addEventListener('click', () => {
    const panel = document.getElementById(panelId);
    if (!panel) return;
    panel.hidden = !panel.hidden;
    // Aynı nota birden fazla yıldız işaretinden ulaşılabilir.
    content.querySelectorAll('button[aria-controls]').forEach(other => {
      if (other.getAttribute('aria-controls') === panelId) other.setAttribute('aria-expanded', String(!panel.hidden));
    });
  });
  return button;
}

function renderTranslation(translation, verse) {
  const authorId = translation.authorId;
  const author = AUTHOR_NAMES[authorId] || translation.author || 'Çeviri';
  const section = element('section', `translation translation-${authorId}`);
  const heading = element('div', 'translation-heading');
  heading.append(element('h3', 'author-name', author));
  if (authorId === 'biz') heading.append(element('span', 'interpretation-label', 'Yorum / tefsir'));
  section.append(heading);
  if (translation.available === false || !translation.text) {
    const missing = element('p', 'translation-unavailable', 'Henüz eklenmedi');
    const url = translation.sourceUrl && safeLink(translation.sourceUrl);
    if (url) {
      const link = element('a', 'translation-source', 'Kaynakta oku ↗');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.setAttribute('aria-label', `${author}: ${verse.ref} ayetini Açık Kuran’da oku`);
      missing.append(document.createTextNode(' · '), link);
    }
    section.append(missing);
    return section;
  }
  const text = element('p', 'translation-text');
  const notes = Array.isArray(translation.footnotes) ? translation.footnotes : [];
  const references = new Set();
  const panelId = index => `note-${verse.ayah}-${authorId}-${index}`;
  if (Array.isArray(translation.parts) && translation.parts.length) {
    translation.parts.forEach(part => {
      if (part.text !== undefined) appendTranslationText(text, part.text, authorId === 'biz');
      if (part.noteId !== undefined) {
        const index = notes.findIndex(note => String(note.id) === String(part.noteId));
        if (index >= 0) {
          references.add(index);
          text.append(makeNoteButton({...notes[index], label:part.label || notes[index].label}, index, author, verse.ref, panelId(index)));
        }
      }
    });
  } else appendTranslationText(text, translation.text, authorId === 'biz');
  section.append(text);
  const unplaced = notes.map((note, index) => ({note, index})).filter(({index}) => !references.has(index));
  if (unplaced.length) {
    const noteLinks = element('div', 'note-links');
    noteLinks.append(element('span', 'note-links-label', 'Açıklamalar'));
    unplaced.forEach(({note, index}) => noteLinks.append(makeNoteButton(note, index, author, verse.ref, panelId(index))));
    section.append(noteLinks);
  }
  notes.forEach((note, index) => {
    const panel = element('div', 'footnote');
    panel.id = panelId(index);
    panel.hidden = true;
    panel.setAttribute('role', 'group');
    panel.setAttribute('aria-label', `${author}: açıklama ${index + 1}`);
    panel.append(element('span', 'footnote-label', `Açıklama ${index + 1}`), element('p', 'footnote-text', noteText(note)));
    section.append(panel);
  });
  return section;
}

function renderVerse(verse, surah) {
  const article = element('article', 'verse');
  article.id = `ayet-${verse.ayah}`;
  article.dataset.ayah = verse.ayah;
  const head = element('div', 'verse-heading');
  const permalink = element('a', 'verse-number', verse.ayah);
  permalink.href = `#/sure/${surah.id}/ayet/${verse.ayah}`;
  permalink.setAttribute('aria-label', `${surah.name} sûresi, ${verse.ayah}. ayet`);
  const title = element('h2', 'verse-title', `${surah.name} ${verse.ref || `${surah.id}:${verse.ayah}`}`);
  head.append(permalink, title);
  article.append(head);
  const reading = element('div', 'reading');
  reading.append(element('span', 'reading-label', 'Türkçe okunuş'), element('p', 'reading-text', verse.reading || 'Okunuş henüz eklenmedi.'));
  if (Array.isArray(verse.readingNotes) && verse.readingNotes.length) {
    const details = element('details', 'reading-notes');
    details.append(element('summary', null, 'Okunuş hakkında'));
    verse.readingNotes.forEach(note => details.append(element('p', null, noteText(note))));
    reading.append(details);
  }
  article.append(reading);
  const translations = element('div', 'translations');
  AUTHOR_ORDER.forEach(authorId => {
    const translation = (verse.translations || []).find(item => item.authorId === authorId) || {authorId, available:false};
    translations.append(renderTranslation(translation, {...verse, ref:verse.ref || `${surah.id}:${verse.ayah}`}));
  });
  article.append(translations);
  return article;
}

function renderSurah(surah, data) {
  content.replaceChildren();
  const intro = element('section', 'surah-intro');
  intro.append(element('span', 'eyebrow', `${surah.id}. SÛRE`), element('h1', null, `${surah.name} sûresi`));
  if (!surah.available) {
    intro.classList.add('empty-surah');
    intro.append(element('p', 'intro-description', 'Bu sûre henüz hazırlanmadı.'));
    const link = element('a', 'return-link', 'Yûnus sûresini oku →');
    link.href = '#/sure/10';
    intro.append(link);
    content.append(intro);
    return;
  }
  const complete = (data.verses || []).every(verse => AUTHOR_ORDER.every(authorId => verse.translations?.some(item => item.authorId === authorId && item.available !== false && item.text)));
  intro.append(element('p', 'intro-description', `${surah.verseCount} ayet · ${complete ? 'Üç çeviri, tek sayfa' : 'Tek sayfada okuma denemesi'}`));
  if (state.catalog.sourceNotes?.length) {
    const notice = element('div', 'source-notice');
    state.catalog.sourceNotes.forEach(note => notice.append(element('p', null, noteText(note))));
    intro.append(notice);
  }
  const hasNotes = (data.verses || []).some(verse => verse.translations?.some(item => item.footnotes?.length));
  if (hasNotes) {
    const guidance = element('p', 'reading-guidance');
    guidance.append(document.createTextNode('Açıklamalar için çevirilerdeki '), element('span', 'guidance-star', '*'), document.createTextNode(' işaretlerine dokunun.'));
    intro.append(guidance);
  }
  content.append(intro);
  const verses = element('div', 'verse-list');
  (data.verses || []).forEach(verse => verses.append(renderVerse(verse, surah)));
  content.append(verses);
}

function renderFooter(surah) {
  const footer = document.getElementById('app-footer');
  footer.replaceChildren();
  footer.hidden = !surah.available;
  if (!surah.available) return;
  const inner = element('div', 'footer-inner');
  const details = element('details', 'source-details');
  details.append(element('summary', null, 'Çeviriler ve kaynaklar'));
  details.append(element('p', null, 'Mehmet Okuyan ve Erhan Aktaş çevirilerinin kaynağı Açık Kuran’dır. Bizim tefsirli çevirimiz, araştırma dosyamızdaki yorumdur; parantezler karşılık verilen kavramları gösterir.'));
  (state.catalog.sources || []).forEach(source => {
    const url = safeLink(source.url || source.sourceUrl);
    const paragraph = element('p', 'source-item');
    const title = source.label || source.name || source.title || 'Kaynak';
    if (url) {
      const link = element('a', null, title);
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      paragraph.append(link);
    } else paragraph.textContent = title;
    if (source.note) paragraph.append(document.createTextNode(` — ${source.note}`));
    details.append(paragraph);
  });
  inner.append(details, element('p', 'footer-caption', 'Okumaya devam etmek için sayfayı kaydırın. Tüm ayetler bu sayfada.'));
  footer.append(inner);
}

function scrollToVerse(ayah) {
  content.querySelectorAll('.is-current').forEach(node => node.classList.remove('is-current'));
  if (!ayah) {
    window.scrollTo({top:0, behavior:'auto'});
    return;
  }
  const verse = document.getElementById(`ayet-${ayah}`);
  if (verse) {
    verse.classList.add('is-current');
    verse.scrollIntoView({block:'start', behavior:'auto'});
    jumpInput.value = ayah;
  }
}

async function renderRoute() {
  if (!state.catalog) return;
  const version = ++state.routeVersion;
  const route = currentRoute();
  const surah = state.catalog.surahs.find(item => item.id === route.surah) || state.catalog.surahs.find(item => item.id === 10);
  if (!surah) return;
  state.surah = surah.id;
  select.value = surah.id;
  jumpForm.hidden = !surah.available;
  jumpInput.max = surah.verseCount;
  jumpInput.value = route.ayah && route.ayah <= surah.verseCount ? route.ayah : 1;
  document.title = `${surah.name} Sûresi · Kur’an Meal`;
  backToTop.href = `#/sure/${surah.id}`;
  if (state.renderedSurah === surah.id) {
    scrollToVerse(route.ayah);
    return;
  }
  try {
    let data = null;
    if (surah.available) {
      if (!surahCache.has(surah.id)) {
        content.replaceChildren(element('p', 'loading-state', 'Çeviriler açılıyor…'));
        surahCache.set(surah.id, await readJson(`data/reader/${String(surah.id).padStart(3, '0')}.json`));
      }
      data = surahCache.get(surah.id);
    }
    if (version !== state.routeVersion) return;
    renderSurah(surah, data);
    renderFooter(surah);
    state.renderedSurah = surah.id;
    requestAnimationFrame(() => { if (version === state.routeVersion) scrollToVerse(route.ayah); });
  } catch {
    if (version !== state.routeVersion) return;
    state.renderedSurah = null;
    const error = element('div', 'loading-state');
    error.append(element('h1', null, 'Çeviriler açılamadı'), element('p', null, 'Yerel sunucunun çalıştığından emin olun ve sayfayı yenileyin.'));
    const retry = element('button', 'retry-button', 'Yeniden dene');
    retry.type = 'button';
    retry.addEventListener('click', renderRoute);
    error.append(retry);
    content.replaceChildren(error);
    document.getElementById('app-footer').hidden = true;
  }
}

function setOfflineStatus(label, ready = false) {
  statusBadge.textContent = label;
  statusBadge.classList.toggle('is-ready', ready);
}

function handleCacheMessage(message) {
  if (!message || typeof message !== 'object') return;
  if (message.type === 'CACHE_PROGRESS') {
    setOfflineStatus('Çevrimdışı kopya hazırlanıyor');
    statusBadge.title = 'Dosyalar bu tarayıcıya kaydediliyor.';
  } else if (message.type === 'CACHE_READY') {
    state.cacheBuild = message.buildId;
    setOfflineStatus('Çevrimdışı hazır', true);
    statusBadge.title = 'Bu sayfa internet ve yerel sunucu kapalıyken de okunabilir.';
    if (state.catalog && message.buildId !== state.catalog.buildId) document.getElementById('update-notice').hidden = false;
  } else if (message.type === 'CACHE_ERROR') {
    setOfflineStatus('Yerel kullanım');
    statusBadge.title = 'Tarayıcıdaki çevrimdışı kopya henüz tamamlanmadı. Yerel sunucu açıkken okumaya devam edebilirsiniz.';
  }
}

async function startOfflineCache() {
  if (!('serviceWorker' in navigator) || !window.isSecureContext) return;
  navigator.serviceWorker.addEventListener('message', event => handleCacheMessage(event.data));
  try {
    const registration = await navigator.serviceWorker.register('sw.js');
    if (registration.active) registration.active.postMessage({type:'CACHE_STATUS'});
    const ready = await navigator.serviceWorker.ready;
    if (ready.active) ready.active.postMessage({type:'CACHE_STATUS'});
  } catch {
    statusBadge.title = 'Tarayıcıdaki çevrimdışı kopya oluşturulamadı. Yerel sunucu üzerinden okumaya devam edebilirsiniz.';
  }
}

document.querySelector('.skip-link').addEventListener('click', event => {
  event.preventDefault();
  content.focus();
  content.scrollIntoView({block:'start'});
});
select.addEventListener('change', () => goToSurah(Number(select.value)));
jumpForm.addEventListener('submit', event => {
  event.preventDefault();
  if (!jumpForm.reportValidity()) return;
  const ayah = Number(jumpInput.value);
  const hash = `#/sure/${state.surah}/ayet/${ayah}`;
  if (window.location.hash === hash) scrollToVerse(ayah);
  else window.location.hash = hash;
});
document.getElementById('font-toggle').addEventListener('click', event => {
  state.largeText = !state.largeText;
  document.body.classList.toggle('large-text', state.largeText);
  event.currentTarget.setAttribute('aria-pressed', String(state.largeText));
  event.currentTarget.setAttribute('aria-label', state.largeText ? 'Normal yazı boyutuna dön' : 'Yazıyı büyüt');
});
document.getElementById('reload-button').addEventListener('click', () => window.location.reload());
document.getElementById('dismiss-update').addEventListener('click', () => { document.getElementById('update-notice').hidden = true; });
window.addEventListener('hashchange', renderRoute);
let scrollScheduled = false;
window.addEventListener('scroll', () => {
  if (scrollScheduled) return;
  scrollScheduled = true;
  requestAnimationFrame(() => {
    backToTop.hidden = window.scrollY < 900 || !state.catalog?.surahs.find(surah => surah.id === state.surah)?.available;
    scrollScheduled = false;
  });
}, {passive:true});

async function boot() {
  try {
    state.catalog = await readJson('data/reader/catalog.json');
    select.replaceChildren();
    state.catalog.surahs.forEach(surah => {
      const option = element('option', null, `${surah.id} · ${surah.name}${surah.available ? '' : ' — henüz boş'}`);
      option.value = surah.id;
      select.append(option);
    });
    select.disabled = false;
    await renderRoute();
    startOfflineCache();
  } catch {
    const error = element('div', 'loading-state');
    error.append(element('h1', null, 'Meal açılamadı'), element('p', null, 'Yerel sunucuyu başlatın ve bu sayfayı sunucunun adresinden açın.'));
    content.replaceChildren(error);
    jumpForm.hidden = true;
  }
}
boot();
