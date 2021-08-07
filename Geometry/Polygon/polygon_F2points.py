from ... import dec
from ..Line import slope
from ..Point import distance, quadrant
from .polygon import polygon
from math import pi, acos, cos, sin

def polygon_F2points(A, B, /, w=1):
    '''
    polygon_F2points(A, B, /, w=1)
    
    polygon from 2 points

    Return a polygon object from 2 given point and width, aka rectangle.

    rotating (x,y) with center point (a,b) and v° rotating angle:
        x' = a + (x-a) * cos(v°) – (y-b) * sin(v°)
        y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
    '''
    if len(P) != 2:
        raise IndexError \
            (f'argument take 2 items but {len(P)} were given')
    if A == B:
        return None
    m = slope(A, B)
    wid = dec(w)/2
    Ax, Ay = dec(A)
    Bx, By = dec(B)
    if m == 0 or m.is_infinite():
        j, k, s = ('x', 'y', False) if m == 0 else ('y', 'x', True)
        v = False if A[j] - B[j] > 0 else True
        q1, q2, q3, q4 = A[k]-wid, B[k]-wid, B[k]+wid, A[k]+wid
        if s:
            if v: a, b, c, d = (q4,Ay), (q3,By), (q2,By), (q1,Ay)
            else: a, b, c, d = (q1,Ay), (q2,By), (q3,By), (q4,Ay)
        else:
            if v: a, b, c, d = (Ax,q1), (Bx,q2), (Bx,q3), (Ax,q4)
            else: a, b, c, d = (Ax,q4), (Bx,q3), (Bx,q2), (Ax,q1)
    else:
        q = quadrant(B)
        if q == 1:
            C = Bx, Ay
            x0, y0 = Ax+wid, Ay
            x1, y1 = Bx-wid, By
        elif q == 2:
            C = Ax, By
            x0, y0 = Ax, Ay+wid
            x1, y1 = Bx, By-wid
        elif q == 3:
            C = Bx, Ay
            x0, y0 = Ax-wid, Ay
            x1, y1 = Bx+wid, By
        elif q == 4:
            C = Ax, By
            x0, y0 = Ax, Ay-wid
            x1, y1 = Bx, By+wid
        an = dec(acos(distance(A,C)/distance(A,B)))
        an0, an1 = an-dec(pi)/2, an+dec(pi)/2
        a = Ax + (x0-Ax) * dec(cos(an0)) - (y0-Ay) * dec(sin(an0)),\
            Ay + (x0-Ax) * dec(sin(an0)) + (y0-Ay) * dec(cos(an0))
        b = Bx + (x1-Bx) * dec(cos(an1)) - (y1-By) * dec(sin(an1)),\
            By + (x1-Bx) * dec(sin(an1)) + (y1-By) * dec(cos(an1))
        c = Bx + (x1-Bx) * dec(cos(an0)) - (y1-By) * dec(sin(an0)),\
            By + (x1-Bx) * dec(sin(an0)) + (y1-By) * dec(cos(an0))
        d = Ax + (x0-Ax) * dec(cos(an1)) - (y0-Ay) * dec(sin(an1)),\
            Ay + (x0-Ax) * dec(sin(an1)) + (y0-Ay) * dec(cos(an1))
    return polygon(a, b, c, d)
