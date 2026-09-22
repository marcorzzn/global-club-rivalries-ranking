/**
 * RIVALITÀ — App principale
 * Futurismo Italiano · Design System 1920s Modernizzato
 * ─────────────────────────────────────────────────────
 * Architettura: Vanilla JS (ES Modules), no framework
 * Dipendenze: Leaflet, D3, html2canvas (CDN)
 */

'use strict';

// ═══════════════════════════════════════════
// STATO GLOBALE
// ═══════════════════════════════════════════
const State = {
  lang: 'it',
  theme: 'light',
  i18n: {},
  encyclopaedia: [],
  ranking: [],
  leagues: [],
  stadiums: [],
  filters: {
    enc: { search: '', continent: '', country: '', type: '' },
    rank: { search: '', continent: '' }
  },
  weights: { wL: 0.40, wP: 0.35, wM: 0.25 },
  encPage: 0,
  PAGE_SIZE: 30,
  mapInstance: null,
  chartsBuilt: false,
  currentSection: 'home'
};

// ═══════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════
async function init() {
  // Ripristina preferenze salvate
  const savedTheme = localStorage.getItem('rivalita-theme') || 'light';
  const savedLang  = localStorage.getItem('rivalita-lang')  || 'it';
  setTheme(savedTheme);
  await setLang(savedLang);

  // Carica dati in parallelo
  await Promise.all([
    loadEncyclopaedia(),
    loadRanking(),
    loadLeagues()
  ]);

  // Setup UI
  setupNav();
  setupHeaderControls();
  setupSliders();
  setupFilters();
  setupTableSort();
  setupModal();
  setupExport();
  setupMapFilters();

  // Routing da hash
  handleHashChange();
  window.addEventListener('hashchange', handleHashChange);

  // Hero stats
  updateHeroStats();
}

// ═══════════════════════════════════════════
// CARICAMENTO DATI
// ═══════════════════════════════════════════
async function loadEncyclopaedia() {
  try {
    const res = await fetch('data/rivalries_encyclopaedia.json');
    if (!res.ok) throw new Error('File non trovato');
    State.encyclopaedia = await res.json();
    populateCountryFilter();
    renderEncyclopaedia();
  } catch (e) {
    console.warn('Enciclopedia:', e.message);
    // Fallback vuoto con messaggio
    document.getElementById('enc-loading').innerHTML =
      `<p style="color:var(--color-text-muted);font-family:var(--font-mono);font-size:0.8rem">
        ${State.i18n['error.data'] || 'Dati in preparazione — riesegui build_data.py'}
      </p>`;
  }
}

async function loadRanking() {
  try {
    const res = await fetch('data/rivalries_ranking.json');
    if (!res.ok) throw new Error('File non trovato');
    State.ranking = await res.json();
    computeScores();
    renderRankingTable();
    populateRadarSelects();
  } catch (e) {
    console.warn('Ranking:', e.message);
    document.getElementById('rank-loading').innerHTML =
      `<p style="color:var(--color-text-muted);font-family:var(--font-mono);font-size:0.8rem">
        ${State.i18n['error.data'] || 'Dati ranking in preparazione — riesegui build_data.py'}
      </p>`;
  }
}

async function loadLeagues() {
  try {
    const res = await fetch('data/leagues_opta.json');
    if (!res.ok) throw new Error('File non trovato');
    const data = await res.json();
    State.leagues = data.leagues || [];
  } catch (e) {
    console.warn('Leghe:', e.message);
  }
}

async function loadStadiums() {
  if (State.stadiums.length > 0) return;
  try {
    const res = await fetch('data/stadiums.json');
    if (!res.ok) throw new Error('File non trovato');
    State.stadiums = await res.json();
  } catch (e) {
    console.warn('Stadi:', e.message);
  }
}

// ═══════════════════════════════════════════
// i18n
// ═══════════════════════════════════════════
async function setLang(lang) {
  State.lang = lang;
  localStorage.setItem('rivalita-lang', lang);
  try {
    const res = await fetch(`i18n/${lang}.json`);
    if (res.ok) State.i18n = await res.json();
  } catch (e) {
    console.warn('i18n:', e.message);
  }
  applyTranslations();
  updateLangToggle();
}

function t(key, fallback) {
  return State.i18n[key] || fallback || key;
}

function applyTranslations() {
  // Text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (State.i18n[key]) el.textContent = State.i18n[key];
  });
  // Placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    if (State.i18n[key]) el.placeholder = State.i18n[key];
  });
  // Nav active
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(a => {
    if (a.dataset.nav === State.currentSection) a.classList.add('active');
    else a.classList.remove('active');
  });
  // html lang
  document.documentElement.lang = State.lang;
}

function updateLangToggle() {
  document.querySelector('.lang-it').classList.toggle('active', State.lang === 'it');
  document.querySelector('.lang-en').classList.toggle('active', State.lang === 'en');
}

// ═══════════════════════════════════════════
// THEME
// ═══════════════════════════════════════════
function setTheme(theme) {
  State.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('rivalita-theme', theme);
}

function toggleTheme() {
  setTheme(State.theme === 'light' ? 'dark' : 'light');
}

// ═══════════════════════════════════════════
// NAVIGAZIONE
// ═══════════════════════════════════════════
function handleHashChange() {
  const hash = window.location.hash.replace('#', '') || 'home';
  navigateTo(hash);
}

function navigateTo(section) {
  const validSections = ['home', 'encyclopaedia', 'ranking', 'map', 'charts', 'about'];
  if (!validSections.includes(section)) section = 'home';

  State.currentSection = section;

  // Sezioni
  document.querySelectorAll('.page-section').forEach(s => {
    if (s.id === section) {
      s.removeAttribute('hidden');
      s.style.display = '';
    } else {
      s.setAttribute('hidden', '');
    }
  });

  // Nav links
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(a => {
    a.classList.toggle('active', a.dataset.nav === section || a.href.includes('#' + section));
  });

  // Chiudi mobile menu
  document.getElementById('mobile-nav').classList.remove('open');

  // Lazy init sezioni
  if (section === 'map') initMap();
  if (section === 'charts') initCharts();
  if (section === 'home') renderFeatured();

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setupNav() {
  document.querySelectorAll('[data-nav], .nav-link, .mobile-nav-link').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href && href.startsWith('#')) {
        e.preventDefault();
        const section = href.replace('#', '');
        window.history.pushState(null, '', `#${section}`);
        navigateTo(section);
      }
    });
  });
}

