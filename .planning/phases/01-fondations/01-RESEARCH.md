# Phase 1: Fondations - Research

**Researched:** 2026-03-02
**Domain:** Python/Jupyter notebook infrastructure — panel data generator, reproducibility, assertions, directory setup
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INFRA-01 | Le formateur peut modifier tous les paramètres de simulation depuis une cellule unique en tête de notebook (constantes ALL_CAPS, aucun magic number ailleurs) | Architecture Patterns > Pattern 1 (Cellule Paramètres) |
| INFRA-02 | Le notebook produit des résultats identiques à chaque exécution `Restart & Run All` via `numpy.random.default_rng(SEED)` | Standard Stack (NumPy 2.x), Code Examples > RNG Pattern |
| INFRA-03 | Une cellule d'assertions valide que les paramètres sont cohérents (`p_visite ∈ [0,1]`, overlap suffisant, effet vrai identique entre scénarios) | Common Pitfalls > Pitfall 3 (p_visite hors [0,1]), Pitfall 5 (effet vrai incohérent) |
| INFRA-04 | Toutes les figures sont automatiquement exportées en PNG vers `figures/` et tous les datasets en CSV vers `data/` lors de l'exécution | Architecture Patterns > Pattern 3 (One function = one figure = one export), Code Examples > Directory Setup |
| DGP-01 | Un générateur de panel partagé `generate_base_panel(params, rng)` produit le DataFrame N_magasins × T_mois utilisé par tous les scénarios | Architecture Patterns > Pattern 2 (Isolated DGP), Code Examples > generate_base_panel skeleton |
| DGP-02 | Chaque magasin est caractérisé par : `taille`, `urbain`, `qualite_equipe` | Code Examples > Store characteristics generation |
| DGP-03 | La variable mensuelle `saison` produit un effet additif paramétrable sur `p_visite` | Code Examples > p_visite computation |
| DGP-04 | Le traitement `pub` est binaire par magasin × mois, avec mécanisme de sélection probabiliste paramétrable | Architecture Patterns > Pattern 2 (Isolated DGP) — note: pub assignment belongs to each scenario, not base panel |
| DGP-05 | L'effet vrai de la pub est +10% sur `p_visite` ET +10% sur `μ_panier`, toutes deux paramétrables ; effet homogène | Common Pitfalls > Pitfall 5, Code Examples > Parameters cell template |
| DGP-06 | Les DAGs causaux sont dessinés via `networkx.DiGraph` avec un layout de nœuds fixe et déterministe (pas de spring_layout) | Standard Stack (networkx 3.x), Code Examples > DAG pattern |

</phase_requirements>

---

## Summary

Phase 1 builds the foundational infrastructure on which all subsequent phases depend: the Parameters cell, the base panel generator `generate_base_panel(params, rng)`, directory setup, and validation assertions. The project is a single Jupyter notebook — not a Python package — so the architecture patterns are notebook-specific conventions (cell ordering, cell execution side-effects, shared mutable state via a single `PARAMS` dict and a single `rng` object).

The technical domain is well-understood: standard scientific Python stack (NumPy 2.x, pandas 2.x, networkx 3.x), all at mature and stable versions. No novel or experimental libraries are required. The main risks in Phase 1 are not technological but calibration-related: the default parameter values must be chosen such that downstream scenarios (Phases 2-5) can produce pedagogically visible effects. Two known calibration concerns flagged in STATE.md are: (a) `N_petit`/`N_grand` ratio should be 10-20x for variance visibility in Scenario 0; (b) `alpha_collider` for `posts_reseaux` in Scenario 3 requires empirical tuning.

The three critical non-negotiable patterns for Phase 1 are: (1) `rng = np.random.default_rng(SEED)` as the sole source of randomness, passed as an argument — never global `np.random.seed()`; (2) `np.clip(p_visite, 0.01, 0.99)` mandatory before every `rng.binomial()` call; (3) a single shared `PARAMS` dict with ALL_CAPS constants, no magic numbers outside the Parameters cell.

