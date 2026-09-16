# MWI-50 Ultra — Indice Globale delle Rivalità di Club (1976–2026)

**Edizione:** Basata sui dati, prima release pubblica (v1.0)  
**Cutoff Dati:** 15 Settembre 2026, 23:59 UTC  

---

## 1. Premessa e Obiettivo
Questo documento definisce la metodologia ufficiale per la compilazione della classifica "MWI-50 Ultra", un ranking delle 100 rivalità calcistiche tra club più intense al mondo nel periodo compreso tra il 1 Gennaio 1976 e il 15 Settembre 2026.
L'obiettivo primario è eliminare la soggettività. Qualsiasi metrica non verificabile tramite fonti pubbliche ed ufficiali è stata omessa, per garantire la totale riproducibilità.

## 2. Criteri di Ammissione (Eleggibilità)
Per essere considerata nel dataset, una rivalità deve soddisfare almeno uno dei seguenti due criteri:
1. Aver disputato **almeno 25 incontri competitivi ufficiali** (escluse le amichevoli) tra il 1976 e il 2026.
2. Aver disputato **almeno una finale continentale ufficiale** tra il 1976 e il 2026 (es. Finale di UEFA Champions League o Copa Libertadores).

## 3. La Formula del MWI-50 Ultra
Il punteggio finale, espresso in un indice da 0 a 100, è calcolato combinando 5 parametri principali. I pesi di default sono:

`MWI-50U = 0.25 R + 0.25 H + 0.20 I + 0.15 S + 0.15 G`

*(Nota: nella Release 1.0, se il dato G risulta mancante o non calcolabile, il suo peso viene redistribuito proporzionalmente sugli altri quattro addendi per garantire il calcolo a base 100).*

### 3.1 R — Ricorrenza e Continuità (25%)
Misura la costanza e il volume degli scontri.
* **Volume (60% di R):** Il numero totale di partite ufficiali disputate nel cinquantennio, rapportato al 95° percentile del dataset (costante `N_cap`).
* **Continuità (40% di R):** Basato su quanti dei 5 decenni considerati (76-85, 86-95, 96-05, 06-15, 16-26) hanno visto disputare almeno un match ufficiale.

### 3.2 H — Importanza Storica e Competitiva (25%)
Misura la gravità sportiva degli incontri.
* **Stakes Domestiche (40% di H):** Punti assegnati in base alla frequenza documentata di scontri validi per la vittoria di un trofeo o per l'assegnazione del campionato. (Fino a 100 pt per finali multiple di coppa e scontri diretti per il titolo).
* **Rilevanza Continentale (35% di H):** Punteggio basato sull'incontro più avanzato raggiunto dalle due squadre in competizioni continentali (es. 100 pt per una finale continentale, 85 pt per una semifinale).
* **Peso Storico dei Club (25% di H):** Calcolato come percentuale di titoli vinti nel proprio paese nel cinquantennio in esame rispetto al totale dei titoli a disposizione.

### 3.3 I — Intensità della Rivalità (20%)
* **Equilibrio (50% di I):** Calcolato usando l'entropia della distribuzione delle Vittorie, Pareggi e Sconfitte nel periodo in esame. Una rivalità a senso unico abbassa drasticamente l'indice.
* **Identità e Nome (25% di I):** 100 pt per un nome di uso ufficiale stabilito storicamente (es. "Superclásico", "Old Firm"); 50 pt per definizioni informali.
* **Fattore Sociale (25% di I):** Misura l'esistenza documentata (sociologica, giornalistica o di ordine pubblico) di fagliare territoriali, religiose o politiche. (es. 100 pt per divisioni profonde come il caso Old Firm).

### 3.4 S — Stadio e Appello di Massa (15%)
* Se il dato sulle presenze (spettatori reali) ha una storicità verificabile superiore al 30% dei match disputati, S è composto per il **50% dalla Capacità Ufficiale Media (2026)** e per il **50% dalla Mediana degli spettatori reali**.
* In assenza di record completi sugli spettatori storici, S si basa unicamente (100%) sulla media della capacità dei due impianti. 

### 3.5 G — Risonanza Globale (15%)
Misura dell'impatto mediatico contemporaneo, misurato (nella finestra dal 2004 al 2026) tramite un protocollo standardizzato di estrazione da Google Trends su 12 mercati target, combinato con i dati di distribuzione dei territori televisivi per la stagione 25/26.

## 4. Fonti e Regole Ferree
* **Zero Allucinazioni:** Nessun dato statistico (partite giocate, spettatori, capacità) è stato inventato. Nel caso di controversie storiche (es. match invalidati e rigiocati), le decisioni seguono la contabilità delle federazioni ufficiali (es. UEFA, CONMEBOL, Federazioni Locali).
* **Fonti Primarie:** Database ufficiali, referti delle Leghe di riferimento, bilanci e note sulle infrastrutture dei club, e l'archivio *RSSSF* come fonte storica di secondo livello.

## 5. Dinamicità del Ranking
Il MWI-50 Ultra è studiato come ranking parametrico. Tramite l'applicazione HTML dedicata, l'utente può modificare l'importanza (peso) data ad ogni singola voce della formula (ad esempio riducendo l'importanza del parametro storicità per prediligere l'equilibrio tecnico e le dimensioni dello stadio) ed ottenere la classifica aggiornata in tempo reale.