function setupHeaderControls() {
  // Theme
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

  // Lang
  document.getElementById('lang-toggle').addEventListener('click', () => {
    setLang(State.lang === 'it' ? 'en' : 'it');
    // Re-render content that depends on language
    renderEncyclopaedia();
    renderRankingTable();
  });

  // Mobile menu
  document.getElementById('mobile-menu-btn').addEventListener('click', () => {
    const nav = document.getElementById('mobile-nav');
    nav.classList.toggle('open');
    nav.setAttribute('aria-hidden', !nav.classList.contains('open'));
  });
}

// ═══════════════════════════════════════════
// HERO STATS
// ═══════════════════════════════════════════
function updateHeroStats() {
  animateCount('stat-rivalries', State.encyclopaedia.length);
  animateCount('stat-ranked', State.ranking.length);
  animateCount('stat-leagues', State.leagues.length);
  const countries = new Set(State.encyclopaedia.map(r => r.country).filter(Boolean));
  animateCount('stat-countries', countries.size);
}

function animateCount(id, target) {
  const el = document.getElementById(id);
  if (!el || !target) { if (el) el.textContent = '—'; return; }
  let current = 0;
  const step = Math.max(1, Math.floor(target / 40));
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString();
    if (current >= target) clearInterval(interval);
  }, 30);
}

// ═══════════════════════════════════════════
// FEATURED (home)
// ═══════════════════════════════════════════
function renderFeatured() {
  const container = document.getElementById('featured-grid');
  if (!container) return;

  // Top 6 per score se ranking disponibile, altrimenti primi 6 enciclopedia
  const source = State.ranking.length > 0
    ? State.ranking.slice(0, 6)
    : State.encyclopaedia.slice(0, 6);

  if (source.length === 0) {
    container.innerHTML = '';
    return;
  }

  container.innerHTML = source.map((r, i) => buildRivalryCard(r, i, true)).join('');
  attachCardListeners(container);
}

// ═══════════════════════════════════════════
// FORMULA & SCORE
// ═══════════════════════════════════════════
function computeScores() {
  if (!State.ranking.length) return;

  const { wL, wP, wM } = State.weights;
  const sum = wL + wP + wM;
  const nwL = wL / sum;
  const nwP = wP / sum;
  const nwM = wM / sum;

  // L e M: normalizzazione lineare su 100
  const maxL = Math.max(...State.ranking.map(r => r.l_raw || 0)) || 1;
  const maxM = Math.max(...State.ranking.map(r => r.m_raw || 0)) || 1;

  // P: normalizzazione LOGARITMICA — evita che un singolo derby
  // con migliaia di precedenti schiacci tutto il resto.
  // Formula: log(p+1) / log(maxP+1) × 100
  const maxP = Math.max(...State.ranking.map(r => r.p_raw || 0)) || 1;
  const maxLogP = Math.log(maxP + 1) || 1;

  State.ranking.forEach(r => {
    const L = ((r.l_raw || 0) / maxL) * 100;
    const P = (Math.log((r.p_raw || 0) + 1) / maxLogP) * 100;
    const M = ((r.m_raw || 0) / maxM) * 100;

    // B = Bonus Derby: moltiplicatore per prossimità geografica.
    // Stessa città   → ×1.15
    // Stessa regione → ×1.05
    // Altro          → ×1.00 (nessun malus)
    const B = r.derby_type === 'city' ? 1.15 : r.derby_type === 'regional' ? 1.05 : 1.0;

    r.score_l = +L.toFixed(1);
    r.score_p = +P.toFixed(1);
    r.score_m = +M.toFixed(1);
    r.derby_bonus = B;
    r.score = +((nwL * L + nwP * P + nwM * M) * B).toFixed(2);
  });

  // Sort desc per score
  State.ranking.sort((a, b) => b.score - a.score);
}

// ═══════════════════════════════════════════
// SLIDERS
// ═══════════════════════════════════════════
function setupSliders() {
  const sliderWL = document.getElementById('slider-wl');
  const sliderWP = document.getElementById('slider-wp');
  const sliderWM = document.getElementById('slider-wm');

  if (!sliderWL) return;

  function onSliderChange() {
    State.weights.wL = +sliderWL.value / 100;
    State.weights.wP = +sliderWP.value / 100;
    State.weights.wM = +sliderWM.value / 100;

    // Normalizza display
    const total = State.weights.wL + State.weights.wP + State.weights.wM;
    document.getElementById('val-wl').textContent = (State.weights.wL / total).toFixed(2);
    document.getElementById('val-wp').textContent = (State.weights.wP / total).toFixed(2);
    document.getElementById('val-wm').textContent = (State.weights.wM / total).toFixed(2);

    // Ricalcola e re-render
    computeScores();
    renderRankingTable();
  }

  sliderWL.addEventListener('input', onSliderChange);
  sliderWP.addEventListener('input', onSliderChange);
  sliderWM.addEventListener('input', onSliderChange);

  document.getElementById('sliders-reset').addEventListener('click', () => {
    sliderWL.value = 40;
    sliderWP.value = 35;
    sliderWM.value = 25;
    State.weights = { wL: 0.40, wP: 0.35, wM: 0.25 };
    document.getElementById('val-wl').textContent = '0.40';
    document.getElementById('val-wp').textContent = '0.35';
    document.getElementById('val-wm').textContent = '0.25';
    computeScores();
    renderRankingTable();
  });

  document.getElementById('export-btn').addEventListener('click', () => {
    document.getElementById('export-overlay').removeAttribute('hidden');
    buildExportSlides();
  });
}

// ═══════════════════════════════════════════
// FILTRI ENCICLOPEDIA
// ═══════════════════════════════════════════
function setupFilters() {
  const encSearch    = document.getElementById('enc-search');
  const encContinent = document.getElementById('enc-continent');
  const encCountry   = document.getElementById('enc-country');
  const encType      = document.getElementById('enc-type');
  const rankSearch   = document.getElementById('rank-search');
  const rankContinent = document.getElementById('rank-continent');

  if (encSearch) {
    let debounceTimer;
    encSearch.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        State.filters.enc.search = encSearch.value.trim().toLowerCase();
        State.encPage = 0;
        renderEncyclopaedia();
      }, 200);
    });
  }

  if (encContinent) {
    encContinent.addEventListener('change', () => {
      State.filters.enc.continent = encContinent.value;
      State.filters.enc.country = '';
      if (document.getElementById('enc-country')) {
        document.getElementById('enc-country').value = '';
      }
      State.encPage = 0;
      renderEncyclopaedia();
      populateCountryFilter();
    });
  }

  if (encCountry) {
    encCountry.addEventListener('change', () => {
      State.filters.enc.country = encCountry.value;
      State.encPage = 0;
      renderEncyclopaedia();
    });
  }

  if (encType) {
    encType.addEventListener('change', () => {
      State.filters.enc.type = encType.value;
      State.encPage = 0;
      renderEncyclopaedia();
    });
  }

  if (rankSearch) {
    let debounceTimer;
    rankSearch.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        State.filters.rank.search = rankSearch.value.trim().toLowerCase();
        renderRankingTable();
      }, 200);
    });
  }

  if (rankContinent) {
    rankContinent.addEventListener('change', () => {
      State.filters.rank.continent = rankContinent.value;
      renderRankingTable();
    });
  }

  // Load more button
  const loadMore = document.getElementById('enc-load-more');
  if (loadMore) {
    loadMore.addEventListener('click', () => {
      State.encPage++;
      renderEncyclopaedia(true);
    });
  }
}

