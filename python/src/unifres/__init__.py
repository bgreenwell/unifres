"""A unified framework for residual diagnostics in generalized linear models and beyond."""

__version__ = "0.1.0"

from .residuals import fresiduals
from .plots import fredplot, ffplot

# This controls what `from unifres import *` does
__all__ = ["fresiduals", "fredplot", "ffplot"]
