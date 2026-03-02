# Pitfalls Research

**Domain:** Educational causal inference simulation notebooks (Python/Jupyter)
**Researched:** 2026-03-02
**Confidence:** MEDIUM — external search tools unavailable; findings drawn from causal inference literature, statistical pedagogy, and Python numerical computing knowledge.

---

## Pitfalls Critiques

### Pitfall 1 — DGP du collider implémenté incorrectement

**Ce qui se passe :**
Le scénario 3 exige que `posts_reseaux` soit causé par `pub` ET `ventes`, et que conditionner sur `posts_reseaux` crée une association spurieuse. Si le bruit est trop faible ou les coefficients trop similaires, le biais du collider est invisible à l'échantillon.

**Comment éviter :**
- `posts_reseaux = alpha * pub + beta * (ventes - mean_ventes)/std_ventes + epsilon` avec epsilon à variance substantielle
- Valider : la regression avec `posts_reseaux` vs sans doit produire des coefficients `pub` différents d'au moins 5%
- Standardiser `ventes` avant de l'utiliser comme prédicteur

**Signes d'alerte :** coefficient `pub` identique avec et sans `posts_reseaux` ; avertissement de multicolinéarité de statsmodels.

**Phase concernée :** Construction du DGP (générateur de base) — valider dès la première implémentation.

---

### Pitfall 2 — Biais du médiateur trop petit pour être visible

**Ce qui se passe :**
Si `pub` opère principalement via `nb_visites` (grande `effet_pub`) plutôt que via `panier_moyen` (petite `effet_pub_panier`), ajouter `panier_moyen` à la régression change à peine le coefficient — les apprenants voient "pas de différence".

**Comment éviter :**
- Calibrer les paramètres par défaut pour que la voie `pub → panier_moyen → ventes` porte 30–40% de l'effet total
- Cellule de validation : imprimer la décomposition "Effet via nb_visites: X%, via panier_moyen: Y%"
- Asserter : contribution de la voie 2 > 20%

**Signes d'alerte :** coefficient `pub` change de moins de 10% quand `panier_moyen` est ajouté.

**Phase concernée :** Calibration des paramètres — Scénario 2.

---

### Pitfall 3 — Biais de petits nombres invisible (N_potentiel insuffisamment différencié)

**Ce qui se passe :**
Si `N_potentiel_petit = 50` et `N_potentiel_grand = 200` (ratio 4x), la différence de variance du panier_moyen est à peine perceptible visuellement.

**Comment éviter :**
- Utiliser `N_potentiel_petit = 15–30`, `N_potentiel_grand = 300–500` (ratio 10–20x)
- Utiliser des violin plots ou strip plots jitterisés, pas des boxplots
- Superposer l'écart-type théorique de `panier_moyen` pour chaque classe de taille

**Signes d'alerte :** Le premier plot montre des IQR qui se chevauchent entre classes de taille.

**Phase concernée :** Calibration des paramètres — Scénario 0.

---

### Pitfall 4 — Non-reproductibilité via l'API NumPy legacy

**Ce qui se passe :**
`np.random.seed(42)` en tête + `np.random.binomial(...)` dans les cellules = reproductibilité fragile. Toute cellule lancée hors ordre change silencieusement tous les résultats suivants.

**Comment éviter :**
- `rng = np.random.default_rng(SEED)` créé une seule fois dans la cellule Paramètres
- Tous les tirages : `rng.binomial(...)`, `rng.normal(...)`, etc.
- Ne jamais utiliser `np.random.seed()` nulle part

**Signes d'alerte :** Exécuter les cellules dans un ordre différent produit des figures différentes.

**Phase concernée :** Construction du DGP (fondational) — dès la première cellule de données.

---

### Pitfall 5 — Probabilités de sélection extrêmes : pas d'overlap, leçon perdue

**Ce qui se passe :**
`P(pub=1 | bonne_equipe) = 0.9` et `P(pub=1 | mauvaise_equipe) = 0.1` crée un chevauchement quasi-nul. L'estimateur ajusté est très bruité — les apprenants croient que "l'ajustement ne marche pas".

**Comment éviter :**
- Confondance modérée : `P(pub=1 | bonne_equipe) ≈ 0.7`, `P(pub=1 | mauvaise_equipe) ≈ 0.3`
- Valider : chaque cellule traitement × confondant a > 5 observations
- Valider : l'IC 95% de l'estimateur ajusté contient l'effet vrai aux paramètres par défaut

