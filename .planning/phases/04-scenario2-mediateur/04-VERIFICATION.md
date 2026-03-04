---
phase: 04-scenario2-mediateur
verified: 2026-03-04T14:30:00Z
status: passed
score: 6/6 must-haves verified
re_verification: false
---

# Phase 4: Scénario 2 — Surcontrôle sur un médiateur — Verification Report

**Phase Goal:** Le formateur peut montrer que contrôler sur `panier_moyen` dans la régression biaise le coefficient de `pub` vers zéro car `panier_moyen` est un médiateur
**Verified:** 2026-03-04T14:30:00Z
**Status:** PASSED
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #  | Truth                                                                                                                               | Status     | Evidence                                                                                         |
|----|-------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------------------------------------------------------------------------------------|
| 1  | DAG 4 noeuds (Pub, Nb visites, Panier moyen, Ventes) en diamond layout, sans arête directe Pub→Ventes, exporté figures/sc2_dag.png | VERIFIED   | Cell 33 edges: Pub→Nb visites, Pub→Panier moyen, Nb visites→Ventes, Panier moyen→Ventes. No ('Pub','Ventes') in cells 31-35. File: 41587 bytes, 840×466px RGBA |
| 2  | OLS sans médiateur (~30.8%) > OLS avec panier_moyen (~21.1%) — biais vers le bas visible et quantifié (-9.7pp)                     | VERIFIED   | Cell 32 output: "ATT: 30.0% \| OLS sans médiateur: 30.8% \| OLS avec panier_moyen: 21.1%" (SEED=42) |
| 3  | Bar chart compare 3 estimateurs : OLS sans médiateur (rouge), OLS avec médiateur (bleu), Valeur vraie ATT (vert)                   | VERIFIED   | Labels 'OLS sans médiateur', 'OLS avec panier_moyen', 'Valeur vraie (ATT)'; colors #e74c3c, #3498db, #2ecc71. figures/sc2_bar.png: 42263 bytes, 940×564px |
| 4  | ATT contrefactuel calculé avec rng_cf_sc2 = np.random.default_rng(SEED+41), isolé du rng_sc2 (SEED+40)                            | VERIFIED   | Both seeds present in cell 32; att_sc2_log computed as (log_Y1_sc2 - log_Y0_sc2).mean()         |
| 5  | CSV exporté data/sc2_mediateur.csv                                                                                                  | VERIFIED   | File exists: 442058 bytes, 4800 rows × 13 columns (magasin_id, taille, urbain, qualite_equipe, n_potentiel, mois, effet_saison_val, p_visite, nb_visites, ventes, panier_moyen, pub, log_rev_int) |
| 6  | Notebook s'exécute de bout en bout (nbconvert exit 0) avec 36 cellules au total                                                     | VERIFIED   | len(nb['cells']) == 36; cell outputs present across all sc2 cells; SUMMARY confirms nbconvert exit 0 |

**Score:** 6/6 truths verified

### Required Artifacts

| Artifact                   | Expected                               | Status     | Details                                          |
|----------------------------|----------------------------------------|------------|--------------------------------------------------|
| `figures/sc2_dag.png`      | DAG Scénario 2 — deux chemins médiateurs | VERIFIED | 41587 bytes, 840×466px RGBA, timestamp 13:59 Mar 4 |
| `figures/sc2_coeff.png`    | Coefficient plot Scénario 2            | VERIFIED   | 62164 bytes, 1269×593px RGBA, timestamp 13:59 Mar 4 |
| `figures/sc2_bar.png`      | Bar chart Scénario 2                   | VERIFIED   | 42263 bytes, 940×564px RGBA, timestamp 13:59 Mar 4 |
| `data/sc2_mediateur.csv`   | Dataset scénario 2                     | VERIFIED   | 442058 bytes, 4800 rows, 13 columns, pub balance 2400/2400 |
| `formation_causalite.ipynb` | 36 cellules, sc2 cells 31-35 insérées | VERIFIED   | 36 cells total; cells 31 (markdown) + 32-35 (code) present with outputs |

### Key Link Verification

| From             | To                     | Via                                                     | Status   | Details                                                             |
|------------------|------------------------|---------------------------------------------------------|----------|---------------------------------------------------------------------|
| code-sc2-data    | df_sc2['pub']          | rng_sc2.binomial(1, 0.5, size=...) niveau magasin      | WIRED    | `rng_sc2.binomial(1, 0.5` present in cell 32; drop_duplicates confirmed |
| code-sc2-data    | model_naive_sc2        | OLS 'log_rev_int ~ pub' (sans médiateur = effet total)  | WIRED    | `'log_rev_int ~ pub'` in cell 32; model fitted and coeff extracted in cell 34 |
| code-sc2-data    | model_med_sc2          | OLS 'log_rev_int ~ pub + panier_moyen' (biaisé)         | WIRED    | `'log_rev_int ~ pub + panier_moyen'` in cell 32; coeff extracted in cell 34 |
| code-sc2-coeff   | att_sc2_log            | (log_Y1_sc2 - log_Y0_sc2).mean()                        | WIRED    | att_sc2_log computed in cell 32 with rng_cf_sc2=SEED+41; used in cells 34 and 35 |

