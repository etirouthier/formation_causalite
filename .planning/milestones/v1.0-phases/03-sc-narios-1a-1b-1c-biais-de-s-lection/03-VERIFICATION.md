---
phase: 03-sc-narios-1a-1b-1c-biais-de-s-lection
verified: 2026-03-04T14:00:00Z
status: human_needed
score: 10/10 must-haves verified
human_verification:
  - test: "Ouvrir formation_causalite.ipynb dans Jupyter et inspecter visuellement les 9 figures (sc1a_dag, sc1a_coeff, sc1a_bar, sc1b_dag, sc1b_coeff, sc1b_bar, sc1c_dag, sc1c_coeff, sc1c_bar)"
    expected: "DAGs : 3 noeuds colorés (bleu/vert/orange), flèches bien orientées (Confondant→Pub, Confondant→Ventes, Pub→Ventes), layout non-superposé. Coefficient plots : OLS naïf (rouge) à droite de ATT (vert), barres d'erreur IC95% visibles. Bar charts : barre rouge la plus haute, ligne pointillée à ATT."
    why_human: "Qualité visuelle des figures (layout, lisibilité, absence de superposition de noeuds) ne peut pas être vérifiée programmatiquement"
  - test: "Vérifier les axes et titres des figures coeff/bar pour les 3 scénarios"
    expected: "Axe x libellé 'Uplift log des ventes (≈ %)' ou similaire — confirme que le refactoring DV log_rev_int se reflète dans les labels des figures exportées"
    why_human: "Le contenu textuel des axes est embarqué dans les PNG — non extractible sans OCR"
  - test: "SC1-03 dans REQUIREMENTS.md est encore marqué [ ] unchecked et la table Traceability affiche 'Pending' pour SC1-01/02/03"
    expected: "Après vérification que l'implémentation est correcte, mettre à jour REQUIREMENTS.md : SC1-03 → [x], et les 3 lignes Traceability SC1-01/02/03 → Complete (03-01)/(03-01)/(03-02)"
    why_human: "La mise à jour de REQUIREMENTS.md est une action éditoriale qui doit être approuvée par le formateur avant modification"
---

# Phase 3: Scénarios 1a, 1b, 1c — Biais de sélection — Verification Report

**Phase Goal:** Le formateur peut montrer que comparer naïvement les groupes traités et non traités surestime l'effet de la pub quand un confondant détermine l'assignation au traitement
**Verified:** 2026-03-04T14:00:00Z
**Status:** human_needed
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| #  | Truth | Status | Evidence |
|----|-------|--------|----------|
| 1  | Scénario 1a: DAG 3 noeuds exporté `figures/sc1a_dag.png` | VERIFIED | Fichier présent (29K), `G_1a`, `sc1a_dag.png` dans notebook |
| 2  | Scénario 1a: OLS naïf surestime l'ATT — coeff et bar chart exportés | VERIFIED | Outputs notebook: ATT=28.4%, OLS naïf=48.5% (+71%), `sc1a_coeff.png` 48K, `sc1a_bar.png` 36K |
| 3  | Scénario 1b: DAG 3 noeuds exporté `figures/sc1b_dag.png` | VERIFIED | Fichier présent (29K), `G_1b`, `sc1b_dag.png` dans notebook |
| 4  | Scénario 1b: OLS naïf surestime l'ATT — coeff et bar chart exportés | VERIFIED | Outputs notebook: ATT=28.3%, OLS naïf=43.9% (+55%), `sc1b_coeff.png` 50K, `sc1b_bar.png` 35K |
| 5  | Scénario 1c: DAG 3 noeuds exporté `figures/sc1c_dag.png` | VERIFIED | Fichier présent (29K), `G_1c`, `sc1c_dag.png` dans notebook |
| 6  | Scénario 1c: OLS naïf (sans C(mois)) surestime l'ATT — biais saisonnier visible | VERIFIED | Outputs notebook: ATT=29.4%, OLS naïf=38.0% (+8.6pp), formula `'log_rev_int ~ pub'` confirmée |
| 7  | OLS ajusté 1c avec C(mois) converge vers ATT | VERIFIED | Output: OLS ajusté=30.7%, ATT=29.4% — delta 1.3pp, dans IC 95% |
| 8  | 3 CSV exportés: sc1a, sc1b, sc1c | VERIFIED | Fichiers présents: sc1a 430K, sc1b 431K, sc1c 434K (tous régénérés 2026-03-04) |
| 9  | RNG locaux dédiés — rng global non pollué | VERIFIED | Seeds: rng_sc1a=SEED+10, cf=SEED+11; rng_sc1b=SEED+20, cf=SEED+21; rng_sc1c=SEED+30, cf=SEED+31 |
| 10 | DV = log_rev_int = log(ventes/n_potentiel), coefficients en log-points | VERIFIED | `df_sc1a['log_rev_int'] = np.log(df_sc1a['ventes'] / df_sc1a['n_potentiel'])` — pattern identique pour 1b et 1c |

