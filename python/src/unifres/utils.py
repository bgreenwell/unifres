from typing import Any, Optional

import numpy as np
from scipy.stats import poisson, nbinom


def is_fitted(model: Any) -> bool:
    """Check if a model object has been fitted.

    This is determined by checking for the presence of a `params` attribute.

    Parameters
    ----------
    model : object
        The model object to check.

    Returns
    -------
    bool
        True if the model appears to be fitted, False otherwise.
    """
    return hasattr(model, "params")


def unifend(model: Any, y: Optional[np.ndarray] = None) -> np.ndarray:
    """Calculate the endpoints of the uniform residual distributions.

    For each observation, this function computes the lower and upper bounds of
    the predicted cumulative distribution function, P(Y < y) and P(Y <= y).

    Parameters
    ----------
    model : object
        A fitted model object from the statsmodels library.
    y : np.ndarray, optional
        The observed response variable. If not provided, it will be
        extracted from the model object.

    Returns
    -------
    np.ndarray
        An (n x 2) array where n is the number of observations. Each row
        contains the [lower, upper] endpoint for a residual's uniform
        distribution.

    Raises
    ------
    ValueError
        If the model type is not a recognized statsmodels model.
    """
    # Basic check for statsmodels results object
    if not hasattr(model, "model") or not hasattr(model, "predict"):
        raise ValueError("This function expects a fitted statsmodels results object.")

    if y is None:
        y = np.asarray(model.model.endog)
    else:
        y = np.asarray(y)
        if len(y) != len(model.fittedvalues):
            raise ValueError(
                f"Length of 'y' ({len(y)}) does not match model fitted values ({len(model.fittedvalues)})."
            )

    class_name = model.__class__.__name__

    # Ordinal models (statsmodels.miscmodels.ordinal_model.OrderedResults)
    if "OrderedResults" in class_name or "OrderedModel" in class_name:
        fv = model.predict()
        fv = np.hstack((np.zeros((fv.shape[0], 1)), fv))
        cumprobs = np.cumsum(fv, axis=1)
        lwr = cumprobs[np.arange(cumprobs.shape[0]), y]
        upr = cumprobs[np.arange(cumprobs.shape[0]), y + 1]

    # GLM results
    elif "GLMResults" in class_name:
        family_name = model.model.family.__class__.__name__
        fv = model.predict()
        if family_name == "Binomial":
            lwr = np.where(y == 1, 1 - fv, 0)
            upr = np.where(y == 1, 1, 1 - fv)
        elif family_name == "Poisson":
            lwr = poisson.cdf(y - 1, mu=fv)
            upr = poisson.cdf(y, mu=fv)
        elif family_name == "NegativeBinomial":
            alpha = getattr(model.model.family, "alpha", None)
            if alpha is None:
                # Some versions might store it differently
                raise ValueError("Could not find 'alpha' for NegativeBinomial GLM.")
            size = 1.0 / alpha
            prob = size / (size + fv)
            lwr = nbinom.cdf(y - 1, n=size, p=prob)
            upr = nbinom.cdf(y, n=size, p=prob)
        else:
            raise ValueError(f"GLM family not supported: {family_name}")

    # Negative Binomial (Discrete)
    elif "NegativeBinomialResults" in class_name:
        fv = model.predict()
        # For Discrete NegativeBinomial, alpha is typically a separate parameter
        # but statsmodels provides it in different ways depending on version
        if hasattr(model, "alpha"):
            alpha = model.alpha
        else:
            # Fallback to last parameter as a last resort
            alpha = model.params[-1]
        size = 1.0 / alpha
        prob = size / (size + fv)
        lwr = nbinom.cdf(y - 1, n=size, p=prob)
        upr = nbinom.cdf(y, n=size, p=prob)

    # Logit/Probit results
    elif "BinaryResults" in class_name or "LogitResults" in class_name or "ProbitResults" in class_name:
        fv = model.predict()
        lwr = np.where(y == 1, 1 - fv, 0)
        upr = np.where(y == 1, 1, 1 - fv)

    else:
        # Final attempt: try to infer from family if it exists
        if hasattr(model.model, "family"):
             # delegate to GLM-like logic
             family_name = model.model.family.__class__.__name__
             fv = model.predict()
             if family_name == "Binomial":
                 lwr = np.where(y == 1, 1 - fv, 0)
                 upr = np.where(y == 1, 1, 1 - fv)
             elif family_name == "Poisson":
                 lwr = poisson.cdf(y - 1, mu=fv)
                 upr = poisson.cdf(y, mu=fv)
             else:
                 raise ValueError(f"Model class '{class_name}' with family '{family_name}' not supported.")
        else:
            raise ValueError(f"Model class not recognized: {class_name}")

    return np.column_stack((lwr, upr))


def expand_endpoints(endpoints: np.ndarray, resolution: int = 101) -> np.ndarray:
    """Expand endpoint pairs into a series of points for plotting.

    This is an internal convenience function used for creating density plots.

    Parameters
    ----------
    endpoints : np.ndarray
        An (n x 2) array of [lower, upper] endpoints.
    resolution : int, optional
        The number of points to interpolate between each endpoint pair,
        by default 101.

    Returns
    -------
    np.ndarray
        A flattened 1D array of the interpolated points.
    """
    z = np.zeros((endpoints.shape[0], resolution))
    for i in range(resolution):
        z[:, i] = (
            endpoints[:, 0] + (endpoints[:, 1] - endpoints[:, 0]) / (resolution - 1) * i
        )
    return z.flatten()
