from ... import dec
from ..Line import line
from .distance import distance
from .point import point
from .quadrant import quadrant

def point_F2pointWdist(A, B, /, *args):
    '''
    point_F2pointWdist(A, B, /, *args)

    point from 2 points with distance

    Return a point of 2 points with a certain distance that is
    on the straight line of the two points. In other words,
    a point lies on a line with a certain distance.

    The method here:
        d = distance(A, B)
        r = dt/d
        C = A + (B-A)*r
    '''
    if type(A) != point:
        point(*A)
    if type(B) != point:
        point(*B)
    if not args:
        return A
    d = distance(A, B)
    tup = tuple((A + (B-A)*(dec(n)/d) for n in args))
    return tup[0] if len(tup) == 1 else tup