**Score:** 10/10 truths verified

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `figures/sc1a_dag.png` | DAG Scénario 1a | VERIFIED | 29K, présent, savefig avant plt.show() confirmé |
| `figures/sc1a_coeff.png` | Coefficient plot Scénario 1a | VERIFIED | 48K, présent |
| `figures/sc1a_bar.png` | Bar chart Scénario 1a | VERIFIED | 36K, présent |
| `figures/sc1b_dag.png` | DAG Scénario 1b | VERIFIED | 29K, présent |
| `figures/sc1b_coeff.png` | Coefficient plot Scénario 1b | VERIFIED | 50K, présent |
| `figures/sc1b_bar.png` | Bar chart Scénario 1b | VERIFIED | 35K, présent |
| `figures/sc1c_dag.png` | DAG Scénario 1c | VERIFIED | 29K, présent |
| `figures/sc1c_coeff.png` | Coefficient plot Scénario 1c | VERIFIED | 59K, présent |
| `figures/sc1c_bar.png` | Bar chart Scénario 1c | VERIFIED | 44K, présent |
| `data/sc1a_selection_qualite.csv` | Dataset scénario 1a | VERIFIED | 430K, présent, col. `log_rev_int` incluse |
| `data/sc1b_selection_urbain.csv` | Dataset scénario 1b | VERIFIED | 431K, présent |
| `data/sc1c_selection_saison.csv` | Dataset scénario 1c | VERIFIED | 434K, présent |
| `formation_causalite.ipynb` | Notebook 31 cellules | VERIFIED | 31 cellules confirmées |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| code-sc1a-data | compute_outcomes | `compute_outcomes(df_sc1a, PARAMS, rng_sc1a)` | WIRED | Appel direct confirmé dans notebook |
| code-sc1a-data | smf.ols | `'log_rev_int ~ pub + C(mois)'` (naïf) + `'log_rev_int ~ pub + qualite_equipe + C(mois)'` (ajusté) | WIRED | Deux appels confirmés — confondant inclus seulement dans ajusté |
| code-sc1b-data | compute_outcomes | `compute_outcomes(df_sc1b, PARAMS, rng_sc1b)` | WIRED | Appel direct confirmé |
| code-sc1b-data | smf.ols | `'log_rev_int ~ pub + C(mois)'` (naïf) + `'log_rev_int ~ pub + urbain + C(mois)'` (ajusté) | WIRED | Deux appels confirmés |
| code-sc1c-data | rng_sc1c.binomial | `probs_1c = np.where(haute_mask, P_PUB_HAUTE_SAISON, P_PUB_BASSE_SAISON)` + assignation niveau ligne | WIRED | Haute_mask basé sur `effet_saison_val > 0`, pas de drop_duplicates — architecture niveau ligne confirmée |
| code-sc1c-data | model_naive_1c | `'log_rev_int ~ pub'` SANS C(mois) | WIRED | Exception structurelle confirmée — biais saisonnier rendu visible par l'omission |
| code-sc1c-data | model_adj_1c | `'log_rev_int ~ pub + C(mois)'` | WIRED | Contrôle saisonnier confirmé |
| coeff plots | ci.conf_int() | `ci.loc['pub', 0]` / `ci.loc['pub', 1]` (indices entiers) | WIRED | Pattern statsmodels 0.14.6 correct — pas `['lower']`/`['upper']` |
| bar charts | ATT + OLS | `att_1a_log`, `coef_naive_1a`, `coef_adj_1a` consommés dans `values_1a` | WIRED | Variables reliant calcul et visualisation confirmées |

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| SC1-01 | 03-01-PLAN.md | Scénario 1a: DAG + coeff plot + bar chart, OLS naïf vs ajusté vs valeur vraie | SATISFIED | 3 PNG présents, outputs: ATT=28.4%, OLS naïf=48.5%, surestimation +71% confirmée |
| SC1-02 | 03-01-PLAN.md | Scénario 1b: DAG + coeff plot + bar chart, OLS naïf vs ajusté vs valeur vraie | SATISFIED | 3 PNG présents, outputs: ATT=28.3%, OLS naïf=43.9%, surestimation +55% confirmée |
| SC1-03 | 03-02-PLAN.md | Scénario 1c: DAG + coeff plot + bar chart, OLS naïf vs ajusté vs valeur vraie | SATISFIED | 3 PNG présents, outputs: ATT=29.4%, OLS naïf=38.0%, biais saisonnier +8.6pp confirmé. **Note: REQUIREMENTS.md marque encore `[ ]` unchecked — mise à jour éditoriale requise** |

**Note critique sur REQUIREMENTS.md:** Le fichier `.planning/REQUIREMENTS.md` n'a pas été mis à jour lors de la completion de la phase :
- Ligne 36: SC1-03 affiche `- [ ]` (devrait être `- [x]`)
- Lignes 93-95: Traceability table affiche "Pending" pour SC1-01/02/03 (devraient afficher "Complete (03-01)" / "Complete (03-01)" / "Complete (03-02)")
- SC1-01 et SC1-02 sont correctement marqués `[x]` dans la liste principale mais la table Traceability les dit encore "Pending"

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| *(aucun)* | — | — | — | — |

