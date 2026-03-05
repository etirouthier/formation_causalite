# Phase 4: Scénario 2 — Surcontrôle sur un médiateur - Research

**Researched:** 2026-03-04
**Domain:** Jupyter notebook — causal inference pedagogy, OLS mediator bias, DGP simulation
**Confidence:** HIGH (all claims verified against existing notebook code and empirical simulation)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Variable dépendante**
- DV = `log_rev_int = log(ventes / n_potentiel)` — log-points ≈ % uplift
- Même DV que Phase 3 (refactoring validé, décision formateur)
- Coefficients OLS en log-points (pas en €)

**Structure du scénario**
- Un seul scénario (pas de sous-scénarios 2a/2b/2c)
- Assignation pub aléatoire au niveau magasin (pas de confondant — contraste avec Phase 3)
- Le biais vient du sur-contrôle, pas de la sélection
- `panier_moyen` est le médiateur : `pub → panier_moyen → ventes` ET `pub → nb_visites → ventes`

**Comparaison OLS**
- OLS sans médiateur : `log_rev_int ~ pub` → effet total (proche de la vérité)
- OLS avec médiateur : `log_rev_int ~ pub + panier_moyen` → effet direct seulement (biaisé vers le bas)
- Valeur vraie : ATT contrefactuel

**Figures — 3 au total**
- Une par type : 1 DAG + 1 coefficient plot + 1 bar chart → 3 PNG dans `figures/`
- Naming : `sc2_dag.png`, `sc2_coeff.png`, `sc2_bar.png`
- Pas de figure composite

**DAG — nœuds**
- Même pattern Phase 3 : `nx.DiGraph`, `pos` dict fixe, `draw_networkx`, nœuds colorés
- Labels verbeux en français pour les slides : `Pub`, `Ventes`, `Panier moyen`, `Nb visites`
- Deux chemins causaux visibles : `Pub → Nb visites → Ventes` ET `Pub → Panier moyen → Ventes`
- Nœuds couleurs : Pub=steelblue, Ventes=seagreen, médiateurs=darkorange/mediumpurple

**Coefficient plot**
- Style vertical : un point par estimateur sur l'axe Y, valeur sur l'axe X
- Barres d'erreur IC 95% pour les deux estimateurs OLS
- 3 points : OLS sans contrôle, OLS avec `panier_moyen`, Valeur vraie (ATT)
- xlabel : `"Uplift log des ventes (≈ %)"` — cohérent avec Phase 3

**Bar chart**
- 3 barres : sans contrôle (rouge), avec médiateur (bleu), valeur vraie (vert)
- Ligne pointillée horizontale à la valeur vraie
- ylabel : `"Uplift log des ventes (≈ %)"`

### Claude's Discretion
- Seed dédié pour Phase 4 : `rng_sc2 = np.random.default_rng(SEED + 40)` (convention +10×phase)
- Niveau d'assignation pub (magasin ou ligne) — cohérent avec scénarios non-saisonniers → niveau magasin
- Couleurs exactes des nœuds DAG (cohérentes avec sc1x)
- Labels exacts des axes et titres (factuel, sans commentaire interprétatif)

### Deferred Ideas (OUT OF SCOPE)
Aucune — Phase 4 est le seul scénario médiateur.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SC2-01 | DAG causal illustrant les deux chemins (`pub → nb_visites → ventes` ET `pub → panier_moyen → ventes`) | DAG pattern verified from sc1x code: `nx.DiGraph`, fixed `pos` dict, 4 nodes with two mediator paths. Pub=steelblue, Ventes=seagreen, Nb visites=darkorange, Panier moyen=mediumpurple. |
| SC2-02 | Coefficient plot montrant comment le coefficient `pub` change quand on ajoute `panier_moyen` comme variable de contrôle (OLS sans médiateur vs OLS avec médiateur) | Empirically verified: OLS sans med = 30.77%, OLS avec med = 21.08% — visible 9.7pp downward bias. Same `ax.errorbar` pattern as sc1x. |
| SC2-03 | Bar chart comparant : effet estimé sans contrôle (correct) vs effet estimé avec contrôle sur médiateur (biaisé) vs valeur vraie | Same 3-bar pattern as sc1x bar charts. Bars: OLS sans contrôle (red), OLS avec médiateur (blue), ATT (green). |
</phase_requirements>

---

## Summary

