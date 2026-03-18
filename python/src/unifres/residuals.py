from typing import Any, List, Optional, Union

import numpy as np
from scipy.stats import uniform

from .utils import unifend


def fresiduals(
    model: Any, type: str = "function", y: Optional[np.ndarray] = None
) -> Union[List[Any], np.ndarray]:
    """Computes functional residuals for a fitted model.

    This function can return the full functional residuals as distribution
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
    Union[List[Any], np.ndarray]
        - If `type="function"`, a list of `scipy.stats.uniform` objects,
          one for each observation.
        - If `type="surrogate"` or `type="probscale"`, a NumPy array of
          the calculated point residuals.

    Raises
    ------
    ValueError
        If the specified `type` is not valid.
    """
    uends = unifend(model, y=y)

    # Create a list of frozen uniform distribution objects
    unifs = [uniform(loc=uend[0], scale=uend[1] - uend[0]) for uend in uends]

    if type == "function":
        return unifs
    elif type == "surrogate":
        return np.array([unif.rvs(1)[0] for unif in unifs])
    elif type == "probscale":
        return np.array([2 * unif.mean() - 1 for unif in unifs])
    else:
        raise ValueError(
            "Invalid type. Choose from 'function', 'surrogate', or 'probscale'."
        )
