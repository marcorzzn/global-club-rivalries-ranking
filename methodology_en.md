# MWI-50 Ultra — Global Club Football Rivalry Index (1976–2026)

**Edition:** Evidence-based (V3 Formula)

---

## 1. Premise & Objective
This document outlines the official methodology used to compile the "MWI-50 Ultra", a ranking of the 100 most intense football club rivalries globally.
The primary objective is to eliminate subjectivity. Any metric that cannot be strictly verified through public and official sources has been excluded to ensure total reproducibility.

## 2. The MWI-50 Ultra V3 Formula
The final score, expressed as an index from 0 to 100, is calculated by combining 8 parameters. The default weights are:

`MWI = 0.18 History + 0.14 Continuity + 0.16 Sporting + 0.14 Stadium + 0.16 Public + 0.10 Media + 0.08 Social + 0.04 Verification`

### 2.1 History (18%)
Total volume of verified official matches played between the clubs.

### 2.2 Continuity (14%)
Evaluates the longevity and consistency of the rivalry, based on `rivalry_age_years` and `active_decade_count`.

### 2.3 Sporting Weight (16%)
Calculated from the average sporting quality of the clubs (`club_strength_avg`) and the strength gap between them.

### 2.4 Stadium Scale (14%)
A measure of the physical scale of the rivalry, based on cumulative and minimum stadium capacities.

### 2.5 Public Attention (16%)
Documented public attention score for the matchup.

### 2.6 Media Coverage (10%)
Global media impact score.

### 2.7 Social Fracture (8%)
The presence of deep-rooted social or territorial divisions and formally documented rivalry names.

### 2.8 Verification Grade (4%)
Every match record is graded based on source redundancy and coherence:
- **A**: 3 or more sources AND at least one Tier A/B source (official club/league site, UEFA/FIFA, ClubElo, Transfermarkt) AND total matches source delta ≤ 5% (or no delta).
- **B**: 2 sources with credible origins and total matches source delta ≤ 10%.
- **C**: Only 1 source, or delta > 10%, or sources are strictly Tier C/D.

## 3. Sources & Strict Rules
* **Zero Fabrication:** No statistical data (matches, attendances, capacities) has been interpolated or estimated.
* **Primary Sources:** Official league databases, club financial and infrastructure reports, UEFA/FIFA, and primary tier databases. Generic aggregators or wikis alone are not sufficient for Tier A/B.

## 4. Ranking Dynamism
The MWI-50 Ultra is designed as a parametric ranking. Using the dedicated HTML application, any user can tweak the weights assigned to the formula's variables to generate an instantly updated, fully transparent ranking.
