from typing import Any, Optional, List, Union

import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

from .utils import unifend, expand_endpoints
from .residuals import fresiduals


def fredplot(
    model: Any,
    x: np.ndarray,
    type: str = "kde",
    lowess: bool = False,
    frac: float = 2 / 3,
    n: Optional[int] = None,
    ax=None,
    **kwargs,
) -> plt.Axes:
    """Create a Functional REsidual Density (FRED) plot.

    This plot shows the density of the functional residuals against a
    continuous predictor variable, which is useful for identifying
    model misspecifications like missing non-linear terms.

    Parameters
    ----------
    model : object
        A fitted model object from statsmodels.
    x : np.ndarray
        The predictor variable to plot on the x-axis.
    type : str, optional
        The type of density plot to generate. One of {"kde", "hex"},
        by default "kde".
    lowess : bool, optional
        If True, add a LOWESS smooth to the plot, by default False.
    frac : float, optional
        The fraction of data used when estimating each y-value of the
        LOWESS smooth, by default 2/3.
    n : int, optional
        The number of observations to subsample, by default None
        (use all).
    ax : matplotlib.axes.Axes, optional
        An existing matplotlib Axes object to plot on. If None, a new
        figure and axes are created.
    **kwargs : dict, optional
        Additional keyword arguments passed to the seaborn plotting function
        (e.g., `sns.kdeplot` or `ax.hexbin`).

    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib Axes object containing the plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    endpoints = unifend(model)

    # Subsample if requested
    if n is not None and n < len(endpoints):
        if len(x) != len(endpoints):
             raise ValueError(
                 f"Length of 'x' ({len(x)}) must match length of model residuals "
                 f"({len(endpoints)}) when subsampling with 'n'."
             )
        indices = np.random.choice(len(endpoints), n, replace=False)
        endpoints = endpoints[indices]
        x = x[indices]

    if len(x) != len(endpoints):
        raise ValueError(
            f"Length of 'x' ({len(x)}) does not match length of model residuals ({len(endpoints)})."
        )

    df = pd.DataFrame(
        {"x": np.repeat(x, 101), "y": expand_endpoints(endpoints, resolution=101)}
    )

    df["y"] = np.where(df["y"] <= 0, 1e-10, df["y"])
    df["y"] = np.where(df["y"] >= 1, 1 - 1e-10, df["y"])

    if type == "kde":
        try:
            sns.kdeplot(data=df, x="x", y="y", ax=ax, **kwargs)
        except AttributeError as e:
            if "'QuadContourSet' object has no attribute 'collections'" in str(e):
                warnings.warn(
                    "A known compatibility issue between seaborn and "
                    "matplotlib was detected. The plot may be incomplete. "
                    "Consider upgrading seaborn and matplotlib.",
                    RuntimeWarning
                )
                # Retry without trying to create a legend, which is often the trigger
                kwargs.pop("label", None)
                sns.kdeplot(data=df, x="x", y="y", ax=ax, **kwargs)
            else:
                raise e

    elif type == "hex":
        # If ax is provided, we use ax.hexbin directly to avoid jointplot figure creation
        gridsize = kwargs.pop("gridsize", 20)
        cmap = kwargs.pop("cmap", "YlGnBu")
        hb = ax.hexbin(df["x"], df["y"], gridsize=gridsize, cmap=cmap, **kwargs)
        # plt.colorbar(hb, ax=ax) # optional
    else:
        raise ValueError("Invalid type. Choose either 'kde' or 'hex'.")

    if lowess:
        smooth = sm.nonparametric.lowess(df["y"], df["x"], frac=frac)
        ax.plot(smooth[:, 0], smooth[:, 1], color="white", linewidth=2)

    ax.set_xlabel(x.name if hasattr(x, "name") else "Predictor")
    ax.set_ylabel("Residual Density")

    return ax


def ffplot(
    model: Any,
    resolution: int = 101,
    n: Optional[int] = None,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """Create a Function-Function (Fn-Fn) plot.

    This plot shows the average of the functional residuals against the
    theoretical CDF of a Uniform(0, 1) random variable.

    Parameters
    ----------
    model : object
        A fitted model object (e.g., from statsmodels) or a list of
        functional residuals.
    resolution : int, optional
        The number of points between 0 and 1 to evaluate, by default 101.
    n : int, optional
        The number of functional residuals to subsample, by default None
        (use all).
    ax : matplotlib.axes.Axes, optional
        An existing matplotlib Axes object to plot on.
    **kwargs : dict, optional
        Additional keyword arguments passed to `ax.plot()`.

    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib Axes object containing the plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    # Get functional residuals
    if isinstance(model, list) and all(hasattr(f, "cdf") for f in model):
        fres = model
    else:
        fres = fresiduals(model, type="function")

    # Subsample if requested
    if n is not None and n < len(fres):
        indices = np.random.choice(len(fres), n, replace=False)
        fres = [fres[i] for i in indices]

    t_vals = np.linspace(0, 1, resolution)
    # Calculate the average CDF value at each t
    avg_cdf = np.mean([f.cdf(t_vals) for f in fres], axis=0)

    ax.plot(t_vals, avg_cdf, **kwargs)
    ax.plot([0, 1], [0, 1], linestyle="--", color="red")  # Reference line

    ax.set_xlabel("t")
    ax.set_ylabel("Average Functional Residual")
    ax.set_title("Function-Function Plot")

    return ax