function populateCountryFilter() {
  const select = document.getElementById('enc-country');
  if (!select) return;

  const filtered = State.filters.enc.continent
    ? State.encyclopaedia.filter(r => r.continent === State.filters.enc.continent)
    : State.encyclopaedia;

  const countries = [...new Set(filtered.map(r => r.country).filter(Boolean))].sort();
  const currentVal = select.value;

  select.innerHTML = `<option value="">${t('filter.all', 'Tutte')}</option>`;
  countries.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    if (c === currentVal) opt.selected = true;
    select.appendChild(opt);
  });
}

// ═══════════════════════════════════════════
// RENDER ENCICLOPEDIA
// ═══════════════════════════════════════════
function getFilteredEncyclopaedia() {
  const { search, continent, country, type } = State.filters.enc;
  return State.encyclopaedia.filter(r => {
    if (continent && r.continent !== continent) return false;
    if (country  && r.country  !== country)    return false;
    if (type     && r.type     !== type)       return false;
    if (search) {
      const q = search.toLowerCase();
      const haystack = [r.name_en, r.name_it, r.team1, r.team2, r.country, r.league]
        .filter(Boolean).join(' ').toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });
}

function renderEncyclopaedia(append = false) {
  const container = document.getElementById('enc-grid');
  const loading   = document.getElementById('enc-loading');
  const loadMore  = document.getElementById('enc-load-more');
  if (!container) return;

  const filtered = getFilteredEncyclopaedia();
  const total    = filtered.length;
  const start    = append ? State.encPage * State.PAGE_SIZE : 0;
  const slice    = filtered.slice(start, start + State.PAGE_SIZE);

  // Count
  const countEl = document.getElementById('enc-count');
  if (countEl) countEl.textContent = total.toLocaleString();

  if (!append) {
    container.innerHTML = '';
    if (loading) loading.remove();
  }

  if (slice.length === 0 && !append) {
    container.innerHTML = `<div class="loading-state"><p style="font-family:var(--font-mono);font-size:0.8rem;color:var(--color-text-muted)">${t('filter.empty', 'Nessuna rivalità trovata per i filtri selezionati.')}</p></div>`;
    if (loadMore) loadMore.hidden = true;
    return;
  }

  slice.forEach((r, i) => {
    container.insertAdjacentHTML('beforeend', buildRivalryCard(r, start + i, false));
  });

  // Attach listeners ai nuovi elementi
  container.querySelectorAll('.rivalry-card:not([data-attached])').forEach(card => {
    card.dataset.attached = 'true';
    card.addEventListener('click', () => {
      const id = card.dataset.id;
      openModal(id, 'encyclopaedia');
    });
  });

  // Load more button
  if (loadMore) {
    const shown = start + State.PAGE_SIZE;
    loadMore.hidden = shown >= total;
  }
}

// ═══════════════════════════════════════════
// BUILD RIVALRY CARD HTML
// ═══════════════════════════════════════════
function buildRivalryCard(rivalry, index, showScore) {
  const name = State.lang === 'it'
    ? (rivalry.name_it || rivalry.name_en)
    : (rivalry.name_en || rivalry.name_it);

  const badgeType = {
    city_derby:    `<span class="card-badge badge-city">${t('badge.city', 'Derby cittadino')}</span>`,
    regional:      `<span class="card-badge badge-regional">${t('badge.regional', 'Regionale')}</span>`,
    national:      `<span class="card-badge badge-national">${t('badge.national', 'Nazionale')}</span>`,
    international: `<span class="card-badge badge-international">${t('badge.intl', 'Internazionale')}</span>`
  };

  const badge = badgeType[rivalry.type] || '';
  const scoreBar = showScore && rivalry.score != null
    ? `<div class="card-score-bar"><div class="card-score-fill" style="width:${Math.min(rivalry.score, 100)}%"></div></div>`
    : '';

  return `
    <article class="rivalry-card" data-id="${rivalry.id || index}" role="listitem" tabindex="0"
             aria-label="${name}" style="animation-delay:${Math.min(index * 0.04, 0.5)}s">
      <div class="card-teams">
        <div class="team-logo-wrap">
          ${rivalry.logo1
            ? `<img class="team-logo" src="${rivalry.logo1}" alt="${rivalry.team1 || ''}" loading="lazy" onerror="this.style.display='none';this.nextSibling.style.display='flex'">`
            : ''}
          <div class="team-logo-placeholder" ${rivalry.logo1 ? 'style="display:none"' : ''}>
            ${rivalry.team1 ? rivalry.team1.substring(0, 2).toUpperCase() : '?'}
          </div>
        </div>
        <span class="card-vs">VS</span>
        <div class="team-logo-wrap">
          ${rivalry.logo2
            ? `<img class="team-logo" src="${rivalry.logo2}" alt="${rivalry.team2 || ''}" loading="lazy" onerror="this.style.display='none';this.nextSibling.style.display='flex'">`
            : ''}
          <div class="team-logo-placeholder" ${rivalry.logo2 ? 'style="display:none"' : ''}>
            ${rivalry.team2 ? rivalry.team2.substring(0, 2).toUpperCase() : '?'}
          </div>
        </div>
      </div>

      <div class="card-name">${name}</div>

      <div class="card-meta">
        ${badge}
        ${rivalry.country ? `<span class="card-country">${rivalry.country}</span>` : ''}
      </div>

      ${scoreBar}
    </article>
  `;
}

function attachCardListeners(container) {
  container.querySelectorAll('.rivalry-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.id;
      openModal(id, 'ranking');
    });
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') card.click();
    });
  });
}

