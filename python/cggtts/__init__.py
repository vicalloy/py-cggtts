# Import the native extension
from . import cggtts

# Re-export the parse_cggtts function from the native extension
from .cggtts import parse_cggtts

__doc__ = cggtts.__doc__
__all__ = ["parse_cggtts"]
