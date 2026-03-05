---
phase: 08-ventes-par-m2-et-dag-uniforme
plan: 02
subsystem: notebook-dag
tags: [dag, visualisation, uniformisation, noir]
dependency_graph:
  requires: []
  provides: [DAG-01]
  affects: [formation_causalite.ipynb]
tech_stack:
  added: []
  patterns: [node_color='black' dans tous les nx.draw_networkx()]
key_files:
  created: []
  modified:
    - formation_causalite.ipynb
decisions:
  - "node_color='black' uniforme — suppression de toutes les color_map (steelblue/seagreen/darkorange/crimson/mediumpurple)"
  - "font_color='white' maintenu pour lisibilite sur fond noir"
metrics:
  duration: ~10 min
  completed: 2026-03-05
---

# Phase 8 Plan 02: DAG Uniforme Noir — Summary

Uniformisation de tous les DAG du notebook en noir : suppression de toutes les color_map variables, remplacement par `node_color='black'` dans les 6 cellules nx.draw_networkx().

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Uniformiser les 6 cellules DAG en noir | 8179ca3 | formation_causalite.ipynb |
| 2 | Exécuter le notebook et vérifier les figures DAG | f6f03a2 | formation_causalite.ipynb |

## Artifacts Produced

- `figures/dag_pattern_demo.png` — Pattern DAG en noir
- `figures/sc1a_dag.png` — DAG sc1a en noir
- `figures/sc1b_dag.png` — DAG sc1b en noir
- `figures/sc1c_dag.png` — DAG sc1c en noir
- `figures/sc2_dag.png` — DAG sc2 en noir
- `figures/sc3_dag.png` — DAG sc3 en noir

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Accolades fermantes orphelines supprimées par erreur**
- **Found during:** Task 2 (exécution notebook)
- **Issue:** Le nettoyage des color_map dict a supprimé les lignes `}` correspondant au dict `pos_sc2` et `pos_sc3`, causant une SyntaxError
- **Fix:** Restauration des `}` fermantes pour les dicts pos_sc2 et pos_sc3
- **Files modified:** formation_causalite.ipynb
- **Commit:** f6f03a2

## Self-Check: PASSED

- formation_causalite.ipynb: FOUND
- figures/dag_pattern_demo.png: FOUND
- figures/sc1a_dag.png: FOUND
- figures/sc1b_dag.png: FOUND
- figures/sc1c_dag.png: FOUND
- figures/sc2_dag.png: FOUND
- figures/sc3_dag.png: FOUND
- Commit 8179ca3: FOUND
- Commit f6f03a2: FOUND
