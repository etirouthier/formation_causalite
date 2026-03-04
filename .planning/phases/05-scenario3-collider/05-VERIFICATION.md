---
phase: 05-scenario3-collider
verified: 2026-03-04T21:30:00Z
status: passed
score: 8/8 must-haves verified
re_verification: false
---

# Phase 5: Scénario 3 Collider — Verification Report

**Phase Goal:** Le formateur peut montrer que contrôler sur `posts_reseaux` introduit un biais là où l'estimation naïve était correcte, parce que `posts_reseaux` est un collider
**Verified:** 2026-03-04T21:30:00Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #   | Truth                                                                                                          | Status     | Evidence                                                                                          |
|-----|----------------------------------------------------------------------------------------------------------------|------------|---------------------------------------------------------------------------------------------------|
| 1   | DAG 3 noeuds V-structure (Pub et Ventes pointent vers Posts réseaux), exporté figures/sc3_dag.png             | VERIFIED   | Cell 38: G_sc3 edges `('Pub','Posts réseaux')` et `('Ventes','Posts réseaux')`, savefig confirmed |
| 2   | OLS naïf (~33.6%) > OLS avec posts_reseaux (~30.5%) — biais vers le bas >= 5% relatif visible                | VERIFIED   | Cell 37 runtime output: `OLS naïf: 33.6%  |  OLS avec posts_reseaux: 30.5%` (biais 9.4%)       |
| 3   | Bar chart compare 3 estimateurs : OLS sans collider (rouge), OLS avec posts_reseaux (orange), ATT (vert)      | VERIFIED   | Cell 40: 3 labels + colors `#e74c3c`, `#e67e22`, `#2ecc71`, savefig sc3_bar.png                  |
| 4   | posts_reseaux calculé APRÈS compute_outcomes depuis df_sc3, fusionné au niveau magasin                        | VERIFIED   | Cell 37: `ventes_agg = df_sc3.groupby('magasin_id')['ventes'].sum()` — pas base_df               |
| 5   | Seeds isolés : rng_sc3 = SEED+50, rng_cf_sc3 = SEED+51                                                       | VERIFIED   | Cell 37: `np.random.default_rng(SEED + 50)` et `np.random.default_rng(SEED + 51)`               |
| 6   | COLLIDER_PUB_VENTES_COEFF = 5e-5 dans la cellule Paramètres (cell index 1) ET dans le dict PARAMS            | VERIFIED   | Cell index 1 contient la constante et `'collider_pub_ventes_coeff': COLLIDER_PUB_VENTES_COEFF`   |
| 7   | CSV exporté data/sc3_collider.csv avec colonne posts_reseaux                                                  | VERIFIED   | Fichier 520K, 4800 lignes, colonnes vérifiées incluant posts_reseaux avec valeurs non-nulles      |
| 8   | Notebook s'exécute de bout en bout avec 41 cellules au total                                                   | VERIFIED   | 41 cellules confirmées, commit 0314b8c mentionne `nbconvert exit 0 sur 41 cellules`               |

**Score:** 8/8 truths verified

