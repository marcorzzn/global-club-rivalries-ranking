# MWI-50 Ultra — Global Club Football Rivalry Index (1976–2026)

**Edition:** Evidence-based, first public release (v1.0)  
**Data Cutoff:** 15 September 2026, 23:59 UTC  

---

## 1. Premise & Objective
This document outlines the official methodology used to compile the "MWI-50 Ultra", a ranking of the 100 most intense football club rivalries globally over the 50-year period spanning from January 1, 1976, to September 15, 2026.
The primary objective is to eliminate subjectivity. Any metric that cannot be strictly verified through public and official sources has been excluded to ensure total reproducibility.

## 2. Eligibility Criteria
To be included in the candidate universe, a pairing of clubs must meet at least one of the following criteria:
1. Having played **at least 25 official competitive matches** (friendlies strictly excluded) against each other within the 1976–2026 window.
2. Having contested **at least one official continental final** against each other within the 1976–2026 window (e.g., UEFA Champions League or Copa Libertadores Final).

## 3. The MWI-50 Ultra Formula
The final score, expressed as an index from 0 to 100, is calculated by combining 5 main dimensions. The default weights are:

`MWI-50U = 0.25 R + 0.25 H + 0.20 I + 0.15 S + 0.15 G`

*(Note: In Release 1.0, if the G dimension is missing or unavailable, its weight is distributed proportionally across the other four dimensions to ensure the score remains base-100).*

### 3.1 R — Recurrence & Longevity (25%)
Measures the frequency and consistency of the matchups.
* **Volume (60% of R):** The total number of official competitive matches played in the 50-year period, capped dynamically against the 95th percentile of the dataset (the constant `N_cap`).
* **Continuity (40% of R):** Evaluated based on how many of the 5 decades (76-85, 86-95, 96-05, 06-15, 16-26) featured at least one official matchup.

### 3.2 H — Competitive & Historical Importance (25%)
Measures the sporting gravity of the fixtures.
* **Domestic Stakes (40% of H):** Points awarded based on documented frequency of title-race meetings or cup finals. (Up to 100 pts for multiple cup finals paired with repeated title deciders).
* **Continental Significance (35% of H):** Scored based on the deepest round the two teams met in a continental competition (e.g., 100 pts for a continental final, 85 pts for a semi-final).
* **Club Historical Weight (25% of H):** Calculated as the combined percentage of major domestic league titles won by the two clubs relative to the total available titles in their country during the 1976-2026 period.

### 3.3 I — Rivalry Intensity (20%)
* **Sporting Balance (50% of I):** Computed using an entropy index over the Win/Draw/Loss distribution in the timeframe. A heavily one-sided rivalry mathematically lowers the index.
* **Identity & Name (25% of I):** 100 pts for an officially recognized and historically established name (e.g., "Superclásico", "Old Firm"); 50 pts for recurring informal designations.
* **Social Intensity (25% of I):** Evaluates the documented existence (academic, journalistic, public order) of socio-economic, political, or territorial divisions. (e.g., 100 pts for multi-dimensional deep-rooted conflicts).

### 3.4 S — Stadium & Mass Appeal (15%)
* If verified real-attendance data covers at least 30% of the matches, S is calculated using **50% Official Average Stadium Capacity (2026)** and **50% Median Verified Attendance**.
* If historical attendance logs are heavily fragmented, S relies entirely (100%) on the average official stadium capacities.

### 3.5 G — Global Resonance (15%)
A measure of contemporary media impact, calculated (for the 2004–2026 window) using a standardized Google Trends data extraction across 12 target global markets, combined with broadcasting footprint data for the 2025/26 season.

## 4. Sources & Strict Rules
* **Zero Fabrication:** No statistical data (matches, attendances, capacities) has been interpolated or estimated. When facing historical discrepancies, official federation logs (e.g., UEFA, CONMEBOL, domestic FAs) served as the ultimate tiebreakers.
* **Primary Sources:** Official league databases, club financial and infrastructure reports, and the *RSSSF* archive acting as a robust secondary verifier.

## 5. Ranking Dynamism
The MWI-50 Ultra is designed as a parametric ranking. Using the dedicated HTML application, any user can tweak the weights assigned to the formula's variables (e.g., lowering historical weight in favor of sporting balance and stadium sizes) to generate an instantly updated, fully transparent ranking.
