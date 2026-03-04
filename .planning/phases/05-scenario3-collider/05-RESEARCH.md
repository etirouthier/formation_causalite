# Phase 5: Scénario 3 — Surcontrôle sur un collider - Research

**Researched:** 2026-03-04
**Domain:** Causal inference pedagogy — collider bias, DGP construction, OLS in Jupyter notebook
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### DGP du collider — posts_reseaux
- Variable **continue** calculée au **niveau magasin**
- Équation : `posts_reseaux = a * pub × ventes_agg + bruit` (terme d'interaction, pas additif)
  - `pub` : assignation magasin (0/1)
  - `ventes_agg` : ventes agrégées par magasin (somme sur les mois)
  - bruit : terme gaussien pour réalisme
- Structure collider : `pub → posts_reseaux ← ventes` — posts_reseaux est causé par les deux
- Narratif laissé au formateur (variable flexible, pas encore nommée définitivement)

#### Paramètres exposés dans PARAMS
- `COLLIDER_PUB_VENTES_COEFF` (ou équivalent ALL_CAPS) dans la cellule Paramètres
- Permet de recalibrer si le biais observé est insuffisant (< 5%) ou trop fort
- Convention de seed : `rng_sc3 = np.random.default_rng(SEED + 50)` (convention +10×phase)

#### Régressions OLS
- OLS naïf : `log_rev_int ~ pub` → effet total (proche de la vérité, pas de confondant)
- OLS sur-contrôlé : `log_rev_int ~ pub + posts_reseaux` → biaisé (direction déterminée empiriquement)
- Valeur vraie : ATT contrefactuel (même pattern que Phase 4)
- Biais requis : au moins 5% de différence visible (success criteria roadmap)

#### Figures — 3 au total (même structure que Phase 4)
- `sc3_dag.png` — DAG networkx, même style que sc2 (pos dict fixe, nœuds colorés)
- `sc3_coeff.png` — coefficient plot vertical, 3 points avec IC 95%
- `sc3_bar.png` — bar chart 3 barres (naïf / sur-contrôlé / vrai) + ligne pointillée
- Naming cohérent avec la convention `sc{N}_*.png`

#### DAG — structure
- Même pattern Phase 4 : `nx.DiGraph`, `pos` dict fixe, `draw_networkx`, nœuds colorés
- Nœuds : `Pub`, `Ventes`, `Posts réseaux` (collider)
- Structure en V inversé visible : `Pub → Posts réseaux ← Ventes`
- Couleur collider distincte des médiateurs (à décider par Claude)
- Labels verbeux en français pour les slides

### Claude's Discretion
- Direction effective du biais (vers le haut ou le bas — déterminée empiriquement par les coefficients)
- Couleur exacte du nœud collider dans le DAG
- Valeur initiale de COLLIDER_PUB_VENTES_COEFF (à calibrer pour ≥ 5% de biais)
- Nœuds DAG : inclure ou non `Nb visites` selon lisibilité
- Labels exacts des axes et titres

### Deferred Ideas (OUT OF SCOPE)
Aucune — discussion restée dans le périmètre de la phase.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SC3-01 | DAG causal illustrant le collider (`pub → posts_reseaux ← ventes`) et le chemin non causal ouvert par le contrôle | DAG pattern from Phase 4 sc2 directly reusable; V-structure layout documented below |
| SC3-02 | Coefficient plot montrant comment le coefficient `pub` change quand on ajoute `posts_reseaux` (OLS sans collider vs OLS avec collider) | OLS pattern from Phase 4 directly reusable; empirical values calibrated: naive=33.6% vs sur-contrôlé=30.5% |
| SC3-03 | Bar chart comparant : estimation naïve (sans contrôle) vs estimation sur-contrôlée (avec collider) vs valeur vraie | Bar chart pattern from Phase 4 directly reusable; empirical values: 33.6% / 30.5% / 30.2% |
</phase_requirements>

---

## Summary

Phase 5 is a direct structural clone of Phase 4 (scénario 2 — médiateur), with one core difference: the controlled variable `posts_reseaux` is a **collider** (caused by both `pub` and `ventes`) rather than a mediator. All notebook patterns — DAG construction, OLS formula, ATT contrefactuel, coefficient plot, bar chart — can be copied from Phase 4 cells 31-35 and adapted for scénario 3. The primary work is the DGP construction for `posts_reseaux` and the empirical calibration of `COLLIDER_PUB_VENTES_COEFF`.

Empirical calibration has been run with SEED=42, `rng_sc3 = np.random.default_rng(SEED + 50)`, `rng_cf_sc3 = np.random.default_rng(SEED + 51)`. With `COLLIDER_PUB_VENTES_COEFF = 5e-5`, the results are: ATT (vrai) = 30.2%, OLS naïf = 33.6%, OLS sur-contrôlé = 30.5%. The bias is 3.2pp (9.4% relative), which exceeds the 5% relative threshold. The direction of bias: controlling on the collider reduces the naive coefficient (downward bias). This is determined empirically — the CONTEXT says "direction déterminée empiriquement par les coefficients."

The key subtlety for the planner: with `COLLIDER_PUB_VENTES_COEFF = 5e-5`, the OLS sur-contrôlé (30.5%) is very close to ATT (30.2%), which may appear visually confusing in the bar chart (it looks like controlling helps). The formateur must explain that this proximity is coincidental and that the pub coefficient changed from 33.6% to 30.5% due to collider bias. The pedagogical contrast between Phase 4 and Phase 5 is the same direction of bias (controlling on both mediator and collider reduces the estimate) but the mechanism is fundamentally different.

**Primary recommendation:** Copy Phase 4 cell structure (5 cells: 1 markdown + 4 code). Use `COLLIDER_PUB_VENTES_COEFF = 5e-5`. Compute `posts_reseaux` after `compute_outcomes` since it requires observed `ventes` per store. Seeds: `SEED+50` for data, `SEED+51` for counterfactual.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| numpy | already in env | RNG, numerical ops | Used throughout project |
| pandas | already in env | groupby aggregation for ventes_agg | Used throughout project |
| statsmodels | already in env | smf.ols() for naive and sur-contrôlé models | Used throughout project |
| networkx | already in env | DAG visualization | Used in all previous scenarios |
| matplotlib | already in env | coefficient plot, bar chart | Used in all previous scenarios |

### No New Dependencies
All libraries already installed. Phase 5 adds zero new imports.

## Architecture Patterns

### Notebook Cell Structure (5 cells matching Phase 4)

```
Cell 36 [markdown]: --- ## Scénario 3 header
Cell 37 [code]:     code-sc3-data  — DGP + OLS + ATT + CSV export
Cell 38 [code]:     code-sc3-dag   — DAG networkx V-structure
Cell 39 [code]:     code-sc3-coeff — coefficient plot 3 points
Cell 40 [code]:     code-sc3-bar   — bar chart 3 barres
```

After insertion: notebook goes from 36 → 41 cells.

### Pattern 1: DGP du collider (posts_reseaux)

**What:** Compute `posts_reseaux` at store level after `compute_outcomes` is called. Use interaction term `pub * ventes_agg` as the signal plus Gaussian noise. Add `COLLIDER_PUB_VENTES_COEFF` to PARAMS cell.

**Critical ordering constraint:** `posts_reseaux` must be computed AFTER `compute_outcomes(df_sc3, PARAMS, rng_sc3)` because it requires observed `ventes` (which includes the pub treatment effect). Then aggregate to store level, compute the collider, and merge back to the row-level panel.

**Example:**
```python
# Source: empirically calibrated in research phase
# In PARAMS cell (cell 1) — add this line:
COLLIDER_PUB_VENTES_COEFF = 5e-5

# In PARAMS dict — add:
# 'collider_pub_ventes_coeff': COLLIDER_PUB_VENTES_COEFF,

# In code-sc3-data cell:
rng_sc3 = np.random.default_rng(SEED + 50)

# Random assignment (same as sc2)
stores_sc3 = base_df[['magasin_id']].drop_duplicates('magasin_id').copy()
stores_sc3['pub'] = rng_sc3.binomial(1, 0.5, size=len(stores_sc3))

# Observed outcomes (pub effect materializes here)
df_sc3 = base_df.merge(stores_sc3[['magasin_id', 'pub']], on='magasin_id')
df_sc3 = compute_outcomes(df_sc3, PARAMS, rng_sc3)
df_sc3['log_rev_int'] = np.log(df_sc3['ventes'] / df_sc3['n_potentiel'])

# Collider DGP — AFTER compute_outcomes (needs observed ventes)
ventes_agg = df_sc3.groupby('magasin_id')['ventes'].sum().reset_index()
ventes_agg.columns = ['magasin_id', 'ventes_agg']
stores_collider = stores_sc3.merge(ventes_agg, on='magasin_id')
bruit_sc3 = rng_sc3.normal(0, 1, size=len(stores_collider))
stores_collider['posts_reseaux'] = (
    COLLIDER_PUB_VENTES_COEFF * stores_collider['pub'] * stores_collider['ventes_agg']
    + bruit_sc3
)
df_sc3 = df_sc3.merge(stores_collider[['magasin_id', 'posts_reseaux']], on='magasin_id')
```

### Pattern 2: ATT Contrefactuel (identique Phase 4)

```python
# Source: Phase 4 pattern (sc2), adapted for sc3
treated_ids_sc3 = stores_sc3[stores_sc3['pub'] == 1]['magasin_id'].values
df_treated_sc3 = df_sc3[df_sc3['magasin_id'].isin(treated_ids_sc3)].copy()
rng_cf_sc3 = np.random.default_rng(SEED + 51)   # seed dédié, isolé
df_cf_sc3 = df_treated_sc3.copy()
df_cf_sc3['pub'] = 0
df_cf_sc3 = compute_outcomes(df_cf_sc3, PARAMS, rng_cf_sc3)
df_cf_sc3['log_rev_int'] = np.log(df_cf_sc3['ventes'] / df_cf_sc3['n_potentiel'])
log_Y1_sc3 = np.log(df_treated_sc3['ventes'] / df_treated_sc3['n_potentiel'])
log_Y0_sc3 = np.log(df_cf_sc3['ventes'] / df_cf_sc3['n_potentiel'])
att_sc3_log = (log_Y1_sc3 - log_Y0_sc3).mean()
```

### Pattern 3: OLS Formulas

```python
# OLS naïf : effet total — CORRECT (assignation aléatoire, pas de confondant)
model_naive_sc3 = smf.ols('log_rev_int ~ pub', data=df_sc3).fit()
# OLS sur-contrôlé : biaisé (collider crée un chemin non causal)
model_coll_sc3  = smf.ols('log_rev_int ~ pub + posts_reseaux', data=df_sc3).fit()
```

**Critical:** No `C(mois)` in formulas — random assignment, no seasonal confounding (same as Phase 4).

### Pattern 4: DAG V-structure (SC3-01)

```python
# Source: Phase 4 DAG pattern — adapted for V-structure (inverted V / collider)
G_sc3 = nx.DiGraph()
G_sc3.add_edges_from([
    ('Pub', 'Ventes'),
    ('Pub', 'Posts réseaux'),    # pub → collider
    ('Ventes', 'Posts réseaux'), # ventes → collider (V-structure)
])
pos_sc3 = {
    'Pub':          (0, 1),
    'Ventes':       (0, 0),
    'Posts réseaux': (1, 0.5),
}
color_map_sc3 = {
    'Pub':           'steelblue',
    'Ventes':        'seagreen',
    'Posts réseaux': 'crimson',     # collider = rouge distinctif (choix Claude)
}
node_colors_sc3 = [color_map_sc3[n] for n in G_sc3.nodes()]

fig, ax = plt.subplots(figsize=(5, 3.5))
nx.draw_networkx(G_sc3, pos_sc3, ax=ax,
                 node_color=node_colors_sc3,
                 node_size=2000, font_size=9, font_color='white',
                 arrows=True, arrowsize=20)
ax.axis('off')
ax.set_title('DAG — Scénario 3 : collider posts_reseaux')
fig.savefig('figures/sc3_dag.png', dpi=150, bbox_inches='tight')
plt.show()
```

**DAG layout rationale:** Pub (top-left) and Ventes (bottom-left) both point TO Posts réseaux (right). This is the V-structure / collider pattern. Including `Pub → Ventes` is necessary to complete the causal graph (pub does affect ventes via visits and basket). The edge `Pub → Ventes` is direct in the DAG even though it passes through mediators — simplify for pedagogical clarity.

**Alternative without Pub→Ventes edge:** If the formateur prefers to show only the collider structure:
```python
G_sc3.add_edges_from([
    ('Pub', 'Posts réseaux'),
    ('Ventes', 'Posts réseaux'),
])
```
This shows the pure collider without the causal path — simpler but loses the full causal story.

### Pattern 5: Coefficient Plot (SC3-02 — identique Phase 4)

```python
# 3 estimateurs : OLS naïf (rouge), OLS sur-contrôlé (orange), ATT (vert)
coef_naive_sc3 = model_naive_sc3.params['pub']
ci_naive_sc3   = model_naive_sc3.conf_int()
xerr_naive_sc3 = [[coef_naive_sc3 - ci_naive_sc3.loc['pub', 0]],
                   [ci_naive_sc3.loc['pub', 1] - coef_naive_sc3]]

coef_coll_sc3 = model_coll_sc3.params['pub']
ci_coll_sc3   = model_coll_sc3.conf_int()
xerr_coll_sc3 = [[coef_coll_sc3 - ci_coll_sc3.loc['pub', 0]],
                  [ci_coll_sc3.loc['pub', 1] - coef_coll_sc3]]

estimators_sc3 = ['OLS sans collider', 'OLS avec posts_reseaux', 'Valeur vraie (ATT)']
```

### Pattern 6: Bar Chart (SC3-03 — identique Phase 4)

```python
labels_sc3 = ['OLS sans collider', 'OLS avec posts_reseaux', 'Valeur vraie (ATT)']
values_sc3 = [coef_naive_sc3, coef_coll_sc3, att_sc3_log]
colors_sc3 = ['#e74c3c', '#e67e22', '#2ecc71']   # rouge / orange / vert
```

**Color choice:** Use orange for the sur-contrôlé (biased) estimator — different from Phase 4's blue — to create visual distinction across scenarios.

### Anti-Patterns to Avoid

- **DO NOT compute `posts_reseaux` before `compute_outcomes`** — the collider needs observed `ventes` (including the pub effect); computing before would use `base_df` ventes (pub=0 only)
- **DO NOT use `rng_sc3` for both data and collider noise AND counterfactual** — separate seeds: `SEED+50` for data+collider, `SEED+51` for counterfactual
- **DO NOT add `C(mois)` to OLS formulas** — random assignment, no seasonal confounding
- **DO NOT put `posts_reseaux` in PARAMS dict** — it's a derived variable, not a parameter (the COEFF is in PARAMS)
- **DO NOT use the same collider noise seed as the data seed** — the `bruit_sc3 = rng_sc3.normal(...)` call consumes from `rng_sc3` after `compute_outcomes`, which is correct; just don't reset the seed
- **DO NOT include `posts_reseaux` in the CSV export if it's store-level** — merge back before export so the row-level CSV has the collider column
- **DO NOT call the biased model "correct"** — it is `model_coll_sc3` (biased), the naive is the correct one

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| OLS with confidence intervals | Custom matrix algebra | `smf.ols().fit().conf_int()` | Already in project, same API as Phase 4 |
| DAG layout | spring_layout or custom positioning | `pos` dict with fixed coordinates | DGP-06 requirement, consistent across scenarios |
| Store-level aggregation | Manual loop | `df.groupby('magasin_id')['ventes'].sum()` | pandas groupby handles N_MAGASINS=200 efficiently |

---

## Common Pitfalls

### Pitfall 1: Collider Computed at Wrong Stage
**What goes wrong:** `posts_reseaux` computed from `base_df` instead of `df_sc3` — uses pub=0 ventes for all stores, zero signal for treated units.
**Why it happens:** Forgetting that `posts_reseaux = f(ventes_observed)` where ventes_observed includes the pub treatment effect.
**How to avoid:** Always compute `ventes_agg` from `df_sc3` AFTER `compute_outcomes(df_sc3, PARAMS, rng_sc3)`.
**Warning signs:** `posts_reseaux` for treated vs control has no systematic difference; bias in OLS is near zero.

### Pitfall 2: Seed Contamination
**What goes wrong:** Using `rng_sc3` for counterfactual computation — creates dependency between data generation and ATT estimation.
**Why it happens:** Forgetting the seed isolation pattern.
**How to avoid:** `rng_cf_sc3 = np.random.default_rng(SEED + 51)` — separate dedicated seed.
**Warning signs:** Results change when noise parameters change in ways that shouldn't affect ATT.

### Pitfall 3: PARAMS Cell Modification
**What goes wrong:** Adding `COLLIDER_PUB_VENTES_COEFF` only in the data cell, not in PARAMS cell (cell 1).
**Why it happens:** Easy to add it as a local variable in code-sc3-data.
**How to avoid:** Must add as ALL_CAPS constant in cell 1 AND add to PARAMS dict (INFRA-01 requirement).
**Warning signs:** Formateur cannot find parameter to tune; `PARAMS` dict doesn't contain the key.

### Pitfall 4: Empty `posts_reseaux` for Control Stores
**What goes wrong:** Confusion: with the multiplicative spec, control stores (pub=0) have `posts_reseaux = bruit` only (near zero signal). This is by design — it shows that posts_reseaux IS a function of pub.
**Why it happens:** Thinking all collider values should be nonzero.
**How to avoid:** Document this in a code comment; it's intentional. Control stores: posts_reseaux ~ N(0,1). Treated stores: posts_reseaux ~ N(alpha * ventes_agg, 1).

### Pitfall 5: Bias Direction Confusion
**What goes wrong:** Expecting naive < avec-collider when actually naive > avec-collider.
**Why it happens:** Collider bias can go either direction depending on the signs of the causal effects.
**How to avoid:** Run empirical verification first. With SEED=42 and alpha=5e-5: naive (33.6%) > avec-collider (30.5%) — downward bias from collider control.
**Warning signs:** `coef_naive_sc3 < coef_coll_sc3` — if this happens, check DGP signs.

### Pitfall 6: nb_cells Count in Verification
**What goes wrong:** Verification assertion `len(nb['cells']) >= 41` fails because cells were inserted at wrong index or duplicate.
**Why it happens:** Phase 4 left 36 cells; Phase 5 adds 5 → 41 total.
**How to avoid:** Verify `len(nb['cells']) == 41` after insertion.

---

## Code Examples

### Complete code-sc3-data cell

```python
# Source: Phase 4 pattern adapted for sc3 collider
# ─────────────────────────────────────────────
# Scénario 3 — Surcontrôle sur un collider
# Assignation pub : aléatoire niveau magasin (pas de confondant)
# Collider : posts_reseaux causé par PUB ET VENTES
# ─────────────────────────────────────────────

rng_sc3 = np.random.default_rng(SEED + 50)

# Assignation pub aléatoire au niveau magasin (p=0.5 — pas de confondant)
stores_sc3 = base_df[['magasin_id']].drop_duplicates('magasin_id').copy()
stores_sc3['pub'] = rng_sc3.binomial(1, 0.5, size=len(stores_sc3))

# Panel complet + outcomes observés
df_sc3 = base_df.merge(stores_sc3[['magasin_id', 'pub']], on='magasin_id')
df_sc3 = compute_outcomes(df_sc3, PARAMS, rng_sc3)
df_sc3['log_rev_int'] = np.log(df_sc3['ventes'] / df_sc3['n_potentiel'])

# Collider DGP — APRÈS compute_outcomes (nécessite ventes observées avec pub)
ventes_agg = df_sc3.groupby('magasin_id')['ventes'].sum().reset_index()
ventes_agg.columns = ['magasin_id', 'ventes_agg']
stores_collider = stores_sc3.merge(ventes_agg, on='magasin_id')
bruit_sc3 = rng_sc3.normal(0, 1, size=len(stores_collider))
stores_collider['posts_reseaux'] = (
    COLLIDER_PUB_VENTES_COEFF * stores_collider['pub'] * stores_collider['ventes_agg']
    + bruit_sc3
)
df_sc3 = df_sc3.merge(stores_collider[['magasin_id', 'posts_reseaux']], on='magasin_id')

# Calcul ATT contrefactuel (rng dédié pour isolation)
treated_ids_sc3 = stores_sc3[stores_sc3['pub'] == 1]['magasin_id'].values
df_treated_sc3 = df_sc3[df_sc3['magasin_id'].isin(treated_ids_sc3)].copy()
rng_cf_sc3 = np.random.default_rng(SEED + 51)
df_cf_sc3 = df_treated_sc3.copy()
df_cf_sc3['pub'] = 0
df_cf_sc3 = compute_outcomes(df_cf_sc3, PARAMS, rng_cf_sc3)
df_cf_sc3['log_rev_int'] = np.log(df_cf_sc3['ventes'] / df_cf_sc3['n_potentiel'])
log_Y1_sc3 = np.log(df_treated_sc3['ventes'] / df_treated_sc3['n_potentiel'])
log_Y0_sc3 = np.log(df_cf_sc3['ventes'] / df_cf_sc3['n_potentiel'])
att_sc3_log = (log_Y1_sc3 - log_Y0_sc3).mean()

# OLS naïf : effet total (correct car assignation aléatoire)
model_naive_sc3 = smf.ols('log_rev_int ~ pub', data=df_sc3).fit()
# OLS sur-contrôlé : biaisé (le collider crée un chemin non causal)
model_coll_sc3  = smf.ols('log_rev_int ~ pub + posts_reseaux', data=df_sc3).fit()

# Export CSV
df_sc3.to_csv('data/sc3_collider.csv', index=False)
print(f"Sc3 — Traités: {len(treated_ids_sc3)}/200 magasins")
print(f"Sc3 — ATT: {att_sc3_log*100:.1f}%  |  OLS naïf: {model_naive_sc3.params['pub']*100:.1f}%  |  OLS avec posts_reseaux: {model_coll_sc3.params['pub']*100:.1f}%")
```

### PARAMS cell additions

```python
# Add to cell 1 (after EFFET_PUB_PANIER):
COLLIDER_PUB_VENTES_COEFF = 5e-5

# Add to PARAMS dict:
'collider_pub_ventes_coeff': COLLIDER_PUB_VENTES_COEFF,
```

---

## Empirical Results (Calibrated)

Results verified by running the DGP with SEED=42, rng_sc3=SEED+50, rng_cf_sc3=SEED+51, COLLIDER_PUB_VENTES_COEFF=5e-5:

| Estimateur | Valeur | Notes |
|------------|--------|-------|
| ATT contrefactuel (vrai) | 30.2% | log-points, ≈ % uplift |
| OLS naïf (sans collider) | 33.6% | correct (aléatoire) |
| OLS sur-contrôlé (avec posts_reseaux) | 30.5% | biaisé vers le bas |
| Biais absolu | 3.2pp | naïf - sur-contrôlé |
| Biais relatif | 9.4% | > seuil de 5% |
| Nb traités | 113/200 | |
| Nb contrôle | 87/200 | |

**Direction du biais:** Downward (downward bias when controlling on collider) — `naive > avec-collider`.

**Nuance pédagogique importante:** Le modèle sur-contrôlé (30.5%) est très proche de l'ATT (30.2%) — proximité fortuite due à la variation d'échantillonnage (naive est lui-même au-dessus de l'ATT de 3.4pp par bruit aléatoire). Le formateur doit expliquer que la proximité avec l'ATT est une coïncidence et que le biais est la variation du coefficient pub entre les deux modèles OLS (33.6% → 30.5% = -3.1pp).

**If bias is insufficient (< 5% relative):** Increase `COLLIDER_PUB_VENTES_COEFF` up to `1e-4` (gives 3.44pp / 10.2% relative — maximum plateau with this DGP).

---

## State of the Art

| Pattern | Phase 4 (Médiateur) | Phase 5 (Collider) | Key difference |
|---------|--------------------|--------------------|----------------|
| Seed data | SEED+40 | SEED+50 | Convention +10×phase |
| Seed CF | SEED+41 | SEED+51 | Convention +10×phase |
| Modèle correct | OLS sans médiateur (naïf) | OLS sans collider (naïf) | Same logic |
| Modèle biaisé | OLS avec panier_moyen | OLS avec posts_reseaux | Different mechanism |
| DGP biais | panier_moyen dans compute_outcomes | posts_reseaux calculé après compute_outcomes | Collider needs observed ventes |
| CSV | sc2_mediateur.csv | sc3_collider.csv | Naming convention |
| Cell count | 31→36 | 36→41 | +5 cells each phase |

---

## Integration: Where to Insert Cells

Insert 5 new cells **after cell index 35** (the last existing cell = code-sc2-bar, index 35).

```python
# Cells to insert at positions 36-40:
# Cell 36: [markdown]  sc3 header
# Cell 37: [code]      code-sc3-data
# Cell 38: [code]      code-sc3-dag
# Cell 39: [code]      code-sc3-coeff
# Cell 40: [code]      code-sc3-bar
```

PARAMS modification is in cell 1 (existing cell — must edit, not insert).

---

## Open Questions

1. **DAG includes `Pub → Ventes` edge or not?**
   - What we know: in the DGP, pub does affect ventes (via p_visite and mu_panier) — so the edge exists causally
   - What's unclear: CONTEXT says nœuds = `Pub`, `Ventes`, `Posts réseaux` — does not mention direct `Pub → Ventes` edge explicitly
   - Recommendation: Include `('Pub', 'Ventes')` to show the complete causal structure; the V-shape `Pub → Posts réseaux ← Ventes` is still visible; alternatively, exclude it for pedagogical simplicity (only 2 edges: pub→collider, ventes→collider)

2. **`Nb visites` nœud in DAG?**
   - What we know: CONTEXT says "Nb visites (si utile)" — discretion to Claude
   - What's unclear: whether showing nb_visites as intermediate node helps or clutters
   - Recommendation: Omit for sc3 DAG. Three-node V-structure (Pub, Ventes, Posts réseaux) is cleaner and focuses the pedagogical message on the collider. Nb visites would require 5+ nodes.

3. **Bar chart visual ambiguity (ATT ≈ avec-collider)?**
   - What we know: numerically, ATT (30.2%) ≈ avec-collider (30.5%) — bars 2 and 3 look almost identical
   - What's unclear: will this confuse students into thinking controlling on collider is "correct"?
   - Recommendation: Accept the ambiguity. Add a comment in the code or markdown explaining that the proximity is coincidental. The key pedagogical point is the CHANGE in the pub coefficient (33.6% → 30.5%) due to adding posts_reseaux, not whether the estimate happens to be close to ATT.

---

## Sources

### Primary (HIGH confidence)
- Empirical calibration run in research phase (2026-03-04) — all numerical values verified by executing the DGP locally
- `formation_causalite.ipynb` cells 31-35 (Phase 4 sc2 patterns) — directly inspected
- `.planning/phases/04-scenario2-mediateur/04-01-PLAN.md` — Phase 4 patterns documented
- `.planning/phases/05-scenario3-collider/05-CONTEXT.md` — locked decisions verified

### Secondary (MEDIUM confidence)
- Causal inference theory: collider bias direction depends on the signs of both causal paths — well-established statistical theory (Pearl, Hernán & Robins), verified consistent with empirical results

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — same libraries as all previous phases, no new dependencies
- Architecture patterns: HIGH — directly adapted from Phase 4 (empirically verified)
- Empirical calibration: HIGH — run locally with SEED=42, exact values computed
- Pitfalls: HIGH — identified through actual calibration runs (pitfall 1 was found during research)

**Research date:** 2026-03-04
**Valid until:** 2026-03-34 (stable — DGP is deterministic with fixed seeds)