**Phase concernée :** Construction DGP — Scénarios 1a/1b/1c.

---

### Pitfall 6 — Effet vrai incohérent entre scénarios

**Ce qui se passe :**
En ajustant les paramètres par scénario pour rendre chaque biais "visible", on change l'effet vrai. Les apprenants ne peuvent pas comparer "le biais 1a surestime de X%" avec "le biais 2 sous-estime de Y%" — les bases sont différentes.

**Comment éviter :**
- Un seul dictionnaire `PARAMS` partagé entre tous les scénarios
- Chaque scénario modifie uniquement le *mécanisme d'assignation*, jamais les effets vrais
- Afficher l'effet vrai en permanence sur toutes les figures de régression

**Signes d'alerte :** `effet_pub` apparaît avec des valeurs différentes dans différentes cellules.

**Phase concernée :** Fondational — cellule Paramètres, architecture.

---

### Pitfall 7 — p_visite hors de [0,1] avec des paramètres extrêmes

**Ce qui se passe :**
`p_visite = p_base + effet_urbain + effet_saison + effet_equipe + effet_pub × pub` peut dépasser 1.0 (tous les effets positifs cumulés). NumPy lève `ValueError: p value must be in range [0, 1]` — le notebook plante.

**Comment éviter :**
- `p_visite = np.clip(p_visite, 0.01, 0.99)` avant chaque `rng.binomial()`
- Assertion dans la cellule Paramètres : `assert p_base + max_positive_effects < 0.99`
- Documenter les plages de valeurs valides

**Signes d'alerte :** NumPy lève `ValueError` ; `nb_visites == N_potentiel` pour tout un groupe.

**Phase concernée :** Fondational — dès la première version du générateur.

---

## Anti-patterns Techniques

| Raccourci | Coût long terme | Solution |
|-----------|-----------------|---------|
| Copy-paste des cellules scénario 1a → 1b → 1c | Bugs fixes dans 1a ne se propagent pas | Fonction `generate_selection_bias(params, confounder_col, p_high, p_low)` |
| Simulation des paniers en boucle Python | 600k itérations → minutes | Tirage vectorisé : `rng.normal(mu, sigma, total_visits)` |
| `np.random.seed()` global | Résultats change si ordre des cellules change | `rng = np.random.default_rng(SEED)` |
| `plt.savefig()` après `plt.show()` | PNG vide | `fig.savefig(path)` AVANT `plt.show()` |
| Paramètres magiques dans les cellules scénario | Formateur ne peut pas créer de variantes | Tout dans la cellule Paramètres, zéro magic number |

---

## Checklist "Ça semble fini mais ce n'est pas fini"

- [ ] **Scénario 3 (collider)** : Imprimer les deux régressions côte à côte — le coefficient `pub` doit visiblement différer
- [ ] **Scénario 2 (médiateur)** : Imprimer la décomposition de l'effet — la voie via `panier_moyen` > 20%
- [ ] **Scénario 0 (petits nombres)** : Imprimer moyenne et écart-type du `panier_moyen` par taille — ratio de variance > 3x
- [ ] **Reproductibilité** : Restart kernel, run all deux fois — CSV identiques bit à bit
- [ ] **Export** : Tous les PNG existent dans le dossier après run clean
- [ ] **Paramètres** : Zéro magic number hors de la cellule Paramètres
- [ ] **Sélection (1a/1b/1c)** : Estimation naïve surestime ET estimation ajustée est plus proche — affichées côte à côte
- [ ] **Effet vrai cohérent** : `true_effect_pub` imprimé dans chaque scénario avec valeur identique
- [ ] **p_visite en [0,1]** : Assertion ou clip présent avant chaque `rng.binomial()`

---

## Sources

- Cunningham, S. "Causal Inference: The Mixtape" — pédagogie collider, médiateur, biais de sélection
- Hernán, M.A. & Robins, J.M. "What If" — mécanismes de surcontrôle et biais de sélection
- NumPy random generator docs : https://numpy.org/doc/stable/reference/random/index.html
- Statsmodels OLS docs : https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html

*Confidence: MEDIUM — basé sur connaissance du domaine, web non disponible*
