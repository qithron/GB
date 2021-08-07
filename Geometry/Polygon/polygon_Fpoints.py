from ... import dec
from ..Line import line, slope
from ..Point import point, intersect, point_F2pointWdist
from .polygon import polygon
from .polygon_F2points import polygon_F2points
from math import cos, sin, pi

def polygon_Fpoints(*P, w=1, smooth=False, level=None):
    '''
    polygon_Fpoints(*P, w=1, smooth=False, level=None)

    polygon from points

    Create new polygon object from 2 points or more with given width.

    rotating (x, y) with center point (a, b) and v° rotating angle:
        x' = a + (x-a) * cos(v°) - (y-b) * sin(v°)
        y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
    '''
    if smooth or level:
        raise SystemExit('not yet')
    if len(P) < 2:
        raise IndexError \
            (f'argument take at least 2 items but {len(P)} were given')
    elif len(P) == 2:
        return polygon_F2points(*P, w=w)
    if P.count(P[0]) == len(P):
        return None
    PT = iter(P)
    A, B = next(PT), next(PT)
    def valB():
        nonlocal B
        while PT.__length_hint__() and A == B:
            B = next(PT)
            if A != B:
                return None
        return True
    valB()
    def func(A, B):
        m = slope(A, B)
        a, b = point(*A)
        x, y = point_F2pointWdist(A, B, wid)
        ang = -dec(pi)/2
        P = a + (x-a) * dec(cos(ang)) - (y-b) * dec(sin(ang)),\
            b + (x-a) * dec(sin(ang)) + (y-b) * dec(cos(ang))
        ang = -ang
        Q = a + (x-a) * dec(cos(ang)) - (y-b) * dec(sin(ang)),\
            b + (x-a) * dec(sin(ang)) + (y-b) * dec(cos(ang))
        return line(P, m=m), line(Q, m=m)
    wid = dec(w)/2
    la0, la1 = func(A, B)
    ls0, ls1 = [la0.P], [la1.P]
    while True:
        A = B
        if valB():
            break
        lb1, lb0 = func(B, A)
        ls0.append(intersect(la0, lb0))
        ls1.append(intersect(la1, lb1))
        la0, la1 = lb0, lb1
    ls0.append(la0.P)
    ls1.append(la1.P)
    return polygon(*ls0, *reversed(ls1))
