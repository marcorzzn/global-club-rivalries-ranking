# Football Rivalry Index - Piano d'Azione

## Stato Attuale del Progetto
- **Dataset**: 100 record in `data/rivalries_v3_all.json`
- **Problemi identificati**:
  - 95 record con `first_official_meeting_year` = null
  - 26 record con ID numerici (es. "071") invece di slug (es. "caf-001")
  - Frontend non gestisce i null correttamente (tratta come 0)
  - Funzione morta `calculateEntropy` presente nel codice
  - API ClubElo restituisce 502 permanente, GDELT richiede backoff

## Task da Completare

### TASK 1: API (GDELT & ClubElo)
**Obiettivo**: Aggiornare i punteggi `media_coverage_score` usando GDELT con exponential backoff.
**Nota**: ClubElo restituisce 502 permanente → accettare come null.

**Implementazione**:
- Script Python che chiama GDELT API con backoff esponenziale
- Aggiorna solo `media_coverage_score` dove possibile
- Gestisce rate limiting correttamente

### TASK 2: Frontend - Renormalizzazione e Trasparenza
**Modifiche a `index.html`**:

1. **Rimuovere `calculateEntropy`** (linee ~614-631)
2. **Renormalizzazione MWI**: 
   - Se un parametro è null, escludere il suo peso
   - Rinormalizzare i pesi rimanenti per sommare 100%
   - Il record non viene penalizzato per dati mancanti
3. **Trasparenza UI**: Mostrare "Dato mancante" invece di 0 silenzioso
4. **Badge di Completezza**: 
   - Calcolare % campi non-null per record
   - Mostrare badge verde/rosso (>50% o <50%)

### TASK 3: Standardizzazione ID
**Script Python**: 
- Identificare tutti gli ID puramente numerici
- Convertire in formato slug basato sulla confederazione:
  - CAF → "caf-XXX"
  - CONMEBOL → "con-XXX" 
  - CONCACAF → "nac-XXX"
  - AFC → "afc-XXX"
  - OFC → "ofc-XXX"
  - UEFA → mantenere slug esistenti o creare appropriati
- Aggiornare eventuali riferimenti incrociati
- Salvare JSON aggiornato

### TASK 4: Popolare first_official_meeting_year (95 record)
**Script `search_years.py`**:

**Regole rigorose**:
- Solo incontri competitivi/ufficiali (League, Cup)
- ESCLUDERE: amichevoli, esibizioni, coppe non ufficiali
- Attenzione a predecessori senza lignaggio esplicito
- Non confondere anno fondazione con anno primo match

**Sistema a Flag**:
- Estrai candidato da tabella/infobox
- Cerca nel testo "prose" anni precedenti
- Se trovato anno precedente: `[FLAG: EARLIER PROSE MENTION FOUND: XXXX]`

**Workflow Batch**:
- Processa 20 record per volta (batch 1: record 11-30)
- Output: `candidates_report_batch.txt`
- Formato report:
  ```
  Matchup: Club A vs Club B
  Candidato Anno: YYYY [eventuale FLAG]
  Source URL: https://...
  Snippet: "testo esatto..."
  ```
- **STOP** dopo ogni batch per approvazione umana

---

## Ordine di Esecuzione
1. ✅ Esplorazione completata
2. **TASK 3**: Standardizzazione ID (più veloce, propedeutico)
3. **TASK 2**: Modifiche frontend
4. **TASK 1**: Script GDELT (opzionale, dato che ClubElo è down)
5. **TASK 4**: search_years.py - Batch 1 (record 11-30)

---

## Note Tecniche
- Ambiente: Python disponibile
- JSON: 100 record totali, solo 5 hanno già first_official_meeting_year
- Confederaazioni presenti: UEFA, CAF, CONMEBOL, CONCACAF, AFC, OFC
