# MWI-50 Ultra — Indice Globale Rivalità Calcistiche (1976–2026)

**Edizione:** Basata sui dati (Formula V3)

---

## 1. Premessa e Obiettivo
Questo documento delinea la metodologia ufficiale utilizzata per compilare l'"MWI-50 Ultra", una classifica delle 100 rivalità calcistiche di club più intense a livello globale.
L'obiettivo primario è eliminare la soggettività. Ogni metrica che non può essere rigorosamente verificata tramite fonti pubbliche e ufficiali è stata esclusa per garantire la totale riproducibilità.

## 2. La Formula MWI-50 Ultra V3
Il punteggio finale, espresso come indice da 0 a 100, è calcolato combinando 8 parametri. I pesi predefiniti sono:

`MWI = 0.18 History + 0.14 Continuity + 0.16 Sporting + 0.14 Stadium + 0.16 Public + 0.10 Media + 0.08 Social + 0.04 Verification`

### 2.1 History (18%)
Volume totale degli incontri ufficiali verificati giocati tra i club.

### 2.2 Continuity (14%)
Valuta la longevità e la costanza della rivalità, in base a `rivalry_age_years` e `active_decade_count`.

### 2.3 Sporting Weight (16%)
Calcolato in base alla qualità sportiva media dei club (`club_strength_avg`) e al divario di forza tra i due.

### 2.4 Stadium Scale (14%)
Una misura della dimensione fisica della rivalità, basata sulle capienze cumulative e minime degli stadi.

### 2.5 Public Attention (16%)
Punteggio documentato dell'attenzione pubblica per lo scontro.

### 2.6 Media Coverage (10%)
Punteggio di impatto mediatico globale.

### 2.7 Social Fracture (8%)
La presenza di divisioni sociali o territoriali radicate e nomi di rivalità formalmente documentati.

### 2.8 Verification Grade (4%)
Ogni record viene valutato in base alla ridondanza e alla coerenza delle fonti:
- **A**: 3 o più fonti E almeno una fonte di Tier A/B (sito ufficiale club/lega, UEFA/FIFA, ClubElo, Transfermarkt) E delta fonti match totali ≤ 5% (o nessun delta).
- **B**: 2 fonti con origini credibili e delta fonti match totali ≤ 10%.
- **C**: Solo 1 fonte, o delta > 10%, o fonti strettamente di Tier C/D.

## 3. Fonti e Regole Ferree
* **Zero Fabbricazioni:** Nessun dato statistico (partite, presenze, capienze) è stato interpolato o stimato.
* **Fonti Primarie:** Database ufficiali delle leghe, report finanziari e infrastrutturali dei club, UEFA/FIFA e database primari di primo livello. Aggregatori generici o wiki da soli non sono sufficienti per il Tier A/B.

## 4. Dinamismo della Classifica
L'MWI-50 Ultra è progettato come una classifica parametrica. Tramite l'applicazione HTML dedicata, l'utente può modificare i pesi assegnati alle variabili della formula per generare una classifica aggiornata istantaneamente e completamente trasparente.
