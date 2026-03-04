# Phase 6: Validation bout-en-bout - Research

**Researched:** 2026-03-04
**Domain:** Jupyter notebook validation, magic number cleanup, end-to-end execution verification
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Portée des magic numbers
- `p=0.5` dans `rng.binomial(1, 0.5, ...)` pour l'assignation pub aléatoire (sc2, sc3) EST un paramètre de simulation → ajouter `P_PUB_ALEATOIRE = 0.5` dans la cellule Paramètres et remplacer les deux occurrences
- Les offsets SEED (SEED+4, SEED+10, SEED+11, SEED+20, SEED+21, SEED+30, SEED+31, SEED+40, SEED+41, SEED+50, SEED+51) sont des détails d'implémentation RNG internes — acceptables tels quels, pas de migration dans PARAMS
- Les paramètres d'affichage (figsize, dpi, markersize, width) ne sont PAS des magic numbers dans ce contexte — laisser en place
- Les seuils d'assertion (ratio > 2.0, p_visite ∈ [0.01, 0.99]) sont des critères de validation pédagogique — acceptables tels quels

#### Cellule de validation finale
- Ajouter une cellule en toute fin de notebook qui vérifie automatiquement :
  1. Présence de tous les fichiers PNG attendus (20 fichiers dans `figures/`)
  2. Présence de tous les CSV attendus (7 fichiers dans `data/`)
  3. Assertion que `EFFET_PUB_VISITES` et `EFFET_PUB_PANIER` dans PARAMS sont bien les valeurs utilisées partout (via `assert PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES`)
- Format : assertions Python + message de succès "✓ Validation notebook : OK" si tout passe
- Si un fichier manque : `AssertionError` avec liste des fichiers absents

#### Warnings
- L'exécution actuelle ne produit aucun warning bloquant — aucun `filterwarnings` supplémentaire nécessaire
- Ne pas supprimer les warnings statsmodels légitimes (convergence, degrés de liberté) — ils sont informatifs

#### Vérification manuelle magic numbers
- Revue systématique du code : seul `p=0.5` (sc2 et sc3) est identifié comme magic number à corriger
- Aucun autre paramètre numérique de simulation hors PARAMS détecté

### Claude's Discretion
- Wording exact du message de succès final
- Ordre des assertions dans la cellule de validation
- Éventuels petits ajustements cosmétiques de commentaires si découverts pendant la revue

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| Cross-cutting | `Restart & Run All` s'exécute de bout en bout sans erreur ni warning bloquant | Notebook déjà validé nbconvert exit 0 — aucune modification structurelle requise |
| Cross-cutting | Tous les fichiers PNG (20) et CSV (7) présents dans `figures/` et `data/` après exécution | Liste exhaustive des fichiers attendus documentée ci-dessous — cell validation les vérifie |
| Cross-cutting | Aucun magic number hors cellule Paramètres | Seul `p=0.5` dans In[24] et In[28] identifié — remplacer par `P_PUB_ALEATOIRE` |
| Cross-cutting | Effet vrai identique entre tous les scénarios (`EFFET_PUB_VISITES` / `EFFET_PUB_PANIER` utilisées partout) | `EFFET_PUB_VISITES` et `EFFET_PUB_PANIER` sont dans PARAMS et injectées via `compute_outcomes(df, PARAMS, rng)` dans tous les scénarios — assertion dans cellule de validation suffit |
</phase_requirements>

---

## Summary

La Phase 6 est une phase de nettoyage et validation, non de développement. L'état actuel du notebook est excellent : 31 cellules s'exécutent sans erreur (nbconvert exit 0), les 20 PNG et 7 CSV sont déjà produits. Il reste deux interventions chirurgicales : (1) ajouter `P_PUB_ALEATOIRE = 0.5` dans la cellule Paramètres (In[1]) et remplacer les deux occurrences de `rng.binomial(1, 0.5, ...)` dans In[24] (sc2) et In[28] (sc3) ; (2) ajouter une nouvelle cellule finale (In[32]) qui vérifie la présence de tous les fichiers générés et l'intégrité des paramètres d'effet, avec un message de succès explicite.

