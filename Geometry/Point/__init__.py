# why must be at the top? if not, it become module object
# rather than class object as i expect
from .point import point

from .distance import distance
from .intersect import intersect
from .midpoint import midpoint
from .point_F2pointWdist import point_F2pointWdist
from .quadrant import quadrant

# __all__ = [m for m in dir() if not m.startswith('_')]
