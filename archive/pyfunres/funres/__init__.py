# read version from installed package
# from importlib.metadata import version
# __version__ = version("funres")
__version__ = "0.1.0"

from .unifend import unifend, fresiduals, fredplot

__all__ = ["unifend", "fresiduals", "fredplot"]