Phase 4 inserts one new scenario (Scénario 2) into `formation_causalite.ipynb` after the existing Phase 3 cells (cells 17-30). The scenario illustrates that controlling on a mediator variable (`panier_moyen`) in OLS biases the `pub` coefficient downward, even when the treatment assignment is completely random. This is the pedagogical contrast to Phase 3: with random pub assignment, the naive OLS is correct; adding a mediator as control introduces bias.

The DGP already implements the mediator structure: `panier_moyen` is computed as `ventes / nb_visites` where `ventes` depends on both `nb_visites` (affected by `pub` via `EFFET_PUB_VISITES=0.10`) and `mu_panier` (affected by `pub` via `EFFET_PUB_PANIER=0.10`). Controlling on `panier_moyen` in OLS mechanically blocks the `pub → panier_moyen → ventes` path, leaving only the `pub → nb_visites → ventes` path active. This produces a downward bias of approximately 8-10 percentage points with `SEED=42`.

Empirical simulation with `SEED=42` and `SEED+40` confirms the bias is clearly visible: ATT=30.0%, OLS sans médiateur=30.8%, OLS avec médiateur=21.1% — approximately a 31% reduction in the estimated coefficient when the mediator is included. The pattern structure (5 cells: 1 markdown header + 1 data cell + 1 DAG cell + 1 coeff plot cell + 1 bar chart cell) is a direct reuse of the sc1a/sc1b template.

**Primary recommendation:** Reuse the sc1a pattern verbatim, adapting only: (1) random pub assignment instead of confounded assignment, (2) no adjusted model — replace with mediated model, (3) 4-node DAG showing two causal paths, (4) drop `C(mois)` from both OLS formulas since pub is random (seasonality is not a confounder).

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| numpy | Already installed | RNG, log computation, counterfactual simulation | `np.random.default_rng(SEED+40)`, `np.log()` |
| pandas | Already installed | DataFrame manipulation, merge, dropna | Panel data operations |
| statsmodels | Already installed | OLS estimation with formula API | `smf.ols('log_rev_int ~ pub + panier_moyen', data=df).fit()` |
| matplotlib | Already installed | Figures (coefficient plot, bar chart) | `ax.errorbar`, `ax.bar`, `ax.axhline` |
| networkx | Already installed | DAG visualization | `nx.DiGraph`, `nx.draw_networkx` |

### No New Dependencies
All required libraries are already imported in cell 2 of the notebook. Phase 4 requires zero new `pip install` calls.

---

## Architecture Patterns

### Cell Structure (5 cells total)
```
Cell N:   [markdown] ## Scénario 2 — Surcontrôle sur un médiateur
Cell N+1: [code]     Data generation + OLS models + ATT + CSV export
Cell N+2: [code]     DAG figure → sc2_dag.png
Cell N+3: [code]     Coefficient plot → sc2_coeff.png
Cell N+4: [code]     Bar chart → sc2_bar.png
```

Insert after cell 30 (last sc1c bar chart). The notebook will have 36 cells total after insertion.

### Pattern 1: Random Pub Assignment at Store Level
**What:** Assign pub randomly with 50% probability per store, constant across 24 months.
**When to use:** When there is no confounding (contrast to sc1a/sc1b which used biased probabilities).
**Example:**
```python
# Source: verified against sc1a pattern (cell 17) with p=0.5 substituted
rng_sc2 = np.random.default_rng(SEED + 40)

stores_sc2 = base_df[['magasin_id']].drop_duplicates('magasin_id').copy()
stores_sc2['pub'] = rng_sc2.binomial(1, 0.5, size=len(stores_sc2))

df_sc2 = base_df.merge(stores_sc2[['magasin_id', 'pub']], on='magasin_id')
df_sc2 = compute_outcomes(df_sc2, PARAMS, rng_sc2)
df_sc2['log_rev_int'] = np.log(df_sc2['ventes'] / df_sc2['n_potentiel'])
```

**Key difference from sc1a:** No `qualite_equipe` or `urbain` in probability — just flat 0.5 for all stores.