**Primary recommendation:** Build Phase 1 as three discrete deliverables in order — (1) Parameters cell + directory setup + imports, (2) `generate_base_panel(params, rng)` function, (3) validation assertions cell — then run `Restart & Run All` to confirm reproducibility.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11+ | Runtime | LTS; up to 25% faster than 3.10; mature wheel availability |
| NumPy | 2.x (2.0+) | Array math, stochastic draws (Binomial, Normal) | `default_rng` API is the current standard; thread-safe, reproducible |
| pandas | 2.x (2.2+) | Panel DataFrame, CSV export, groupby aggregations | Copy-on-write by default in 2.2+; essential for panel data manipulation |
| networkx | 3.6.x | DAG construction and drawing via matplotlib | No system dependency (unlike graphviz); fixed `pos` dict gives deterministic layout |
| matplotlib | 3.8+ | PNG figure export at dpi=150 | Only lib producing publication-quality PNG natively |
| statsmodels | 0.14.x (stable) / 0.15.x (dev) | OLS with formula API, standard errors, confidence intervals | Only option providing SE and p-values needed for the pedagogical narrative |
| JupyterLab | 4.x | Notebook execution environment | Current standard; notebook 6.x is maintenance-only |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| seaborn | 0.13+ | Statistical visualizations (histplot, violinplot) | Used from Phase 2 onward for distribution figures |
| pathlib | stdlib | Directory creation (`figures/`, `data/`) | Use `Path('figures').mkdir(parents=True, exist_ok=True)` |
| scipy | 1.13+ | Statistical distributions (for future use) | Not required in Phase 1; include in requirements for completeness |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| networkx | causalgraphicalmodels | causalgraphicalmodels not maintained since ~2020; networkx actively maintained at 3.6.1 |
| networkx | graphviz (system) | graphviz requires system-level install; creates friction on trainer machine |
| statsmodels | scikit-learn LinearRegression | sklearn produces no standard errors or p-values; pedagogically useless |
| matplotlib (PNG) | plotly / bokeh | plotly/bokeh produce HTML/JS; no native PNG output |
| np.random.default_rng | np.random.seed() global | Legacy API is thread-unsafe and order-dependent; explicitly deprecated for new code |

**Installation:**
```bash
pip install "numpy>=2.0" "pandas>=2.2" "scipy>=1.13" "matplotlib>=3.8" "seaborn>=0.13"
pip install "statsmodels>=0.14" "networkx>=3.0"
pip install "jupyterlab>=4.0"
pip freeze > requirements.txt
```

Note: `linearmodels` is NOT required for Phase 1 or for any scenario in this project. All regressions use `statsmodels.formula.api.ols` (cross-sectional OLS), not panel OLS with within-estimators.

---

## Architecture Patterns

### Recommended Notebook Cell Structure

```
notebook.ipynb
├── [CELL 1] Paramètres globaux (ALL_CAPS constants)
│            SEED, N_MAGASINS, T_MOIS, N_PETIT/MOYEN/GRAND
│            EFFET_PUB_VISITES, EFFET_PUB_PANIER
│            P_BASE_VISITE, EFFET_URBAIN, EFFET_EQUIPE, EFFET_SAISON
│            P_PUB_BONNE_EQUIPE, P_PUB_MAUVAISE_EQUIPE, etc.
│
├── [CELL 2] Imports + rng creation + directory setup
│            import numpy as np; import pandas as pd; etc.
│            rng = np.random.default_rng(SEED)
│            Path('figures').mkdir(parents=True, exist_ok=True)
│            Path('data').mkdir(parents=True, exist_ok=True)
│
├── [CELL 3] generate_base_panel(params, rng) function definition
│
├── [CELL 4] Call generate_base_panel — produce base_df
│
└── [CELL 5] Assertions cell — validate base_df and parameter coherence
```

### Pattern 1: Single Parameters Cell (ALL_CAPS)

**What:** All numeric constants live in one cell at the top of the notebook, named with ALL_CAPS. No magic numbers appear in any other cell.

**When to use:** Every time a number appears in the code — it must be a reference to a constant defined here.

