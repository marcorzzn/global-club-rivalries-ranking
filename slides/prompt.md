# Prompt per Generare le 4 Slide della Classifica per X.com

## Contesto
Il progetto "Global Club Rivalries Ranking" classifica le 100 più grandi rivalità calcistiche al mondo, selezionate tra le squadre delle **Top 50 leghe del ranking Opta**. Il ranking è calcolato con la formula:

**R = (w_L × L + w_T × T + w_I × I + w_S × S) × D**

### Parametri ottimali scelti per le grafiche:
- **w_L = 0.30** (Longevità: partite storiche e decadi di attività)
- **w_T = 0.25** (Prestigio: somma dei trofei maggiori di entrambi i club)
- **w_I = 0.25** (Intensità: tensione sociale e riconoscimento ufficiale della rivalità)
- **w_S = 0.20** (Portata: somma delle capienze degli stadi)
- **D = 1.15** (Bonus del 15% per i derby cittadini)

---

## Prompt da usare per generare ciascuna slide

### Slide 1 — Top 1-25
Genera un'infografica professionale in formato verticale 1:2 (1080×2160px) su sfondo scuro (charcoal #1a1a2e). In alto il titolo "🏆 GLOBAL CLUB RIVALRIES RANKING" con sottotitolo "Top 50 Opta Leagues | 1-25". Sotto, una lista numerata delle prime 25 rivalità con: posizione, logo del club A (piccolo, circolare), nome club A, "vs", logo club B, nome club B, bandiera emoji del paese, e punteggio R arrotondato. Usa accenti dorati (#d4a017) per i numeri e bordi sottili tra le righe. In basso a sinistra la formula "R = (w_L×L + w_T×T + w_I×I + w_S×S) × D" e i pesi scelti. In basso a destra il link al sito. Stile tipografico pulito (Inter o simile), leggibilità massima su mobile.

### Slide 2 — Top 26-50
Stessa struttura della Slide 1, ma con sottotitolo "26-50" e le rivalità dalla posizione 26 alla 50.

### Slide 3 — Top 51-75
Stessa struttura della Slide 1, ma con sottotitolo "51-75" e le rivalità dalla posizione 51 alla 75.

### Slide 4 — Top 76-100 + Metodologia
Stessa struttura per le posizioni 76-100 nella metà superiore. Nella metà inferiore, un blocco "METODOLOGIA" che spiega: "Rivalità selezionate dalle Top 50 leghe Opta. Punteggio calcolato combinando 4 fattori normalizzati: Longevità (volume storico degli scontri), Prestigio (palmarès combinato), Intensità (frattura sociale e nome riconosciuto), Portata (capienze stadi). Bonus 15% per derby cittadini. Fonti: Wikipedia, Transfermarkt, Wikidata. Pesi personalizzabili sul sito." Link al sito GitHub Pages in basso.

---

## Note tecniche per la generazione
- Ratio: 1:2 (1080×2160px o equivalente)
- Font: Inter, Roboto, o sans-serif professionale
- Palette: sfondo #1a1a2e, accento oro #d4a017, testo bianco #f0f0f0
- I loghi dei club possono essere rappresentati come cerchi colorati con le iniziali se non è possibile usare immagini
- Ogni slide deve essere autocontenuta e leggibile indipendentemente
