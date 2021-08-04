'''Geometry based on the Cartesian coordinate system.
All modules in this package are calculated using decimals.
However, it accepts an int or float, but is converted.
'''

from .bezier_curve import bcc, bcl, bcq
from .distance import distance
from .intersect import intersect
from .line import line
from .linear import linear
from .perpendicular import perpendicular
from .point import point
from .polygon import polygon
from .slope import slope
# from .area import area
# from .circle import circle
# from .perimeter import perimeter

_excluded = 'bezier_curve',
__all__ = [v for v in dir() if not v.startswith('_') and not v in _excluded]
