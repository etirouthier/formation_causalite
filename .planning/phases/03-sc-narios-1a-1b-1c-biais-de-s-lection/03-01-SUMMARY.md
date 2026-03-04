---
phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
plan: "01"
subsystem: notebook
tags: [jupyter, pandas, statsmodels, numpy, networkx, causalite, biais-selection, log-dv]

# Dependency graph
requires:
  - phase: 02-scenario0-petits-nombres
    provides: base_df panel, compute_outcomes(), PARAMS, SEED, smf/nx imports
provides:
  - "Scénario 1a refactorisé: log_rev_int DV, ATT log, OLS naïf/ajusté en %, figures coeff+bar"
  - "Scénario 1b refactorisé: log_rev_int DV, ATT log, OLS naïf/ajusté en %, figures coeff+bar"
  - "EFFET_SAISON recalibré: max 0.08 (cycles ±0.04/0.08)"
  - "data/sc1a_selection_qualite.csv avec colonne log_rev_int"
  - "data/sc1b_selection_urbain.csv avec colonne log_rev_int"
  - "figures/sc1a_dag.png, sc1a_coeff.png, sc1a_bar.png"
  - "figures/sc1b_dag.png, sc1b_coeff.png, sc1b_bar.png"
affects: [03-02-sc1c, phase-4, phase-5, phase-6]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "DV log-intensif: log_rev_int = log(ventes/n_potentiel) supprime l'effet de taille magasin"
    - "ATT log: att_log = mean(log(Y1_treated) - log(Y0_cf)) — interprétation en log-points ≈ %"
    - "Print en %: coef*100 pour lisibilité pédagogique"
    - "att_Xlog variable nommée explicitement pour distinguer de l'att en €"

key-files:
  created: []
  modified:
    - formation_causalite.ipynb
    - data/sc1a_selection_qualite.csv
    - data/sc1b_selection_urbain.csv
    - figures/sc1a_coeff.png
    - figures/sc1a_bar.png
    - figures/sc1b_coeff.png
    - figures/sc1b_bar.png

key-decisions:
  - "DV = log(ventes/n_potentiel): mesure intensive, supprime l'effet taille, interprétation en % uplift"
  - "EFFET_SAISON max 0.08 (vs 0.02 avant): assure surestimation visible pour sc1c (biais +8.6pp)"
  - "att_1a_log / att_1b_log / att_1c_log: nommage explicite distingue log-points des € de l'ancienne version"
  - "Cellules sc1c (27-30) modifiées en même temps que 1a/1b pour cohérence DV dans tout le notebook"

patterns-established:
  - "Refactoring DV: ajouter colonne log_rev_int après compute_outcomes(), avant OLS"
  - "Contrefactuel log: recalculer log sur df_cf après compute_outcomes()"

requirements-completed: [SC1-01, SC1-02]

# Metrics
duration: 15min
completed: 2026-03-04
---

# Phase 3 Plan 01: Scénarios 1a et 1b — Refactoring DV log_rev_int Summary

**Refactoring DV ventes→log(ventes/n_potentiel) pour scénarios 1a/1b/1c: surestimation OLS naïf pédagogiquement visible en % (+70%, +55%, +8.6pp)**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-04T13:00:00Z
- **Completed:** 2026-03-04T13:15:00Z
- **Tasks:** 1 (refactoring atomique)
- **Files modified:** 9

## Accomplishments
- EFFET_SAISON recalibré de max 0.02 vers 0.08, permettant un biais saisonnier visible pour sc1c
- 10 cellules notebook modifiées (sc1a: 4, sc1b: 4, sc1c: 2 data+coeff+bar) pour utiliser log_rev_int
- OLS naïf surestime ATT dans les 3 scénarios: 1a (+70%), 1b (+55%), 1c (+8.6pp)
- CSV et figures régénérés avec le nouveau DV

## Task Commits

1. **Refactoring DV + EFFET_SAISON + nbconvert** - `afee35f` (refactor)