**Example:**
```python
# ═══════════════════════════════════════════════════════════
# PARAMÈTRES — modifiez ici uniquement
# ═══════════════════════════════════════════════════════════

SEED        = 42
N_MAGASINS  = 200
T_MOIS      = 24

# Taille des magasins (N_potentiel clients/mois)
N_PETIT  = 30    # NOTE: doit être 10-20x plus petit que N_GRAND
N_MOYEN  = 150
N_GRAND  = 500   # ratio N_GRAND/N_PETIT ≈ 17x — visible dans Scénario 0

# Probabilité de visite de base
P_BASE_VISITE  = 0.05

# Effets additifs sur p_visite
EFFET_URBAIN   = 0.03
EFFET_EQUIPE   = 0.02
EFFET_SAISON   = {1: -0.01, 2: -0.01, 3: 0.0, 4: 0.01, 5: 0.02, 6: 0.02,
                   7: 0.02, 8: 0.01, 9: 0.0, 10: -0.01, 11: 0.01, 12: 0.02}

# Effets causaux vrais de la pub (effet homogène)
EFFET_PUB_VISITES = 0.10  # +10% additif sur p_visite
EFFET_PUB_PANIER  = 0.10  # +10% multiplicatif sur mu_panier

# Panier moyen de base
MU_PANIER_BASE = 50.0
SIGMA_PANIER   = 15.0

# Probabilités de traitement par scénario (pour Phases 3+)
P_PUB_BONNE_EQUIPE    = 0.70
P_PUB_MAUVAISE_EQUIPE = 0.30
P_PUB_URBAIN          = 0.65
P_PUB_RURAL           = 0.25
P_PUB_HAUTE_SAISON    = 0.70
P_PUB_BASSE_SAISON    = 0.30

# Regroupement dans un dict pour passage aux fonctions
PARAMS = {
    'seed': SEED,
    'n_magasins': N_MAGASINS,
    't_mois': T_MOIS,
    'n_petit': N_PETIT,
    'n_moyen': N_MOYEN,
    'n_grand': N_GRAND,
    'p_base_visite': P_BASE_VISITE,
    'effet_urbain': EFFET_URBAIN,
    'effet_equipe': EFFET_EQUIPE,
    'effet_saison': EFFET_SAISON,
    'effet_pub_visites': EFFET_PUB_VISITES,
    'effet_pub_panier': EFFET_PUB_PANIER,
    'mu_panier_base': MU_PANIER_BASE,
    'sigma_panier': SIGMA_PANIER,
    'p_pub_bonne_equipe': P_PUB_BONNE_EQUIPE,
    'p_pub_mauvaise_equipe': P_PUB_MAUVAISE_EQUIPE,
    'p_pub_urbain': P_PUB_URBAIN,
    'p_pub_rural': P_PUB_RURAL,
    'p_pub_haute_saison': P_PUB_HAUTE_SAISON,
    'p_pub_basse_saison': P_PUB_BASSE_SAISON,
}
```

### Pattern 2: Explicit RNG Passed as Argument

**What:** A single `Generator` object created once from `SEED`, passed as argument to all functions that need randomness. Never use `np.random.seed()` or `np.random.binomial()`.

**When to use:** Every function that draws random numbers takes `rng` as a parameter.

**Example:**
```python
# Source: https://numpy.org/doc/stable/reference/random/generator.html
rng = np.random.default_rng(SEED)

def generate_base_panel(params, rng):
    """
    Génère le panel partagé N_magasins × T_mois.
    rng est passé en argument — jamais utilisé comme global.
    """
    # ... uses rng.choice(), rng.binomial(), rng.normal()
    pass

base_df = generate_base_panel(PARAMS, rng)
```

### Pattern 3: One Function = One Figure = One Export

**What:** Each visualization function saves its figure to `figures/` automatically. The caller never needs to call `savefig` separately.

**When to use:** Every plotting function in the notebook.

**Example:**
```python
def plot_something(df, params, filename='figures/default.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... draw ...
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()   # AFTER savefig — order matters (savefig first, show second)
```

**CRITICAL:** `fig.savefig(path)` MUST come BEFORE `plt.show()`. Calling `show()` first clears the figure buffer, producing an empty PNG.

### Pattern 4: Scenario Isolation via DataFrame Copy

**What:** Each scenario derives its DataFrame from `base_df.copy()`. The base panel is never modified in place.

**When to use:** Every scenario function.

**Example:**
```python
# CORRECT — never modifies base_df
scenario_1a_df = base_df.copy()
scenario_1a_df['pub'] = assign_treatment_by_team(scenario_1a_df, rng, PARAMS)

# WRONG — modifies shared state
base_df['pub'] = ...   # Never do this
```

### Pattern 5: DAG with Fixed Position Dict

**What:** NetworkX DAGs use a manually defined `pos` dict, not `spring_layout` (which is stochastic).

**When to use:** All DAG visualizations (Phase 1 introduces the pattern; used from Phase 3 onward).