// ═══════════════════════════════════════════
// RENDER RANKING TABLE
// ═══════════════════════════════════════════
function getFilteredRanking() {
  const { search, continent } = State.filters.rank;
  return State.ranking.filter(r => {
    if (continent && r.continent !== continent) return false;
    if (search) {
      const q = search.toLowerCase();
      const hay = [r.name_en, r.name_it, r.team1, r.team2, r.league, r.country]
        .filter(Boolean).join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

function renderRankingTable() {
  const tbody   = document.getElementById('ranking-tbody');
  const loading = document.getElementById('rank-loading');
  if (!tbody) return;

  const filtered = getFilteredRanking();
  const countEl  = document.getElementById('rank-count');
  if (countEl) countEl.textContent = filtered.length.toLocaleString();

  if (loading) loading.remove();

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:2rem;font-family:var(--font-mono);font-size:0.8rem;color:var(--color-text-muted)">${t('filter.empty', 'Nessun risultato trovato.')}</td></tr>`;
    return;
  }

  const maxScore = filtered[0]?.score || 100;

  tbody.innerHTML = filtered.map((r, i) => {
    const globalRank = State.ranking.indexOf(r) + 1;
    const rank = globalRank || i + 1;
    const name = State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it);
    const scorePct = ((r.score || 0) / maxScore * 100).toFixed(1);

    const rankClass = rank <= 3 ? 'rank-num-top' : rank <= 10 ? 'rank-num-gold' : '';
    const derbyBadge = r.derby_type === 'city'
      ? `<span class="derby-badge derby-city">${t('badge.city_short', '🏙 DERBY')}</span>`
      : r.derby_type === 'regional'
      ? `<span class="derby-badge derby-regional">${t('badge.regional_short', '🗺 REGION')}</span>`
      : '—';

    const leagueLine = r.league
      ? `${r.league}${r.league_rank ? ` <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--color-text-muted)">#${r.league_rank}</span>` : ''}`
      : '—';

    return `
      <tr>
        <td class="col-rank"><span class="${rankClass}">${rank}</span></td>
        <td class="col-rivalry">
          <div class="rivalry-cell">
            <div class="rival-logos">
              ${r.logo1 ? `<img class="rival-logo" src="${r.logo1}" alt="${r.team1||''}" loading="lazy" onerror="this.style.display='none'">` : `<div class="rival-logo-placeholder">${(r.team1||'?').substring(0,2).toUpperCase()}</div>`}
              <span class="rival-vs">vs</span>
              ${r.logo2 ? `<img class="rival-logo" src="${r.logo2}" alt="${r.team2||''}" loading="lazy" onerror="this.style.display='none'">` : `<div class="rival-logo-placeholder">${(r.team2||'?').substring(0,2).toUpperCase()}</div>`}
            </div>
            <span class="rival-name" data-id="${r.id || i}" title="${name}">${name}</span>
          </div>
        </td>
        <td class="col-league">${leagueLine}</td>
        <td class="col-score score-cell">
          <div class="score-bar-wrap">
            <div class="score-bar"><div class="score-bar-fill" style="width:${scorePct}%"></div></div>
            <span class="score-val">${(r.score || 0).toFixed(1)}</span>
          </div>
        </td>
        <td class="col-l"><span class="param-cell">${(r.score_l || 0).toFixed(0)}</span></td>
        <td class="col-p"><span class="param-cell">${(r.score_p || 0).toFixed(0)}</span></td>
        <td class="col-m"><span class="param-cell">${(r.score_m || 0).toFixed(0)}</span></td>
        <td>${derbyBadge}</td>
        <td>${r.wikipedia_url ? `<a class="wiki-link" href="${r.wikipedia_url}" target="_blank" rel="noopener" title="Wikipedia">↗ Wiki</a>` : '—'}</td>
      </tr>
    `;
  }).join('');

  // Click su rival-name per aprire modal
  tbody.querySelectorAll('.rival-name').forEach(el => {
    el.addEventListener('click', () => openModal(el.dataset.id, 'ranking'));
  });
}

function setupTableSort() {
  document.querySelectorAll('.ranking-table th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      const map = { score: 'score', l: 'score_l', p: 'score_p', m: 'score_m' };
      const field = map[key] || 'score';

      // Toggle direction
      const isDesc = th.classList.contains('sort-desc') || th.classList.contains('sort-active');
      document.querySelectorAll('.ranking-table th').forEach(h => {
        h.classList.remove('sort-active', 'sort-asc', 'sort-desc');
      });

      th.classList.add('sort-active');
      if (isDesc) {
        th.classList.add('sort-asc');
        State.ranking.sort((a, b) => (a[field] || 0) - (b[field] || 0));
      } else {
        th.classList.add('sort-desc');
        State.ranking.sort((a, b) => (b[field] || 0) - (a[field] || 0));
      }
      renderRankingTable();
    });
  });
}

// ═══════════════════════════════════════════
// MODAL
// ═══════════════════════════════════════════
function setupModal() {
  const modal = document.getElementById('rivalry-modal');
  const closeBtn = document.getElementById('modal-close');

  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });
}

