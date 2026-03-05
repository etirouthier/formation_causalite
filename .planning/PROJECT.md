
# Générateur de données — Formation Causalité

## What This Is

Un notebook Jupyter (Python) standalone qui génère des données simulées illustrant quatre biais causaux classiques (petits nombres, sélection, médiateur, collider), tous construits sur le même modèle de données cohérent. Le formateur exécute `Restart & Run All` pour produire 20 figures PNG et 7 CSV qu'il intègre dans sa présentation.

**Shipped v1.0 :** 42 cellules, ~993 lignes Python, 6 phases, 9 plans. Notebook prêt à distribuer.

## Core Value

Permettre au formateur d'illustrer visuellement et avec des données reproductibles quatre biais causaux classiques, tous construits sur le même modèle de données cohérent — pour que les apprenants comparent les scénarios entre eux.

## Modèle de données

### Structure

Panel (magasin × mois) agrégé. Une ligne = un magasin un mois donné.

**Caractéristiques des magasins (fixes dans le temps) :**
- `taille` : multinomial {petit, moyen, grand} — détermine N_potentiel (nombre de clients potentiels/mois)
- `urbain` : binaire (0/1) — effet additif sur p_visite
- `qualite_equipe` : binaire (0/1) — effet additif sur p_visite

**Variables mensuelles :**
- `mois` : 1–12, effet saisonnier additif sur p_visite (paramétrable)
- `pub` : binaire (0/1), traitement publicité ce mois-ci pour ce magasin

### Générateur micro-fondé

Pour chaque magasin `s` et mois `t` :

```
N_potentiel(s)       ← dépend de taille {petit, moyen, grand}
p_visite(s, t)       = p_base + effet_urbain(s) + effet_saison(t) + effet_equipe(s) + effet_pub × pub(s,t)
nb_visites(s, t)     ~ Binomial(N_potentiel(s), p_visite(s, t))
μ_panier(s, t)       = μ_base + effet_pub_panier × pub(s,t)
panier_i             ~ Normal(μ_panier, σ_panier)   [pour chaque visiteur i]
ventes(s, t)         = Σ panier_i  sur nb_visites(s, t)
panier_moyen(s, t)   = ventes(s, t) / nb_visites(s, t)
```

