# GEMINI.md: `unifres` Project Context

## Project Overview
`unifres` (Unified Residuals) is a cross-platform implementation (R and Python) of the functional residual methodology described in Liu, Lin, & Zhang (2025). It provides a unified diagnostic framework for generalized linear models (GLMs) and beyond, effectively handling both discrete (binary, count, ordinal) and continuous outcomes.

### Main Technologies
- **R Package:** Built using the S3 object system. Key dependencies include `stats`, `MASS`, `mgcv`, `VGAM`, and `pscl`.
- **Python Package:** Uses a modern `src` layout with `hatchling` as the build backend. Core dependencies are `numpy`, `scipy`, `statsmodels`, `matplotlib`, and `seaborn`.
- **Documentation:** A unified documentation site powered by **Quarto**, located in the `docs/` directory.

### Architecture
- **Functional Residuals:** The core logic computes lower and upper cumulative probability bounds for each observation, creating "functional" residuals that follow a Uniform(0,1) distribution under correct model specification.
- **Cross-Language Parity:** Both implementations support Function-Function (Fn-Fn) plots for overall adequacy and Functional Residual Density (FRED) plots for identifying specific misspecifications.

---

## Building and Running

### R Package (`r/unifres`)
The R package uses standard `devtools` workflows.
- **Load Package:** `devtools::load_all("r/unifres")`
- **Run Tests:** `devtools::test("r/unifres")`
- **Generate Docs:** `devtools::document("r/unifres")`
- **Check Package:** `devtools::check("r/unifres")`

### Python Package (`python/`)
The Python package uses `uv` or `pip` for environment management.
- **Install (Editable):** `pip install -e "python/.[dev]"`
- **Run Tests:** `pytest python/tests/ -v --cov=unifres`
- **Build Package:** `hatch build python/`

### Documentation Site
- **Render Site:** `quarto render docs`
- **Preview Site:** `quarto preview docs`

---

## Development Conventions

### R Package
- **S3 Dispatch:** All core functions (`fresiduals`, `fredplot`, `ffplot`, `unifend`) are S3 generics. Ensure new model support is added via specific methods (e.g., `unifend.newclass`).
- **Documentation:** Use **roxygen2** tags. Every exported function must include a `@returns` tag and a `@references` tag pointing to the Liu et al. (2025) paper.
- **Testing:** Use `testthat`. Ensure `link.scale` behavior is explicitly handled in surrogate residual tests.

### Python Package
- **Type Checking:** Use type hints for all function signatures.
- **Model Detection:** Avoid brittle `str(type(model))` checks. Prefer checking `model.__class__.__name__` or verifying attributes like `.model` and `.predict`.
- **Plotting:** All plotting functions (`fredplot`, `ffplot`) must accept an optional `ax` parameter. For `hex` plots, use `ax.hexbin` to allow subplot integration.
- **Warnings:** Use the standard `warnings.warn()` module instead of `print()` for internal library warnings.

### General
- **Functional Parity:** When adding support for a new model family in one language, aim to implement the equivalent in the other to maintain project balance.
- **Audit History:** See `COPILOT_AUDIT.md` for a historical record of significant architectural fixes and logic corrections (March 2026).
