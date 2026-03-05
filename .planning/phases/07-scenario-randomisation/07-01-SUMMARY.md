---
phase: 07-scenario-randomisation
plan: 01
subsystem: notebook
tags: [jupyter, numpy, matplotlib, pandas, causalite, randomisation]

# Dependency graph
requires:
  - phase: 06-validation-bout-en-bout
    provides: cellule validation finale avec PNG_ATTENDUS et CSV_ATTENDUS
provides:
  - Section Scenario 4 randomisation dans notebook (3 cellules)
  - data/sc4_randomisation_grand.csv — 200 magasins avec assignation aleatoire pub
  - data/sc4_randomisation_petit.csv — 30 magasins avec assignation aleatoire pub
  - figures/sc4_balance_grand.png — balance grand echantillon N=200
  - figures/sc4_balance_petit.png — balance petit echantillon N=30
  - Cellule validation mise a jour (22 PNG, 9 CSV)
affects: [08-vm2-dag-uniforme]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - rng_sc4 = np.random.default_rng(SEED + 70) — convention +10*phase, phase=7
    - stores = base_df[cols].drop_duplicates('magasin_id').copy().reset_index(drop=True)
    - stores['pub'] = rng.binomial(1, P_PUB_ALEATOIRE, size=len(stores))
    - balance_table() helper : groupby pub, agg pct_urbain/pct_bonne_equipe/pct_taille/n
    - plot_balance() helper : 3 axes matplotlib (urbain, equipe, taille groupee)

key-files:
  created:
    - data/sc4_randomisation_grand.csv
    - data/sc4_randomisation_petit.csv
    - figures/sc4_balance_grand.png
    - figures/sc4_balance_petit.png
  modified:
    - formation_causalite.ipynb

key-decisions:
  - "SEED+70 pour sc4 — convention +10*phase maintenue (phase=7)"
  - "Grand echantillon = tous les 200 magasins de base_df ; petit = 30 tires sans remise depuis le grand"
  - "Couleurs steelblue (Temoin) / darkorange (Traite) coherentes avec palette existante des scenarios"
  - "Ligne pointillee a 0.5 sur axes pct_urbain et pct_bonne_equipe — valeur theorique sous randomisation"
  - "balance_table() et plot_balance() comme helpers locaux — evite repetition code grand/petit"

patterns-established:
  - "Helper balance_table(df) : groupby pub -> agg pct_urbain, pct_bonne_equipe, pct_taille, n"
  - "Helper plot_balance(bal, title, filename) : fig 3 axes, savefig, plt.show()"

requirements-completed: [RAND-01, RAND-02, RAND-03, RAND-04]

# Metrics
duration: 8min
completed: 2026-03-05
---

# Phase 7 Plan 01: Scenario Randomisation Summary

**Demonstration visuelle balance par randomisation — grand echantillon (N=200) equilibre, petit echantillon (N=30) desequilibres par hasard seul — avec tableaux de balance, 2 CSV et 2 PNG exportes**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-05T11:20:00Z
- **Completed:** 2026-03-05T11:33:00Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Ajout du Scenario 4 au notebook (3 cellules : markdown + donnees + figures) avec insertion propre en index 41-43
- Grand echantillon (N=200) : barres traite et temoin visiblement equilibrees sur pct_urbain, pct_bonne_equipe, distribution taille
- Petit echantillon (N=30) : desequilibres apparents par hasard seul illustres visuellement
- Cellule validation mise a jour avec 22 PNG et 9 CSV attendus — notebook execute sans erreur bout-en-bout

## Task Commits

1. **Task 1: Inserer section donnees Scenario 4** - `9c19b5e` (feat)
2. **Task 2: Ajouter figures balance + mise a jour cellule validation** - `61c72f4` (feat)

## Files Created/Modified

- `/workspaces/formation_causalite/formation_causalite.ipynb` — 3 nouvelles cellules sc4 (45 cellules total), validation mise a jour
- `/workspaces/formation_causalite/data/sc4_randomisation_grand.csv` — 200 magasins, colonnes magasin_id/taille/urbain/qualite_equipe/pub
- `/workspaces/formation_causalite/data/sc4_randomisation_petit.csv` — 30 magasins, memes colonnes
- `/workspaces/formation_causalite/figures/sc4_balance_grand.png` — balance N=200 (3 axes)
- `/workspaces/formation_causalite/figures/sc4_balance_petit.png` — balance N=30 (3 axes)

## Decisions Made

- SEED+70 pour rng_sc4 : convention +10*phase maintenue (phase=7), isole le rng sc4 du reste
- Grand echantillon = tous les 200 magasins de base_df (pas de tirage supplementaire) ; petit = 30 tires sans remise depuis le grand — meme population de base
- Helpers locaux balance_table() et plot_balance() : eliminent la repetition code pour les deux tailles d'echantillon
- Couleurs steelblue/darkorange coherentes avec la palette existante des scenarios 1-3
- Ligne pointillee 0.5 seulement sur les axes pct_urbain et pct_bonne_equipe (pas sur distribution taille car pas de valeur theorique simple)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Scenario 4 complet et valide dans le notebook
- 45 cellules, execution bout-en-bout sans erreur
- Phase 8 (VM2 DAG uniforme) peut s'appuyer sur le meme pattern base_df + helpers locaux

---
*Phase: 07-scenario-randomisation*
*Completed: 2026-03-05*