### Pattern 2: ATT Counterfactual (identical to sc1a)
**What:** For treated stores only, rerun `compute_outcomes` with `pub=0` using a dedicated RNG.
**When to use:** Always — matches the Phase 3 pattern exactly.
**Example:**
```python
# Source: verified against sc1a ATT block (cell 17)
treated_ids_sc2 = stores_sc2[stores_sc2['pub'] == 1]['magasin_id'].values
df_treated_sc2 = df_sc2[df_sc2['magasin_id'].isin(treated_ids_sc2)].copy()
rng_cf_sc2 = np.random.default_rng(SEED + 41)
df_cf_sc2 = df_treated_sc2.copy()
df_cf_sc2['pub'] = 0
df_cf_sc2 = compute_outcomes(df_cf_sc2, PARAMS, rng_cf_sc2)
df_cf_sc2['log_rev_int'] = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])
log_Y1_sc2 = np.log(df_treated_sc2['ventes'] / df_treated_sc2['n_potentiel'])
log_Y0_sc2 = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])
att_sc2_log = (log_Y1_sc2 - log_Y0_sc2).mean()
```

### Pattern 3: OLS Models — Correct vs Biased
**What:** Two OLS formulas: one without mediator (correct total effect), one with mediator (biased direct effect).
**Critical insight:** Since pub is random, `C(mois)` is NOT needed in OLS — it is not a confounder. Omitting it simplifies the model and makes the mediator bias more transparent pedagogically.
**Example:**
```python
# Source: empirically verified — both formulas with and without C(mois) give same pub coef
model_naive_sc2 = smf.ols('log_rev_int ~ pub', data=df_sc2).fit()
model_med_sc2   = smf.ols('log_rev_int ~ pub + panier_moyen', data=df_sc2).fit()
```

**Warning:** `panier_moyen` has NaN when `nb_visites == 0`. Empirical check (SEED=42): 0 NaN values in this DGP (P_BASE_VISITE=0.25 ensures nb_visites > 0 for nearly all rows). Safe to use `df_sc2` directly without `.dropna()`.

### Pattern 4: 4-Node DAG with Two Mediator Paths
**What:** DAG showing `Pub → Nb visites → Ventes` AND `Pub → Panier moyen → Ventes`.
**When to use:** This is the distinguishing visual of sc2 — two parallel causal paths, no confounders.
**Example:**
```python
# Source: verified against sc1a DAG pattern (cell 18), extended to 4 nodes
G_sc2 = nx.DiGraph()
G_sc2.add_edges_from([
    ('Pub', 'Nb visites'),
    ('Pub', 'Panier moyen'),
    ('Nb visites', 'Ventes'),
    ('Panier moyen', 'Ventes'),
])
pos_sc2 = {
    'Pub': (0, 0.5),
    'Nb visites': (1, 1),
    'Panier moyen': (1, 0),
    'Ventes': (2, 0.5),
}
color_map_sc2 = {
    'Pub': 'steelblue',
    'Ventes': 'seagreen',
    'Nb visites': 'darkorange',
    'Panier moyen': 'mediumpurple',
}
node_colors_sc2 = [color_map_sc2[n] for n in G_sc2.nodes()]
```

