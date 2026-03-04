---
phase: 05-scenario3-collider
plan: "01"
subsystem: notebook
tags: [jupyter, causal-inference, collider-bias, networkx, statsmodels, ols, dgp]

# Dependency graph
requires:
  - phase: 04-scenario2-mediateur
    provides: "Notebook avec 36 cellules, patterns DAG/OLS/ATT/figures, base_df, compute_outcomes, PARAMS dict"
provides:
  - "Scénario 3 collider — 5 cellules insérées (cells 36-40), notebook 41 cellules"
  - "figures/sc3_dag.png — DAG V-structure collider (Pub → Posts réseaux ← Ventes)"
  - "figures/sc3_coeff.png — coefficient plot 3 estimateurs"
  - "figures/sc3_bar.png — bar chart 3 estimateurs"
  - "data/sc3_collider.csv — dataset sc3 avec colonne posts_reseaux"
  - "COLLIDER_PUB_VENTES_COEFF = 5e-5 dans cellule Paramètres et PARAMS dict"
affects: [06-conclusion, formations-pedagogiques]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Collider DGP via terme d'interaction pub × ventes_agg (calculé APRÈS compute_outcomes)"
    - "Seed convention SEED+50 (données) / SEED+51 (contrefactuel) pour Phase 5"
    - "node_colors_sc3 dérivé dynamiquement via color_map_sc3 dict (pas liste littérale)"

key-files:
  created:
    - figures/sc3_dag.png
    - figures/sc3_coeff.png
    - figures/sc3_bar.png
    - data/sc3_collider.csv
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "OLS naïf (sans collider) est le modèle CORRECT en sc3 — même logique qu'en sc2 (assignation aléatoire)"
  - "Couleur collider = crimson (rouge) pour distinction visuelle forte vs médiateur (bleu sc2)"
  - "DAG inclut l'arête Pub → Ventes pour montrer la structure causale complète (pas seulement le V-structure)"
  - "Biais direction vers le bas : naive (33.6%) > avec-collider (30.5%) — déterminé empiriquement avec SEED=42, alpha=5e-5"
  - "Proximité ATT (30.2%) ≈ avec-collider (30.5%) est fortuite, commentée dans le code bar chart"

patterns-established:
  - "Pattern 6: Collider DGP — calculer ventes_agg depuis df_sc3 APRÈS compute_outcomes, puis merge stores_collider dans df_sc3 avant export CSV"

requirements-completed: [SC3-01, SC3-02, SC3-03]

# Metrics
duration: 5min
completed: 2026-03-04
---

# Phase 5 Plan 01: Scénario 3 Collider Summary

**Collider bias illustration — posts_reseaux (pub x ventes_agg) reduces naive OLS 33.6% to 30.5% (-3.1pp, 9.4% relative) while ATT true = 30.2% (SEED=42, COLLIDER_PUB_VENTES_COEFF=5e-5)**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-04T14:00:00Z
- **Completed:** 2026-03-04T14:05:00Z
- **Tasks:** 1/1
- **Files modified:** 5

## Accomplishments
- COLLIDER_PUB_VENTES_COEFF = 5e-5 ajouté dans la cellule Paramètres (cell 1) ET dans le dict PARAMS
- 5 cellules scénario 3 insérées (cells 36-40) — notebook passe de 36 à 41 cellules, nbconvert exit 0
- Collider DGP posts_reseaux calculé après compute_outcomes depuis df_sc3 avec seeds isolés (SEED+50/SEED+51)
- OLS naïf 33.6% > OLS avec posts_reseaux 30.5% — biais relatif 9.4% > seuil 5% pédagogique
- 3 PNG (sc3_dag crimson V-structure, sc3_coeff, sc3_bar) + CSV sc3_collider.csv avec colonne posts_reseaux

## Task Commits

Each task was committed atomically:

1. **Task 1: Modifier la cellule Paramètres et insérer les 5 cellules du scénario 3** - `0314b8c` (feat)

**Plan metadata:** (à venir — commit docs)

## Files Created/Modified
- `formation_causalite.ipynb` - PARAMS cell modifiée (COLLIDER_PUB_VENTES_COEFF), 5 cellules sc3 insérées (36-40), notebook exécuté
- `figures/sc3_dag.png` - DAG V-structure collider (Pub steelblue, Ventes seagreen, Posts réseaux crimson)
- `figures/sc3_coeff.png` - Coefficient plot 3 estimateurs : naïf rouge, avec-collider orange, ATT vert
- `figures/sc3_bar.png` - Bar chart 3 barres avec ligne pointillée ATT
- `data/sc3_collider.csv` - Dataset row-level sc3 avec colonne posts_reseaux (200 magasins × 24 mois)

## Decisions Made
- OLS naïf (sans collider) est le modèle CORRECT en sc3 — même inversion pédagogique qu'en Phase 4 (naïf = correct car assignation aléatoire)
- Couleur collider = crimson pour distinction visuelle forte (médiateur Phase 4 = bleu)
- DAG inclut Pub → Ventes en plus de la V-structure pour montrer la structure causale complète
- Biais direction downward (naive > avec-collider) déterminé empiriquement et documenté dans RESEARCH.md
- Proximité fortuite ATT (30.2%) ≈ avec-collider (30.5%) commentée explicitement dans le code

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None — empirical values correspondent exactement aux prévisions du RESEARCH.md (ATT 30.2%, naïf 33.6%, avec-collider 30.5%, traités 113/200).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 5 complete — scénario 3 collider entièrement validé
- Notebook à 41 cellules, nbconvert exit 0
- Les 4 scénarios pédagogiques sont maintenant implémentés (sc0, sc1a/b/c, sc2, sc3)
- Phase 6 (conclusion/synthèse) peut démarrer

## Self-Check: PASSED

All files verified:
- formation_causalite.ipynb: FOUND
- figures/sc3_dag.png: FOUND
- figures/sc3_coeff.png: FOUND
- figures/sc3_bar.png: FOUND
- data/sc3_collider.csv: FOUND
- 05-01-SUMMARY.md: FOUND
- Commit 0314b8c: FOUND

---
*Phase: 05-scenario3-collider*
*Completed: 2026-03-04*