**Effet vrai de la pub (paramétrable, par défaut) :**
- +10% sur p_visite (via `effet_pub` additif sur la probabilité de base)
- +10% sur μ_panier (via `effet_pub_panier`)
- Effet homogène (pas d'hétérogénéité entre magasins)

Tous les paramètres sont exposés dans une cellule "Paramètres" en tête de notebook.

## Scénarios pédagogiques

### Scénario 0 — Biais de petits nombres

**Mécanisme :** Les petits magasins ont un N_potentiel faible → le panier_moyen observé a une variance élevée (TCL). Les magasins aux extrêmes de la distribution du panier_moyen sont sur-représentés par les petits magasins.

**Biais illustré :** Sélectionner les "meilleurs" magasins en regardant les bords de distribution est une méthode non pertinente — on sélectionne du bruit, pas de la qualité.

**Figures :** Distribution du panier_moyen par taille de magasin ; scatter nb_visites vs variance du panier_moyen.

---

### Scénario 1a — Biais de sélection par qualité d'équipe

**Mécanisme :** P(pub=1 | bonne_equipe) >> P(pub=1 | mauvaise_equipe), paramétrable.

**Confondant :** qualite_equipe → pub ET qualite_equipe → p_visite → ventes.

**DAG :** qualite_equipe → pub → ventes ← qualite_equipe

**Biais illustré :** Comparer naïvement ventes_pub vs ventes_sans_pub surestime l'effet de la pub.

---

### Scénario 1b — Biais de sélection par localisation

**Mécanisme :** P(pub=1 | urbain) >> P(pub=1 | rural), paramétrable.

**Confondant :** urbain → pub ET urbain → p_visite → ventes.

---

### Scénario 1c — Biais de sélection par saison

**Mécanisme :** P(pub=1 | mois_haute_saison) >> P(pub=1 | mois_basse_saison), paramétrable.

**Confondant :** saison → pub ET saison → p_visite → ventes.

---

### Scénario 2 — Surcontrôle sur un médiateur

**Mécanisme :** ventes = nb_visites × panier_moyen. La pub agit SUR les deux composantes. Ajouter panier_moyen comme variable de contrôle dans la régression bloque une partie du chemin causal.

**DAG :** pub → panier_moyen → ventes ET pub → nb_visites → ventes. Contrôler sur panier_moyen bloque pub → panier_moyen → ventes.

**Biais illustré :** Le coefficient de pub devient biaisé vers zéro quand on contrôle sur un médiateur.

---

### Scénario 3 — Surcontrôle sur un collider

**Mécanisme :** Une variable `posts_reseaux` est générée comme conséquence conjointe de la pub ET des ventes :
`posts_reseaux(s,t) ~ f(pub(s,t), ventes(s,t)) + ε`

**DAG :** pub → posts_reseaux ← ventes. Contrôler sur posts_reseaux ouvre un chemin non causal entre pub et ventes.

**Biais illustré :** En pensant "neutraliser" l'effet de la pub via posts_reseaux, on introduit un biais — posts_reseaux est un collider.

## Requirements

### Validated

- ✓ Notebook Python/Jupyter unique avec cellule "Paramètres" en tête — v1.0
- ✓ Générateur micro-fondé (Binomial × Normal) avec tous paramètres exposés — v1.0
- ✓ Scénario 0 : biais de petits nombres avec figures (distribution, scatter, top10, loi des grands nombres) — v1.0
- ✓ Scénarios 1a/1b/1c : biais de sélection (équipe, localisation, saison) avec DAG + figures — v1.0
- ✓ Scénario 2 : surcontrôle sur médiateur avec visualisation coefficients — v1.0
- ✓ Scénario 3 : surcontrôle sur collider avec visualisation coefficients — v1.0
- ✓ Export des figures (PNG) et des données (CSV) dans des dossiers dédiés — v1.0
- ✓ Seed de reproductibilité paramétrable — v1.0
- ✓ `Restart & Run All` sans erreur, validation finale par nbconvert — v1.0

### Active

*(Aucun — planning prochain milestone à définir)*

### Out of Scope

- Interface interactive (widgets, dash, streamlit) — le formateur édite directement le notebook
- Version R — Python uniquement pour la v1
- Données individuelles clients non agrégées — agrégation magasin×mois uniquement
- Effets hétérogènes de la pub — effet homogène pour simplifier la pédagogie

## Context

Formation introductive à l'évaluation des effets causaux. Le public est des praticiens data/analytics, pas des chercheurs. Les apprenants n'ont pas accès au notebook — le formateur en tire des figures pour une présentation. L'exemple fil rouge (pub → ventes) est maintenu sur tous les scénarios pour permettre la comparaison des biais entre eux.

**État actuel (v1.0) :** Notebook 42 cellules, ~993 lignes Python, 20 PNG + 7 CSV générés. Tech stack : numpy, pandas, matplotlib, statsmodels, networkx. Exécution complète validée par `nbconvert --execute` (exit 0).

## Constraints

- **Langage** : Python 3, Jupyter Notebook — bibliothèques standard (numpy, pandas, matplotlib, statsmodels)
- **Reproductibilité** : seed numpy paramétrable en tête de notebook
- **Autonomie** : le notebook doit tourner de bout en bout sans erreur avec les paramètres par défaut

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Modèle micro-fondé client par client | Crée naturellement le biais de petits nombres via la variance binomiale | ✓ Validé — biais clairement visible en production |
| panier_moyen dépend uniquement de la pub | Simplifie la modélisation du Scénario 2 (médiateur pur) | ✓ Validé — pédagogiquement clair |
| Pas d'effets hétérogènes de la pub | Garde l'accent sur les biais de sélection/contrôle, pas sur l'estimation d'effets individuels | ✓ Validé — cohérent avec l'objectif pédagogique |
| Paramètres exposés dans une cellule unique | Permet au formateur de créer facilement des variantes pour exercices | ✓ Validé — ALL_CAPS, aucun magic number hors PARAMS |
| DV = log_rev_int pour scénarios 1a/1b/1c | Effets multiplicatifs plus réalistes, ATT en log-points interprétable | ✓ Validé — biais de sélection visible et calibré |
| P_PUB_ALEATOIRE pour sc2/sc3 | Sélection aléatoire dans sc2/sc3 évite le biais de sélection — met en évidence le biais de contrôle seul | ✓ Validé — contrôle propre dans v1.0 |
| Collider COLLIDER_PUB_VENTES_COEFF ajustable | SNR suffisant pour biais visible (A=5, B=2, ~9pp de biais) | ✓ Validé — pédagogiquement lisible |

---
*Last updated: 2026-03-05 after v1.0 milestone*