Analyse exhaustive :
- Aucun commentaire `TODO`/`FIXME`/`PLACEHOLDER` trouvé
- Aucun `return null`/`return {}`/`return []` dans les cellules de scénario
- `node_colors = [color_map[n] for n in G.nodes()]` — pattern correct (pas de liste littérale)
- `fig.savefig(...)` avant `plt.show()` confirmé pour les 9 figures (sc1a/1b/1c × dag/coeff/bar)
- `ci.loc['pub', 0]` et `ci.loc['pub', 1]` — accès correct par index entier pour statsmodels 0.14.6
- `xerr = [[coef - lower], [upper - coef]]` — distances positives confirmées

---

### Human Verification Required

#### 1. Validation visuelle des 9 figures

**Test:** Ouvrir `formation_causalite.ipynb` dans Jupyter (ou inspecter les PNG dans `figures/`) et vérifier les 9 figures exportées.

**Expected:**
- DAGs (sc1a_dag, sc1b_dag, sc1c_dag) : 3 noeuds colorés (bleu=Pub, vert=Ventes, orange=Confondant), flèches correctement orientées (Confondant→Pub, Confondant→Ventes, Pub→Ventes), layout sans superposition, titre factuel
- Coefficient plots (sc1a_coeff, sc1b_coeff, sc1c_coeff) : 3 points sur axe Y (OLS naïf rouge en haut, OLS ajusté bleu au milieu, ATT vert en bas), barres d'erreur IC95% sur OLS naïf et ajusté, ligne pointillée verticale à ATT, OLS naïf clairement à droite de ATT
- Bar charts (sc1a_bar, sc1b_bar, sc1c_bar) : 3 barres colorées (rouge > bleu ≈ vert), ligne pointillée horizontale à ATT, axe Y libellé "Uplift log des ventes (≈ %)"

**Why human:** Qualité visuelle, lisibilité, absence de superposition de noeuds dans les DAGs, et cohérence des labels d'axes ne peuvent pas être vérifiées programmatiquement sur des PNG.

#### 2. Mise à jour REQUIREMENTS.md

**Test:** Confirmer que l'implémentation de SC1-03 est correcte, puis mettre à jour `.planning/REQUIREMENTS.md`.

**Expected:** Trois modifications :
1. Ligne 36: `- [ ] **SC1-03**` → `- [x] **SC1-03**`
2. Ligne 93: `SC1-01 | Phase 3 | Pending` → `SC1-01 | Phase 3 | Complete (03-01)`
3. Ligne 94: `SC1-02 | Phase 3 | Pending` → `SC1-02 | Phase 3 | Complete (03-01)`
4. Ligne 95: `SC1-03 | Phase 3 | Pending` → `SC1-03 | Phase 3 | Complete (03-02)`

**Why human:** Cette mise à jour documentaire doit être approuvée par le formateur avant application — c'est la confirmation que le contenu pédagogique est validé, pas seulement que le code tourne.

---

### Empirical Bias Summary (Confirmed from Notebook Cell Outputs)

| Scénario | Confondant | Mécanisme | ATT_log | OLS naïf | OLS ajusté | Biais |
|----------|-----------|-----------|---------|----------|------------|-------|
| 1a | qualite_equipe | Niveau magasin, constant | 28.4% | 48.5% | 28.3% | +71% surestimation |
| 1b | urbain | Niveau magasin, constant | 28.3% | 43.9% | 32.0% | +55% surestimation |
| 1c | saison (effet_saison_val) | Niveau ligne, varie par mois | 29.4% | 38.0% | 30.7% | +8.6pp surestimation |

Le biais est dans la bonne direction (OLS naïf > ATT) pour les 3 scénarios. L'OLS ajusté converge vers ATT dans tous les cas. La démonstration pédagogique est fonctionnelle.

---

### Architectural Notes

**Refactoring DV:** Le PLAN 03-01 original spécifiait `ventes ~` dans les formules OLS. Le SUMMARY 03-01 documente le refactoring vers `log_rev_int = log(ventes/n_potentiel)` effectué dans le commit `afee35f`. L'implémentation réelle utilise `log_rev_int` — c'est une amélioration architecturale approuvée par le formateur (documentée dans PAUSE.md). Les must_haves sont satisfaits avec la DV refactorisée.

**Scénario 1c — Exception structurelle confirmée:** L'OLS "naïf" de 1c est `'log_rev_int ~ pub'` SANS `C(mois)` — contrairement à 1a/1b où le naïf inclut `C(mois)`. C'est intentionnel : l'omission des dummies mois est ce qui rend le biais saisonnier visible. L'OLS "ajusté" de 1c est `'log_rev_int ~ pub + C(mois)'`.

---

### Gaps Summary

Aucune lacune fonctionnelle. Tous les artefacts sont présents, substantiels et correctement câblés. Le seul item ouvert est la validation visuelle des figures (qualité pédagogique) qui requiert un humain, et la mise à jour documentaire de REQUIREMENTS.md (SC1-03 et table Traceability).

---

_Verified: 2026-03-04T14:00:00Z_
_Verifier: Claude (gsd-verifier)_
