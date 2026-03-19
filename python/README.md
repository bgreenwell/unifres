# unifres (Python)

**A unified framework for residual diagnostics in generalized linear models and beyond.**

## Overview

The **unifres** Python package provides an implementation of the unifying functional residual methodology described in:

> Liu, D., Lin, Z., & Zhang, H. (2025). A unified framework for residual diagnostics in generalized linear models and beyond. *Journal of the American Statistical Association*, 129. [https://doi.org/10.1080/01621459.2025.2504037](https://doi.org/10.1080/01621459.2025.2504037).

This framework addresses limitations in traditional residuals for discrete outcome data by using functional residuals that capture residual randomness beyond what classical point statistics can represent.

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/bgreenwell/unifres.git
cd unifres/python

# Install using pip
pip install -e .
```

### Using uv (recommended)

```bash
cd unifres/python
uv pip install -e .
```

## Usage

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

# Fit a logistic regression model
X = sm.add_constant(x)
model = sm.GLM(y, X, family=sm.families.Binomial()).fit()

# Compute functional residuals
fres = fresiduals(model, type="function")

# Create diagnostic plots
ffplot(model)  # Function-function plot
fredplot(model, x)  # Functional residual density plot
```

## Key features

- **Functional residuals**: Transform residuals into distribution objects that capture full residual randomness
- **Multiple residual types**:
  - `type="function"`: Full functional residuals as scipy distribution objects
  - `type="surrogate"`: Point residuals via random sampling
  - `type="probscale"`: Probability-scale residuals
- **Diagnostic plots**:
  - `ffplot()`: Function-function plots for model adequacy assessment
  - `fredplot()`: Functional residual density plots for identifying misspecification
- **Model support**: Works with statsmodels GLM, including:
  - Binomial/Logistic regression
  - Poisson regression
  - Negative Binomial regression
  - Ordinal regression models

## Documentation

For comprehensive documentation, examples, and methodology details, visit:
[https://bgreenwell.github.io/unifres](https://bgreenwell.github.io/unifres)

## Related package

An R implementation is also available: [unifres R package](https://github.com/bgreenwell/unifres/tree/main/r/unifres)

## License

GPL-3 or later. See [LICENSE](LICENSE) for details.

## Citation

If you use this package in your research, please cite:

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

## Authors

- Brandon M. Greenwell
- Dungang Liu
- Zewei Lin
- Heping Zhang
