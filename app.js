// Constants & Globals
let rivalriesData = [];
let maxTotalMatches = 1;
let maxCombinedTrophies = 1;
let maxCapacity = 1;
let map;
let markers = [];
let currentLang = localStorage.getItem('lang') || 'it';
let i18n = {};

const countryEmojis = {
    "Italy": "🇮🇹", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Spain": "🇪🇸", "Germany": "🇩🇪",
    "France": "🇫🇷", "Argentina": "🇦🇷", "Brazil": "🇧🇷", "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱", "Turkey": "🇹🇷", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Uruguay": "🇺🇾",
    "Mexico": "🇲🇽", "USA": "🇺🇸", "Greece": "🇬🇷", "Algeria": "🇩🇿",
    "Morocco": "🇲🇦", "Tunisia": "🇹🇳", "Egypt": "🇪🇬", "South Africa": "🇿🇦",
    "Ghana": "🇬🇭", "Kenya": "🇰🇪", "Tanzania": "🇹🇿", "DR Congo": "🇨🇩",
    "Sudan": "🇸🇩", "Ivory Coast": "🇨🇮", "Iran": "🇮🇷", "Saudi Arabia": "🇸🇦",
    "Colombia": "🇨🇴", "Chile": "🇨🇱", "Peru": "🇵🇪", "Ecuador": "🇪🇨",
    "Paraguay": "🇵🇾", "Bolivia": "🇧🇴",
    "Egypt / Morocco": "🇪🇬🇲🇦", "Egypt / Tunisia": "🇪🇬🇹🇳",
    "Tunisia / Morocco": "🇹🇳🇲🇦", "Ecuador / Brazil": "🇪🇨🇧🇷",
    "Spain / Germany": "🇪🇸🇩🇪"
};

// Default Weights
const defaultWeights = { l: 0.30, t: 0.25, i: 0.25, s: 0.20 };
let weights = { ...defaultWeights };

// Elements
const domL = document.getElementById('slider-l');
const domT = document.getElementById('slider-t');
const domI = document.getElementById('slider-i');
const domS = document.getElementById('slider-s');
const valL = document.getElementById('val-l');
const valT = document.getElementById('val-t');
const valI = document.getElementById('val-i');
const valS = document.getElementById('val-s');

document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    setupListeners();
    await loadTranslations(currentLang);
    await loadData();
    initMap();
    renderAll();
});

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-mode');
    } else {
        document.body.classList.add('dark-mode');
    }
}

function setupListeners() {
    document.getElementById('theme-toggle').addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    });

    document.getElementById('lang-toggle').addEventListener('click', async () => {
        currentLang = currentLang === 'it' ? 'en' : 'it';
        localStorage.setItem('lang', currentLang);
        await loadTranslations(currentLang);
        applyTranslations();
        renderTable(); // re-render table if any translated text is inside
    });

    [domL, domT, domI, domS].forEach(el => {
        el.addEventListener('input', handleSliderChange);
    });

    document.getElementById('reset-sliders').addEventListener('click', () => {
        weights = { ...defaultWeights };
        updateSlidersUI();
        renderTable();
    });
}

async function loadTranslations(lang) {
    try {
        const response = await fetch(`i18n/${lang}.json`);
        if(response.ok) {
            i18n = await response.json();
            applyTranslations();
        }
    } catch(e) {
        console.error("Failed to load i18n", e);
    }
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (i18n[key]) {
            if (el.tagName === 'INPUT' && el.type === 'placeholder') {
                el.placeholder = i18n[key];
            } else {
                el.innerHTML = i18n[key];
            }
        }
    });
}

function getI18n(key) {
    return i18n[key] || key;
}

async function loadData() {
    try {
        const response = await fetch('data/rivalries.json');
        if (response.ok) {
            rivalriesData = await response.json();
            computeMaxValues();
        } else {
            console.error("Data file not found. Ensure data/rivalries.json exists.");
        }
    } catch(e) {
        console.error("Error loading data", e);
    }
}

function computeMaxValues() {
    if (rivalriesData.length === 0) return;
    maxTotalMatches = Math.max(...rivalriesData.map(r => r.total_matches));
    maxCombinedTrophies = Math.max(...rivalriesData.map(r => r.club_a.trophies + r.club_b.trophies));
    maxCapacity = Math.max(...rivalriesData.map(r => r.stadium_capacity_sum));
}

function handleSliderChange() {
    const raw = {
        l: parseFloat(domL.value),
        t: parseFloat(domT.value),
        i: parseFloat(domI.value),
        s: parseFloat(domS.value)
    };
    
    const sum = raw.l + raw.t + raw.i + raw.s;
    if (sum === 0) {
        weights = { l: 0.25, t: 0.25, i: 0.25, s: 0.25 };
    } else {
        weights = {
            l: raw.l / sum,
            t: raw.t / sum,
            i: raw.i / sum,
            s: raw.s / sum
        };
    }
    
    updateSlidersUI();
    renderTable();
}

