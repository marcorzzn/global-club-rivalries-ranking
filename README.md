# RIVALITÀ — L'Atlante del Calcio Mondiale

**Enciclopedia completa e ranking scientifico di tutte le rivalità calcistiche del mondo.**

🌐 **[Sito Live](https://marcorzzn.github.io/global-club-rivalries-ranking/)** · 🇮🇹 Italiano / 🇬🇧 English · ◑ Dark/Light mode

---

## Il Progetto

**RIVALITÀ** è un atlante digitale del calcio mondiale con due anime:

1. **Enciclopedia** — Tutte le rivalità calcistiche documentate su Wikipedia (~400-600 rivalità), organizzate per continente, nazione e tipo, con storia bilingue e link alle pagine Wikipedia.

2. **Classifica Scientifica** — Ranking di tutte le rivalità nelle leghe classificate da Opta (classifica completa, nessuna esclusione), calcolato con formula trasparente e parametri regolabili in tempo reale.

### Design
Stile ispirato al **Futurismo Italiano degli anni '20** — Fortunato Depero, F.T. Marinetti. Palette: Rosso Carminio · Nero Assoluto · Avorio · Oro. Modernizzato per massima leggibilità.

---

## La Formula

```
R = (wL × L + wP × P + wM × M) × B
```

| Parametro | Nome | Descrizione | Peso default |
|-----------|------|-------------|--------------|
| **L** | Prestigio Lega | Posizione nel ranking Opta completo | 0.40 |
| **P** | Precedenti | Numero totale di match storici (normalizzato con log) | 0.35 |
| **M** | Longevità | Decenni consecutivi con almeno una sfida | 0.25 |
| **B** | Derby Bonus | ×1.15 (stessa città) · ×1.05 (stessa regione) | — |

I pesi sono **liberamente regolabili** via slider. Si normalizzano automaticamente a 1. La classifica si ricalcola in tempo reale.

---

## Fonti Dati

| Dato | Fonte | Copertura |
|------|-------|-----------|
| Lista rivalità + storia | [Wikipedia — Category:Association football rivalries](https://en.wikipedia.org/wiki/Category:Association_football_rivalries) | 100% |
| Ranking globale leghe | [Opta / The Analyst](https://theanalyst.com) | Snapshot settembre 2025 |
| Coordinate stadi | [Wikidata SPARQL](https://query.wikidata.org) (P625) | Copertura variabile |
| Logo squadre | [Wikimedia Commons](https://commons.wikimedia.org) | Copertura variabile |
| Head-to-head count | Wikipedia (infobox rivalità) | Copertura variabile |

**Dati raccolti per 50 stagioni: 1975/76 – 2025/26.**

---

## Feature

- 📖 **Enciclopedia** con filtri per continente, nazione, tipo + ricerca live
- 🏆 **Ranking scientifico** con formula trasparente e slider regolabili
- 🗺️ **Mappa globale** degli stadi (Leaflet.js + CartoDB)
- 📊 **4 visualizzazioni D3**: treemap, timeline storica, sunburst leghe, spider chart
- 🌍 **Bilingue** completo — IT/EN switcher per ogni contenuto
- ◑ **Dark/Light mode**
- 📱 **PWA** — installabile, funziona offline
- 📤 **Export slide** — 4 PNG in formato 1:2 con le prime 100 rivalità

---

## Struttura

```
├── index.html          ← SPA principale
├── style.css           ← Design system futurista
├── app.js              ← Logica app (routing, formula, mappa, grafici, export)
├── manifest.json       ← PWA manifest
├── data/
│   ├── rivalries_encyclopaedia.json  ← Tutte le rivalità Wikipedia
│   ├── rivalries_ranking.json        ← Dataset ranking (leghe Opta)
│   ├── leagues_opta.json             ← Ranking Opta completo
│   └── stadiums.json                 ← Coordinate stadi
├── i18n/
│   ├── it.json         ← Traduzioni italiano
│   └── en.json         ← English translations
├── scripts/
│   ├── scrape_wikipedia.py    ← Raccolta dati enciclopedia
│   ├── build_ranking_data.py  ← Dataset ranking
│   └── build_stadiums.py      ← Coordinate stadi
└── .github/workflows/pages.yml
```

---

## Limitazioni Consapevoli

- **Fill rate stadi escluso**: i dati di affluenza per ogni partita (1976-2026) non sono uniformemente disponibili su scala globale. Non inclusi per mantenere il rigore scientifico.
- **Snapshot Opta**: il ranking delle leghe è uno snapshot fisso (settembre 2025). Il sito non si aggiorna automaticamente.
- **Head-to-head**: i conteggi provengono da Wikipedia. Le competizioni storicamente meno documentate possono avere dati incompleti.

---

## Licenza

MIT — [LICENSE](LICENSE)

---

## 🇮🇹 In breve

**RIVALITÀ** è un atlante digitale delle rivalità calcistiche mondiali. Enciclopedia (tutte le rivalità Wikipedia) + classifica scientifica (leghe Opta, formula aperta). Design ispirato al Futurismo italiano anni '20.
