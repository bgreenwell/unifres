from typing import Any, List, Optional, Union

import numpy as np
from scipy.stats import uniform

from .utils import unifend


class FunctionalResidual:
    """A class representing a functional residual.

    This class provides a robust implementation of the cumulative distribution
    function (CDF) for functional residuals, handling the case where the
    distribution is a point mass (i.e., lower and upper bounds are equal).
    """

    def __init__(self, lwr: float, upr: float):
        self.lwr = lwr
        self.upr = upr
        self.scale = upr - lwr

    def cdf(self, t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculate the cumulative distribution function at t."""
        if self.scale == 0:
            return np.where(t >= self.lwr, 1.0, 0.0)
        
        # Use scipy.stats.uniform for the non-degenerate case
        return uniform.cdf(t, loc=self.lwr, scale=self.scale)

    def rvs(self, size: int = 1) -> np.ndarray:
        """Generate random samples from the functional residual."""
        if self.scale == 0:
            return np.full(size, self.lwr)
        return uniform.rvs(loc=self.lwr, scale=self.scale, size=size)

    def mean(self) -> float:
        """Calculate the mean of the functional residual."""
        return (self.lwr + self.upr) / 2.0


def fresiduals(
    model: Any, type: str = "function", y: Optional[np.ndarray] = None
) -> Union[List[FunctionalResidual], np.ndarray]:
    """Computes functional residuals for a fitted model.

    This function can return the full functional residuals as distribution-like
    objects, or it can return point-based residuals derived from them
    (surrogate or probability-scale).

    Parameters
    ----------
    model : object
        A fitted model object from the statsmodels library.
    type : str, optional
        The type of residual to compute. One of {"function", "surrogate",
        "probscale"}, by default "function".
    y : np.ndarray, optional
        The observed response variable. If not provided, it will be
        extracted from the model object.

    Returns
    -------
    Union[List[FunctionalResidual], np.ndarray]
        - If `type="function"`, a list of `FunctionalResidual` objects,
          one for each observation.
        - If `type="surrogate"` or `type="probscale"`, a NumPy array of
          the calculated point residuals.

    Raises
    ------
    ValueError
        If the specified `type` is not valid.
    """
    uends = unifend(model, y=y)

    # Create a list of functional residual objects
    fres_list = [FunctionalResidual(uend[0], uend[1]) for uend in uends]

    if type == "function":
        return fres_list
    elif type == "surrogate":
        return np.array([f.rvs(1)[0] for f in fres_list])
    elif type == "probscale":
        return np.array([2 * f.mean() - 1 for f in fres_list])
    else:
        raise ValueError(
            "Invalid type. Choose from 'function', 'surrogate', or 'probscale'."
        )
