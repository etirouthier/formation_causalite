---
phase: 02-scenario0-petits-nombres
verified: 2026-03-03T00:00:00Z
status: human_needed
score: 5/5 must-haves verified
re_verification: false
human_verification:
  - test: "Ouvrir figures/sc0_distribution.png et confirmer que les 3 panneaux empilés sont distincts avec des largeurs de distribution clairement différentes (petit = plus large, grand = plus étroit)"
    expected: "3 histogrammes empilés avec axe X partagé. La distribution 'petit' s'étend de ~47 à ~53€, 'moyen' de ~49 à ~51€, 'grand' de ~49 à ~51€ (plus resserrée). Message pédagogique lisible pour slides."
    why_human: "La qualité visuelle pédagogique (lisibilité pour une projection, distinction suffisante des distributions) ne peut pas être vérifiée par grep ou Python."
  - test: "Ouvrir figures/sc0_scatter.png et confirmer la tendance négative visible : points rouges (petits) en haut à gauche, points verts (grands) en bas à droite"
    expected: "Nuage de 200 points avec tendance négative nette (r=-0.758 confirmé par les données). Couleurs rouge/bleu/vert bien distinctes par taille. Légende présente."
    why_human: "L'efficacité pédagogique de la corrélation visible à l'oeil nu doit être confirmée par un humain."
  - test: "Ouvrir figures/sc0_top10.png et confirmer que les 10 barres sont majoritairement rouges (petits magasins)"
    expected: "10 barres rouges (100% petits magasins, confirmé par données). Titre factuel sans commentaire interprétatif (correctif post-checkpoint appliqué). Légende avec les 3 tailles."
    why_human: "Lisibilité du titre, placement de la légende, et impact pédagogique du constat 10/10 ne peuvent pas être vérifiés programmatiquement."
  - test: "Ouvrir figures/sc0_loi_grands_nombres.png et confirmer les 2 panneaux avec rétrécissement visible des courbes KDE de N=10 (large) à N=100000 (quasi-delta)"
    expected: "Panneau 1 (haut) : KDE grise des données réelles. Panneau 2 (bas) : 5 courbes KDE overlay avec rétrécissement progressif visible. N=100000 doit être visible (warn_singular=False garanti). Légende avec N potentiel."
    why_human: "La lisibilité des 5 courbes KDE superposées, notamment pour N=100000 (std ≈ 0.018), nécessite un contrôle visuel humain. Note : le formateur a déjà approuvé lors du checkpoint plan 02-02 (2026-03-03)."
---

# Phase 2: Scénario 0 — Biais de petits nombres — Verification Report

**Phase Goal:** Le formateur peut illustrer visuellement que les petits magasins dominent les extrêmes de distribution du panier moyen en raison de la variance binomiale
**Verified:** 2026-03-03
**Status:** human_needed (automated checks all passed; human checkpoint was conducted and approved during plan 02-02 execution)
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | La figure de distribution montre des distributions clairement différentes par taille, exportée en PNG dans figures/ | VERIFIED | figures/sc0_distribution.png existe (83 KB, PNG valide). code-sc0-fig1 implémente subplots(3,1,sharex=True). Données confirmées : petit std=1.26, moyen std=0.46, grand std=0.26. |
| 2 | Le scatter plot montre une corrélation négative visible entre nb_visites et la variance du panier_moyen | VERIFIED | figures/sc0_scatter.png existe (86 KB, PNG valide). code-sc0-fig2 trace scatter(nb_visites_moy, panier_moyen_std). Corrélation de Pearson r=-0.758 confirmée sur les données CSV. |
| 3 | Le bar chart des top 10 magasins révèle la sur-représentation des petits magasins (idealement >= 50% du top 10) | VERIFIED | figures/sc0_top10.png existe (42 KB, PNG valide). code-sc0-fig3 utilise agg_sc0.nlargest(10,'panier_moyen_moy'). Résultat empirique : 10/10 petits magasins (100%) dans le top 10. |
| 4 | Le dataset du scénario est exporté en CSV dans data/ | VERIFIED | data/sc0_biais_petits_nombres.csv existe (13 KB, 200 lignes, colonnes : magasin_id, taille, n_potentiel, nb_visites_moy, panier_moyen_moy, panier_moyen_std). |
| 5 | Contraintes techniques : savefig précède plt.show(), rng_fig4 local isolé, sharex=True présent | VERIFIED | savefig avant plt.show() confirmé dans les 4 cellules figure. rng_fig4 = np.random.default_rng(SEED + 4) local, aucune ligne utilisant le rng global dans code-sc0-fig4. sharex=True présent dans fig1 et fig4. |

