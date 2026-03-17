# Contributing to unifres

Thank you for considering contributing to **unifres**! We welcome contributions from the community, whether they're bug reports, feature requests, documentation improvements, or code contributions.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, data samples)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (R/Python version, OS, package versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any related packages** that implement similar features

### Pull Requests

1. Fork the repository and create your branch from `main`
2. Make your changes in your fork
3. Add tests for any new functionality
4. Ensure all tests pass
5. Update documentation as needed
6. Submit a pull request

## Development Setup

### For R Package Development

```r
# Install development dependencies
install.packages(c("devtools", "testthat", "roxygen2", "covr"))

# Clone and navigate to R package
git clone https://github.com/bgreenwell/unifres.git
cd unifres/r/unifres

# Load package for development
devtools::load_all()

# Run tests
devtools::test()

# Check package
devtools::check()

# Generate documentation
devtools::document()
```

### For Python Package Development

```bash
# Clone repository
git clone https://github.com/bgreenwell/unifres.git
cd unifres/python

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Or using uv (recommended)
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=unifres --cov-report=html
```

## Coding Standards

### R Code Style

- Follow the [tidyverse style guide](https://style.tidyverse.org/)
- Use `<-` for assignment (not `=`)
- Maximum line length: 80 characters
- Use roxygen2 for documentation
- All exported functions must have examples
- Use `testthat` for testing

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black default)
- Use NumPy-style docstrings
- Use `pytest` for testing

### Documentation

- R: Use roxygen2 comments with examples
- Python: Use NumPy-style docstrings
- Update NEWS.md for user-facing changes
- Add examples for new features
- Update README.md if adding major features

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Include edge cases and error conditions
- Use descriptive test names that explain what is being tested

## Testing Guidelines

### R Testing

```r
# Run all tests
devtools::test()

# Run tests with coverage
covr::report()

# Run specific test file
testthat::test_file("tests/testthat/test-fresiduals.R")
```

### Python Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=unifres --cov-report=term --cov-report=html

# Run specific test file
pytest tests/test_residuals.py -v

# Run specific test
pytest tests/test_residuals.py::TestResiduals::test_poisson_glm -v
```

## Commit Messages

- Use clear and descriptive commit messages
- Start with a verb in present tense ("Add", "Fix", "Update")
- Keep the first line under 50 characters
- Add detailed description if needed after a blank line

Examples:
```
Add support for beta regression models

Implements fresh residuals and diagnostic plots for beta
regression models using the betareg package.
```

```
Fix edge case in fredplot with zero counts

Handles the case where all residuals are exactly zero,
which previously caused a division by zero error.
```

## Pull Request Process

1. **Update Documentation**: Ensure any new functionality is documented
2. **Add Tests**: Include tests that cover your changes
3. **Pass CI**: All CI checks must pass (R CMD check, Python tests, coverage)
4. **Update NEWS**: Add an entry to NEWS.md describing your changes
5. **Request Review**: Assign reviewers or wait for maintainer review

### PR Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added and passing
- [ ] No decrease in code coverage
- [ ] NEWS.md updated
- [ ] All CI checks passing

## Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Questions?

Feel free to open an issue with your question or contact the maintainers:

- Brandon Greenwell: greenwell.brandon@gmail.com
- GitHub Issues: https://github.com/bgreenwell/unifres/issues

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (GPL-3 or later).

---

Thank you for contributing to unifres! 🎉
