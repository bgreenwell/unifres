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
The R package uses standard `devtools` workflows. All commands should be run from the project root:

```r
# Load package for interactive development
devtools::load_all("r/unifres")

# Run tests
devtools::test("r/unifres")

# Regenerate documentation from roxygen2 comments
devtools::document("r/unifres")

# Run R CMD check (includes tests, documentation checks, etc.)
devtools::check("r/unifres")

# Install package locally
devtools::install("r/unifres")
```

### Python Package (`python/`)
The Python package uses `uv` for environment management. The virtual environment is located at `python/.venv`.

**Initial setup:**
```bash
cd python
uv venv                         # Create virtual environment
uv pip install -e ".[dev]"      # Install package in editable mode with dev dependencies
```

**Development workflow:**
```bash
# Activate virtual environment (if needed)
source python/.venv/bin/activate  # On macOS/Linux
# or
python\.venv\Scripts\activate     # On Windows

# Run tests
pytest python/tests/ -v --cov=unifres

# Run tests from project root (without activating venv)
python/.venv/bin/pytest python/tests/ -v --cov=unifres

# Build package
cd python
hatch build

# Update dependencies
uv pip install -e ".[dev]" --upgrade
```

### Documentation Site
The documentation site is built with Quarto.

**Render documentation:**
```bash
# Render all documentation
cd docs
quarto render

# Preview documentation locally
quarto preview

# Render with specific Python environment
export QUARTO_PYTHON="python/.venv/bin/python"
quarto render docs --execute
```

**Important notes:**
- **Python Examples:** Python examples are maintained in `docs/examples-python.ipynb` (Jupyter Notebook) instead of `.qmd` to ensure reliable figure capture by the Jupyter engine.
- **R Examples:** R examples are in `docs/examples-r.qmd` and render using the installed R package.
- **No hybrid files:** R and Python examples are kept separate. There is no quickstart file mixing both languages.
- **Subsampling:** When working with large datasets in examples, use the `n` parameter in `ffplot` and `fredplot` (e.g., `n=1000`) to keep rendering times manageable.

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