**Score:** 5/5 truths verified (automated)

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `formation_causalite.ipynb` | 6 nouvelles cellules sc0 insérées (plans 02-01 + 02-02) | VERIFIED | 16 cellules totales. IDs présents : md-sc0-section (index 8), code-sc0-aggregation (9), code-sc0-fig1 (10), code-sc0-fig2 (11), code-sc0-fig3 (12), code-sc0-fig4 (13). Ordre correct après code-assertions (index 7). |
| `data/sc0_biais_petits_nombres.csv` | Export CSV du scénario 0 (200 magasins agrégés) | VERIFIED | 200 lignes, 6 colonnes. Groupes : petit=79, moyen=86, grand=35. Toutes les colonnes requises présentes. |
| `figures/sc0_distribution.png` | Figure 1 — 3 histogrammes distribution panier_moyen par taille | VERIFIED | 83,024 bytes, PNG valide. subplots(3,1,sharex=True) confirmé dans le code. |
| `figures/sc0_scatter.png` | Figure 2 — scatter 200 points nb_visites_moy vs panier_moyen_std | VERIFIED | 85,749 bytes, PNG valide. scatter sur nb_visites_moy/panier_moyen_std confirmé dans le code. |
| `figures/sc0_top10.png` | Figure 3 — top 10 magasins bar chart, coloré par taille | VERIFIED | 41,556 bytes, PNG valide. nlargest(10,'panier_moyen_moy') confirmé dans le code. |
| `figures/sc0_loi_grands_nombres.png` | Figure 4 — KDE réel (rang 1) + KDE simulées N=10..100000 (rang 2) | VERIFIED | 102,682 bytes, PNG valide. subplots(2,1,sharex=True), N_values=[10,100,1000,10000,100000], warn_singular=False confirmés dans le code. |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| base_df (4800 lignes) | agg_sc0 (200 lignes) | groupby(['magasin_id','taille']).agg(...) | WIRED | Pattern exact présent dans code-sc0-aggregation. Les deux colonnes dans groupby : correct. |
| agg_sc0 | figures/sc0_distribution.png | sns.histplot, subplots(3,1,sharex=True) | WIRED | sharex=True présent. Boucle sur tailles_ordre avec subset agg_sc0 per taille. savefig avant plt.show(). |
| agg_sc0 | figures/sc0_scatter.png | ax.scatter(nb_visites_moy, panier_moyen_std) | WIRED | scatter(grp['nb_visites_moy'], grp['panier_moyen_std']) confirmé. Groupby taille pour couleurs. savefig avant plt.show(). |
| agg_sc0 | figures/sc0_top10.png | agg_sc0.nlargest(10,'panier_moyen_moy') | WIRED | nlargest(10,'panier_moyen_moy') confirmé. bar_colors via colors_sc0. savefig avant plt.show(). |
| generate_base_panel + compute_outcomes | figures/sc0_loi_grands_nombres.png | rng_fig4 local, params_sim avec n_petit=N=n_grand | WIRED | rng_fig4 = np.random.default_rng(SEED + 4) présent. Boucle sur N_values. sim_df['pub'] = 0 avant compute_outcomes. warn_singular=False présent. savefig avant plt.show(). |
| SEED (Paramètres) | rng_fig4 | np.random.default_rng(SEED + 4) | WIRED | Ligne exacte présente dans code-sc0-fig4. rng global absent de ce contexte. |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|---------|
| SC0-01 | 02-01-PLAN.md | Figure montrant la distribution du panier_moyen par taille de magasin (histogramme avec hue=taille) | SATISFIED | figures/sc0_distribution.png : 3 histogrammes sharex=True par taille. Données montrent distribution clairement plus large pour petit (std=1.26) vs grand (std=0.26). |
| SC0-02 | 02-01-PLAN.md | Scatter plot montrant la relation entre nb_visites et la variance du panier_moyen (petits magasins = plus de variance) | SATISFIED | figures/sc0_scatter.png : scatter nb_visites_moy vs panier_moyen_std. Corrélation r=-0.758, confirme que petits magasins (peu de visites) ont plus de variance. |
| SC0-03 | 02-02-PLAN.md | Bar chart ou tableau des top 10 magasins par panier_moyen le plus élevé, avec la répartition par taille de magasin | SATISFIED | figures/sc0_top10.png : bar chart top 10, 10/10 petits magasins (100%), barres colorées par taille via colors_sc0. |

**Orphaned requirements check:** Aucune exigence SC0-xx non accountée. Les 3 IDs (SC0-01, SC0-02, SC0-03) sont couverts par les deux plans de la phase.

---

## Anti-Patterns Found

