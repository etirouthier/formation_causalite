# FEATURES.md — Causal Inference Training Notebook

**Domain:** Python/Jupyter educational notebook for causal inference pedagogy
**Research date:** 2026-03-02
**Confidence:** MEDIUM (based on domain knowledge, web search unavailable)

---

## Table Stakes

Features that must exist or the tool fails its pedagogical purpose.

### Infrastructure
- **Unique cellule "Paramètres"** — tous les paramètres du DGP exposés en tête de notebook (N magasins, T mois, seed, effets)
- **Seed de reproductibilité** — numpy.random.seed(N) paramétrable, résultats identiques à chaque exécution
- **Exécution bout en bout sans erreur** — `Run All` produit toutes les figures sans exception
- **Export figures** — PNG haute résolution vers dossier `figures/` avec nommage descriptif
- **Export données** — CSV vers dossier `data/` pour chaque scénario

### Scénarios causaux
- **Scénario 0 — Biais de petits nombres** — distribution du panier_moyen par taille de magasin, illustrant la variance binomiale
- **Scénario 1a — Sélection par équipe** — DAG + comparaison naïve vs estimation non-biaisée
- **Scénario 1b — Sélection par localisation** — DAG + comparaison urbain/rural
- **Scénario 1c — Sélection par saison** — DAG + comparaison haute/basse saison
- **Scénario 2 — Surcontrôle médiateur** — visualisation du changement de coefficient en ajoutant panier_moyen
- **Scénario 3 — Surcontrôle collider** — visualisation du biais introduit par le contrôle sur posts_reseaux

### Pédagogie
- **Histoire causale correcte** — le DGP implémente exactement ce que les DAGs représentent
- **Modèle de données cohérent** — tous les scénarios partagent le même générateur de base
- **Affichage des résultats de régression** — coefficients, intervalles de confiance, comparaisons

---

## Differentiators

Features that distinguish a high-quality educational tool.

### Visualisation
- **DAGs avec networkx** — graphes causaux dessinés programmatiquement, cohérents avec les scénarios
- **Graphique de comparaison des coefficients** — côte à côte : estimation naïve vs estimation correcte (vs vraie valeur)
- **Visualisation de la sensibilité paramétrique** — commentaires montrant comment changer p_selection affecte le biais
- **Scatter plots annotés** — points colorés par groupe (traité/non-traité) avec annotations explicatives

### Modélisation
- **Générateur micro-fondé Binomial×Normal** — crée naturellement le biais de petits nombres via la variance statistique, sans artifice
- **Mécanisme de sélection probabiliste** — P(pub=1 | caractéristique) paramétrable, pas déterministe
- **Variable collider explicite** — posts_reseaux générée comme conséquence conjointe de pub et ventes

### Contenu
- **Narrative en français** — cellules markdown explicatives en français (rare dans les outils existants anglophones)
- **Valeur vraie connue** — le formateur sait la "bonne réponse" car il contrôle le DGP

---

## Anti-Features

Choses à ne délibérément PAS construire pour cette version.

| Feature | Raison |
|---------|--------|
| Widgets interactifs (ipywidgets) | Complexité technique, le formateur édite directement les paramètres |
| Effets hétérogènes de la pub | Distrait du message principal (biais de sélection/contrôle) |
| Intégration de données réelles | Hors scope — simulation pure pour contrôle pédagogique total |
| Génération automatique de slides | Le formateur extrait les figures manuellement dans sa présentation |
| Export données individuelles clients | Agrégation magasin×mois suffit pour tous les scénarios |
| Version R | Python uniquement pour la v1 |
| Refresh dynamique | Pas besoin — le formateur relance le notebook entier |
| Interface web (Streamlit/Dash) | Over-engineering pour un usage formateur unique |

---

## Dépendances entre features

```
seed numpy
  └── générateur panel de base (N_magasins × T_mois)
        ├── Scénario 0 (variance par taille) ← Binomial×Normal
        ├── Scénario 1a (sélection équipe) ← probabilité de traitement
        ├── Scénario 1b (sélection localisation) ← probabilité de traitement
        ├── Scénario 1c (sélection saison) ← probabilité de traitement
        ├── Scénario 2 (médiateur) ← décomposition nb_visites × panier_moyen
        └── Scénario 3 (collider) ← variable posts_reseaux dérivée

DAG (networkx)
  └── dépend de : structure causale de chaque scénario

Exports (figures PNG, CSV)
  └── dépend de : tous les scénarios complétés
```

---

## Analyse concurrentielle

| Dimension | Mixtape (Cunningham) | The Effect (Huntington-Klein) | causaldata (R) | Ce projet |
|-----------|---------------------|-------------------------------|----------------|-----------|
| Langue | Anglais | Anglais | Anglais | **Français** |
| Format | Livre + code | Livre + code | Package R | **Notebook standalone** |
| Public | Chercheurs | Chercheurs/praticiens | Développeurs R | **Formateurs** |
| DGP contrôlé | Partiel | Oui | Oui | **Oui + paramétrable** |
| Biais de petits nombres | Non | Non | Non | **Oui** |
| Biais de sélection multiple | 1 exemple | 1-2 exemples | Variable | **3 scénarios** |
| Surcontrôle médiateur | Oui | Oui | Non | **Oui** |
| Surcontrôle collider | Oui | Oui | Non | **Oui** |
| Fil rouge unique | Non | Non | Non | **Oui (pub/ventes)** |
| DAGs générés | Non | Oui (dagitty) | Non | **Oui (networkx)** |

---

## Définition du MVP (P1)

9 features P1 pour le lancement :

1. Cellule paramètres unique
2. Seed de reproductibilité
3. Générateur panel Binomial×Normal
4. Scénario 0 : biais de petits nombres
5. Scénarios 1a/1b/1c : biais de sélection
6. Scénario 2 : surcontrôle médiateur
7. Scénario 3 : surcontrôle collider
8. Export figures PNG
9. Export données CSV

*Confidence: MEDIUM — basé sur connaissance du domaine, pas vérifié contre documentation live*
