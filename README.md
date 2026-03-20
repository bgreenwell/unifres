# unifres: Unified Residual Diagnostics

<!-- badges: start -->
[![R-CMD-check](https://github.com/bgreenwell/unifres/actions/workflows/R-CMD-check.yml/badge.svg)](https://github.com/bgreenwell/unifres/actions/workflows/R-CMD-check.yml)
[![Python Tests](https://github.com/bgreenwell/unifres/actions/workflows/python-tests.yml/badge.svg)](https://github.com/bgreenwell/unifres/actions/workflows/python-tests.yml)
[![Documentation](https://img.shields.io/badge/docs-quarto-blue.svg)](https://bgreenwell.github.io/unifres/)
[![License: GPL-3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
<!-- badges: end -->

**A unified framework for residual diagnostics in generalized linear models and beyond.**

Available in **R** and **Python**, `unifres` implements the functional residual methodology described in [Liu, Lin, & Zhang (2025)](https://doi.org/10.1080/01621459.2025.2504037), providing powerful diagnostic tools that work seamlessly across discrete and continuous outcomes.

---

## Why functional residuals?

Traditional residual diagnostics struggle with discrete data:

- **Binary outcomes**: Residuals can only take two values
- **Count data**: Discrete nature creates artificial patterns
- **Ordinal data**: Difficult to interpret traditional residuals

**Functional residuals solve these problems** by representing the entire distribution of residual randomness, not just a single point estimate.

---

## Key features

### Unified framework
A single approach for binary, count, ordinal, zero-inflated, and continuous outcomes

### Powerful diagnostics
- **Function-Function (Fn-Fn) Plots**: Assess overall model adequacy
- **Functional Residual Density (FRED) Plots**: Identify specific model failures

### Three residual types
- **Functional**: Full distribution objects
- **Surrogate**: Point residuals for traditional plots
- **Probability-scale**: Centered residuals for interpretation

---

## Installation

### R

```r
# Install from GitHub
remotes::install_github("bgreenwell/unifres", subdir = "r/unifres")
```

### Python

```bash
# Install from GitHub with pip
pip install git+https://github.com/bgreenwell/unifres.git#subdirectory=python

# Or install with uv (faster)
uv pip install git+https://github.com/bgreenwell/unifres.git#subdirectory=python
```

[→ Full Installation Guide](https://bgreenwell.github.io/unifres/installation.html)

---

## Usage

### R

```r
library(unifres)

# Generate example data
set.seed(1217)
n <- 1000
x <- rnorm(n)
z <- 1 - 2*x + 3*x^2 + rlogis(n)
y <- ifelse(z > 0, 1, 0)

# Fit model
fit <- glm(y ~ x + I(x^2), family = binomial)

# Compute functional residuals
fres <- fresiduals(fit)

# Create diagnostic plots
ffplot(fit)                    # Function-function plot
fredplot(fit, x = x)          # FRED plot
```

### Python

```python
import numpy as np
import statsmodels.api as sm
from unifres import fresiduals, ffplot, fredplot

# Generate example data
np.random.seed(1217)
n = 1000
x = np.random.normal(size=n)
z = 1 - 2*x + 3*x**2 + np.random.logistic(size=n)
y = np.where(z > 0, 1, 0)

# Fit model
X = sm.add_constant(np.column_stack([x, x**2]))
model = sm.GLM(y, X, family=sm.families.Binomial()).fit()

# Compute functional residuals
fres = fresiduals(model)

# Create diagnostic plots
ffplot(model)
fredplot(model, x)
```

---

## Supported models

### R package

| Model type | Function | Status |
|------------|----------|--------|
| GLM (binomial, Poisson, quasi-Poisson) | `glm()` | ✅ |
| Negative Binomial | `MASS::glm.nb()` | ✅ |
| Generalized Additive Models | `mgcv::gam()` | ✅ |
| Ordinal Regression | `VGAM::vglm()` | ✅ |
| Zero-Inflated Poisson | `pscl::zeroinfl()` | ✅ |

### Python package

| Model type | Function | Status |
|------------|----------|--------|
| GLM (binomial, Poisson, NegBin) | `statsmodels.GLM` | ✅ |
| Negative Binomial | `statsmodels.NegativeBinomial` | ✅ |
| Ordinal Regression | `statsmodels.OrderedModel` | ✅ |

---

## Examples

### Detecting missing polynomial terms

<details>
<summary>Click to expand R example</summary>

```r
library(unifres)

# Generate data with quadratic relationship
set.seed(42)
n <- 500
x <- rnorm(n)
z <- 1 - 2*x + 3*x^2 + rlogis(n)
y <- ifelse(z > 0, 1, 0)

# Fit wrong model (missing x²)
fit_wrong <- glm(y ~ x, family = binomial)

# Fit correct model
fit_correct <- glm(y ~ x + I(x^2), family = binomial)

# Compare with Fn-Fn plots
par(mfrow = c(1, 2))
ffplot(fit_wrong, main = "Missing x²")
ffplot(fit_correct, main = "Correct Model")

# FRED plots reveal the pattern
par(mfrow = c(1, 2))
fredplot(fit_wrong, x = x, type = "hex")
fredplot(fit_correct, x = x, type = "hex")
```

</details>

<details>
<summary>Click to expand Python example</summary>

```python
from unifres import fresiduals, ffplot, fredplot
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Generate data with quadratic relationship
np.random.seed(42)
n = 500
x = np.random.normal(size=n)
z = 1 - 2*x + 3*x**2 + np.random.logistic(size=n)
y = np.where(z > 0, 1, 0)

# Fit models
X_wrong = sm.add_constant(x)
X_correct = sm.add_constant(np.column_stack([x, x**2]))
model_wrong = sm.GLM(y, X_wrong, family=sm.families.Binomial()).fit()
model_correct = sm.GLM(y, X_correct, family=sm.families.Binomial()).fit()

# Compare with Fn-Fn plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ffplot(model_wrong, ax=axes[0])
axes[0].set_title("Missing x²")
ffplot(model_correct, ax=axes[1])
axes[1].set_title("Correct Model")
plt.show()
```

</details>

[→ More Examples: R](https://bgreenwell.github.io/unifres/examples-r.html) | [Python](https://bgreenwell.github.io/unifres/examples-python.html)

---

## Documentation

- [Full documentation](https://bgreenwell.github.io/unifres/)
- [Installation guide](https://bgreenwell.github.io/unifres/installation.html)
- [R examples](https://bgreenwell.github.io/unifres/examples-r.html)
- [Python examples](https://bgreenwell.github.io/unifres/examples-python.html)
- [Methodology](https://bgreenwell.github.io/unifres/methodology.html)
- [API reference: R](https://bgreenwell.github.io/unifres/reference_r/index.html) | [Python](https://bgreenwell.github.io/unifres/reference_python/index.html)

---

## What's in a name?

The name `unifres` has multiple layered meanings:

- **Uni**fied **Res**iduals: A unified diagnostic framework for diverse statistical models
- **Uni**form Distribution: Residuals follow Uniform(0,1) under correct specification
- **F**unctional **Res**iduals: The novel tool at the heart of the package

---

## Citation

If you use **unifres** in your research, please cite:

> Liu, D., Lin, Z., & Zhang, H. (2025). A unified framework for residual diagnostics in generalized linear models and beyond. *Journal of the American Statistical Association*, 1–29. https://doi.org/10.1080/01621459.2025.2504037

**BibTeX:**

```bibtex
@article{liu2025unified,
  title={A unified framework for residual diagnostics in generalized linear models and beyond},
  author={Liu, Dungang and Lin, Zewei and Zhang, Heping},
  journal={Journal of the American Statistical Association},
  pages={1--29},
  year={2025},
  publisher={Taylor \& Francis},
  doi={10.1080/01621459.2025.2504037}
}
```

---

## Contributing

We welcome contributions! See our [Contributing Guide](https://bgreenwell.github.io/unifres/contributing.html) for details.

### Development

**R Package:**
```r
# Clone and install
devtools::install_deps()
devtools::load_all()
devtools::test()
devtools::check()
```

**Python Package:**
```bash
# Clone and install in dev mode
pip install -e ".[dev]"
pytest tests/ -v --cov=unifres
```

---

## Authors

- **Brandon M. Greenwell** - [greenwell.brandon@gmail.com](mailto:greenwell.brandon@gmail.com)
- **Dungang Liu** - [dungang.liu@uc.edu](mailto:dungang.liu@uc.edu)
- **Zewei Lin** - [pqt19@txstate.edu](mailto:pqt19@txstate.edu)

---

## License

- **R Package**: GPL-3 or later
- **Python Package**: GPL-3 or later

See [LICENSE](LICENSE) files for details.

---

## Acknowledgments

This work implements the methodology described in Liu, Lin, & Zhang (2025). We thank the authors for their groundbreaking research in residual diagnostics.

---

<div align="center">

**[Visit documentation](https://bgreenwell.github.io/unifres/)** | **[Installation](https://bgreenwell.github.io/unifres/installation.html)** | **[Examples](https://bgreenwell.github.io/unifres/examples-r.html)**

</div>
