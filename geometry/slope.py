from .. import decimal, dec
from .point import point

def slope(A, B, /):
    '''
    slope(A, B, /):

    Slope of 2 points. use line.m for line slope instead.
    '''
    if type(A) != point:
        A = point(*A)
    if type(B) != point:
        B = point(*B)
    if A == B:
        return None
    x1, y1 = A
    x2, y2 = B
    with decimal.localcontext() as ctx:
        ctx.traps[decimal.DivisionByZero] = False
        m = (y2 - y1)/(x2 - x1)
    return m.normalize()
