---
phase: 08-ventes-par-m2-et-dag-uniforme
plan: "01"
subsystem: notebook-dgp
tags: [ventes_par_m2, variable-derivee, figure, sc0]
dependency_graph:
  requires: []
  provides: [ventes_par_m2-colonne, sc0_ventes_par_m2-figure]
  affects: [formation_causalite.ipynb, data/base_panel.csv, data/sc0_biais_petits_nombres.csv]
tech_stack:
  added: []
  patterns: [groupby-agg-derive, intensive-variable]
key_files:
  modified:
    - formation_causalite.ipynb
    - data/base_panel.csv
    - data/sc0_biais_petits_nombres.csv
  created:
    - figures/sc0_ventes_par_m2.png
decisions:
  - "ventes_par_m2 = ventes / n_potentiel calculee dans base_df avant export et dans agg_sc0 apres groupby"
  - "ventes agregees via sum dans agg_sc0 pour permettre le calcul par magasin"
  - "Cellule code-sc0-fig-vm2 inseree apres les 4 figures sc0 existantes (apres code-sc0-fig4)"
metrics:
  duration: "5 min"
  completed: "2026-03-05"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 3
  files_created: 1
---

# Phase 08 Plan 01: Ventes par m2 — Variable Derivee et Figure Summary

**One-liner:** Variable intensive ventes_par_m2 = ventes/n_potentiel ajoutee au panel de base et a l'aggreage sc0, avec barplot par taille (petit/moyen/grand).

## What Was Built

- `base_df['ventes_par_m2']` calcule avant `to_csv()` dans `code-dgp-exec` — colonne presente dans `data/base_panel.csv`
- `ventes=('ventes', 'sum')` ajoute dans le groupby de `code-sc0-aggregation`, puis `agg_sc0['ventes_par_m2'] = agg_sc0['ventes'] / agg_sc0['n_potentiel']`
- Nouvelle cellule `code-sc0-fig-vm2` : barplot ventes_par_m2 moyen par taille avec `colors_sc0`
- `figures/sc0_ventes_par_m2.png` ajoute a `PNG_ATTENDUS` dans la cellule de validation finale

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Calculer ventes_par_m2 et l'inclure dans le CSV exporte | e809348 | formation_causalite.ipynb, data/base_panel.csv |
| 2 | Ajouter une figure ventes_par_m2 par taille | 0f5836b | figures/sc0_ventes_par_m2.png, data/sc0_biais_petits_nombres.csv |

## Verification Results

- `data/base_panel.csv` contient la colonne `ventes_par_m2` — OK
- `figures/sc0_ventes_par_m2.png` existe — OK
- `data/sc0_biais_petits_nombres.csv` contient `ventes_par_m2` — OK
- `jupyter nbconvert --execute` termine sans erreur — OK

## Deviations from Plan

**1. [Rule 2 - Missing functionality] Aggregation ventes dans agg_sc0**
- **Found during:** Task 1
- **Issue:** La colonne `ventes` n'etait pas agregee dans `agg_sc0` (seuls `n_potentiel`, `nb_visites`, `panier_moyen` l'etaient), rendant impossible le calcul `ventes_par_m2` au niveau magasin
- **Fix:** Ajout de `ventes=('ventes', 'sum')` dans le `.agg()` de `code-sc0-aggregation`
- **Files modified:** formation_causalite.ipynb (cell code-sc0-aggregation)
- **Commit:** e809348

## Self-Check: PASSED
