---
phase: 04-scenario2-mediateur
plan: "01"
subsystem: notebook
tags: [jupyter, statsmodels, networkx, matplotlib, pandas, causal-inference, mediator-bias]

# Dependency graph
requires:
  - phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
    provides: "log_rev_int DV, compute_outcomes, generate_base_panel, base_df, PARAMS — réutilisés directement"
provides:
  - "Scénario 2 complet : DAG, coefficient plot, bar chart illustrant le biais de surcontrôle sur un médiateur"
  - "figures/sc2_dag.png — DAG 4 noeuds diamond layout"
  - "figures/sc2_coeff.png — coefficient plot 3 estimateurs avec IC 95%"
  - "figures/sc2_bar.png — bar chart 3 barres rouge/bleu/vert"
  - "data/sc2_mediateur.csv — dataset scénario 2"
affects:
  - 05-scenario3-collider
  - 06-scenario4-iv

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Assignation pub aléatoire p=0.5 niveau magasin — contraste avec sc1a/sc1b (assignation confondante)"
    - "OLS avec médiateur (biaisé) vs OLS sans médiateur (correct) — inversion pédagogique vs Phase 3"
    - "DAG 4 noeuds diamond : Pub→Nb visites→Ventes, Pub→Panier moyen→Ventes, pas d'arête directe Pub→Ventes"
    - "Seeds dédiés SEED+40 (données) et SEED+41 (contrefactuel) pour isolation Phase 4"

key-files:
  created:
    - figures/sc2_dag.png
    - figures/sc2_coeff.png
    - figures/sc2_bar.png
    - data/sc2_mediateur.csv
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "OLS sans médiateur est le modèle CORRECT en sc2 (pas le naïf biaisé) — inversion du message Phase 3"
  - "Pas de C(mois) dans les formules OLS car assignation aléatoire — saison n'est pas un confondant"
  - "panier_moyen est un médiateur pur dans le DGP (pas un confondant) — contrôler dessus bloque le chemin causal"
  - "rng_cf_sc2 = SEED+41, rng_sc2 = SEED+40 — seeds isolés pour reproductibilité indépendante"

patterns-established:
  - "DAG 4-noeud diamond layout fixe (Pub left, Ventes right, médiateurs center) — pattern réutilisable pour sc3/sc4"

requirements-completed: [SC2-01, SC2-02, SC2-03]

# Metrics
duration: 5min
completed: 2026-03-04
---

# Phase 4 Plan 01: Scénario 2 — Surcontrôle sur un médiateur Summary

**Scénario médiateur inséré en 5 cellules : OLS sans médiateur 30.8% (correct) vs OLS avec panier_moyen 21.1% (biaisé -9.7pp), biais visible avec assignation parfaitement aléatoire (SEED+40/+41)**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-04T13:58:04Z
- **Completed:** 2026-03-04T14:00:03Z
- **Tasks:** 1/1
- **Files modified:** 5

## Accomplishments

- 5 cellules scénario 2 insérées (1 markdown + 4 code) — notebook passe de 31 à 36 cellules
- Biais de surcontrôle quantifié empiriquement : OLS avec médiateur sous-estime de -9.7pp (-31% relatif)
- 3 PNG (sc2_dag.png, sc2_coeff.png, sc2_bar.png) et 1 CSV (sc2_mediateur.csv) produits
- nbconvert exit 0, 36 cellules, résultats ATT=30.0% / OLS_sans=30.8% / OLS_avec=21.1% confirmés avec SEED=42

## Task Commits

Each task was committed atomically:

1. **Task 1: Insérer les 5 cellules du scénario 2 et exécuter le notebook** - `286193d` (feat)

**Plan metadata:** (voir ci-dessous — commit docs séparé)

## Files Created/Modified

- `formation_causalite.ipynb` — 5 cellules sc2 insérées, notebook exécuté (36 cellules, outputs inclus)
- `figures/sc2_dag.png` — DAG 4 noeuds diamond layout, deux chemins causaux via médiateurs
- `figures/sc2_coeff.png` — coefficient plot 3 estimateurs (rouge OLS sans, bleu OLS avec, vert ATT)
- `figures/sc2_bar.png` — bar chart 3 barres avec ligne pointillée ATT
- `data/sc2_mediateur.csv` — dataset panel 4800 lignes avec assignation aléatoire pub

## Decisions Made

- OLS sans médiateur est le modèle correct ici (inversion vs Phase 3) : nommé `model_naive_sc2` pour signifier "sans contrôle" et non "mauvais"
- Pas de `C(mois)` dans les formules OLS — assignation aléatoire, la saison n'est pas un confondant (simplifie le message pédagogique)
- Seeds isolés SEED+40 pour données, SEED+41 pour contrefactuel — convention +10*phase maintenue

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 4 complète — scénario 2 validé empiriquement (ATT=30.0%, OLS sans méd=30.8%, OLS avec méd=21.1%)
- Phase 5 (Scénario 3 — collider) peut démarrer : `base_df`, `compute_outcomes`, et patterns DAG/OLS/bar réutilisables
- Point d'attention Phase 5 : alpha_collider pour `posts_reseaux` est non trivial (blocker connu en STATE.md)

---
*Phase: 04-scenario2-mediateur*
*Completed: 2026-03-04*