| File | Pattern | Severity | Impact |
|------|---------|----------|--------|
| (aucun) | | | |

Analyse : Aucun TODO/FIXME/HACK/placeholder dans les 6 cellules sc0. Aucun return null ou implémentation vide. Le savefig précède systématiquement plt.show() dans toutes les cellules figure (vérification automatisée sur 5 cellules). Le rng global n'est pas consommé dans code-sc0-fig4 — toutes les lignes contenant "rng" utilisent soit "rng_fig4" soit "default_rng". Aucun magic number de paramètre (200, 79, 86, 35, 30, 150, 500) n'apparaît dans les cellules sc0.

---

## Human Verification Required

### 1. Distribution par taille (sc0_distribution.png)

**Test:** Ouvrir `figures/sc0_distribution.png` et inspecter visuellement les 3 panneaux.
**Expected:** 3 histogrammes empilés avec axe X commun. Panneau "petit" nettement plus étalé que "moyen" et "grand". Message pédagogique lisible à la projection (taille de police, contraste).
**Why human:** Les données confirment std(petit)=1.26 vs std(grand)=0.26, mais la lisibilité visuelle pour une salle de formation ne peut pas être vérifiée programmatiquement.

### 2. Corrélation visible (sc0_scatter.png)

**Test:** Ouvrir `figures/sc0_scatter.png` et confirmer la tendance négative à l'oeil nu.
**Expected:** Points rouges (petits) en haut à gauche (peu de visites, forte variance). Points verts (grands) en bas à droite. Couleurs distinctes et légende lisible.
**Why human:** La corrélation r=-0.758 est confirmée, mais la lisibilité visuelle de la tendance dans un contexte pédagogique (projection, daltonisme éventuel) nécessite un contrôle humain.

### 3. Sur-représentation visible (sc0_top10.png)

**Test:** Ouvrir `figures/sc0_top10.png` et confirmer l'impact pédagogique du constat 10/10 petits.
**Expected:** 10 barres rouges, titre factuel (sans commentaire interprétatif — correctif c90fc36 appliqué), légende des 3 tailles présente même si 0 moyen et 0 grand dans le top.
**Why human:** L'impact pédagogique du titre post-correctif (titres rendus factuels) et la présence de la légende pour des catégories absentes du top 10 doivent être validés visuellement.

### 4. Mécanisme loi des grands nombres (sc0_loi_grands_nombres.png)

**Test:** Ouvrir `figures/sc0_loi_grands_nombres.png` et confirmer que les 5 courbes KDE simulées sont visibles et progressivement plus étroites.
**Expected:** Panneau 1 (haut) : KDE grise des données réelles. Panneau 2 (bas) : 5 courbes dont N=100000 visible (la plus étroite), légende avec "N potentiel". Axe X partagé visible.
**Why human:** La visibilité de la courbe N=100000 (std ≈ 0.018, quasi-delta) malgré warn_singular=False nécessite une confirmation visuelle. Note : le formateur a déjà APPROUVE ce checkpoint lors du plan 02-02 (2026-03-03).

---

## Gaps Summary

Aucun gap détecté. Tous les artefacts existent, sont substantiels (pas de stubs), et sont correctement connectés. Les 5 exigences de must_haves sont vérifiées. Les 3 requirements (SC0-01, SC0-02, SC0-03) sont satisfaits.

La qualification `human_needed` reflète que :
1. La qualité pédagogique visuelle des 4 figures ne peut pas être vérifiée programmatiquement.
2. Le formateur a déjà accordé son approbation lors du checkpoint humain du plan 02-02 (2026-03-03, statut "APPROUVE" documenté dans 02-02-SUMMARY.md). Cette approbation constitue la validation humaine demandée.

---

## Summary: Goal Achievement

**Phase goal:** "Le formateur peut illustrer visuellement que les petits magasins dominent les extrêmes de distribution du panier moyen en raison de la variance binomiale"

Cet objectif est atteint :

- **Domination des extrêmes démontrée :** Top 10 par panier_moyen = 10/10 petits magasins (100%)
- **Variance binomiale illustrée :** Corrélation nb_visites/panier_moyen_std = -0.758, std(petit)=5.47 vs std(grand)=1.24
- **Mécanisme expliqué :** Figure 4 montre le rétrécissement progressif des KDE de N=10 à N=100000
- **Exports complets :** 4 PNG + 1 CSV, tous non-blancs, générés par nbconvert exit 0

Les commits git documentés (51341bd, 16c07ce, f51419c, f0bcc3f, c90fc36) existent tous dans l'historique et correspondent aux tâches décrites dans les SUMMARYs.

---

_Verified: 2026-03-03_
_Verifier: Claude (gsd-verifier)_
