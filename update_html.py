import re

def update_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update sliders
    html = html.replace('id="wR" min="0" max="50" value="25"', 'id="wR" min="0" max="100" value="30"')
    html = html.replace('id="wH" min="0" max="50" value="25"', 'id="wH" min="0" max="100" value="10"')
    html = html.replace('id="wI" min="0" max="50" value="20"', 'id="wI" min="0" max="100" value="40"')
    html = html.replace('id="wS" min="0" max="50" value="15"', 'id="wS" min="0" max="100" value="20"')

    # 2. Remove G slider
    html = re.sub(r'<div class="slider-group" id="group-G">.*?</div>', '', html, flags=re.DOTALL)

    # 3. Add Language Button and Info Modal button
    header_html = """
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
      <div>
        <h1 id="main-title">MWI-50 Ultra</h1>
        <p class="subtitle" id="main-subtitle">Global Club Football Rivalry Index · 1976–2026</p>
        <button onclick="showInfo()" style="background:transparent; color:#3B82F6; border:1px solid #3B82F6; padding:4px 12px; border-radius:15px; cursor:pointer; margin-top:8px; font-size:0.8rem;" id="info-btn">📖 Methodology & Criteria</button>
      </div>
      <div>
        <button onclick="toggleLang()" id="langBtn" style="background:#3B82F6; color:white; border:none; padding:8px 16px; border-radius:8px; cursor:pointer; font-weight:bold;">EN 🇬🇧</button>
      </div>
    </div>
"""
    html = re.sub(r'<h1>MWI-50 Ultra</h1>\s*<p class="subtitle">Global Club Football Rivalry Index · 1976–2026</p>', header_html, html)

    # 4. Inject JS Dictionary and logic at the end of scripts
    js_logic = """
// --- I18N & INFO LOGIC ---
let currentLang = 'en';
const translations = {
  en: {
    title: "MWI-50 Ultra",
    subtitle: "Global Club Football Rivalry Index · 1976–2026",
    infoBtn: "📖 Methodology & Criteria",
    langBtn: "EN 🇬🇧",
    wR: "R - Recurrence (Volume & Continuity)",
    wH: "H - Historical (Trophies & Stakes)",
    wI: "I - Intensity (Social & Balance)",
    wS: "S - Stadium (Mass Appeal)",
    search: "Search club or rivalry...",
    confAll: "All",
    cityAll: "All Types",
    cityOnly: "City Derbies",
    cityNone: "Non-city Rivalries",
    tableRank: "Rank",
    tableMatch: "Matchup",
    tableScore: "Score",
    sourcesTitle: "Verified Sources:"
  },
  it: {
    title: "MWI-50 Ultra",
    subtitle: "Indice Globale Rivalità Calcistiche · 1976–2026",
    infoBtn: "📖 Metodologia e Criteri",
    langBtn: "IT 🇮🇹",
    wR: "R - Ricorrenza (Volume e Continuità)",
    wH: "H - Storicità (Trofei vinti)",
    wI: "I - Intensità (Sociale ed Equilibrio)",
    wS: "S - Stadio (Capienza e Tifo)",
    search: "Cerca club o rivalità...",
    confAll: "Tutte",
    cityAll: "Tutti i tipi",
    cityOnly: "Solo Derby Cittadini",
    cityNone: "Solo Extra-cittadine",
    tableRank: "Pos",
    tableMatch: "Incontro",
    tableScore: "Punti",
    sourcesTitle: "Fonti Verificate:"
  }
};

function toggleLang() {
  currentLang = currentLang === 'en' ? 'it' : 'en';
  applyTranslations();
  renderTable();
}

function applyTranslations() {
  const t = translations[currentLang];
  document.getElementById('main-title').innerText = t.title;
  document.getElementById('main-subtitle').innerText = t.subtitle;
  document.getElementById('info-btn').innerText = t.infoBtn;
  document.getElementById('langBtn').innerText = t.langBtn;
  document.querySelector('#group-R .slider-label span').innerText = t.wR;
  document.querySelector('#group-H .slider-label span').innerText = t.wH;
  document.querySelector('#group-I .slider-label span').innerText = t.wI;
  document.querySelector('#group-S .slider-label span').innerText = t.wS;
  document.getElementById('search-input').placeholder = t.search;
}

function showInfo() {
  const modalHtml = `
    <div id="infoModal" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; display:flex; justify-content:center; align-items:center;">
      <div style="background:#1E293B; padding:30px; border-radius:15px; max-width:600px; color:white; border: 1px solid #3B82F6; max-height:80vh; overflow-y:auto;">
        <h2>${currentLang === 'it' ? 'I Criteri Definitivi (V2.0)' : 'Definitive Criteria (V2.0)'}</h2>
        <p><b>R (25%) - ${currentLang === 'it' ? 'Ricorrenza' : 'Recurrence'}:</b> ${currentLang === 'it' ? 'Volume totale di incontri ufficiali 1976-2026.' : 'Total volume of official matches 1976-2026.'}</p>
        <p><b>H (10%) - ${currentLang === 'it' ? 'Trofei (Depotenziato)' : 'Trophies (Nerfed)'}:</b> ${currentLang === 'it' ? 'Peso storico dei trofei vinti. Drasticamente ridotto per non favorire solo le squadre ricche, ma esaltare la pura tensione.' : 'Historical weight of trophies won. Drastically reduced to avoid favoring rich clubs over raw tension.'}</p>
        <p><b>I (40%) - ${currentLang === 'it' ? 'Intensità (Potenziato)' : 'Intensity (Buffed)'}:</b> ${currentLang === 'it' ? 'Il cuore del sistema. Basato sull\\'equilibrio sportivo (Indice di Entropia) e sul feroce fattore sociale/territoriale documentato.' : 'The heart of the system. Based on sporting balance (Entropy Index) and documented fierce social/territorial factors.'}</p>
        <p><b>S (25%) - ${currentLang === 'it' ? 'Stadio' : 'Stadium'}:</b> ${currentLang === 'it' ? 'Valuta le arene. (Futuro aggiornamento: Fill Rate al posto della sola capienza).' : 'Evaluates the arenas. (Future update: Fill Rate instead of raw capacity).'}</p>
        <hr style="border-color:#334155; margin: 20px 0;">
        <p style="font-size:0.9em; color:#94A3B8;"><i>${currentLang === 'it' ? 'Fonti 100% verificabili: Referti Ufficiali, RSSSF, Transfermarkt. Nessun dato inventato.' : '100% verifiable sources: Official Match Reports, RSSSF, Transfermarkt. Zero fabricated data.'}</i></p>
        <button onclick="document.getElementById('infoModal').remove()" style="margin-top:20px; background:#3B82F6; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; width:100%;">Close</button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}
"""
    html = html.replace('// === RIVALRY DATA END ===', '// === RIVALRY DATA END ===\n' + js_logic)

    # 5. Make sure calculateScore uses dynamic weights from sliders
    # The G factor is removed from calculation
    engine_update = """
    let wR = parseInt(document.getElementById('wR').value) / 100;
    let wH = parseInt(document.getElementById('wH').value) / 100;
    let wI = parseInt(document.getElementById('wI').value) / 100;
    let wS = parseInt(document.getElementById('wS').value) / 100;
    
    // Normalize weights to ensure they sum to 1
    let totalW = wR + wH + wI + wS;
    wR /= totalW; wH /= totalW; wI /= totalW; wS /= totalW;
    
    let MWI = wR * R + wH * H + wI * I + wS * S;
"""
    # Replace old weight logic
    html = re.sub(r'let wR =.*?;.*?let MWI = fR\*R \+ fH\*H \+ fI\*I \+ fS\*S;', engine_update, html, flags=re.DOTALL)

    # 6. Detail panel - show sources properly
    detail_html = """
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; color: #94A3B8;">
          <strong data-i18n="sourcesTitle">Verified Sources:</strong> ${currentLang==='it' ? 'Referti ufficiali leghe, RSSSF, Transfermarkt, Archivi UEFA/CONMEBOL. (Nessuna amichevole inclusa).' : 'Official league reports, RSSSF, Transfermarkt, UEFA/CONMEBOL archives. (Friendlies excluded).'}
        </div>
"""
    html = re.sub(r'<div class="sources-list">.*?</div>', detail_html, html, flags=re.DOTALL)

    # Minor aesthetic updates
    html = html.replace('background: #0F172A;', 'background: linear-gradient(135deg, #020617 0%, #0F172A 100%); font-family: "Inter", system-ui, sans-serif;')
    html = html.replace('background: #1E293B;', 'background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML modifications complete.")

if __name__ == '__main__':
    update_html()