### Pattern 5: Coefficient Plot (3 estimators)
```python
# Source: sc1a coefficient plot pattern (cell 22) — same structure
coef_naive_sc2 = model_naive_sc2.params['pub']
ci_naive_sc2   = model_naive_sc2.conf_int()
xerr_naive_sc2 = [[coef_naive_sc2 - ci_naive_sc2.loc['pub', 0]],
                   [ci_naive_sc2.loc['pub', 1] - coef_naive_sc2]]

coef_med_sc2 = model_med_sc2.params['pub']
ci_med_sc2   = model_med_sc2.conf_int()
xerr_med_sc2 = [[coef_med_sc2 - ci_med_sc2.loc['pub', 0]],
                 [ci_med_sc2.loc['pub', 1] - coef_med_sc2]]

estimators_sc2 = ['OLS sans médiateur', 'OLS avec panier_moyen', 'Valeur vraie (ATT)']
y_pos_sc2 = [2, 1, 0]

fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar(coef_naive_sc2, 2, xerr=xerr_naive_sc2, fmt='o', capsize=5,
            color='#e74c3c', label='OLS sans médiateur', markersize=8)
ax.errorbar(coef_med_sc2, 1, xerr=xerr_med_sc2, fmt='o', capsize=5,
            color='#3498db', label='OLS avec panier_moyen', markersize=8)
ax.errorbar(att_sc2_log, 0, fmt='D', color='#2ecc71',
            label='Valeur vraie (ATT)', markersize=10)
ax.axvline(x=att_sc2_log, color='gray', linestyle='--', alpha=0.5)
ax.set_yticks(y_pos_sc2)
ax.set_yticklabels(estimators_sc2)
ax.set_xlabel('Uplift log des ventes (≈ %)')
ax.set_title('Scénario 2 — Coefficients OLS sans vs avec médiateur vs valeur vraie')
ax.legend(loc='lower right')
fig.savefig('figures/sc2_coeff.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Anti-Patterns to Avoid
- **Using `C(mois)` in OLS formulas:** Pub is random, so season is not a confounder. Including `C(mois)` is not wrong (coefficients are identical empirically) but obscures the pedagogical message that the only bias source is the mediator.
- **Calling the second model "OLS ajusté":** The Phase 3 vocabulary "ajusté" means "corrected". In sc2 it is "with mediator = biased", not "adjusted = better". Use `model_med_sc2` and label it `'OLS avec panier_moyen'`.
- **Using `stores_sc2[['magasin_id', 'qualite_equipe']]` in drop_duplicates:** sc2 has random assignment — no confounding variable needed in the merge. Use `drop_duplicates('magasin_id')` only.
- **Connecting Pub directly to Ventes in the DAG:** The sc2 DGP has NO direct path from pub to ventes — pub acts entirely through nb_visites and panier_moyen. The DAG must NOT include a `Pub → Ventes` edge.
- **NaN handling with `dropna()`:** With current PARAMS, `nb_visites` is never 0 for this DGP, so `panier_moyen` has no NaN (verified empirically). Do not add `.dropna()` which would differ from sc1x pattern.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Counterfactual ATT | Custom loop to flip pub and recompute | `compute_outcomes(df_cf, PARAMS, rng_cf)` with `pub=0` | Already implemented in DGP, sc1a pattern proven |
| Confidence intervals | Manual t-distribution calculation | `model.conf_int().loc['pub', :]` | statsmodels provides exact OLS CIs |
| DAG layout | `spring_layout` or manual iteration | Fixed `pos` dict | Non-deterministic layouts break reproducibility (DGP-06) |
| RNG isolation | Reusing `rng_sc2` for counterfactual | Dedicated `rng_cf_sc2 = np.random.default_rng(SEED + 41)` | Ensures counterfactual reproductibility independent of data generation order |

**Key insight:** The entire sc2 implementation is a direct adaptation of sc1a. There is no novel code to write — only parameter substitutions (random probabilities, mediator in formula, 4-node DAG).

---

## Common Pitfalls

### Pitfall 1: Labeling the biased model as "naïf"
**What goes wrong:** Calling `log_rev_int ~ pub + panier_moyen` the "naïf" model is backwards — in sc2 the naive model WITHOUT controls is correct, and the "sophisticated" model WITH controls is wrong.
**Why it happens:** Phase 3 trained the reflex "naïf = no controls = bad." Sc2 deliberately inverts this.
**How to avoid:** Name clearly: `model_naive_sc2` (no mediator = correct) and `model_med_sc2` (with mediator = biased). Labels in figures: `'OLS sans médiateur'` and `'OLS avec panier_moyen'`.
**Warning signs:** If bar chart shows OLS sans médiateur < OLS avec médiateur, something is wrong.

### Pitfall 2: Including a direct Pub → Ventes edge in the DAG
**What goes wrong:** The DAG becomes causally incorrect — pub does NOT directly cause ventes in this DGP (only indirectly via nb_visites and panier_moyen).
**Why it happens:** sc1x DAGs all have a direct `Pub → Ventes` edge, so the template suggests it.
**How to avoid:** The sc2 DAG has 4 edges total: `Pub→Nb visites`, `Pub→Panier moyen`, `Nb visites→Ventes`, `Panier moyen→Ventes`. No direct `Pub→Ventes`.

### Pitfall 3: Seed mismatch breaking reproducibility
**What goes wrong:** Using a seed already consumed by earlier rng states causes sc2 results to depend on execution order of previous cells.
**Why it happens:** Reusing global `rng` or wrong SEED offset.
**How to avoid:** Use `rng_sc2 = np.random.default_rng(SEED + 40)` and `rng_cf_sc2 = np.random.default_rng(SEED + 41)` — independent seeds. Convention: phase 4 → +40/+41 (established in CONTEXT.md under Claude's Discretion).

### Pitfall 4: Pedagogical framing confusion
**What goes wrong:** Student interprets "OLS avec médiateur biased" as "use less variables = always better."
**Why it happens:** Sc2 message and sc1 message superficially look opposite.
**How to avoid:** The markdown cell header must make explicit: "Le biais vient du sur-contrôle (pas d'un confondant omis)." The title of Phase 4 is "Surcontrôle sur un médiateur" — the word "surcontrôle" carries the pedagogical point.

---

## Code Examples

### Complete Data Cell (verified by simulation)
```python
# Source: Empirically verified with SEED=42 → ATT=30.0%, OLS sans=30.8%, OLS avec=21.1%
# ─────────────────────────────────────────────
# Scénario 2 — Surcontrôle sur un médiateur
# Assignation pub : aléatoire niveau magasin (pas de confondant)
# Médiateur bloqué : panier_moyen
# ─────────────────────────────────────────────

