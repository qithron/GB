from .. import DC, dec
from .line import line
from .point import point

def perpendicular(O, L, /):
    '''
    perpendicular(O, L, /):

    Return a perpendicular line.
    First argument can be a point, line or sequence types.
    Second argument must be a line.
    '''
    if type(L) != line:
        raise TypeError(f'Second argument must be a {line}')
    if type(O) != point and type(O) != line:
        P = point(*O)
    elif type(O) == point:
        P = O
    elif type(O) == line:
        P = O.P
    else:
        raise TypeError(
            f'First argument must be a {point}, {line} or sequence types')
    if L.m.is_infinite():
        m = dec().copy_sign(-L.m)
    else:
        m = DC.divide(*L.m.as_integer_ratio()[::-1]).copy_sign(-L.m)\
            if L.m else None
    return line(P, m=m)
