---
phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
plan: "01"
subsystem: notebook
tags: [jupyter, statsmodels, networkx, matplotlib, pandas, numpy, causalite, dag, ols, att, selection-bias]

# Dependency graph
requires:
  - phase: 02-scenario0-petits-nombres
    provides: base_df (4800 lignes), compute_outcomes(), generate_base_panel(), smf importé, nx importé, patterns DAG et export

provides:
  - Scénario 1a : DAG confondant qualite_equipe, OLS naïf/ajusté/ATT, 3 PNG, 1 CSV (sc1a_selection_qualite.csv)
  - Scénario 1b : DAG confondant urbain, OLS naïf/ajusté/ATT, 3 PNG, 1 CSV (sc1b_selection_urbain.csv)
  - 8 cellules de code dans le notebook (2 markdown + 6 code : data×2, dag×2, coeff×2, bar×2)
  - Pattern ATT contrefactuel (rng dédié pour le CF, séparé du rng d'assignation)

affects:
  - 03-02 (scénario 1c — saison)
  - ROADMAP phases 4-6

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "rng local dédié par scénario (rng_sc1a = np.random.default_rng(SEED + 10)) pour isoler l'état aléatoire"
    - "ATT contrefactuel via rng_cf distinct (SEED + 11) — garantit la reproductibilité indépendamment du nombre de traités"
    - "OLS avec conf_int().loc['pub', 0] et .loc['pub', 1] — colonnes integers statsmodels 0.14.6"
    - "xerr errorbar = [[coef-lower], [upper-coef]] — distances positives, pas bornes absolues"
    - "colors_est redéfini dans code-sc1b-coeff pour robustesse (disponible même sans code-sc1a-bar)"

key-files:
  created:
    - figures/sc1a_dag.png
    - figures/sc1a_coeff.png
    - figures/sc1a_bar.png
    - figures/sc1b_dag.png
    - figures/sc1b_coeff.png
    - figures/sc1b_bar.png
    - data/sc1a_selection_qualite.csv
    - data/sc1b_selection_urbain.csv
  modified:
    - formation_causalite.ipynb (10 nouvelles cellules, index 16-25)

key-decisions:
  - "colors_est redéfini dans code-sc1b-coeff (pas de dépendance sur code-sc1a-bar) — robustesse à la réexécution partielle"
  - "ATT calculé uniquement sur les magasins traités (treated_ids) avec rng_cf dédié — isolé de rng_sc"
  - "drop_duplicates('magasin_id') obligatoire avant assignation pub niveau magasin — évite 24 tirages par magasin"

patterns-established:
  - "Pattern ATT scénarios 1a/1b : df_treated = df[df['magasin_id'].isin(treated_ids)].copy() + rng_cf distinct"
  - "Pattern OLS double : model_naive = smf.ols('ventes ~ pub + C(mois)') + model_adj = smf.ols avec confondant"

requirements-completed: [SC1-01, SC1-02]

# Metrics
duration: 15min
completed: 2026-03-04
---

# Phase 3 Plan 01: Scénarios 1a et 1b Summary

**DAG + OLS naïf/ajusté/ATT pour biais de sélection qualite_equipe (1a) et urbain (1b) — 8 PNG et 2 CSV générés via nbconvert en 15 min**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-04T08:23:00Z
- **Completed:** 2026-03-04T08:38:00Z
- **Tasks:** 2
- **Files modified:** 1 notebook + 8 fichiers générés

## Accomplishments

- 10 cellules insérées dans formation_causalite.ipynb (index 16-25) : 2 markdown de section + 2 cellules data/ATT/OLS + 2 cellules DAG + 2 cellules coeff plot + 2 cellules bar chart
- 6 PNG exportés : sc1a_dag.png, sc1a_coeff.png, sc1a_bar.png, sc1b_dag.png, sc1b_coeff.png, sc1b_bar.png
- 2 CSV exportés : data/sc1a_selection_qualite.csv (4800 lignes), data/sc1b_selection_urbain.csv (4800 lignes)
- rng isolés : SEED+10/+11 pour 1a, SEED+20/+21 pour 1b — rng global non pollué

## Task Commits

1. **Task 1: Insérer cellules données et DAG pour scénarios 1a et 1b** - `eb5df4d` (feat)
2. **Task 2: Insérer coefficient plots et bar charts pour scénarios 1a et 1b** - `541f6ba` (feat)

## Files Created/Modified

- `formation_causalite.ipynb` - 10 nouvelles cellules (index 16-25), notebook passe de 16 à 26 cellules
- `figures/sc1a_dag.png` - DAG NetworkX 3 noeuds (Qualité équipe, Pub, Ventes)
- `figures/sc1a_coeff.png` - Errorbar plot 3 estimateurs pour 1a
- `figures/sc1a_bar.png` - Bar chart comparaison estimateurs pour 1a
- `figures/sc1b_dag.png` - DAG NetworkX 3 noeuds (Localisation, Pub, Ventes)
- `figures/sc1b_coeff.png` - Errorbar plot 3 estimateurs pour 1b
- `figures/sc1b_bar.png` - Bar chart comparaison estimateurs pour 1b
- `data/sc1a_selection_qualite.csv` - Panel 4800 lignes sc1a
- `data/sc1b_selection_urbain.csv` - Panel 4800 lignes sc1b

## Decisions Made

- `colors_est` redéfini dans `code-sc1b-coeff` (pas dépendant de `code-sc1a-bar`) pour robustesse lors des réexécutions partielles du notebook
- ATT contrefactuel calculé avec `rng_cf_1a = np.random.default_rng(SEED + 11)` distinct de `rng_sc1a` — évite la contamination d'état si le nombre de traités change
- `drop_duplicates('magasin_id')` appliqué avant assignation pub niveau magasin — anti-pattern critique évité

## Deviations from Plan

### Observation critique — Direction du biais pédagogique inversée

**Contexte :** Le plan et la RESEARCH.md affirment que "OLS naïf surestime l'ATT" (must_haves.truths). La RESEARCH.md cite empiriquement ATT≈1070, OLS naïf≈1664 (+56% de surestimation).

**Constat d'exécution :**
- Sc1a : ATT=1070 €, OLS naïf=837 € → OLS **sous**estime l'ATT (37% en dessous)
- Sc1b : ATT=1127 €, OLS naïf=1105 € → OLS **sous**estime légèrement l'ATT

**Analyse :** Le confondant `qualite_equipe` crée une sélection positive (traités ont meilleur team → plus de visites), mais l'effet sur p_visite est faible (`EFFET_EQUIPE=0.02`). Par accident de tirage avec SEED=42, les magasins traités de 1a ont proportionnellement plus de petits magasins (43/102=42%) et moins de grands (16/102=16%) que les contrôles (36/98=37% petits, 19/98=19% grands). L'effet taille sur les ventes absolues (petits ≈ 202€/mois vs grands ≈ 3375€/mois) domine le biais positif de `qualite_equipe`. Résultat : baseline traitée < baseline contrôle → biais négatif.

**Cause racine :** `EFFET_EQUIPE=0.02` est trop faible pour dominer la variance de taille. La RESEARCH.md avait un résultat incorrect (1664) — non reproductible avec le notebook actuel.

**Ce que cela ne bloque pas :** Le code est correct, les figures sont générées, le notebook s'exécute sans erreur. Les figures montrent un écart OLS naïf ≠ ATT, ce qui est pédagogiquement intéressant. Seule la *direction* du biais est inversée par rapport à l'attendu.

**Impact architectural :** Corriger la direction nécessiterait d'augmenter `EFFET_EQUIPE` ou `EFFET_URBAIN` dans PARAMS — ce qui affecterait Phase 2 (Scénario 0) et Phase 1 (validation assertions). C'est une décision architectural à prendre par l'utilisateur.

**Action requise du formateur :** Décider si la direction inversée du biais est acceptable pour la formation, ou si les paramètres DGP doivent être recalibrés (ce qui réinitialise la chaîne de reproductibilité).

---

**Total deviations:** 0 auto-fixées
**Impact sur le plan :** Code correct per `<action>`. Observation pédagogique documentée. Décision DGP reportée à l'utilisateur.

## Issues Encountered

- La RESEARCH.md citait OLS naïf ≈ 1664 pour 1a, non reproductible empiriquement (résultat réel : 837). La recherche préalable avait une erreur de vérification. Le code du plan est correct, mais l'expectation de surestimation ne se vérifie pas avec SEED=42 et les paramètres actuels du DGP.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 03-02 (Scénario 1c — sélection par saison) peut démarrer : `base_df`, `compute_outcomes`, et le pattern ATT contrefactuel sont tous établis et fonctionnels
- La question de la calibration DGP (direction du biais) doit être tranchée avant la validation pédagogique finale
- Préoccupation pour 03-02 : si `EFFET_SAISON` suit la même dynamique (effet trop faible vs variance taille), le biais saisonnier pour 1c pourrait aussi être inversé — à surveiller lors de l'exécution de 03-02

---
*Phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection*
*Completed: 2026-03-04*