function openModal(id, source) {
  const pool = source === 'ranking' ? State.ranking : State.encyclopaedia;
  let rivalry = pool.find(r => String(r.id) === String(id));
  if (!rivalry && source === 'ranking') {
    rivalry = State.encyclopaedia.find(r => String(r.id) === String(id));
  }
  if (!rivalry) {
    // Try numeric index
    const idx = parseInt(id, 10);
    rivalry = pool[idx] || State.encyclopaedia[idx];
  }
  if (!rivalry) return;

  const modal = document.getElementById('rivalry-modal');
  const badges = document.getElementById('modal-badges');
  const body   = document.getElementById('modal-body');

  const name = State.lang === 'it' ? (rivalry.name_it || rivalry.name_en) : (rivalry.name_en || rivalry.name_it);
  const summaryIT = rivalry.summary_it || rivalry.summary_en || t('modal.nodesc', 'Descrizione non disponibile.');
  const summaryEN = rivalry.summary_en || t('modal.nodesc', 'Description not available.');

  // Badges
  const typeLabel = {
    city_derby:    t('badge.city', 'Derby Cittadino'),
    regional:      t('badge.regional', 'Rivalità Regionale'),
    national:      t('badge.national', 'Rivalità Nazionale'),
    international: t('badge.intl', 'Rivalità Internazionale')
  };

  badges.innerHTML = rivalry.type
    ? `<span class="card-badge badge-${rivalry.type.replace('_derby', '_city')}">${typeLabel[rivalry.type] || rivalry.type}</span>`
    : '';

  if (rivalry.country) {
    badges.innerHTML += ` <span class="card-badge" style="border-color:var(--color-text-muted);color:var(--color-text-muted)">${rivalry.country}</span>`;
  }

  // Score breakdown if in ranking
  const rankEntry = State.ranking.find(r => r.id === rivalry.id) || (source === 'ranking' ? rivalry : null);
  const statsBlock = rankEntry && rankEntry.score != null ? `
    <div class="modal-stats">
      <div class="modal-stat">
        <span class="modal-stat-num">${(rankEntry.score || 0).toFixed(1)}</span>
        <span class="modal-stat-label">${t('modal.stat.score', 'Score Totale')}</span>
      </div>
      <div class="modal-stat">
        <span class="modal-stat-num" style="color:var(--color-var-p)">${rankEntry.p_raw != null ? rankEntry.p_raw.toLocaleString() : '—'}</span>
        <span class="modal-stat-label">${t('modal.stat.matches', 'Partite Storiche')}</span>
      </div>
      <div class="modal-stat">
        <span class="modal-stat-num" style="color:var(--color-var-m)">${rankEntry.m_raw != null ? rankEntry.m_raw : '—'}</span>
        <span class="modal-stat-label">${t('modal.stat.decades', 'Decenni Attivi')}</span>
      </div>
    </div>
    <div class="modal-source">
      ${t('modal.source.league', 'Lega')}: ${rankEntry.league || '—'} · Opta ${rankEntry.league_rank ? '#' + rankEntry.league_rank : ''} ·
      ${t('modal.source.snapshot', 'Snapshot')}: ${t('modal.source.date', 'settembre 2025')}
    </div>
  ` : '';

  body.innerHTML = `
    <div class="modal-teams-header">
      <div class="modal-team">
        ${rivalry.logo1 ? `<img class="modal-team-logo" src="${rivalry.logo1}" alt="${rivalry.team1||''}" loading="lazy">` : `<div class="team-logo-placeholder" style="width:64px;height:64px;font-size:1rem">${(rivalry.team1||'?').substring(0,3).toUpperCase()}</div>`}
        <span class="modal-team-name">${rivalry.team1 || '—'}</span>
      </div>
      <div class="modal-vs-block">
        <span class="modal-vs">VS</span>
      </div>
      <div class="modal-team">
        ${rivalry.logo2 ? `<img class="modal-team-logo" src="${rivalry.logo2}" alt="${rivalry.team2||''}" loading="lazy">` : `<div class="team-logo-placeholder" style="width:64px;height:64px;font-size:1rem">${(rivalry.team2||'?').substring(0,3).toUpperCase()}</div>`}
        <span class="modal-team-name">${rivalry.team2 || '—'}</span>
      </div>
    </div>

    <h2 class="modal-rivalry-name">${name}</h2>

    ${statsBlock}

    <!-- Language tabs -->
    <div class="lang-tabs">
      <button class="lang-tab ${State.lang === 'it' ? 'active' : ''}" data-lang="it">🇮🇹 Italiano</button>
      <button class="lang-tab ${State.lang === 'en' ? 'active' : ''}" data-lang="en">🇬🇧 English</button>
    </div>

    <div class="lang-content ${State.lang === 'it' ? 'active' : ''}" data-lang-content="it">
      <p class="modal-text">${summaryIT}</p>
    </div>
    <div class="lang-content ${State.lang === 'en' ? 'active' : ''}" data-lang-content="en">
      <p class="modal-text">${summaryEN}</p>
    </div>

    ${rivalry.wikipedia_url ? `
      <div style="margin-top:var(--space-xl);text-align:center">
        <a href="${rivalry.wikipedia_url}" target="_blank" rel="noopener" class="modal-wiki-link">
          ↗ ${t('modal.readmore', 'Leggi di più su Wikipedia')}
        </a>
      </div>
    ` : ''}

    <div class="modal-source" style="margin-top:var(--space-xl)">
      ${t('modal.source.label', 'Fonte')}: <a href="${rivalry.wikipedia_url || 'https://en.wikipedia.org'}" target="_blank" rel="noopener">Wikipedia</a> ·
      ${t('modal.source.retrieved', 'Dati recuperati')}: ${rivalry.data_retrieved || '2025-09-21'}
    </div>
  `;

  // Tab listeners
  body.querySelectorAll('.lang-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      body.querySelectorAll('.lang-tab, .lang-content').forEach(el => el.classList.remove('active'));
      tab.classList.add('active');
      body.querySelector(`[data-lang-content="${tab.dataset.lang}"]`)?.classList.add('active');
    });
  });

  modal.removeAttribute('hidden');
  modal.focus?.();
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('rivalry-modal').setAttribute('hidden', '');
  document.body.style.overflow = '';
}

// ═══════════════════════════════════════════
// MAP
// ═══════════════════════════════════════════
function setupMapFilters() {
  document.querySelectorAll('.map-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.map-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterMapMarkers(btn.dataset.filter);
    });
  });
}

async function initMap() {
  if (State.mapInstance) return; // già inizializzata
  await loadStadiums();

  const mapEl = document.getElementById('leaflet-map');
  if (!mapEl || typeof L === 'undefined') return;

  State.mapInstance = L.map('leaflet-map', {
    center: [20, 0],
    zoom: 2,
    zoomControl: true,
    attributionControl: true
  });

  // Tile: CartoDB Voyager (stile clean, leggibile)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(State.mapInstance);

  // Custom marker icon
  const rivalryIcon = L.divIcon({
    className: 'custom-div-icon',
    html: `<div style="
      width:10px;height:10px;
      background:var(--color-accent,#C8102E);
      border:2px solid white;
      border-radius:50%;
      box-shadow:0 1px 4px rgba(0,0,0,0.4)
    "></div>`,
    iconSize: [10, 10],
    iconAnchor: [5, 5]
  });

  State._mapMarkers = [];

  State.stadiums.forEach(stadium => {
    if (!stadium.lat || !stadium.lng) return;

    // Trova rivalità di questo club
    const clubRivalries = [...State.ranking, ...State.encyclopaedia].filter(r =>
      r.team1 === stadium.club || r.team2 === stadium.club
    );

    const marker = L.marker([stadium.lat, stadium.lng], { icon: rivalityIcon });

    const popupContent = `
      <div class="rivalry-popup">
        <div class="popup-club">${stadium.club}</div>
        <div class="popup-stadium">${stadium.stadium || '—'}</div>
        ${stadium.capacity ? `<div class="popup-capacity">${t('map.capacity', 'Capienza')}: ${Number(stadium.capacity).toLocaleString()}</div>` : ''}
        ${clubRivalries.length ? `
          <div class="popup-rivals">
            ${t('map.rivalries', 'Rivalità')}:
            ${clubRivalries.slice(0, 3).map(r => {
              const name = State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it);
              return `<div>◆ ${name}</div>`;
            }).join('')}
            ${clubRivalries.length > 3 ? `<div style="color:#999">+${clubRivalries.length - 3} ${t('map.more', 'altre')}</div>` : ''}
          </div>
        ` : ''}
        <div style="margin-top:8px">
          <span style="color:#999;font-size:0.65rem">${stadium.city}, ${stadium.country}</span>
        </div>
      </div>
    `;

    marker.bindPopup(popupContent, { maxWidth: 250 });
    marker._stadiumData = stadium;
    State._mapMarkers.push(marker);
    marker.addTo(State.mapInstance);
  });
}