## Files Created/Modified
- `formation_causalite.ipynb` - 10 cellules modifiées: PARAMS + sc1a-data/coeff/bar + sc1b-data/coeff/bar + sc1c-data/coeff/bar
- `data/sc1a_selection_qualite.csv` - Régénéré avec colonne log_rev_int
- `data/sc1b_selection_urbain.csv` - Régénéré avec colonne log_rev_int
- `data/sc1c_selection_saison.csv` - Régénéré avec colonne log_rev_int
- `figures/sc1a_coeff.png` - Axe xlabel "Uplift log des ventes (≈ %)"
- `figures/sc1a_bar.png` - Axe ylabel "Uplift log des ventes (≈ %)"
- `figures/sc1b_coeff.png` - Axe xlabel "Uplift log des ventes (≈ %)"
- `figures/sc1b_bar.png` - Axe ylabel "Uplift log des ventes (≈ %)"
- `figures/sc1c_coeff.png` - Axe xlabel "Uplift log des ventes (≈ %)"
- `figures/sc1c_bar.png` - Axe ylabel "Uplift log des ventes (≈ %)"

## Decisions Made
- DV = log(ventes/n_potentiel) choisi car mesure intensive (supprime l'effet de taille), interprétation directe en log-points ≈ % uplift, pédagogiquement plus clair
- EFFET_SAISON max 0.08 (dict recalibré ±0.04/0.08) pour créer un biais saisonnier visible sans dépasser max_p < 0.99 (max_p = 0.83 après recalibration)
- sc1c modifié en même temps que 1a/1b pour cohérence totale du DV dans le notebook (évite variable att_1c en € et att_1c_log en % coexistant)

## Résultats empiriques (SEED=42)

| Scénario | ATT_log | OLS naïf | OLS ajusté | Biais |
|----------|---------|----------|------------|-------|
| 1a (qualite_equipe) | 28.4% | 48.5% | 28.3% | +70.8% surestimation |
| 1b (urbain) | 28.3% | 43.9% | 32.0% | +55.1% surestimation |
| 1c (saison, es_max=0.08) | 29.4% | 38.0% | 30.7% | +8.6pp surestimation |

## Deviations from Plan

### Scope extension (Rule 2 — completeness)

**1. [Rule 2 - Completeness] Cellules sc1c modifiées en même temps**
- **Found during:** Task 1 (modification notebook)
- **Issue:** Le plan 03-01 ne couvre que 1a et 1b, mais les cellules 1c étaient déjà en place (commit c5982cb) avec l'ancien DV `ventes`. Les laisser avec `ventes ~` aurait créé une incohérence de DV dans le notebook.
- **Fix:** Modification simultanée de cells 27/29/30 (sc1c) pour utiliser log_rev_int et att_1c_log
- **Files modified:** formation_causalite.ipynb (cells 27, 29, 30)
- **Committed in:** afee35f (même commit de refactoring)

---

**Total deviations:** 1 auto-étendu (completeness)
**Impact on plan:** Extension de scope minimale nécessaire pour cohérence DV dans tout le notebook.

## Issues Encountered
- Les SUMMARY.md précédents (03-01 et 03-02) avaient été supprimés lors du pause-work — recréés dans cette exécution.

## Self-Check

### Commits
- `afee35f` (refactor(03-01): DV ventes→log_rev_int pour scénarios 1a, 1b et 1c) — FOUND ✓

### Files
- `formation_causalite.ipynb` — FOUND ✓
- `data/sc1a_selection_qualite.csv` — FOUND ✓
- `data/sc1b_selection_urbain.csv` — FOUND ✓
- `figures/sc1a_coeff.png` — FOUND ✓
- `figures/sc1b_coeff.png` — FOUND ✓

## Self-Check: PASSED

## Next Phase Readiness
- Plan 03-01 complet: 8 cellules 1a+1b refactorisées + EFFET_SAISON calibré
- Plan 03-02 à reprendre: cellules sc1c déjà refactorisées dans ce run, besoin de vérification humaine des figures 1c (checkpoint pending)
- Blockers: aucun — biais pédagogique validé empiriquement

---
*Phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection*
*Completed: 2026-03-04*