### Requirements Coverage

| Requirement | Source Plan | Description                                                                                                       | Status    | Evidence                                                                                                  |
|-------------|-------------|-------------------------------------------------------------------------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------|
| SC2-01      | 04-01-PLAN  | DAG causal illustrant les deux chemins (pub→nb_visites→ventes ET pub→panier_moyen→ventes)                        | SATISFIED | Cell 33: G_sc2 with 4 nodes, 4 edges (Pub→Nb visites, Pub→Panier moyen, Nb visites→Ventes, Panier moyen→Ventes). No direct Pub→Ventes. Diamond layout confirmed. |
| SC2-02      | 04-01-PLAN  | Coefficient plot montrant comment le coefficient pub change avec panier_moyen comme contrôle                      | SATISFIED | Cell 34: errorbar plot with coef_naive_sc2 (30.8%) vs coef_med_sc2 (21.1%) vs att_sc2_log (30.0%). figures/sc2_coeff.png exported. |
| SC2-03      | 04-01-PLAN  | Bar chart comparant effet sans contrôle (correct) vs avec contrôle médiateur (biaisé) vs valeur vraie            | SATISFIED | Cell 35: bar chart with labels 'OLS sans médiateur', 'OLS avec panier_moyen', 'Valeur vraie (ATT)'. figures/sc2_bar.png exported. |

No orphaned requirements: REQUIREMENTS.md maps SC2-01, SC2-02, SC2-03 to Phase 4 (Complete 04-01) — all three claimed and verified.

### Anti-Patterns Found

| File                         | Line | Pattern                  | Severity | Impact  |
|------------------------------|------|--------------------------|----------|---------|
| formation_causalite.ipynb    | —    | None found in sc2 cells  | —        | —       |

Checked sc2 cells 31-35:
- No `TODO`/`FIXME`/`PLACEHOLDER` comments
- No `return null`/`return {}`/`return []`
- No empty handlers
- No `C(mois)` in OLS formulas (correctly absent — aléatoire, no seasonal confounding)
- `fig.savefig(...)` precedes `plt.show()` in all three figure cells (cells 33, 34, 35)
- `node_colors_sc2` built dynamically (`[color_map_sc2[n] for n in G_sc2.nodes()]`) — not a literal list

Anti-pattern note: The full notebook contains `('Pub', 'Ventes')` in cells 18, 21, 28 — but these belong to sc1a, sc1b, sc1c DAGs respectively, where a Pub→Ventes edge is expected. The sc2 DAG (cells 31-35) has no such edge.

### Human Verification Required

#### 1. Visual clarity of DAG diamond layout

**Test:** Open `figures/sc2_dag.png`. Confirm Pub is left, Ventes right, Nb visites top-center, Panier moyen bottom-center. Arrows clearly show two separate paths from Pub to Ventes. No direct Pub→Ventes arrow visible.
**Expected:** Four colored nodes (steelblue Pub, seagreen Ventes, darkorange Nb visites, mediumpurple Panier moyen) with white font labels, two distinct causal paths.
**Why human:** Image rendering and label readability cannot be verified programmatically.

#### 2. Pedagogical contrast in coefficient plot

**Test:** Open `figures/sc2_coeff.png`. Confirm the OLS sans médiateur point (rouge, ~0.308) is clearly to the right of OLS avec panier_moyen (bleu, ~0.211), and close to ATT (vert, ~0.300). IC 95% bars visible. Vertical dashed line at ATT value.
**Expected:** Clear downward bias visible between red and blue points; green diamond approximately aligned with red dot, confirming the naive estimate is correct and the "sophisticated" model is biased.
**Why human:** Visual impression and pedagogical clarity cannot be verified programmatically.

#### 3. Bar chart communicates bias direction

**Test:** Open `figures/sc2_bar.png`. Confirm three bars: rouge (tallest, ~0.308), bleu (shortest, ~0.211), vert (ATT, ~0.300). Horizontal dashed line at ATT. X-axis labels readable.
**Expected:** The bar chart visually communicates that adding panier_moyen control deflates the estimate by ~9.7pp (-31% relative).
**Why human:** Visual readability and label clarity require human assessment.

### Gaps Summary

No gaps. All 6 must-have truths verified, all 4 key links wired, all 3 requirements (SC2-01, SC2-02, SC2-03) satisfied with implementation evidence. All output artifacts exist with substantive content. Computed values match expected results (SEED=42): ATT=30.0%, OLS sans=30.8%, OLS avec=21.1%, biais=-9.7pp.

---
_Verified: 2026-03-04T14:30:00Z_
_Verifier: Claude (gsd-verifier)_