**Example:**
```python
# Source: https://networkx.org/documentation/stable/reference/drawing.html
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([('pub', 'ventes'), ('equipe', 'pub'), ('equipe', 'ventes')])

# FIXED layout — deterministic, not spring_layout
pos = {'pub': (0, 0), 'ventes': (2, 0), 'equipe': (1, 1)}

fig, ax = plt.subplots(figsize=(6, 4))
nx.draw_networkx(G, pos, ax=ax,
                 node_color=['steelblue', 'green', 'orange'],
                 node_size=2000,
                 font_size=12,
                 arrows=True)
ax.set_title('DAG — Scénario 1a : Sélection par qualité d\'équipe')
fig.savefig('figures/dag_scenario_1a.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Pattern 6: generate_base_panel Micro-Founded Logic

**What:** The base panel generates store characteristics once, then for each store-month: computes `p_visite` additively, clips to [0.01, 0.99], draws `nb_visites` from Binomial, draws individual baskets from Normal, aggregates to `ventes` and `panier_moyen`.

**Key invariant:** In `generate_base_panel`, the `pub` column is NOT set — this is the responsibility of each scenario. The base panel contains only store characteristics and the counterfactual outcomes (nb_visites and panier_moyen under pub=0 for reference, or without any treatment).

**Recommended approach:** Generate `pub=0` baseline in base panel. Each scenario overrides `pub` column and recomputes `nb_visites`, `ventes`, `panier_moyen` based on the treatment assignment mechanism.

```python
def generate_base_panel(params, rng):
    """
    Retourne un DataFrame avec N_magasins × T_MOIS lignes.
    Colonnes : magasin_id, mois, taille, n_potentiel, urbain,
               qualite_equipe, effet_saison_val
    NB : pub, nb_visites, ventes, panier_moyen sont assignés par chaque scénario.
    """
    n = params['n_magasins']
    t = params['t_mois']

    # Caractéristiques des magasins (fixes dans le temps)
    tailles = rng.choice(['petit', 'moyen', 'grand'], size=n,
                         p=[0.4, 0.4, 0.2])
    n_potentiel_map = {
        'petit': params['n_petit'],
        'moyen': params['n_moyen'],
        'grand': params['n_grand'],
    }
    urbain = rng.binomial(1, 0.5, size=n)
    qualite_equipe = rng.binomial(1, 0.5, size=n)

    # Construire le panel magasin × mois
    rows = []
    for s in range(n):
        for t_idx in range(1, t + 1):
            mois = ((t_idx - 1) % 12) + 1
            rows.append({
                'magasin_id': s,
                'mois': mois,
                'taille': tailles[s],
                'n_potentiel': n_potentiel_map[tailles[s]],
                'urbain': urbain[s],
                'qualite_equipe': qualite_equipe[s],
                'effet_saison_val': params['effet_saison'][mois],
            })

    return pd.DataFrame(rows)
```

**Alternative (vectorized, preferred for performance):**
```python
# Vectorized construction avoids Python loops over 200×24=4800 iterations
magasins = pd.DataFrame({
    'magasin_id': range(n),
    'taille': rng.choice(['petit', 'moyen', 'grand'], size=n, p=[0.4, 0.4, 0.2]),
    'urbain': rng.binomial(1, 0.5, size=n),
    'qualite_equipe': rng.binomial(1, 0.5, size=n),
})
magasins['n_potentiel'] = magasins['taille'].map(n_potentiel_map)
mois_df = pd.DataFrame({'mois': range(1, t + 1)})
base_df = magasins.merge(mois_df, how='cross')  # pandas 2.x cross join
base_df['effet_saison_val'] = base_df['mois'].map(params['effet_saison'])
```

### Pattern 7: compute_outcomes Helper

**What:** A shared helper function that, given a DataFrame with `pub` assigned, computes `p_visite`, `nb_visites`, `ventes`, `panier_moyen`. Called by every scenario.

```python
def compute_outcomes(df, params, rng):
    """
    Calcule nb_visites, ventes, panier_moyen pour chaque ligne.
    Entrée : df avec colonnes taille, urbain, qualite_equipe,
             effet_saison_val, pub.
    Modifie df en place et retourne df.
    """
    p_visite = (
        params['p_base_visite']
        + params['effet_urbain'] * df['urbain']
        + params['effet_equipe'] * df['qualite_equipe']
        + df['effet_saison_val']
        + params['effet_pub_visites'] * df['pub']
    )
    # OBLIGATOIRE — empêche ValueError de NumPy si p > 1 ou p < 0
    p_visite = np.clip(p_visite, 0.01, 0.99)

    df['p_visite'] = p_visite
    df['nb_visites'] = rng.binomial(df['n_potentiel'].values,
                                    p_visite.values)

    mu_panier = params['mu_panier_base'] * (
        1 + params['effet_pub_panier'] * df['pub']
    )

    # Tirage vectorisé des paniers individuels (évite la boucle Python)
    # ventes(s,t) = sum of nb_visites(s,t) Normal draws
    # Approximation valide par CLT : ventes ~ Normal(nb_visites * mu, nb_visites * sigma²)
    df['ventes'] = (
        df['nb_visites'] * mu_panier
        + rng.normal(0, params['sigma_panier'], len(df)) * np.sqrt(df['nb_visites'])
    )
    df['panier_moyen'] = np.where(
        df['nb_visites'] > 0,
        df['ventes'] / df['nb_visites'],
        np.nan
    )
    return df
