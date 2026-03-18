# GEMINI AUDIT: unifres Monorepo

**Date:** Tuesday, March 17, 2026
**Scope:** R Package (`r/unifres/`), Python Package (`python/`), and Quarto Website (`docs/`)
**Objective:** Alignment with "A Unified Framework for Residual Diagnostics in Generalized Linear Models and Beyond" (Liu, Lin, & Zhang, 2025).

---

## 1. R Package (`r/unifres/`)

### 🚩 Critical Bug: `ffplot` Subsampling
- **File:** `r/unifres/R/ffplot.R` (Lines 46 & 63)
- **Issue:** The code uses `sample.int(n)` which returns a random permutation of $1 \dots n$. It should use `sample.int(length(fres), size = n)` to correctly subsample from the entire dataset.
- **Impact:** Fn-Fn plots with `n` specified currently only show the first `n` observations in the dataset, leading to biased diagnostics if the data is ordered.

### 🚩 Logic Bug: `unifend.zeroinfl` Return Value
- **File:** `r/unifres/R/utils.R` (Line 155)
- **Issue:** The function assigns the result to `res` but lacks an explicit `return(res)` or simply evaluating `res` at the end.
- **Impact:** While R returns the last expression by default, this is fragile and inconsistent with other methods in the same file.

### 💡 Enhancement: `ffplot.envelop`
- **Issue:** The reproducibility materials (`resources/Functional-Residuals/R_functions/ffplot.envelop.R`) contain a bootstrap-based testing framework that is missing from the package.
- **Recommendation:** Port this logic into the `unifres` package to allow users to visualize "probable envelopes" (confidence bands) for Fn-Fn plots.

---

## 2. Python Package (`python/src/unifres/`)

### 🚩 Feature Gap: `fredplot` Normal Scale
- **File:** `python/src/unifres/plots.py`
- **Issue:** The Python implementation only supports the "uniform" scale. The R package and the paper (Section 2.3, Figure 4b) highlight the "normal" scale ($\Phi^{-1}(u)$) for better visualization of tails.
- **Recommendation:** Implement a `scale="normal"` option in `fredplot`.

### 🚩 Feature Gap: Model Support
- **File:** `python/src/unifres/utils.py`
- **Issue:** Python lacks support for Zero-Inflated and GAM models, which are supported in the R version.
- **Recommendation:** Extend `unifend()` to support `statsmodels.discrete.count_model.ZeroInflatedPoisson` and `statsmodels.gam.generalized_additive_model.GLMGam`.

---

## 3. Quarto Website (`docs/`)

### 🚩 Mathematical Inconsistency: `probscale` Formula
- **File:** `docs/methodology.qmd` (Section: Probability-Scale Residuals)
- **Issue:** Documentation states $r_i^{(p)} = \mathbb{E}[U_i] - 0.5$. However, the paper (Eq. 7) and both package implementations use $R_{PS} = 2\mathbb{E}[U_i] - 1$.
- **Impact:** The documentation incorrectly implies a range of $[-0.5, 0.5]$ instead of $[-1, 1]$.

### 🚩 Documentation Depth: R Reference
- **File:** `docs/reference_r/index.qmd`
- **Issue:** The R reference is a single manually-written page, whereas the Python reference is rich and auto-generated via `quartodoc`.
- **Recommendation:** Use an R-equivalent tool (like `pkgdown` or `roxygen2` integration) to generate more detailed R API docs.

### 💡 Enhancement: Case Studies
- **Recommendation:** The `resources/` directory contains real-world datasets (Wine Quality, Bike Sharing). These should be converted into "Case Study" pages on the website to demonstrate the framework's effectiveness on real data vs. simulations.

---

## 4. General Recommendations

1.  **Terminology Alignment:** The package uses "FRED plots" (Functional REsidual Density), but the paper uses "functional-residual-vs-covariate plots." The website should explicitly link these terms to avoid confusion for academic readers.
2.  **Continuous Outcome Support:** While the methodology supports continuous data as a special case, the current `unifend()` implementations in both languages primarily focus on discrete/ordinal models. Adding a generic `Gaussian` family handler would complete the "Unified" promise.
3.  **Cross-Language Testing:** Implement a small suite of shared test cases (e.g., using a fixed seed and simple CSV dataset) to ensure R and Python outputs are identical for the same model/data.
