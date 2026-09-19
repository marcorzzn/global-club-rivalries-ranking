# 🏆 Global Club Rivalries Ranking

**The definitive, data-driven ranking of the world's greatest football club rivalries.**

🌐 **[Live Website](https://marcorzzn.github.io/global-club-rivalries-ranking/)** | 🇮🇹 Italiano / 🇬🇧 English

---

## Overview

This project ranks **100 football rivalries** from clubs belonging to the **Top 50 leagues in the Opta ranking**, using a transparent, fully parameterizable mathematical formula. Every data point is sourced, verified, and traceable — no estimates, no null values, no guesswork.

### Features

- 📊 **Interactive ranking table** with real-time recalculation
- 🗺️ **Global stadium map** powered by Leaflet.js
- ⚙️ **Adjustable weights** — tune the 4 formula parameters via sliders
- 🌙 **Dark / Light mode** toggle
- 🇮🇹🇬🇧 **Bilingual** — full Italian and English support
- 📱 **Responsive** — works on desktop, tablet, and mobile

---

## The Formula

Each rivalry receives a score **R** computed as:

**R = (w<sub>L</sub> × L + w<sub>T</sub> × T + w<sub>I</sub> × I + w<sub>S</sub> × S) × D**

| Parameter | Description | Default Weight |
|-----------|-------------|----------------|
| **L** (Longevity) | Historical volume: total matches played, active decades | **0.30** |
| **T** (Prestige) | Combined major trophies (league titles + continental) | **0.25** |
| **I** (Intensity) | Social fracture score + recognized rivalry name bonus | **0.25** |
| **S** (Scale) | Combined stadium capacity of both clubs | **0.20** |
| **D** (Derby Bonus) | ×1.15 multiplier if both clubs share the same city | — |

All 4 weights are **freely adjustable** on the website. They are automatically normalized so their sum equals 1.

---

## Data Sources

| Data Point | Source | Coverage |
|------------|--------|----------|
| Rivalry list & match counts | [Wikipedia: List of football rivalries](https://en.wikipedia.org/wiki/List_of_association_football_rivalries) | 100% |
| Stadium coordinates | [Wikidata](https://www.wikidata.org/) (P625) & Google Maps | 100% |
| Club logos | [Wikimedia Commons](https://commons.wikimedia.org/) (direct URLs) | 100% |
| Trophy counts | Wikipedia club pages, verified against Transfermarkt | 100% |
| Stadium capacity | Wikipedia stadium pages | 100% |

**Zero null values.** Every field in every entry has a verified, sourced value.

---

## Scope

Rivalries were selected exclusively from clubs belonging to leagues ranked in the **Top 50 of the Opta Power Rankings**. This covers all major confederations: UEFA, CONMEBOL, CAF, AFC. The dataset spans rivalries from Europe, South America, Africa, the Middle East, and beyond.

---

## Project Structure

```
├── index.html          ← Single-page website
├── style.css           ← Styling (dark/light mode, responsive)
├── app.js              ← Logic (ranking, map, sliders, i18n)
├── data/
│   └── rivalries.json  ← Definitive dataset (100 entries, 0 nulls)
├── i18n/
│   ├── it.json         ← Italian translations
│   └── en.json         ← English translations
├── slides/
│   └── prompt.md       ← Prompt for generating X.com graphics
├── build_data.py       ← Script to regenerate rivalries.json
└── .github/workflows/
    └── pages.yml       ← GitHub Pages auto-deploy
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🇮🇹 Panoramica (Italiano)

Questo progetto classifica le **100 più grandi rivalità calcistiche** tra club appartenenti alle **prime 50 leghe del ranking Opta**. Il punteggio è calcolato con una formula matematica trasparente e completamente parametrizzabile. Ogni dato è verificato e tracciabile: nessuna stima, nessun valore nullo.

La formula combina 4 fattori: **Longevità** (volume storico), **Prestigio** (trofei), **Intensità** (frattura sociale), **Portata** (capienze stadi), con un bonus del 15% per i derby cittadini. Tutti i pesi sono regolabili liberamente tramite gli slider sul sito.

**[Visita il sito →](https://marcorzzn.github.io/global-club-rivalries-ranking/)**