```

**Note on micro-foundation vs vectorized approximation:** The exact micro-founded model draws `nb_visites` Normal samples per row. For N_MAGASINS=200, T_MOIS=24, and N_GRAND=500, this means up to 200×24×500=2.4M individual draws. This is acceptable in NumPy but requires careful vectorized implementation. The CLT approximation above (`ventes ~ Normal(n*mu, n*sigma²)`) is pedagogically equivalent and faster — use it unless the exact distribution matters.

### Anti-Patterns to Avoid

| Anti-pattern | Why Bad | Solution |
|--------------|---------|---------|
| `np.random.seed(42)` global | Thread-unsafe; results change if cells execute out of order | `rng = np.random.default_rng(SEED)` once, pass as argument |
| `np.random.binomial(n, p, size)` | Uses legacy global state | `rng.binomial(n, p, size)` |
| `plt.show()` before `fig.savefig()` | Clears figure buffer → empty PNG | `fig.savefig(path)` FIRST, then `plt.show()` |
| `plt.savefig()` after `plt.show()` | Same problem | Use explicit `fig, ax = plt.subplots()` then `fig.savefig()` |
| `base_df['pub'] = ...` | Modifies shared base panel | `scenario_df = base_df.copy()` then assign to copy |
| Spring layout for DAGs | Non-deterministic positions between runs | Manual `pos` dict with fixed coordinates |
| `graphviz` for DAGs | Requires system-level installation | `networkx` + `matplotlib` only |
| Magic numbers in scenario cells | Trainer must hunt for values to change | All numbers in Parameters cell as ALL_CAPS constants |
| Loop over rows for basket draws | Extremely slow (minutes for large panels) | Vectorized NumPy operations |

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Reproducible RNG | Custom seeding scheme | `np.random.default_rng(SEED)` | Generator API handles thread safety, stream independence |
| OLS with standard errors | Manual matrix inversion | `statsmodels.formula.api.ols` | SE, p-values, conf_int() all built-in; handles numerical stability |
| DAG drawing | Custom matplotlib arrows | `networkx.draw_networkx` | Handles arrow routing, node sizing, label positioning |
| Directory creation | `os.makedirs()` with try/except | `pathlib.Path.mkdir(parents=True, exist_ok=True)` | Idiomatic Python 3; handles existing dirs cleanly |
| Cross join (panel construction) | Nested loops | `df1.merge(df2, how='cross')` | pandas 2.x built-in; vectorized |

**Key insight:** Every "utility" problem in this project has a standard library solution. The creative work is calibration and pedagogy, not infrastructure.

---

## Common Pitfalls

### Pitfall 1: p_visite Outside [0, 1] Causing NumPy Crash

**What goes wrong:** `p_visite = p_base + effet_urbain + effet_saison + effet_equipe + effet_pub × pub` can exceed 1.0 (all positive effects cumulate). NumPy raises `ValueError: p value must be in range [0, 1]` and the notebook crashes.

**Why it happens:** Additive effects on a probability don't respect [0,1] bounds. With `p_base=0.05`, `effet_urbain=0.03`, `effet_equipe=0.02`, `effet_saison=0.02`, and `effet_pub=0.10`, the cumulative `p = 0.22` — safe. But if the trainer sets `EFFET_PUB_VISITES = 0.80`, the value reaches 0.87 for some stores. Edge cases exist even with default parameters.

**How to avoid:** `p_visite = np.clip(p_visite, 0.01, 0.99)` MUST appear before every `rng.binomial()` call. Additionally, add an assertion in the validation cell: `assert P_BASE_VISITE + EFFET_URBAIN + EFFET_EQUIPE + max(EFFET_SAISON.values()) + EFFET_PUB_VISITES < 0.99`.

**Warning signs:** `ValueError` from NumPy; `nb_visites` always equals `N_potentiel` for some group.

### Pitfall 2: Legacy NumPy API Breaking Reproducibility

**What goes wrong:** Using `np.random.seed(42)` at cell top and `np.random.binomial(...)` in the DGP. If any cell is run out of order (e.g., re-running just the scenario cell), the global RNG state is different and results change silently.

**Why it happens:** The legacy API uses a single global RNG state. `Restart & Run All` works, but partial re-execution breaks reproducibility.

**How to avoid:** Use `rng = np.random.default_rng(SEED)` once (in the imports cell), pass `rng` as argument to all functions. The `Generator` object is stateful but explicit — its state is controlled by the caller.

**Warning signs:** Running cells in different order produces different CSVs; `git diff` on exported CSVs shows changes after identical code run.

### Pitfall 3: Inconsistent True Effect Between Scenarios

**What goes wrong:** Adjusting `EFFET_PUB_VISITES` per-scenario to make each bias "more visible" changes the true effect. Learners cannot compare "Scenario 1a overestimates by X%" vs "Scenario 2 underestimates by Y%" because the baselines differ.

**Why it happens:** The temptation to tune per-scenario is strong when one scenario's bias seems small.

**How to avoid:** One `PARAMS` dict shared across all scenarios. The true effects (`EFFET_PUB_VISITES`, `EFFET_PUB_PANIER`) never change between scenarios. Each scenario modifies ONLY the treatment assignment mechanism (`pub` column).

**Warning signs:** `EFFET_PUB` appears with different values in different cells.

### Pitfall 4: N_petit / N_grand Ratio Too Small (Calibration)

**What goes wrong:** If `N_PETIT=50` and `N_GRAND=200` (ratio 4x), the variance difference of `panier_moyen` across store sizes is barely perceptible. Scenario 0 fails its pedagogical purpose.

**Why it happens:** The CLT variance of `panier_moyen` scales as σ²/n. A 4x ratio gives only 2x difference in standard deviation — visually marginal.

**How to avoid:** Use ratio 10-20x: `N_PETIT=20-30`, `N_GRAND=300-500`. Default recommendation: `N_PETIT=30`, `N_GRAND=500` (ratio ~17x). Include a diagnostic in the validation cell printing mean and SD of `panier_moyen` by `taille`.

**Warning signs:** Violin plots of `panier_moyen` by taille show overlapping IQRs for petit/moyen.

### Pitfall 5: savefig After show Produces Empty PNG

**What goes wrong:** Calling `plt.show()` then `plt.savefig()` saves an empty figure. The display flushes the figure buffer.

**Why it happens:** `plt.show()` renders and clears the current figure in interactive backends.

**How to avoid:** Always use explicit `fig, ax = plt.subplots()`, call `fig.savefig(path, dpi=150, bbox_inches='tight')` BEFORE `plt.show()`.

**Warning signs:** All PNGs in `figures/` are blank white images.

### Pitfall 6: Cross Join Not Available in Old pandas

**What goes wrong:** `df1.merge(df2, how='cross')` raises `ValueError` in pandas < 1.2.0.

**Why it happens:** `how='cross'` was added in pandas 1.2.0 (January 2021).

**How to avoid:** Confirm pandas >= 2.2 in requirements. The `how='cross'` merge is the idiomatic vectorized way to build a panel from magasins × mois.

**Warning signs:** Import error or ValueError on the merge call.

---

## Code Examples

### Directory Setup

```python
# Source: https://docs.python.org/3/library/pathlib.html
from pathlib import Path

