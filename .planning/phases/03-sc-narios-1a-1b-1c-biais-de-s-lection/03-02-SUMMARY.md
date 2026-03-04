---
phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
plan: "02"
subsystem: notebook
tags: [jupyter, pandas, numpy, statsmodels, networkx, matplotlib, causalite, biais-selection]

# Dependency graph
requires:
  - phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
    provides: "Scénarios 1a et 1b insérés (10 cellules), 6 PNG + 2 CSV, base_df + compute_outcomes"

provides:
  - "5 cellules scénario 1c (1 markdown + 4 code) dans formation_causalite.ipynb"
  - "figures/sc1c_dag.png — DAG 3 noeuds (Pub, Ventes, Saison)"
  - "figures/sc1c_coeff.png — coefficient plot OLS naïf vs ajusté vs ATT"
  - "figures/sc1c_bar.png — bar chart comparaison estimateurs 1c"
  - "data/sc1c_selection_saison.csv — panel 4800 lignes avec pub niveau ligne"
  - "Notebook 31 cellules exécuté (nbconvert exit 0)"

affects: [04-scenario2-mediateur, 05-scenario3-collider]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Assignation pub niveau ligne (binomial sur 4800 lignes sans drop_duplicates) — différent de 1a/1b"
    - "OLS naïf 1c : ventes ~ pub SANS C(mois) pour rendre biais saisonnier visible"
    - "Seeds dédiés SEED+30 (assignation) et SEED+31 (contrefactuel) pour isoler reproductibilité"

key-files:
  created:
    - figures/sc1c_dag.png
    - figures/sc1c_coeff.png
    - figures/sc1c_bar.png
    - data/sc1c_selection_saison.csv
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "OLS naïf 1c formule = 'ventes ~ pub' (sans C(mois)) — exception structurelle de 1c vs 1a/1b où le naïf inclut C(mois)"
  - "Assignation pub au niveau ligne (pas magasin) : binomial(1, probs_1c) sur 4800 lignes directement"
  - "ATT contrefactuel 1c calculé sur les lignes pub=1 (pas magasin_id) — cohérent avec niveau d'assignation"
  - "Biais directionnel 1c : ATT=1253.8€ > OLS naïf=1188.2€ (sous-estimation comme 1a/1b) — formateur doit valider si acceptable pédagogiquement"

patterns-established:
  - "Scénario 1c : niveau ligne — pas de drop_duplicates avant assignation pub"
  - "rng_cf_1c indépendant du rng_sc1c pour isolation des outcomes contrefactuels"

requirements-completed: [SC1-03]

# Metrics
duration: 15min
completed: 2026-03-04
---

# Phase 3 Plan 02: Scénario 1c (sélection par saison) Summary

**5 cellules scénario 1c insérées dans le notebook (31 cellules, nbconvert exit 0) — assignation pub niveau ligne, OLS naïf sans C(mois), 3 PNG + 1 CSV exportés**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-03-04T09:00:00Z
- **Completed:** 2026-03-04T09:15:00Z
- **Tasks:** 1 of 2 (stopped at checkpoint:human-verify)
- **Files modified:** 5 (notebook + 3 PNG + 1 CSV)

## Accomplishments
- 5 nouvelles cellules scénario 1c insérées à la fin du notebook (cellules 26-30)
- Assignation pub au niveau ligne (4800 lignes) avec probabilité conditionnelle haute/basse saison
- OLS naïf 1c = `ventes ~ pub` (sans C(mois)) — permet de rendre le biais saisonnier visible pédagogiquement
- OLS ajusté 1c = `ventes ~ pub + C(mois)` — contrôle la saison via dummies mensuels
- Notebook complet exécuté sans erreur (nbconvert exit 0, 31 cellules)
- Résultats : ATT=1253.8€, OLS naïf=1188.2€, OLS ajusté=1097.2€

## Task Commits

Chaque tâche commitée atomiquement :

1. **Task 1: Insérer les 5 cellules scénario 1c + nbconvert** - `c5982cb` (feat)

**Plan metadata:** A créer après checkpoint humain

## Files Created/Modified
- `formation_causalite.ipynb` - 5 nouvelles cellules sc1c ajoutées, notebook ré-exécuté (31 cellules)
- `figures/sc1c_dag.png` - DAG 3 noeuds : Saison → Pub, Saison → Ventes, Pub → Ventes
- `figures/sc1c_coeff.png` - Coefficient plot : OLS naïf (sans mois) vs OLS ajusté + C(mois) vs ATT
- `figures/sc1c_bar.png` - Bar chart comparaison des 3 estimateurs
- `data/sc1c_selection_saison.csv` - Panel 4800 lignes avec colonnes pub, ventes, etc.

## Decisions Made
- OLS naïf 1c formule = `'ventes ~ pub'` sans C(mois) — exception structurelle intentionnelle, différente de 1a/1b où le naïf inclut C(mois). Le biais saisonnier est visible via la différence entre naïf et ajusté.
- Assignation pub au niveau ligne (binomial sur toutes les 4800 lignes) sans `drop_duplicates` — architectural différent de 1a/1b qui opèrent au niveau magasin.
- Seeds dédiés SEED+30 et SEED+31 pour isoler reproductibilité de l'assignation et du contrefactuel.

## Deviations from Plan

None - plan exécuté exactement comme spécifié.

## Issues Encountered

**Observation sur la direction du biais 1c :** ATT=1253.8€ > OLS naïf=1188.2€ (sous-estimation, pas surestimation). Ce comportement est cohérent avec le même phénomène observé pour 1a et 1b (documenté dans STATE.md blockers). La haute saison augmente simultanément la probabilité de pub ET les ventes, mais le modèle sans C(mois) capte une partie de cet effet via la corrélation pub-saison. Le formateur doit valider si cette direction est acceptable pédagogiquement dans le checkpoint humain.

## Next Phase Readiness
- Checkpoint humain requis : formateur doit valider visuellement les 9 figures (3 DAGs, 3 coeff plots, 3 bar charts)
- Si approuvé : phase 3 complete, prêt pour phase 4 (scénario 2 — médiateur)
- Si problème de direction du biais : recalibration des paramètres EFFET_SAISON ou P_PUB_HAUTE_SAISON/P_PUB_BASSE_SAISON requise

---
*Phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection*
*Completed: 2026-03-04*

## Self-Check: PASSED

All files and commits verified:
- FOUND: figures/sc1c_dag.png
- FOUND: figures/sc1c_coeff.png
- FOUND: figures/sc1c_bar.png
- FOUND: data/sc1c_selection_saison.csv
- FOUND: formation_causalite.ipynb
- FOUND: .planning/phases/03-sc-narios-1a-1b-1c-biais-de-s-lection/03-02-SUMMARY.md
- COMMIT c5982cb: feat(03-02): insérer 5 cellules scénario 1c et exécuter notebook
