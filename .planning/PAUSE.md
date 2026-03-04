# Pause Work — Phase 3, Wave 2 checkpoint

**Paused:** 2026-03-04
**Context:** En pleine exécution de /gsd:execute-phase 3

## Où on en est

Wave 1 (03-01) exécutée + commitée + recalibrée (EFFET_EQUIPE/URBAIN 0.02→0.20).
Wave 2 (03-02) : Task 1 commitée (cellules 1c insérées, c5982cb), checkpoint atteint.

**Le formateur a demandé un refactoring architectural** — changer le DV de `ventes` vers `log(ventes / n_potentiel)` pour :
- Interprétation en % (uplift)
- Mesure intensive (supprime l'effet de taille de magasin)

## Paramètres à modifier (AVANT de réécrire les cellules)

Cellule 1 du notebook (code-params) :
- EFFET_EQUIPE : 0.20 ✓ (déjà appliqué, commit 60c4f21)
- EFFET_URBAIN : 0.20 ✓ (déjà appliqué, commit 60c4f21)
- **EFFET_SAISON max : 0.02 → 0.08** (à faire)
  - Nouveau dict : {1:-0.04, 2:-0.04, 3:0.0, 4:0.04, 5:0.08, 6:0.08, 7:0.08, 8:0.04, 9:0.0, 10:-0.04, 11:0.04, 12:0.08}
  - max_pv = 0.83 < 0.99 ✓

## Résultats attendus après refactoring (SEED=42, vérifiés empiriquement)

DV = log(ventes / n_potentiel). Interprétation : log-points ≈ % uplift.

| Scénario | ATT_log | OLS naïf | OLS ajusté | Biais |
|----------|---------|----------|------------|-------|
| 1a (qualite_equipe) | ~28% | ~49% | ~28% | +75% surestimation |
| 1b (urbain) | ~29% | ~45% | ~33% | +56% surestimation |
| 1c (saison, es_max=0.08) | ~29% | ~38% | ~31% | +8.6pp visible |

## Travail restant

### 1. Modifier PARAMS dans notebook
- Changer EFFET_SAISON dict (max 0.02 → 0.08)
- Vérifier assertions re-passent (OK d'après simulation)

### 2. Réécrire les cellules de Phase 3 (10 cellules 03-01 + 5 cellules 03-02)

**Changements dans chaque cellule data (code-sc1x-data) :**
- Ajouter : `df_sc1x['log_rev_int'] = np.log(df_sc1x['ventes'] / df_sc1x['n_potentiel'])`
- ATT en log : `att_1x_log = (log_Y1_treated - log_Y0_cf).mean()`
- Formules OLS : remplacer `ventes ~` par `log_rev_int ~`
- Print : afficher en % (×100)

**Changements dans chaque cellule coeff/bar (code-sc1x-coeff, code-sc1x-bar) :**
- Variables : `coef_naive_1x` etc. = résultats OLS sur log_rev_int
- `att_1x` → `att_1x_log` (valeur log)
- Xlabel : "Uplift log des ventes (≈ %)" 
- Titre : factuel, sans commentaire

### 3. Ré-exécuter le notebook complet (nbconvert)

### 4. Reprendre le checkpoint 03-02 avec les nouvelles figures

## Note sur les commits déjà en place

- eb5df4d : feat(03-01) task 1 — cellules data+dag 1a+1b (à réécrire)
- 541f6ba : feat(03-01) task 2 — cellules coeff+bar 1a+1b (à réécrire)
- 60c4f21 : fix(params) EFFET_EQUIPE/URBAIN (conservé)
- c5982cb : feat(03-02) task 1 — cellules 1c (à réécrire)

Les cellules insérées sont toutes dans formation_causalite.ipynb — il faut les remplacer par les nouvelles versions.

## Commande pour reprendre

/gsd:execute-phase 3

Lire ce fichier PAUSE.md + RESEARCH.md + CONTEXT.md avant de commencer.