Le travail est minime et à risque très faible. Les deux `0.5` littéraux sont des paramètres de simulation au sens strict (probabilité d'assignation du traitement pub) : les rendre explicites dans PARAMS améliore la lisibilité pédagogique sans modifier le comportement. La cellule de validation finale sert à la fois de test de bout-en-bout automatique et de signal visible au formateur que le notebook est prêt.

**Primary recommendation:** Un seul plan suffira pour cette phase — modifier la cellule PARAMS (In[1]), corriger In[24] et In[28], ajouter la cellule de validation (In[32]), puis exécuter nbconvert pour confirmer exit 0.

---

## Standard Stack

### Core
| Outil | Version | Purpose | Why Standard |
|-------|---------|---------|--------------|
| Python | 3.x (existant) | Langage du notebook | Déjà en place |
| jupyter nbconvert | existant | Validation `Restart & Run All` automatisée | Déjà utilisé dans les phases précédentes |
| pathlib.Path | stdlib | Vérification d'existence des fichiers | Déjà importé (`from pathlib import Path`) |

### Supporting
| Outil | Version | Purpose | When to Use |
|-------|---------|---------|-------------|
| `assert` Python | stdlib | Validation en cellule finale | Pour toutes les vérifications de cohérence |

**Installation:** Aucune installation requise — stack entièrement existant.

---

## Architecture Patterns

### État actuel du notebook (In[1] à In[31])

```
In[1]   — Cellule PARAMS (ALL_CAPS + PARAMS dict)        ← modifier : ajouter P_PUB_ALEATOIRE
In[2]   — Imports (numpy, pandas, matplotlib, seaborn, statsmodels, networkx, Path)
In[3]   — generate_base_panel()
In[4]   — compute_outcomes() + base_df + exports CSV/DAG
In[5]   — Assertions de cohérence (p_visite, nb_visites, ratio variance)
In[6]   — Scénario 0 : agrégation agg_sc0 + CSV
In[7]   — sc0 : Figure 1 (distribution)
In[8]   — sc0 : Figure 2 (scatter)
In[9]   — sc0 : Figure 3 (top 10)
In[10]  — sc0 : Figure 4 (loi des grands nombres)
In[11]  — Pattern DAG (dag_pattern_demo.png)
In[12]  — sc1a : données + CSV
In[13]  — sc1a : DAG
In[14]  — sc1b : données + CSV
In[15]  — sc1c : données + CSV
In[16]  — sc1c : DAG
In[17]  — sc1a : coefficient plot
In[18]  — sc1a : bar chart
In[19]  — sc1b : coefficient plot
In[20]  — sc1b : bar chart (contient sc1b_dag implicitement)
In[21]  — sc1c : coefficient plot
In[22]  — sc1c : bar chart
In[23]  — sc1b : DAG (ordre notebook)
In[24]  — sc2 : données + CSV                            ← modifier : 0.5 → P_PUB_ALEATOIRE
In[25]  — sc2 : DAG
In[26]  — sc2 : coefficient plot
In[27]  — sc2 : bar chart
In[28]  — sc3 : données + CSV                            ← modifier : 0.5 → P_PUB_ALEATOIRE
In[29]  — sc3 : DAG
In[30]  — sc3 : coefficient plot
In[31]  — sc3 : bar chart
In[32]  — NOUVELLE : cellule de validation finale         ← créer
```

### Pattern 1: Ajout du paramètre P_PUB_ALEATOIRE dans PARAMS (In[1])

**What:** Ajouter la constante ALL_CAPS dans la section Paramètres, et l'injecter dans le dict PARAMS.
**When to use:** Immédiatement — avant de corriger les cellules sc2 et sc3.
**Example:**
```python
# À ajouter dans In[1], après les lignes P_PUB_BASSE_SAISON
P_PUB_ALEATOIRE = 0.5    # sc2, sc3 : assignation pub aléatoire (pas de confondant)

PARAMS = {
    # ... paramètres existants ...
    'p_pub_basse_saison': P_PUB_BASSE_SAISON,
    'p_pub_aleatoire': P_PUB_ALEATOIRE,       # ajouter ici
    'collider_pub_coeff':    COLLIDER_PUB_COEFF,
    'collider_ventes_coeff': COLLIDER_VENTES_COEFF,
}
```

### Pattern 2: Remplacement des occurrences de 0.5 dans sc2 et sc3

**What:** Remplacer le littéral `0.5` par `P_PUB_ALEATOIRE` dans les deux cellules d'assignation pub.
**When to use:** Après modification de In[1].
**Example:**
```python
# In[24] — avant
stores_sc2['pub'] = rng_sc2.binomial(1, 0.5, size=len(stores_sc2))

# In[24] — après
stores_sc2['pub'] = rng_sc2.binomial(1, P_PUB_ALEATOIRE, size=len(stores_sc2))

# In[28] — avant
stores_sc3['pub'] = rng_sc3.binomial(1, 0.5, size=len(stores_sc3))

# In[28] — après
stores_sc3['pub'] = rng_sc3.binomial(1, P_PUB_ALEATOIRE, size=len(stores_sc3))
```

### Pattern 3: Cellule de validation finale (In[32])

**What:** Nouvelle cellule de code à la fin du notebook qui vérifie présence des fichiers et cohérence des paramètres d'effet.
**When to use:** Comme dernière cellule du notebook.
**Example:**
```python
# ═══════════════════════════════════════════════════════════
# VALIDATION FINALE — Notebook bout-en-bout
# ═══════════════════════════════════════════════════════════

from pathlib import Path

# 1. Fichiers PNG attendus (20 fichiers)
PNG_ATTENDUS = [
    'figures/dag_pattern_demo.png',
    'figures/sc0_distribution.png',
    'figures/sc0_loi_grands_nombres.png',
    'figures/sc0_scatter.png',
    'figures/sc0_top10.png',
    'figures/sc1a_bar.png',
    'figures/sc1a_coeff.png',
    'figures/sc1a_dag.png',
    'figures/sc1b_bar.png',
    'figures/sc1b_coeff.png',
    'figures/sc1b_dag.png',
    'figures/sc1c_bar.png',
    'figures/sc1c_coeff.png',
    'figures/sc1c_dag.png',
    'figures/sc2_bar.png',
    'figures/sc2_coeff.png',
    'figures/sc2_dag.png',
    'figures/sc3_bar.png',
    'figures/sc3_coeff.png',
    'figures/sc3_dag.png',
]

# 2. Fichiers CSV attendus (7 fichiers)
CSV_ATTENDUS = [
    'data/base_panel.csv',
    'data/sc0_biais_petits_nombres.csv',
    'data/sc1a_selection_qualite.csv',
    'data/sc1b_selection_urbain.csv',
    'data/sc1c_selection_saison.csv',
    'data/sc2_mediateur.csv',
    'data/sc3_collider.csv',
]

# Vérification présence des PNG
png_manquants = [f for f in PNG_ATTENDUS if not Path(f).exists()]
assert not png_manquants, f"PNG manquants : {png_manquants}"

# Vérification présence des CSV
csv_manquants = [f for f in CSV_ATTENDUS if not Path(f).exists()]
assert not csv_manquants, f"CSV manquants : {csv_manquants}"

# 3. Cohérence des effets vrais entre scénarios
assert PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES, \
    f"Incohérence effet_pub_visites : PARAMS={PARAMS['effet_pub_visites']} ≠ {EFFET_PUB_VISITES}"
assert PARAMS['effet_pub_panier'] == EFFET_PUB_PANIER, \
    f"Incohérence effet_pub_panier : PARAMS={PARAMS['effet_pub_panier']} ≠ {EFFET_PUB_PANIER}"

print(f"✓ Validation notebook : OK")
print(f"  {len(PNG_ATTENDUS)} PNG présents dans figures/")
print(f"  {len(CSV_ATTENDUS)} CSV présents dans data/")
print(f"  Effet pub visites : {EFFET_PUB_VISITES:.0%} (cohérent)")
print(f"  Effet pub panier  : {EFFET_PUB_PANIER:.0%} (cohérent)")
```

### Anti-Patterns to Avoid
- **Modifier compute_outcomes() ou generate_base_panel():** Ces fonctions sont correctes et validées — ne pas y toucher.
- **Supprimer des warnings statsmodels:** Les warnings de convergence sont pédagogiquement informatifs — les laisser.
- **Hardcoder les noms de fichiers sans liste explicite:** La liste explicite PNG_ATTENDUS/CSV_ATTENDUS est préférable à `glob('figures/*.png')` car elle vérifie que LES BONS fichiers sont présents, pas juste n'importe quel PNG.
- **Utiliser PARAMS['p_pub_aleatoire'] dans la cellule de validation au lieu de P_PUB_ALEATOIRE:** La validation finale doit utiliser les constantes ALL_CAPS comme référence canonique, pas PARAMS.

---

## Don't Hand-Roll

| Problème | Ne pas construire | Utiliser plutôt | Pourquoi |
|---------|-------------------|-----------------|---------|
| Vérifier l'existence d'un fichier | Code os.path custom | `pathlib.Path(f).exists()` | Déjà importé dans le notebook |
| Valider la présence de tous les fichiers | Boucle complexe | List comprehension + assert | Pattern simple, lisible, cohérent avec assertsions existantes |
| Lancer Restart & Run All pour validation | Script shell custom | `jupyter nbconvert --to notebook --execute` | Déjà utilisé dans les phases précédentes |

**Key insight:** Toute la logique de validation est constructible avec des assertions Python standard — pas besoin de framework de test externe.

---

## Common Pitfalls

### Pitfall 1: Oublier d'ajouter P_PUB_ALEATOIRE dans le dict PARAMS
**What goes wrong:** La constante ALL_CAPS est définie mais pas injectée dans PARAMS — la modification est incomplète.
**Why it happens:** Deux endroits à modifier dans In[1] : la déclaration de la constante ET l'entrée dans PARAMS.
**How to avoid:** Vérifier que `'p_pub_aleatoire': P_PUB_ALEATOIRE` est bien dans le dict PARAMS après modification.
**Warning signs:** `PARAMS` ne contient pas `p_pub_aleatoire` après exécution de In[1].

### Pitfall 2: Path relatif dans la cellule de validation
**What goes wrong:** `Path('figures/sc0_distribution.png').exists()` retourne False si le CWD n'est pas la racine du projet.
**Why it happens:** Jupyter utilise le répertoire du notebook comme CWD par défaut — mais ce n'est pas garanti.
**How to avoid:** Le notebook utilise déjà des paths relatifs (`Path('figures').mkdir(...)`) et nbconvert s'exécute depuis la racine — le même pattern fonctionne. Pas de changement nécessaire, cohérent avec le reste du notebook.
**Warning signs:** `Path('figures').exists()` retourne False en début de cellule.

### Pitfall 3: Assertion sur `PARAMS['effet_pub_visites'] == EFFET_PUB_VISITES` toujours vraie
**What goes wrong:** Cette assertion est triviale si PARAMS est construit dans la même cellule que EFFET_PUB_VISITES — elle ne teste pas vraiment la cohérence inter-scénarios.
**Why it happens:** PARAMS est initialisé une fois avec la valeur correcte, jamais modifié.
**How to avoid:** L'assertion reste utile car elle explicite la garantie formellement et sera visible dans l'output du notebook. Compléter avec le message print confirmant les valeurs numériques effectives.

### Pitfall 4: La liste PNG_ATTENDUS/CSV_ATTENDUS doit être exhaustive
**What goes wrong:** Oublier un fichier dans la liste → la validation passe même si le fichier manque.
**Why it happens:** Compter manuellement 20 PNG est source d'erreur.
**How to avoid:** Comparer la liste hardcodée avec `ls figures/` : les 20 PNG actuels sont documentés dans le CONTEXT.md. Cross-check avec les lignes `savefig` dans le notebook (20 occurrences confirmées).

---

## Code Examples

### Inventaire complet des fichiers attendus (vérifié depuis le notebook)

Depuis l'analyse des appels `savefig` et `to_csv` dans le notebook :

**20 PNG dans `figures/` :**
```
dag_pattern_demo.png   sc0_distribution.png   sc0_loi_grands_nombres.png
sc0_scatter.png        sc0_top10.png
sc1a_bar.png           sc1a_coeff.png         sc1a_dag.png
sc1b_bar.png           sc1b_coeff.png         sc1b_dag.png
sc1c_bar.png           sc1c_coeff.png         sc1c_dag.png
sc2_bar.png            sc2_coeff.png          sc2_dag.png
sc3_bar.png            sc3_coeff.png          sc3_dag.png
```

**7 CSV dans `data/` :**
```
base_panel.csv
sc0_biais_petits_nombres.csv
sc1a_selection_qualite.csv
sc1b_selection_urbain.csv
sc1c_selection_saison.csv
sc2_mediateur.csv
sc3_collider.csv
```

### Commande de validation post-modification
```bash
jupyter nbconvert --to notebook --execute formation_causalite.ipynb \
    --output /tmp/formation_causalite_validated.ipynb \
    --ExecutePreprocessor.timeout=300
echo "Exit code: $?"
```

---

## State of the Art

| Ancien état | État après Phase 6 | Impact |
|-------------|-------------------|--------|
| `rng.binomial(1, 0.5, ...)` dans In[24] et In[28] | `rng.binomial(1, P_PUB_ALEATOIRE, ...)` | INFRA-01 pleinement satisfait |
| Pas de cellule de validation finale | In[32] avec 20+7 assertions fichiers + cohérence paramètres | Formateur a confirmation explicite "OK" |
| 31 cellules | 32 cellules | Notebook complet |

---

## Open Questions

Aucune question ouverte. Tous les points ambigus ont été résolus dans CONTEXT.md :
- Portée des magic numbers : décidée
- Cellule de validation : format décidé
- Warnings : décidé (ne pas toucher)

---

## Sources

### Primary (HIGH confidence)
- Analyse directe du notebook `formation_causalite.ipynb` via `nbconvert --to script` — inventaire exhaustif des `savefig`, `to_csv`, et occurrences de `0.5`
- CONTEXT.md phase 06 — décisions utilisateur locked
- REQUIREMENTS.md — critères de succès phase 6

### Secondary (MEDIUM confidence)
- Pattern existant `assert condition, message` dans In[5] du notebook — réutilisé pour la cellule finale

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stack entièrement existant, aucune dépendance externe
- Architecture: HIGH — deux modifications chirurgicales clairement identifiées + nouvelle cellule
- Pitfalls: HIGH — vérifiés directement depuis le code source du notebook

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stable — pas de dépendances externe changeantes)
