import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Make sure your project's src directory is in the Python path
# You might run this script from the root of the 'python' directory
# e.g., python -m examples.simple_test
from unifres import fresiduals, fredplot


def run_example():
    """
    Runs a simple logistic regression example to test core functionality.
    """
    # 1. Generate data from a known logistic regression model
    # This matches the example from the original R code.
    print("Generating sample data...")
    np.random.seed(1217)
    n = 1000
    x = np.random.normal(size=n)
    # The true model includes a quadratic term
    z = 1 - 2 * x + 3 * x**2 + np.random.logistic(size=n)
    y = np.where(z > 0, 1, 0)

    # Create a pandas DataFrame
    df = pd.DataFrame({"y": y, "x": x, "x_sq": x**2})
    X_wrong = sm.add_constant(df["x"])
    X_right = sm.add_constant(df[["x", "x_sq"]])

    # 2. Fit two models: one wrong, one right
    print("Fitting models...")
    # Wrong model (misses the quadratic term)
    fit_wrong = sm.GLM(df["y"], X_wrong, family=sm.families.Binomial()).fit()

    # Right model (includes the quadratic term)
    fit_right = sm.GLM(df["y"], X_right, family=sm.families.Binomial()).fit()

    # 3. Create FRED plots for both models
    print("Generating FRED plots...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot for the wrong model
    fredplot(fit_wrong, x=df["x"], lowess=True, ax=axes[0], type="hex")
    axes[0].set_title("Wrong Model (y ~ x)")

    # Plot for the right model
    fredplot(fit_right, x=df["x"], lowess=True, ax=axes[1], type="hex")
    axes[1].set_title("Correct Model (y ~ x + x^2)")

    fig.suptitle("Functional Residual Plots (FRED plots)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_example()