Note: Le check automatisé du PLAN testait `nb['cells'][0]` (index 0 = cellule markdown d'introduction), alors que la cellule Paramètres est à l'index 1. La constante `COLLIDER_PUB_VENTES_COEFF` est correctement présente dans la cellule Paramètres (index 1) — faux négatif du script de vérification du plan.

### Required Artifacts

| Artifact                  | Expected                                  | Status     | Details                                                      |
|---------------------------|-------------------------------------------|------------|--------------------------------------------------------------|
| `figures/sc3_dag.png`     | DAG Scénario 3 — V-structure collider     | VERIFIED   | 32K, produit le 2026-03-04 à 21:02                           |
| `figures/sc3_coeff.png`   | Coefficient plot Scénario 3               | VERIFIED   | 62K, 3 estimateurs avec IC 95% pour les deux OLS             |
| `figures/sc3_bar.png`     | Bar chart Scénario 3                      | VERIFIED   | 44K, 3 barres rouge/orange/vert avec ligne pointillée ATT    |
| `data/sc3_collider.csv`   | Dataset scénario 3 avec posts_reseaux     | VERIFIED   | 520K, 4800 lignes (200 magasins × 24 mois), colonne posts_reseaux présente |

### Key Link Verification

| From              | To                  | Via                                                          | Status   | Details                                                                  |
|-------------------|---------------------|--------------------------------------------------------------|----------|--------------------------------------------------------------------------|
| code-sc3-data     | posts_reseaux       | df_sc3.groupby('magasin_id')['ventes'].sum() — pas base_df  | WIRED    | `ventes_agg = df_sc3.groupby('magasin_id')['ventes'].sum()` confirmé    |
| code-sc3-data     | model_naive_sc3     | OLS `log_rev_int ~ pub` (sans collider = correct)           | WIRED    | `smf.ols('log_rev_int ~ pub', data=df_sc3).fit()` présent               |
| code-sc3-data     | model_coll_sc3      | OLS `log_rev_int ~ pub + posts_reseaux` (biaisé)            | WIRED    | `smf.ols('log_rev_int ~ pub + posts_reseaux', data=df_sc3).fit()` présent|
| code-sc3-dag      | G_sc3               | V-structure : Pub et Ventes tous deux pointent vers Posts réseaux | WIRED | Edges `('Pub','Posts réseaux')` et `('Ventes','Posts réseaux')` confirmés |

### Requirements Coverage

| Requirement | Source Plan | Description                                                                                             | Status     | Evidence                                                                 |
|-------------|-------------|---------------------------------------------------------------------------------------------------------|------------|--------------------------------------------------------------------------|
| SC3-01      | 05-01       | DAG causal illustrant le collider (pub → posts_reseaux ← ventes) et le chemin non causal ouvert        | SATISFIED  | Cell 38: G_sc3 V-structure, 3 noeuds avec Posts réseaux en crimson, sc3_dag.png exporté |
| SC3-02      | 05-01       | Coefficient plot montrant comment le coefficient pub change quand on ajoute posts_reseaux               | SATISFIED  | Cell 39: errorbar avec IC95%, OLS naïf 33.6% vs OLS avec collider 30.5%, sc3_coeff.png exporté |
| SC3-03      | 05-01       | Bar chart comparant estimation naïve vs sur-contrôlée vs valeur vraie                                  | SATISFIED  | Cell 40: 3 barres (rouge/orange/vert) + ligne pointillée ATT 30.2%, sc3_bar.png exporté |

Aucun requirement orphelin — les 3 IDs SC3-01/02/03 sont tous revendiqués par le plan 05-01 et tous satisfaits.

### Anti-Patterns Found

Aucun anti-pattern bloquant détecté sur les cellules scénario 3 (index 36-40) :

| Check                              | Result | Notes                                                     |
|------------------------------------|--------|-----------------------------------------------------------|
| TODO/FIXME/placeholder comments    | Aucun  | Cellules propres                                          |
| Empty returns (null/{}/ [])        | Aucun  | Pas applicable (code scientifique)                        |
| savefig avant plt.show             | OK     | Cells 38, 39, 40 : savefig positionné avant plt.show     |
| base_df.groupby dans sc3           | Absent | df_sc3.groupby utilisé correctement                      |
| C(mois) dans formules OLS sc3      | Absent | Pas de contrôle saisonnier (assignation aléatoire)        |
| node_colors_sc3 liste littérale    | Absent | Dérivé dynamiquement via `color_map_sc3[n] for n in`     |
| posts_reseaux mergé avant CSV      | OK     | Merge effectué avant `df_sc3.to_csv(...)`                 |

### Human Verification Required

#### 1. Clarté pédagogique du message collider

**Test:** Ouvrir le notebook exécuté, lire la cellule markdown scénario 3 (index 36), puis observer le coefficient plot et le bar chart.
**Expected:** Le formateur peut expliquer visuellement que contrôler sur posts_reseaux déplace l'estimation vers le bas (33.6% → 30.5%), et que cette "correction" est en réalité un biais ouvert par le collider — même si le résultat se rapproche de l'ATT vrai (30.2%), c'est une coïncidence.
**Why human:** La qualité du contraste pédagogique (Phase 3 : ajuster corrige / Phase 4 : ajuster biaise / Phase 5 : ajuster biaise aussi mais mécanisme différent) ne peut pas être vérifiée programmatiquement.

#### 2. Apparence visuelle du DAG V-structure

**Test:** Ouvrir `figures/sc3_dag.png`.
**Expected:** 3 noeuds clairement distincts par couleur (Pub en steelblue, Ventes en seagreen, Posts réseaux en crimson), les deux flèches pointant vers Posts réseaux visibles, structure en V inversé reconnaissable.
**Why human:** La lisibilité et la clarté visuelle du DAG ne peuvent pas être vérifiées par grep.

### Gaps Summary

Aucun gap — tous les must-haves sont vérifiés. La phase 5 atteint son objectif pédagogique.

---

_Verified: 2026-03-04T21:30:00Z_
_Verifier: Claude (gsd-verifier)_