Path('figures').mkdir(parents=True, exist_ok=True)
Path('data').mkdir(parents=True, exist_ok=True)
```

### RNG Initialization (Reproducible)

```python
# Source: https://numpy.org/doc/stable/reference/random/generator.html
import numpy as np

rng = np.random.default_rng(SEED)
# rng is now the sole source of randomness for the entire notebook
# Pass rng as argument to every function that needs it
```

### Binomial Draw with Mandatory Clip

```python
# Source: https://numpy.org/doc/stable/reference/random/generator.html
p_visite = (
    params['p_base_visite']
    + params['effet_urbain'] * df['urbain']
    + params['effet_equipe'] * df['qualite_equipe']
    + df['effet_saison_val']
    + params['effet_pub_visites'] * df['pub']
)
# MANDATORY — prevents ValueError if p > 1.0 or p < 0.0
p_visite = np.clip(p_visite, 0.01, 0.99)
nb_visites = rng.binomial(df['n_potentiel'].values, p_visite.values)
```

### Assertions Cell (Validation)

```python
# INFRA-03 — Cellule d'assertions
# 1. Paramètre cohérence
max_cumulative_p = (P_BASE_VISITE + EFFET_URBAIN + EFFET_EQUIPE
                    + max(EFFET_SAISON.values()) + EFFET_PUB_VISITES)
