# Project Research Summary

**Project:** Formation Causalite — Notebook pedagogique d'inference causale
**Domain:** Python/Jupyter educational notebook — causal inference simulation
**Researched:** 2026-03-02
**Confidence:** MEDIUM

## Executive Summary

Ce projet est un notebook Jupyter pedagogique standalone destine aux formateurs francophones souhaitant enseigner les biais causaux courants (selection, surcontrole mediateur, surcontrole collider, biais de petits nombres) a travers un fil rouge unique : l'impact d'une campagne publicitaire sur les ventes de magasins. L'approche recommandee par la recherche est une architecture en 5 couches (Parametres → Generateur de base → Scenarios → Visualisation → Export), avec un generateur de donnees de panel N_magasins × T_mois partage entre tous les scenarios. Ce fil rouge commun est la cle differentiatrice : contrairement aux references anglophones existantes (Mixtape, The Effect), chaque scenario derive du meme DGP de base, ce qui permet des comparaisons directes de biais entre scenarios.

La pile technologique recommandee est mature et bien documentee : Python 3.11+, NumPy 2.x avec l'API `default_rng`, pandas 2.x, statsmodels pour les OLS avec erreurs standard, networkx pour les DAGs, et matplotlib/seaborn pour les figures. Les choix sont deliberement conservateurs — pas de widgets interactifs, pas de Streamlit, pas de graphviz — pour minimiser la friction d'installation sur la machine du formateur et garantir un `Run All` sans erreur.

Les risques principaux sont lies a la calibration des parametres plutot qu'a la technologie : un DGP mal calibre rend les biais pedagogiquement invisibles (collider sans effet observable, mediateur dont la voie 2 est negligeable, petits nombres avec variance trop faible). La prevention passe par des assertions de validation explicites dans le notebook lui-meme, et par des valeurs par defaut soigneusement choisies plutot qu'arbitraires.

## Key Findings

### Recommended Stack

La pile est construite autour de l'ecosysteme scientifique Python standard, sans dependances exotiques. NumPy 2.x avec `np.random.default_rng(SEED)` remplace l'API legacy (`np.random.seed()`) pour garantir la reproductibilite meme si les cellules sont executees hors ordre. statsmodels est prefere a scikit-learn pour les regressions car il produit des erreurs standard et p-values necessaires a la narration pedagogique. networkx remplace les outils specialises DAG (causalgraphicalmodels, graphviz) car il n'a pas de dependance systeme et permet un layout fixe et deterministe.

**Core technologies:**
- Python 3.11+ : runtime — LTS avec gains de performance substantiels vs 3.10
- NumPy 2.x : simulations stochastiques — `default_rng` obligatoire pour la reproductibilite
- pandas 2.x : panel DataFrame, groupby, export CSV — copy-on-write par defaut en 2.2+
- statsmodels 0.14+ : OLS avec formula API — seule option produisant SE et p-values
- networkx 3.x : DAGs programmatiques avec layout fixe — pas de dependance graphviz
- matplotlib 3.8+ / seaborn 0.13+ : figures PNG haute resolution pour les slides

### Expected Features

Tous les scenarios sont MVP (P1) : il n'y a pas de fonctionnalites a differer en v2 car le scope est deliberement restreint. Les anti-features (widgets, Streamlit, version R, refresh dynamique) sont activement exclues pour rester dans les limites d'un outil formateur simple.

**Must have (table stakes):**
- Cellule Parametres unique avec constantes ALL_CAPS — le formateur ne doit modifier qu'un seul endroit
- Seed de reproductibilite via `default_rng` — resultats identiques sur `Restart & Run All`
- Generateur de panel Binomial × Normal — cree naturellement le biais de petits nombres via la variance statistique
- Scenario 0 : biais de petits nombres — distribution du panier_moyen par taille de magasin
- Scenarios 1a/1b/1c : biais de selection — par equipe, localisation, saison
- Scenario 2 : surcontrole mediateur — changement de coefficient OLS lors de l'ajout de panier_moyen
- Scenario 3 : surcontrole collider — biais introduit par le controle sur posts_reseaux
- Export figures PNG vers `figures/` et donnees CSV vers `data/`

**Should have (competitive differentiators):**
- DAGs networkx avec layout fixe — cohence visuelle entre tous les scenarios
- Graphiques de comparaison des coefficients avec IC 95% — estimation naive vs correcte vs vraie valeur
- Valeur vraie connue affichee sur toutes les figures de regression — avantage pedagogique du DGP controle
- Narrative en francais — rare dans l'ecosysteme causal inference majoritairement anglophone

**Defer (v2+, si jamais):**
- Widgets interactifs ipywidgets — le formateur edite directement les parametres
- Effets heterogenes — hors scope pedagogique v1
- Interface web Streamlit/Dash — over-engineering pour usage formateur unique
- Version R — Python uniquement pour v1

### Architecture Approach

