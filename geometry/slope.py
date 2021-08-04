from .. import decimal, dec
from .point import point

def slope(A, B, /):
    '''Calculating slope from 2 point.'''
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
