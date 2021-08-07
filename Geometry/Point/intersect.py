from ... import decimal, dec
from ..Line import line
from .point import point

def intersect(A, B, /):
    '''
    intersect(A, B, /)

    Intersect of 2 lines:
        a₁x + b₁y + c₁ = 0
        a₂x + b₂y + c₂ = 0
            x' = (c₁b₂ - c₂b₁) / (a₁b₂ - a₂b₁)
            y' = (a₁c₂ - a₂c₁) / (a₁b₂ - a₂b₁)
    '''
    if type(A) == line == type(B):
        a1, b1, c1 = dec((A.a, A.b, -A.c))
        a2, b2, c2 = dec((B.a, B.b, -B.c))
        x = (c1*b2 - c2*b1)
        y = (a1*c2 - a2*c1)
        n = (a1*b2 - a2*b1)
        if n == 0 == x == y:
            return dec('inf')
        elif n == 0:
            return None
        return point(x/n, y/n)
    else:
        raise TypeError(
            f'both of arguments must be a {line} only')