L'architecture en 5 couches separees assure que la cellule Parametres est la seule surface de modification pour le formateur, que le generateur de base est cree une seule fois et partage entre tous les scenarios (via des DataFrames derives, jamais via modification en place), et que chaque figure est une fonction independante avec export PNG integre. Cette separation garantit la coherence de l'effet vrai entre scenarios — le pitfall le plus silencieux et le plus damaging pour la pedagogie.

**Major components:**
1. Couche 1 — Parametres (cellule unique) : toutes les constantes ALL_CAPS, SEED, effets causaux vrais, probabilites de selection
2. Couche 2 — Generateur de base : `generate_base_panel(params, rng)` produit le panel N_magasins × T_mois partage
3. Couche 3 — Scenarios : chaque scenario derive `base_df.copy()` et assigne son propre mecanisme de traitement
4. Couche 4 — Visualisation : une fonction = une figure = un export PNG automatique
5. Couche 5 — Export : PNG vers `figures/`, CSV vers `data/`, dossiers crees au demarrage

### Critical Pitfalls

1. **DGP du collider mal calibre (Scenario 3)** — Si le bruit de `posts_reseaux` est trop faible, le biais du collider est invisible. Standardiser `ventes` avant de l'utiliser comme predicteur ; valider que le coefficient `pub` differe d'au moins 5% avec vs sans `posts_reseaux`.

2. **Biais du mediateur trop petit pour etre visible (Scenario 2)** — Calibrer les parametres pour que la voie `pub → panier_moyen → ventes` porte 30-40% de l'effet total. Ajouter une cellule de validation qui imprime la decomposition de l'effet et asserte que la voie 2 > 20%.

3. **Non-reproductibilite via l'API NumPy legacy** — `np.random.seed()` global est fragile si les cellules sont executees hors ordre. Utiliser exclusivement `rng = np.random.default_rng(SEED)` passe en argument, jamais en global.

4. **Probabilites de selection extremes detruisant l'overlap (Scenarios 1a/1b/1c)** — `P(pub|bonne_equipe) = 0.9` vs `0.1` cree un chevauchement quasi-nul et fait apparaitre l'estimateur ajuste comme "ne fonctionnant pas". Confondance moderee recommandee : 0.70 vs 0.30.

5. **Effet vrai incoherent entre scenarios** — Ajuster les parametres scenario par scenario casse la comparabilite. Un seul dictionnaire `PARAMS` partage ; chaque scenario modifie uniquement le mecanisme d'assignation, jamais les effets vrais.

6. **p_visite hors [0,1] avec parametres additifs** — L'accumulation d'effets positifs (urbain + equipe + saison + pub) peut depasser 1.0 et faire planter NumPy. `np.clip(p_visite, 0.01, 0.99)` obligatoire avant chaque `rng.binomial()`.

## Implications for Roadmap

La sequence de construction est dictee par les dependances : le generateur de base doit preceder tous les scenarios, et le Scenario 0 (le plus simple) sert de validation du DGP avant d'aborder les scenarios plus complexes. Les pitfalls critiques 3, 5, 6 sont fondationnaux et doivent etre resolus avant d'ecrire le premier scenario.

### Phase 1 : Fondations — Infrastructure et DGP de base

**Rationale:** Toutes les dependances partent de la cellule Parametres et du generateur de base. Les pitfalls les plus critiques (non-reproductibilite, effet vrai incoherent, p_visite hors [0,1]) doivent etre elimines avant d'ecrire un seul scenario.
**Delivers:** Notebook squelette avec cellule Parametres, imports, creation des dossiers, et `generate_base_panel()` valide.
**Addresses:** Infrastructure (cellule parametres, seed, export dossiers)
**Avoids:** Pitfall 3 (API NumPy legacy), Pitfall 5 (effet vrai incoherent), Pitfall 6 (p_visite hors [0,1])

### Phase 2 : Scenario 0 — Biais de petits nombres