assert max_cumulative_p < 0.99, (
    f"p_visite maximale cumulée ({max_cumulative_p:.2f}) dépasse 0.99 — "
    f"réduire les effets additifs"
)

# 2. p_visite ∈ [0.01, 0.99] dans le DataFrame produit
assert (base_df['p_visite'].between(0.01, 0.99)).all(), (
    "p_visite hors [0.01, 0.99] — np.clip() appliqué mais vérifier le DGP"
)

# 3. Overlap suffisant (illustratif — sera plus pertinent pour Scénarios 1x)
assert base_df['nb_visites'].min() > 0, "Des lignes ont nb_visites=0 — augmenter p_base_visite"

# 4. Ratio de variance par taille (diagnostic pédagogique)
variance_by_taille = base_df.groupby('taille')['panier_moyen'].std()
ratio = variance_by_taille['petit'] / variance_by_taille['grand']
assert ratio > 2.0, (
    f"Variance ratio petit/grand = {ratio:.1f}x — augmenter N_GRAND ou réduire N_PETIT "
    f"(cible : > 3x pour visibilité pédagogique)"
)
print("✓ Assertions passed")
print(f"  Max cumulative p_visite: {max_cumulative_p:.3f}")
print(f"  Variance ratio (petit/grand panier_moyen): {ratio:.1f}x")
```

### OLS with statsmodels Formula API

```python
# Source: https://www.statsmodels.org/stable/example_formulas.html
import statsmodels.formula.api as smf

model = smf.ols('ventes ~ pub + qualite_equipe', data=scenario_1a_df)
result = model.fit()

# Extract coefficient and confidence interval
coef_pub = result.params['pub']
ci_pub = result.conf_int().loc['pub']  # Series with [0, 1] for lower, upper bound
print(f"Coefficient pub: {coef_pub:.2f} [{ci_pub[0]:.2f}, {ci_pub[1]:.2f}]")
print(f"Vraie valeur: {PARAMS['effet_pub_visites']} × MU_PANIER_BASE × N_POTENTIEL_MOYEN")
```

### DAG with Fixed Layout

```python
# Source: https://networkx.org/documentation/stable/reference/drawing.html
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ('pub', 'ventes'),
    ('qualite_equipe', 'pub'),
    ('qualite_equipe', 'ventes'),
])

# FIXED layout — same coordinates every run
pos = {
    'pub':           (0, 0),
    'ventes':        (2, 0),
    'qualite_equipe': (1, 1),
}

node_colors = ['steelblue', 'seagreen', 'darkorange']
fig, ax = plt.subplots(figsize=(6, 4))
nx.draw_networkx(G, pos, ax=ax,
                 node_color=node_colors,
                 node_size=2500,
                 font_size=11,
                 font_color='white',
                 arrows=True,
                 arrowsize=25)