function updateSlidersUI() {
    domL.value = weights.l.toFixed(2);
    domT.value = weights.t.toFixed(2);
    domI.value = weights.i.toFixed(2);
    domS.value = weights.s.toFixed(2);
    
    valL.innerText = weights.l.toFixed(2);
    valT.innerText = weights.t.toFixed(2);
    valI.innerText = weights.i.toFixed(2);
    valS.innerText = weights.s.toFixed(2);
}

function computeRScore(r) {
    // L
    const L = Math.log(r.total_matches) / Math.log(maxTotalMatches);
    // T
    const combinedTrophies = r.club_a.trophies + r.club_b.trophies;
    const T = combinedTrophies / maxCombinedTrophies;
    // I
    let I = (r.social_fracture_score / 3.0) + (r.documented_name ? 0.15 : 0);
    I = Math.min(I, 1.0);
    // S
    const S = r.stadium_capacity_sum / maxCapacity;
    // D
    const D = r.city_derby ? 1.15 : 1.0;

    const R = (weights.l * L + weights.t * T + weights.i * I + weights.s * S) * D;
    return R;
}

function renderTable() {
    const tbody = document.getElementById('ranking-body');
    tbody.innerHTML = '';

    if (rivalriesData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nessun dato disponibile / No data available</td></tr>';
        return;
    }

    const scoredData = rivalriesData.map(r => ({
        ...r,
        score: computeRScore(r)
    }));

    scoredData.sort((a, b) => b.score - a.score);

    scoredData.forEach((r, index) => {
        const tr = document.createElement('tr');
        
        const emoji = countryEmojis[r.country] || r.country;
        const derbyBadge = r.city_derby ? `<span class="badge-derby">${getI18n('table.badge_derby')}</span>` : '';

        // Club Logos with fallback
        const logoA = `<img src="${r.club_a.logo_url}" alt="${r.club_a.short}" class="club-logo" onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'><circle cx=\\'50\\' cy=\\'50\\' r=\\'50\\' fill=\\'${encodeURIComponent(r.club_a.color)}\\'/><text x=\\'50\\' y=\\'55\\' font-size=\\'30\\' text-anchor=\\'middle\\' fill=\\'white\\'>${r.club_a.short}</text></svg>';">`;
        const logoB = `<img src="${r.club_b.logo_url}" alt="${r.club_b.short}" class="club-logo" onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'><circle cx=\\'50\\' cy=\\'50\\' r=\\'50\\' fill=\\'${encodeURIComponent(r.club_b.color)}\\'/><text x=\\'50\\' y=\\'55\\' font-size=\\'30\\' text-anchor=\\'middle\\' fill=\\'white\\'>${r.club_b.short}</text></svg>';">`;

        tr.innerHTML = `
            <td><strong>${index + 1}</strong></td>
            <td>
                <div class="club-info">
                    ${logoA} <span>${r.club_a.name}</span>
                    <span class="vs-text">vs</span>
                    ${logoB} <span>${r.club_b.name}</span>
                    ${derbyBadge}
                </div>
            </td>
            <td><span style="font-size:1.2rem;" title="${r.country}">${emoji}</span></td>
            <td class="score-val">${(r.score * 100).toFixed(1)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function initMap() {
    map = L.map('map').setView([40.0, 10.0], 2);
    
    // CartoDB Positron for cleaner look fitting both dark and light themes (mostly light base)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    renderMapMarkers();
}

function renderMapMarkers() {
    // Clear old markers
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    const bounds = [];

    rivalriesData.forEach(r => {
        // Club A
        if (r.club_a.lat && r.club_a.lon) {
            const markerA = L.circleMarker([r.club_a.lat, r.club_a.lon], {
                color: r.club_a.color,
                fillColor: r.club_a.color,
                fillOpacity: 0.8,
                radius: 6
            }).addTo(map);
            markerA.bindPopup(`<strong>${r.club_a.name}</strong><br>${r.club_a.stadium}<br>${getI18n('club.trophies')}: ${r.club_a.trophies}`);
            markers.push(markerA);
            bounds.push([r.club_a.lat, r.club_a.lon]);
        }
        
        // Club B
        if (r.club_b.lat && r.club_b.lon) {
            const markerB = L.circleMarker([r.club_b.lat, r.club_b.lon], {
                color: r.club_b.color,
                fillColor: r.club_b.color,
                fillOpacity: 0.8,
                radius: 6
            }).addTo(map);
            markerB.bindPopup(`<strong>${r.club_b.name}</strong><br>${r.club_b.stadium}<br>${getI18n('club.trophies')}: ${r.club_b.trophies}`);
            markers.push(markerB);
            bounds.push([r.club_b.lat, r.club_b.lon]);
        }
    });

    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

function renderAll() {
    updateSlidersUI();
    renderTable();
}