**Rationale:** Le scenario le plus simple (pas d'OLS, pas de DAG complexe) sert de validation visuelle du DGP. Si la variance par taille est invisible ici, le DGP est mal calibre et il faut corriger avant d'aller plus loin.
**Delivers:** Figures de distribution du panier_moyen par taille de magasin + export PNG/CSV
**Uses:** seaborn.histplot/violinplot, pandas groupby
**Avoids:** Pitfall de calibration (ratio de taille N_petit vs N_grand insuffisant — minimum 10-20x recommande)

### Phase 3 : Scenarios 1a/1b/1c — Biais de selection

**Rationale:** Les trois scenarios de selection partagent le meme mecanisme (`generate_selection_bias` parametree par confondant + probabilites) et doivent etre construits ensemble pour eviter le copy-paste qui empeche la propagation des corrections.
**Delivers:** DAGs networkx, comparaisons naive vs ajustee avec IC 95%, exports
**Uses:** networkx.DiGraph avec layout fixe, statsmodels OLS formula API
**Avoids:** Pitfall 4 (probabilites extremes sans overlap) ; anti-pattern copy-paste

### Phase 4 : Scenario 2 — Surcontrole mediateur

**Rationale:** Requiert une decomposition de l'effet via `nb_visites` vs `panier_moyen` bien calibree. Construction apres les scenarios 1x car utilise le meme pattern OLS avec comparaison.
**Delivers:** Visualisation du changement de coefficient OLS lors de l'ajout du mediateur + cellule de validation de decomposition
**Avoids:** Pitfall 2 (biais mediateur trop petit — voie 2 doit representer 30-40% de l'effet total)

### Phase 5 : Scenario 3 — Surcontrole collider

**Rationale:** Le scenario le plus delicat a calibrer (le biais collider est facilement invisible). Construit en dernier car beneficie de tous les patterns etablis dans les phases precedentes.
**Delivers:** Variable `posts_reseaux` comme collider, comparaison OLS avec vs sans collider, DAG
**Avoids:** Pitfall 1 (DGP collider mal calibre — bruit insuffisant, coefficient pub identique avec/sans collider)

### Phase 6 : Validation bout-en-bout et polish

**Rationale:** La checklist "ca semble fini mais ce n'est pas fini" du PITFALLS.md identifie 9 points de validation qui ne peuvent etre verifies qu'apres que tous les scenarios sont complets.
**Delivers:** Notebook propre, `Restart & Run All` sans erreur, tous les PNG presentes, zero magic number hors cellule Parametres
**Addresses:** Checklist complete de PITFALLS.md (reproductibilite, exports, effets visibles, comparaisons affichees)

### Phase Ordering Rationale

- Les phases 1 et 2 doivent preceder toutes les autres car le generateur de base et sa validation sont des prerequis techniques absolus.
- Les phases 3, 4, 5 peuvent theoriquement se faire en parallele mais la progression simple→complexe (selection→mediateur→collider) reduit le risque de bugs de calibration non detectes.
- La phase 6 est separee car les validations bout-en-bout necessitent que tous les scenarios soient stables.
- L'architecture en 5 couches impose que la couche Parametres et la couche Generateur soient completes avant d'ecrire le code des couches Scenarios et Visualisation.

### Research Flags

Phases necessitant une recherche approfondie lors de la planification detaillee :
- **Phase 2 (Scenario 0) :** Calibration du ratio de taille optimal pour la visibilite de la variance — tester empiriquement avec les parametres par defaut recommandes (N_petit=20, N_grand=400)
- **Phase 5 (Scenario 3 collider) :** Calibration du coefficient alpha de la variable `posts_reseaux` — valeur par defaut non triviale, necessite des essais pour garantir la visibilite du biais

Phases avec patterns etablis (pas besoin de recherche approfondie) :
- **Phase 1 (Infrastructure) :** Patterns standard de notebook scientifique Python, bien documentes
- **Phase 3 (Selection) :** Pattern OLS statsmodels avec formula API bien etabli
- **Phase 6 (Validation) :** Checklist manuelle, pas de code nouveau

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Versions specifiques a verifier avant de pincer (cutoff aout 2025) ; logique technologique solide |
| Features | MEDIUM | Scope bien defini par le contexte pedagogique ; pas de validation aupres d'apprenants reels |
| Architecture | HIGH | Patterns standard pour notebooks scientifiques Python, bien etablis et eprouves |
| Pitfalls | MEDIUM | Bases sur connaissance du domaine causal inference et Python numerique ; pas de test empirique |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Calibration des parametres par defaut :** Les valeurs exactes recommandees (N_petit=20, N_grand=400, alpha_collider=?, decomposition_mediateur=30-40%) devront etre validees empiriquement lors de l'implementation de la Phase 2. Le notebook doit inclure des cellules de diagnostic.
- **Versions de bibliotheques :** Verifier que `linearmodels` est necessaire (STACK.md le mentionne pour panel OLS with FE) ou si `statsmodels` OLS suffit pour tous les scenarios. Si les scenarios 1x n'utilisent pas de within-estimator, `linearmodels` peut etre exclu.
- **Format de la narration francaise :** Le niveau de detail des cellules Markdown (concis pour formateurs expertes vs didactique pour novices) n'est pas specifie dans la recherche — a decider avec le client.

## Sources

### Primary (HIGH confidence)
- NumPy documentation — `numpy.random.default_rng` et API Generator (connaissance structurelle)
- statsmodels documentation — OLS formula API, `result.params`, `result.conf_int()`
- Architecture patterns for scientific notebooks — conventions etablies du domaine

### Secondary (MEDIUM confidence)
- Cunningham, S. "Causal Inference: The Mixtape" — pedagogie collider, mediateur, biais de selection
- Hernan, M.A. & Robins, J.M. "What If" — mecanismes de surcontrole et biais de selection
- networkx documentation — DiGraph, draw_networkx, layouts

### Tertiary (LOW confidence — a valider)
- Analyse concurrentielle (Mixtape, The Effect, causaldata) — basee sur connaissance du domaine, pas de verification live
- Versions specifiques des bibliotheques — a verifier contre PyPI avant de pincer dans requirements.txt

---
*Research completed: 2026-03-02*
*Ready for roadmap: yes*