function filterMapMarkers(filter) {
  if (!State._mapMarkers || !State.mapInstance) return;

  State._mapMarkers.forEach(marker => {
    const club = marker._stadiumData?.club;
    let show = true;

    if (filter === 'top10') {
      const top10clubs = new Set(
        State.ranking.slice(0, 10).flatMap(r => [r.team1, r.team2])
      );
      show = top10clubs.has(club);
    } else if (filter === 'derby') {
      const derbyClubs = new Set(
        State.ranking
          .filter(r => r.derby_type === 'city')
          .flatMap(r => [r.team1, r.team2])
      );
      show = derbyClubs.has(club);
    }

    if (show) {
      if (!State.mapInstance.hasLayer(marker)) marker.addTo(State.mapInstance);
    } else {
      if (State.mapInstance.hasLayer(marker)) State.mapInstance.removeLayer(marker);
    }
  });
}

// ═══════════════════════════════════════════
// CHARTS (D3)
// ═══════════════════════════════════════════
function initCharts() {
  if (State.chartsBuilt) return;
  State.chartsBuilt = true;

  if (typeof d3 === 'undefined') {
    console.warn('D3 non disponibile');
    return;
  }

  buildTreemap();
  buildTimeline();
  buildSunburst();
  buildLeaguesBar();
}

function buildTreemap() {
  const el = document.getElementById('chart-treemap');
  if (!el || !State.ranking.length) return;

  const w = el.clientWidth || 800;
  const h = 400;
  const margin = { top: 10, right: 10, bottom: 10, left: 10 };

  const svg = d3.select(el).append('svg')
    .attr('width', w).attr('height', h)
    .attr('viewBox', `0 0 ${w} ${h}`)
    .attr('preserveAspectRatio', 'xMidYMid meet');

  const continentColors = {
    'Europe': '#C8102E',
    'South America': '#1A5A9E',
    'North America': '#1A7A40',
    'Africa': '#C9A84C',
    'Asia': '#8B2FC9',
    'Oceania': '#2FC9B5'
  };

  const root = d3.hierarchy({
    name: 'root',
    children: d3.groups(State.ranking.slice(0, 80), r => r.continent || 'Other')
      .map(([continent, items]) => ({
        name: continent,
        children: items.map(r => ({
          name: State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it),
          value: r.score || 1,
          continent: r.continent,
          data: r
        }))
      }))
  }).sum(d => d.value).sort((a, b) => b.value - a.value);

  d3.treemap()
    .size([w - margin.left - margin.right, h - margin.top - margin.bottom])
    .paddingOuter(4)
    .paddingInner(2)
    .round(true)(root);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  const leaf = g.selectAll('g')
    .data(root.leaves())
    .join('g')
    .attr('transform', d => `translate(${d.x0},${d.y0})`);

  leaf.append('rect')
    .attr('width', d => d.x1 - d.x0)
    .attr('height', d => d.y1 - d.y0)
    .attr('rx', 2)
    .attr('fill', d => continentColors[d.data.continent] || '#888')
    .attr('opacity', 0.75)
    .attr('stroke', 'var(--color-bg)')
    .attr('stroke-width', 1)
    .style('cursor', 'pointer')
    .on('click', (event, d) => {
      if (d.data.data?.id != null) openModal(d.data.data.id, 'ranking');
    });

  leaf.filter(d => (d.x1 - d.x0) > 60 && (d.y1 - d.y0) > 24)
    .append('text')
    .attr('x', 4).attr('y', 14)
    .attr('font-family', 'Bebas Neue, sans-serif')
    .attr('font-size', d => Math.min(12, (d.x1 - d.x0) / 6))
    .attr('fill', 'white')
    .attr('opacity', 0.9)
    .text(d => d.data.name)
    .each(function(d) {
      const node = d3.select(this);
      const maxW = d.x1 - d.x0 - 8;
      let text = d.data.name;
      while (this.getComputedTextLength && this.getComputedTextLength() > maxW && text.length > 0) {
        text = text.slice(0, -1);
        node.text(text + '…');
      }
    });

  // Tooltip
  const tooltip = d3.select('body').select('.d3-tooltip');
  const tip = tooltip.empty()
    ? d3.select('body').append('div').attr('class', 'd3-tooltip').style('position', 'fixed').style('background', 'var(--color-surface)').style('border', '1px solid var(--color-border)').style('padding', '8px 12px').style('border-radius', '4px').style('font-size', '0.75rem').style('font-family', 'DM Mono, monospace').style('pointer-events', 'none').style('display', 'none').style('z-index', '9999')
    : tooltip;

  leaf.on('mouseover', (event, d) => {
    tip.style('display', 'block').html(`<strong>${d.data.name}</strong><br>${d.data.continent || ''}<br>Score: ${(d.data.value || 0).toFixed(1)}`);
  })
  .on('mousemove', event => {
    tip.style('left', (event.clientX + 12) + 'px').style('top', (event.clientY - 28) + 'px');
  })
  .on('mouseout', () => tip.style('display', 'none'));
}

