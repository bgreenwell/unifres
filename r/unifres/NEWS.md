# unifres (development version)

## unifres 0.1.1

*Patch release - 2025-03-18*

### Bug Fixes

#### R Package

- **CRITICAL FIX**: Fixed `ffplot()` subsampling bug where `sample.int(n)` incorrectly sampled only the first `n` observations in random order instead of randomly sampling `n` observations from the entire dataset. This affected `ffplot.unifres()` and `ffplot.default()` when the `n` parameter was specified. For ordered data, this bug could lead to severe bias in diagnostic plots. Thanks to GEMINI audit for identifying this issue.

- **FIX**: Added explicit `return(res)` statement to `unifend.zeroinfl()` for consistency with other methods in the same file and to follow best practices (previously relied on R's implicit return of last expression).

### Documentation

- **FIX**: Corrected probability-scale residual formula in methodology documentation from $r_i^{(p)} = \mathbb{E}[U_i] - 0.5$ to the correct formula $r_i^{(p)} = 2\mathbb{E}[U_i] - 1$, which properly reflects the implementation and gives residuals centered at 0 with range [-1, 1].

- **STYLE**: Converted all documentation headings from Title Case to sentence case following modern documentation best practices, while preserving capitalization of proper nouns (Python, R, GitHub) and acronyms (GLM, GAM, FRED, API).

### Testing

- Added regression test for `ffplot()` subsampling with ordered data to prevent future regressions of the subsampling bug.

## unifres 0.1.0

*Initial release - 2025-03-17*

### New Features

#### Both R and Python

- Implemented `fresiduals()` function for computing functional residuals from fitted models
- Three residual types supported:
  - `type = "function"`: Full functional residuals as distribution objects
  - `type = "surrogate"`: Point residuals via random sampling from functional residuals
  - `type = "probscale"`: Probability-scale residuals
- Implemented `ffplot()` for Function-Function diagnostic plots
- Implemented `fredplot()` / `fredplot()` for Functional REsidual Density plots
- Support for multiple model families:
  - Binomial/Logistic regression
  - Poisson regression
  - Negative Binomial regression
  - Quasi-Poisson regression (R only)
  - Zero-inflated Poisson regression (R via pscl)
  - Ordinal regression (R via VGAM)

#### R Package Specific

- S3 generic methods with `unifres` class for functional residuals
- Integration with base R graphics (plot, abline)
- Optional dependencies: hexbin, lattice, MASS for advanced plotting
- Support for mgcv::gam models
- Support for VGAM ordinal and zero-inflated models

#### Python Package Specific

- Type hints throughout for better IDE support
- Returns scipy.stats frozen distributions for functional residuals
- Integration with matplotlib and seaborn for plotting
- Support for statsmodels GLM, NegativeBinomial, and ordinal models
- KDE and hexbin plot types for fredplot()

### Documentation

- Comprehensive README with quick start examples
- Function documentation with examples (R: roxygen2, Python: NumPy-style docstrings)
- CONTRIBUTING.md with development guidelines
- LICENSE files (GPL-3 or later)

### Infrastructure

- GitHub Actions CI/CD:
  - R CMD check on multiple platforms and R versions
  - Python tests on multiple platforms and Python versions
  - Code coverage reporting via Codecov
  - Quarto documentation publishing
- Comprehensive test suites (>80% coverage target)
- Properly configured .gitignore and .Rbuildignore

### References

Liu, D., Lin, Z., & Zhang, H. (2025). A unified framework for residual diagnostics in generalized linear models and beyond. *Journal of the American Statistical Association*, 1–29. https://doi.org/10.1080/01621459.2025.2504037
