---
status: complete
phase: 01-fondations
source: [01-01-SUMMARY.md, 01-02-SUMMARY.md]
started: 2026-03-03T10:00:00Z
updated: 2026-03-03T10:15:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Structure du notebook
expected: Ouvrir formation_causalite.ipynb — 3 cellules dans l'ordre : (1) titre markdown, (2) Paramètres ALL_CAPS + dict PARAMS, (3) Imports+setup avec rng et pathlib mkdir
result: pass

### 2. Dossiers créés automatiquement
expected: Après avoir exécuté la cellule Imports+setup (ou Restart & Run All), les dossiers figures/ et data/ existent à la racine du projet
result: pass

### 3. Restart & Run All sans erreur
expected: Exécuter toutes les cellules (Restart & Run All dans Jupyter, ou jupyter nbconvert --execute formation_causalite.ipynb) — aucune exception, aucun traceback, exit code 0
result: pass

### 4. Panel reproductible
expected: Deux exécutions successives produisent un data/base_panel.csv identique — même valeurs ligne par ligne (SEED=42 garantit la reproductibilité)
result: pass

### 5. base_panel.csv correct
expected: data/base_panel.csv existe avec exactement 4800 lignes et 11 colonnes (magasin_id, taille, urbain, qualite_equipe, n_potentiel, mois, effet_saison_val, p_visite, nb_visites, ventes, panier_moyen) — la colonne pub est ABSENTE
result: pass

### 6. Assertions passent
expected: La cellule Assertions s'exécute sans lever d'exception et affiche : "Assertions OK — max p_visite cumulee: 0.420, variance ratio: 4.4x"
result: pass

### 7. DAG PNG exporté
expected: figures/dag_pattern_demo.png existe après exécution — c'est un DAG avec 3 nœuds et un layout fixe (pas une image blanche), dimensions ~859×411px
result: pass

## Summary

total: 7
passed: 7
issues: 0
pending: 0
skipped: 0

## Gaps

[none yet]