function buildTimeline() {
  const el = document.getElementById('chart-timeline');
  if (!el || !State.ranking.length) return;

  const top20 = State.ranking.slice(0, 20).filter(r => r.first_decade && r.last_decade);
  if (!top20.length) return;

  const w = el.clientWidth || 600;
  const rowH = 28;
  const labelW = 160;
  const h = top20.length * rowH + 40;

  const svg = d3.select(el).append('svg')
    .attr('width', w).attr('height', h)
    .attr('viewBox', `0 0 ${w} ${h}`);

  const minDecade = d3.min(top20, r => r.first_decade) || 1880;
  const maxDecade = d3.max(top20, r => r.last_decade) || 2020;

  const x = d3.scaleLinear()
    .domain([minDecade, maxDecade])
    .range([labelW, w - 20]);

  // Axis
  const axis = d3.axisTop(x).tickFormat(d => `'${String(d).slice(2)}`).ticks(10);
  svg.append('g').attr('transform', `translate(0,20)`).call(axis)
    .attr('font-family', 'DM Mono, monospace').attr('font-size', 9)
    .select('.domain').remove();

  top20.forEach((r, i) => {
    const y = 24 + i * rowH;
    const name = State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it);

    // Label
    svg.append('text')
      .attr('x', labelW - 8).attr('y', y + 12)
      .attr('text-anchor', 'end').attr('dominant-baseline', 'middle')
      .attr('font-family', 'Bebas Neue, sans-serif').attr('font-size', 10)
      .attr('fill', 'var(--color-text)').attr('opacity', 0.8)
      .text(name.length > 22 ? name.slice(0, 20) + '…' : name);

    // Bar
    svg.append('rect')
      .attr('x', x(r.first_decade)).attr('y', y + 6)
      .attr('width', Math.max(4, x(r.last_decade) - x(r.first_decade)))
      .attr('height', 14)
      .attr('rx', 2)
      .attr('fill', `hsl(${(i * 18) % 360}, 70%, 45%)`)
      .attr('opacity', 0.8);
  });
}

function buildSunburst() {
  const el = document.getElementById('chart-sunburst');
  if (!el || !State.ranking.length) return;

  const size = Math.min(el.clientWidth || 300, 300);
  const radius = size / 2;

  const svg = d3.select(el).append('svg')
    .attr('width', size).attr('height', size)
    .attr('viewBox', `${-radius} ${-radius} ${size} ${size}`);

  const byLeague = d3.groups(State.ranking.slice(0, 100), r => r.league || 'Other');
  const data = {
    name: 'root',
    children: byLeague.slice(0, 20).map(([league, items]) => ({
      name: league,
      value: items.length,
      children: items.map(r => ({
        name: State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it),
        value: 1
      }))
    }))
  };

  const root = d3.hierarchy(data).sum(d => d.value);
  d3.partition().size([2 * Math.PI, radius])(root);

  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
    .padRadius(radius / 2)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1 - 1);

  const color = d3.scaleOrdinal(d3.schemeTableau10);

  svg.selectAll('path')
    .data(root.descendants().slice(1))
    .join('path')
    .attr('d', arc)
    .attr('fill', d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
    .attr('opacity', d => d.depth === 1 ? 0.9 : 0.6)
    .attr('stroke', 'var(--color-bg)')
    .attr('stroke-width', 0.5);

  // Labels for first level
  svg.selectAll('text')
    .data(root.descendants().filter(d => d.depth === 1 && (d.x1 - d.x0) > 0.3))
    .join('text')
    .attr('transform', d => {
      const [x, y] = arc.centroid(d);
      return `translate(${x},${y})`;
    })
    .attr('text-anchor', 'middle')
    .attr('font-family', 'Bebas Neue, sans-serif')
    .attr('font-size', 8)
    .attr('fill', 'white')
    .text(d => d.data.name.slice(0, 12));
}

function buildLeaguesBar() {
  const el = document.getElementById('chart-leagues');
  if (!el || !State.ranking.length) return;

  const byLeague = d3.groups(State.ranking, r => r.league || 'Other')
    .map(([league, items]) => ({ league, count: items.length }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 15);

  const w = el.clientWidth || 400;
  const h = 300;
  const margin = { top: 10, right: 20, bottom: 10, left: 120 };
  const innerW = w - margin.left - margin.right;
  const innerH = h - margin.top - margin.bottom;

  const svg = d3.select(el).append('svg')
    .attr('width', w).attr('height', h);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  const y = d3.scaleBand().domain(byLeague.map(d => d.league)).range([0, innerH]).padding(0.2);
  const x = d3.scaleLinear().domain([0, d3.max(byLeague, d => d.count)]).range([0, innerW]);

  g.selectAll('rect')
    .data(byLeague)
    .join('rect')
    .attr('y', d => y(d.league))
    .attr('height', y.bandwidth())
    .attr('width', d => x(d.count))
    .attr('rx', 2)
    .attr('fill', 'var(--color-accent)')
    .attr('opacity', (d, i) => 1 - i * 0.04);

  g.selectAll('.league-label')
    .data(byLeague)
    .join('text')
    .attr('class', 'league-label')
    .attr('x', -6)
    .attr('y', d => y(d.league) + y.bandwidth() / 2)
    .attr('dominant-baseline', 'middle')
    .attr('text-anchor', 'end')
    .attr('font-family', 'DM Mono, monospace')
    .attr('font-size', 9)
    .attr('fill', 'var(--color-text)')
    .text(d => d.league.length > 18 ? d.league.slice(0, 16) + '…' : d.league);

  g.selectAll('.count-label')
    .data(byLeague)
    .join('text')
    .attr('class', 'count-label')
    .attr('x', d => x(d.count) + 4)
    .attr('y', d => y(d.league) + y.bandwidth() / 2)
    .attr('dominant-baseline', 'middle')
    .attr('font-family', 'DM Mono, monospace')
    .attr('font-size', 9)
    .attr('fill', 'var(--color-text-muted)')
    .text(d => d.count);
}

function populateRadarSelects() {
  const selA = document.getElementById('radar-a');
  const selB = document.getElementById('radar-b');
  if (!selA || !selB || !State.ranking.length) return;

  const options = State.ranking.slice(0, 50).map((r, i) => {
    const name = State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it);
    return `<option value="${i}">${name}</option>`;
  }).join('');

  selA.innerHTML = `<option value="">${t('chart.radar.select', 'Seleziona A')}</option>` + options;
  selB.innerHTML = `<option value="">${t('chart.radar.select', 'Seleziona B')}</option>` + options;

  [selA, selB].forEach(sel => sel.addEventListener('change', buildRadar));
}

