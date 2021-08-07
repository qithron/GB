from ... import decimal, dec
from ..Point import point

def slope(A, B, /):
    '''
    slope(A, B, /):

    Slope of 2 points. Use line.m for slope of line object instead.
    '''
    x1, y1 = A if type(A) == point else point(*A)
    x2, y2 = B if type(B) == point else point(*B)
    if x1 == x2 and y1 == y2:
        return None
    with decimal.localcontext() as ctx:
        ctx.traps[decimal.DivisionByZero] = False
        m = (y2 - y1)/(x2 - x1)
    return m.normalize()
