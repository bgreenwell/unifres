import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

from scipy.stats import poisson, Uniform


def is_fitted(model):
    """
    Check if the model is fitted by trying to access its parameters.

    Parameters
    ----------
    model : object
        The model to check.

    Returns
    -------
    bool
        True if the model is fitted, False otherwise.
    """
    try:
        model.params
        return True
    except AttributeError:
        return False


def unifend(model, y=None):
    """
    Get the endpoints of the predicted probabilities for an ordinal model.

    Parameters
    ----------
    model : statsmodels model
        The fitted ordinal model from statsmodels.
    y : np.ndarray, optional
        The observed response variable. If not provided, it will be extracted
        from the model.

    Returns
    -------
    np.ndarray
        The endpoints of the predicted probabilities for each observation.
    """
    typename = str(type(model))
    if "statsmodels" not in typename:
        raise ValueError("This function is only implemented for statsmodels models.")

    # Get the observed response values if not provided
    if y is None:
        y = model.model.endog

    # Ordinal models ----------------------------------------------------------
    if "ordinal_model" in typename:
        fv = model.predict()
        fv = np.hstack((np.zeros((fv.shape[0], 1)), fv))
        cumprobs = np.cumsum(fv, axis=1)
        lwr = cumprobs[np.arange(cumprobs.shape[0]), y]
        upr = cumprobs[np.arange(cumprobs.shape[0]), y + 1]
    # Binary models -----------------------------------------------------------
    elif "BinaryResultsWrapper" in typename:
        fv = model.predict()
        lwr = np.where(y == 1, 1 - fv, 0)
        upr = np.where(y == 1, 1, 1 - fv)
    # Poisson models ----------------------------------------------------------
    elif "PoissonResultsWrapper" in typename:
        fv = model.predict()
        lwr = poisson.cdf(y - 1, mu=fv)
        upr = poisson.cdf(y, mu=fv)
    else:
        raise ValueError("Model type not recognized.")
    return np.column_stack((lwr, upr))


def expand(endpoints, resolution=101, flat=False):
    """
    Expand the endpoints to a specified resolution.

    Parameters
    ----------
    endpoints : np.ndarray
        The endpoints to expand.
    resolution : int
        The resolution to expand to.
    flat : bool
        If True, return a flat array. If False, return a 2D array.

    Returns
    -------
    np.ndarray
        The expanded endpoints.

    Note
    ----
    The expanded endpoints are created by linearly interpolating between the
    lower and upper bounds of the endpoints. This is a convenience function
    not meant for external use.
    """
    z = np.zeros((endpoints.shape[0], resolution))
    for i in range(resolution):
        z[:, i] = (
            endpoints[:, 0] + (endpoints[:, 1] - endpoints[:, 0]) / (resolution - 1) * i
        )
    if flat:
        z = z.flatten()
    return z


def fredplot(
    model,
    x,
    type="kde",
    lowess=False,
    frac=2 / 3,
    color="white",
    linewidth=2,
    linestyle="solid",
    **kwargs,
):
    """
    Create a FRED plot for the given model and data.

    Parameters
    ----------
    model : statsmodels model
        The fitted ordinal model.
    x : np.ndarray
        The predictor variable.
    type : str, optional
        The type of plot to generate. Either "kde" (default) or "hex".
    lowess : bool, optional
        If True, add a LOWESS smooth to the plot.
    frac : float, optional
        Between 0 and 1. The fraction of the data used when estimating each
        y-value of the LOWESS smooth.
    color : str, optional
        The color of the LOWESS smooth.
    linewidth : float, optional
        The width of the LOWESS smooth.
    linestyle : str, optional
        The style of the LOWESS smooth.
    **kwargs : dict, optional
        Additional keyword arguments to pass to the primary plotting function
        (i.e., sns.kdeplot(), sns.jointplot(), or sns.histplot()).

    Returns
    -------
    None
    """
    endpoints = unifend(model)
    df = pd.DataFrame({"x": np.repeat(x, 101), "y": expand(endpoints, flat=True)})
    df["y"] = np.where(df["y"] == 0, 1e-10, df["y"])
    df["y"] = np.where(df["y"] == 1, 1 - 1e-10, df["y"])

    if type == "kde":
        sns.kdeplot(data=df, x="x", y="y", **kwargs)
    elif type == "hex":
        g = sns.jointplot(data=df, x="x", y="y", kind="hex", **kwargs)
        g.ax_marg_x.remove()
        g.ax_marg_y.remove()
    elif type == "hist":
        sns.histplot(data=df, x="x", y="y", **kwargs)
    else:
        raise ValueError("Invalid type. Choose either 'kde' or 'hex'.")

    if lowess:
        smooth = sm.nonparametric.lowess(df["y"], df["x"], frac=frac)
        plt.plot(
            smooth[:, 0],
            smooth[:, 1],
            color=color,
            linewidth=linewidth,
            linestyle=linestyle,
        )
        # plt.plot(smooth[:, 0], smooth[:, 1], **line_kws)

    plt.xlabel("x")
    plt.ylabel("Residual")
    plt.show()


def fresiduals(model, type="function", y=None):
    uends = unifend(model, y=y)
    unifs = [Uniform(a=uend[0], b=uend[1]) for uend in uends]

    if type == "function":
        return unifs
    elif type == "surrogate":
        return [unif.sample(1)[0] for unif in unifs]
    elif type == "probscale":
        return [2 * unif.mean() - 1 for unif in unifs]
    else:
        raise ValueError(
            "Invalid type. Choose from 'function', 'probability', or 'cumulative'."
        )