function buildRadar() {
  const selA = document.getElementById('radar-a');
  const selB = document.getElementById('radar-b');
  const el   = document.getElementById('chart-radar');
  if (!selA || !selB || !el) return;

  const rA = State.ranking[parseInt(selA.value, 10)];
  const rB = State.ranking[parseInt(selB.value, 10)];
  if (!rA || !rB) return;

  el.innerHTML = '';

  const size = Math.min(el.clientWidth || 280, 280);
  const cx = size / 2, cy = size / 2, r = size * 0.38;
  const axes = [
    { key: 'score_l', label: 'L' },
    { key: 'score_p', label: 'P' },
    { key: 'score_m', label: 'M' }
  ];
  const n = axes.length;
  const angle = (i) => (Math.PI * 2 / n) * i - Math.PI / 2;

  const svg = d3.select(el).append('svg')
    .attr('width', size).attr('height', size);

  // Grid circles
  [0.25, 0.5, 0.75, 1].forEach(pct => {
    svg.append('circle')
      .attr('cx', cx).attr('cy', cy)
      .attr('r', r * pct)
      .attr('fill', 'none')
      .attr('stroke', 'var(--color-border)')
      .attr('stroke-width', 0.5);
  });

  // Axes
  axes.forEach((ax, i) => {
    const a = angle(i);
    svg.append('line')
      .attr('x1', cx).attr('y1', cy)
      .attr('x2', cx + r * Math.cos(a))
      .attr('y2', cy + r * Math.sin(a))
      .attr('stroke', 'var(--color-border)').attr('stroke-width', 1);

    svg.append('text')
      .attr('x', cx + (r + 14) * Math.cos(a))
      .attr('y', cy + (r + 14) * Math.sin(a))
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
      .attr('font-family', 'Bebas Neue, sans-serif').attr('font-size', 12)
      .attr('fill', 'var(--color-text)').text(ax.label);
  });

  function polygon(rivalry, color) {
    const pts = axes.map((ax, i) => {
      const val = (rivalry[ax.key] || 0) / 100;
      const a = angle(i);
      return [cx + r * val * Math.cos(a), cy + r * val * Math.sin(a)];
    });
    svg.append('polygon')
      .attr('points', pts.map(p => p.join(',')).join(' '))
      .attr('fill', color).attr('opacity', 0.3)
      .attr('stroke', color).attr('stroke-width', 2);
  }

  polygon(rA, '#C8102E');
  polygon(rB, '#1A5A9E');

  // Legend
  const nameA = State.lang === 'it' ? (rA.name_it || rA.name_en) : (rA.name_en || rA.name_it);
  const nameB = State.lang === 'it' ? (rB.name_it || rB.name_en) : (rB.name_en || rB.name_it);

  [[nameA, '#C8102E', 16], [nameB, '#1A5A9E', 28]].forEach(([name, color, y]) => {
    svg.append('rect').attr('x', 8).attr('y', size - y - 6).attr('width', 10).attr('height', 10).attr('fill', color).attr('opacity', 0.7).attr('rx', 2);
    svg.append('text').attr('x', 22).attr('y', size - y).attr('dominant-baseline', 'middle').attr('font-family', 'DM Mono, monospace').attr('font-size', 8).attr('fill', 'var(--color-text)').text(name.slice(0, 30));
  });
}

// ═══════════════════════════════════════════
// EXPORT SLIDE
// ═══════════════════════════════════════════
function setupExport() {
  document.getElementById('export-close').addEventListener('click', () => {
    document.getElementById('export-overlay').setAttribute('hidden', '');
  });

  document.getElementById('export-overlay').addEventListener('click', e => {
    if (e.target === document.getElementById('export-overlay')) {
      document.getElementById('export-overlay').setAttribute('hidden', '');
    }
  });

  document.getElementById('export-download').addEventListener('click', downloadSlides);
}

function buildExportSlides() {
  const top100 = State.ranking.slice(0, 100);
  const slideSize = 25;
  const theme = document.querySelector('input[name="export-theme"]:checked')?.value || 'light';
  const bg    = theme === 'dark' ? '#0A0A0A' : '#F5F0E8';
  const fg    = theme === 'dark' ? '#F5F0E8' : '#0A0A0A';
  const red   = '#C8102E';

  for (let s = 0; s < 4; s++) {
    const slide = document.getElementById(`slide-${s + 1}`);
    if (!slide) continue;

    const items = top100.slice(s * slideSize, (s + 1) * slideSize);

    slide.style.cssText = `
      background:${bg};
      color:${fg};
      font-family:'Bebas Neue',sans-serif;
      padding:16px;
      display:flex;
      flex-direction:column;
    `;

    slide.innerHTML = `
      <div style="border-bottom:3px solid ${red};padding-bottom:8px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:flex-end">
        <div style="font-size:1.4rem;letter-spacing:0.06em;color:${red}">RIVALITÀ</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.5rem;letter-spacing:0.1em;opacity:0.5">${s * slideSize + 1}–${(s + 1) * slideSize}</div>
      </div>
      ${items.map((r, i) => {
        const rank = s * slideSize + i + 1;
        const name = State.lang === 'it' ? (r.name_it || r.name_en) : (r.name_en || r.name_it);
        const rankColor = rank <= 3 ? red : rank <= 10 ? '#C9A84C' : fg;
        return `
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;border-bottom:0.5px solid rgba(128,128,128,0.2)">
            <span style="font-size:0.9rem;min-width:24px;text-align:right;color:${rankColor};opacity:${rank <= 10 ? 1 : 0.7}">${rank}</span>
            <span style="font-size:0.65rem;flex:1;letter-spacing:0.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${name}</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.55rem;color:${red};min-width:32px;text-align:right">${(r.score||0).toFixed(1)}</span>
          </div>
        `;
      }).join('')}
      <div style="margin-top:auto;padding-top:8px;font-family:'DM Mono',monospace;font-size:0.4rem;letter-spacing:0.08em;opacity:0.4;text-align:center">
        RIVALITÀ · ATLANTE DEL CALCIO MONDIALE · DATI: 1975/76–2025/26 · OPTA SNAPSHOT SET.2025
      </div>
    `;
  }
}

async function downloadSlides() {
  if (typeof html2canvas === 'undefined') {
    alert(t('export.error', 'html2canvas non disponibile'));
    return;
  }

  const slides = document.querySelectorAll('.slide-preview');
  const btn = document.getElementById('export-download');
  btn.textContent = t('export.generating', 'Generazione in corso...');
  btn.disabled = true;

  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    try {
      const canvas = await html2canvas(slide, {
        scale: 3,
        useCORS: true,
        allowTaint: true,
        backgroundColor: null,
        logging: false
      });
      const link = document.createElement('a');
      link.download = `rivalita-slide-${i + 1}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      await new Promise(r => setTimeout(r, 300));
    } catch (e) {
      console.error('Export slide', i + 1, e);
    }
  }

  btn.textContent = t('export.download', '↓ Scarica 4 slide PNG');
  btn.disabled = false;
}

// ═══════════════════════════════════════════
// AVVIO
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', init);