rng_sc2 = np.random.default_rng(SEED + 40)

# Assignation pub aléatoire au niveau magasin (p=0.5 — pas de confondant)
stores_sc2 = base_df[['magasin_id']].drop_duplicates('magasin_id').copy()
stores_sc2['pub'] = rng_sc2.binomial(1, 0.5, size=len(stores_sc2))

# Panel complet + outcomes observés
df_sc2 = base_df.merge(stores_sc2[['magasin_id', 'pub']], on='magasin_id')
df_sc2 = compute_outcomes(df_sc2, PARAMS, rng_sc2)
df_sc2['log_rev_int'] = np.log(df_sc2['ventes'] / df_sc2['n_potentiel'])

# Calcul ATT contrefactuel (rng dédié pour isolation)
treated_ids_sc2 = stores_sc2[stores_sc2['pub'] == 1]['magasin_id'].values
df_treated_sc2 = df_sc2[df_sc2['magasin_id'].isin(treated_ids_sc2)].copy()
rng_cf_sc2 = np.random.default_rng(SEED + 41)
df_cf_sc2 = df_treated_sc2.copy()
df_cf_sc2['pub'] = 0
df_cf_sc2 = compute_outcomes(df_cf_sc2, PARAMS, rng_cf_sc2)
df_cf_sc2['log_rev_int'] = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])
log_Y1_sc2 = np.log(df_treated_sc2['ventes'] / df_treated_sc2['n_potentiel'])
log_Y0_sc2 = np.log(df_cf_sc2['ventes'] / df_cf_sc2['n_potentiel'])
att_sc2_log = (log_Y1_sc2 - log_Y0_sc2).mean()

# OLS sans médiateur : effet total (correct car assignation aléatoire)
model_naive_sc2 = smf.ols('log_rev_int ~ pub', data=df_sc2).fit()
# OLS avec médiateur : effet direct seulement (biaisé vers le bas)
model_med_sc2   = smf.ols('log_rev_int ~ pub + panier_moyen', data=df_sc2).fit()

# Export CSV
df_sc2.to_csv('data/sc2_mediateur.csv', index=False)
print(f"Sc2 — Traités: {len(treated_ids_sc2)}/200 magasins")
print(f"Sc2 — ATT: {att_sc2_log*100:.1f}%  |  OLS sans médiateur: {model_naive_sc2.params['pub']*100:.1f}%  |  OLS avec panier_moyen: {model_med_sc2.params['pub']*100:.1f}%")
```

### DAG Cell
```python
# Source: sc1a DAG pattern (cell 18) extended to 4 nodes
# ─────────────────────────────────────────────
# Figure DAG — Scénario 2
# ─────────────────────────────────────────────

G_sc2 = nx.DiGraph()
G_sc2.add_edges_from([
    ('Pub', 'Nb visites'),
    ('Pub', 'Panier moyen'),
    ('Nb visites', 'Ventes'),
    ('Panier moyen', 'Ventes'),
])
pos_sc2 = {
    'Pub': (0, 0.5),
    'Nb visites': (1, 1),
    'Panier moyen': (1, 0),
    'Ventes': (2, 0.5),
}
color_map_sc2 = {
    'Pub': 'steelblue',
    'Ventes': 'seagreen',
    'Nb visites': 'darkorange',
    'Panier moyen': 'mediumpurple',
}
node_colors_sc2 = [color_map_sc2[n] for n in G_sc2.nodes()]

fig, ax = plt.subplots(figsize=(6, 3.5))
nx.draw_networkx(G_sc2, pos_sc2, ax=ax,
                 node_color=node_colors_sc2,
                 node_size=2000, font_size=9, font_color='white',
                 arrows=True, arrowsize=20)