ax.axis('off')
ax.set_title('DAG — Scénario 1a : Sélection par qualité d\'équipe')
fig.savefig('figures/dag_scenario_1a.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `np.random.seed()` + `np.random.binomial()` | `rng = np.random.default_rng(SEED)` + `rng.binomial()` | NumPy 1.17 (2019), standard in 2.x | Reproducibility even with out-of-order cell execution |
| `os.makedirs(path, exist_ok=True)` | `Path(path).mkdir(parents=True, exist_ok=True)` | Python 3.4+ pathlib | Idiomatic; cross-platform; no import of `os` needed separately |
| pandas < 1.2 cross join via `merge` key column | `df.merge(df2, how='cross')` | pandas 1.2.0 (January 2021) | Clean panel construction without dummy key column |
| `causalgraphicalmodels` for DAGs | `networkx.DiGraph` | ~2020 (causalgraphicalmodels abandoned) | No maintenance risk; no system dependency |

**Deprecated/outdated:**
- `np.random.seed()` + `np.random.RandomState`: Replaced by Generator API since NumPy 1.17. Still works but explicitly not recommended for new code.
- `jupyter notebook` 6.x: In maintenance-only mode. Use JupyterLab 4.x.
- `linearmodels`: Not needed for this project — cross-sectional OLS via statsmodels is sufficient for all scenarios.

---

## Open Questions

1. **Exact micro-foundation vs CLT approximation for basket draws**
   - What we know: The exact DGP draws `nb_visites` Normal samples per store-month, then sums. For N_GRAND=500 stores × 24 months × 200 stores, this is manageable in NumPy.
   - What's unclear: Whether the CLT approximation `ventes ~ Normal(n*mu, sqrt(n)*sigma)` is close enough to preserve the pedagogical variance patterns for Scenario 0.
   - Recommendation: Start with CLT approximation (vectorized, fast). If Scenario 0 validation shows variance ratio < 3x, switch to exact micro-foundation for petit stores where CLT is least accurate (small n).

2. **Default parameter values for saison effect dict**
   - What we know: `EFFET_SAISON` should be an additive effect on `p_visite` per month. The project context suggests paramétrable seasonal effects.
   - What's unclear: Whether to represent saison as a dict {1:val, 2:val, ...} or as a function/array. The dict approach is more readable for trainers.
   - Recommendation: Use a dict `{1: -0.01, 2: -0.01, ..., 12: 0.02}` in the Parameters cell. This is directly readable and editable by trainers with no Python knowledge.

3. **Whether base_df should include p_visite and outcomes for pub=0 baseline**
   - What we know: The architecture research shows the base panel contains store characteristics only, with scenarios assigning pub and computing outcomes.
   - What's unclear: Whether to pre-compute a "pub=0" baseline in generate_base_panel (useful for Scenario 0) or leave it entirely to each scenario.
   - Recommendation: `generate_base_panel` returns characteristics only (magasin_id, taille, n_potentiel, urbain, qualite_equipe, mois, effet_saison_val). Each scenario assigns pub=0 or pub=1 and calls `compute_outcomes()`. This keeps the base panel free of outcome variables and clarifies the separation of concerns.

---

## Sources

### Primary (HIGH confidence)

- NumPy 2.4 official documentation — [Random Generator API](https://numpy.org/doc/stable/reference/random/generator.html) — verified `default_rng`, `binomial`, `normal`, `choice` signatures
- NetworkX 3.6.1 official documentation — [Drawing reference](https://networkx.org/documentation/stable/reference/drawing.html) — verified `draw_networkx` and manual `pos` dict pattern
- Python 3 official documentation — [pathlib](https://docs.python.org/3/library/pathlib.html) — verified `Path.mkdir(parents=True, exist_ok=True)`
- statsmodels 0.14.6 official documentation — [Formula API](https://www.statsmodels.org/stable/example_formulas.html) — verified `smf.ols`, `result.params`, `result.conf_int()`
- Project research files: `.planning/research/SUMMARY.md`, `.planning/research/ARCHITECTURE.md`, `.planning/research/STACK.md`, `.planning/research/PITFALLS.md` — HIGH confidence (project-specific decisions)

### Secondary (MEDIUM confidence)

- WebSearch cross-reference: NumPy 2.4 is the current stable (consistent with research cutoff Aug 2025 showing 2.x)
- WebSearch cross-reference: NetworkX current stable is 3.6.1 (confirmed via docs URL)
- WebSearch cross-reference: statsmodels 0.14.6 stable / 0.15.0 dev (confirmed via docs URLs)

### Tertiary (LOW confidence — needs validation)

- Default parameter values (`N_PETIT=30`, `N_GRAND=500`, `P_BASE_VISITE=0.05`): Recommended in project research but flagged as requiring empirical calibration. STATE.md explicitly notes this as an open blocker.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — verified against official docs (NumPy 2.4, NetworkX 3.6.1, statsmodels 0.14.6); all at stable, well-maintained versions
- Architecture: HIGH — patterns are standard scientific Python notebook conventions; all code patterns verified against official APIs
- Pitfalls: HIGH — sourced from project PITFALLS.md (domain-specific research) + verified against NumPy official docs (clip before binomial is explicitly documented behavior)
- Parameter calibration: LOW — default values are recommendations, require empirical testing during Phase 1 execution

**Research date:** 2026-03-02
**Valid until:** 2026-04-02 (stable libraries; architecture patterns are long-lived)