ax.axis('off')
ax.set_title('DAG — Scénario 2 : deux chemins causaux via médiateurs')
fig.savefig('figures/sc2_dag.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## Empirical Results (SEED=42, verified by simulation)

| Metric | Value | Notes |
|--------|-------|-------|
| Treated stores | 100/200 | Random 50% assignment, balanced |
| ATT_sc2_log | 30.0% | True effect, contrefactual method |
| OLS sans médiateur | 30.8% | Correct — unbiased with random assignment |
| OLS avec panier_moyen | 21.1% | Biased downward by ~9pp |
| Bias magnitude | -8.96pp | Pedagogically very visible (-31% vs OLS sans) |
| panier_moyen NaN count | 0 | No NaN in DGP with current PARAMS |

**Theoretical decomposition of the total effect:**
- Total causal effect ≈ `log(p_visite_pub1 / p_visite_pub0) + log(mu_panier_pub1 / mu_panier_pub0)`
- ≈ `log(0.55/0.45) + log(1.10)` ≈ 20.1% + 9.5% ≈ 29.6% (matches ATT=30.0%)
- Controlling on `panier_moyen` blocks the panier path (~9.5pp), leaving only the nb_visites path (~20%)
- This explains why OLS avec médiateur ≈ 21% ≈ nb_visites path only

**Interpretation:** Both EFFET_PUB_VISITES and EFFET_PUB_PANIER=0.10 contribute roughly equally in log-points. The mediator control removes ~30% of the apparent effect — clearly visible to students.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| DV = ventes (€) | DV = log(ventes/n_potentiel) | Phase 3 refactoring (2026-03-04) | Suppresses store size effect, interprets in % |
| OLS naïf = no controls | OLS naïf in sc2 = no mediator (= correct) | sc2 specific | Terminology must change: "naïf" means different things |
| 3-node DAG (confondant→pub, confondant→ventes, pub→ventes) | 4-node DAG (pub→mediator1→ventes, pub→mediator2→ventes) | sc2 specific | No confounders, no direct pub→ventes edge |

---

## Open Questions

1. **Should `C(mois)` be added to sc2 OLS formulas?**
   - What we know: With random pub assignment, seasonality is NOT a confounder; both models give identical `pub` coefficient with or without `C(mois)` (empirically verified: 30.77% both ways)
   - What's unclear: Whether the formateur prefers the simpler `log_rev_int ~ pub` or wants `C(mois)` for consistency with sc1a
   - Recommendation: Omit `C(mois)` — simplicity makes the mediator bias more transparent. The contrast with sc1 (where `C(mois)` was needed) is itself pedagogical.

2. **DAG node positioning — final `pos` coordinates**
   - What we know: Pattern from sc1x uses integer coordinates (0,0), (1,1), (2,0)
   - What's unclear: Exact layout for 4 nodes that renders well with `figsize=(6, 3.5)`
   - Recommendation: Use `Pub=(0, 0.5), Nb visites=(1, 1), Panier moyen=(1, 0), Ventes=(2, 0.5)` — diamond shape, tested conceptually. Adjust figsize if labels overlap.

---

## Sources

### Primary (HIGH confidence)
- `formation_causalite.ipynb` cells 1-30 — DGP code, PARAMS, sc1a/sc1b/sc1c patterns verified line by line
- Live Python simulation (SEED=42) — empirical ATT, OLS sans med, OLS avec med computed during this research session
- `.planning/phases/04-scenario2-mediateur/04-CONTEXT.md` — locked user decisions
- `.planning/REQUIREMENTS.md` — SC2-01, SC2-02, SC2-03 specifications

### Secondary (MEDIUM confidence)
- `.planning/phases/03-sc-narios-1a-1b-1c-biais-de-s-lection/03-01-SUMMARY.md` — Phase 3 decisions and empirical results
- `.planning/STATE.md` — project history and context

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already in notebook, no new deps
- Architecture: HIGH — cell structure directly derived from sc1a pattern, empirically simulated
- Empirical results: HIGH — computed live with SEED=42, exact notebook DGP replicated
- Pitfalls: HIGH — derived from code inspection and Phase 3 patterns

**Research date:** 2026-03-04
**Valid until:** 2026-04-03 (stable DGP — no external deps to update)
