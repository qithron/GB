from ..Point import point
from .line import line

def linear(O, L, /):
    '''
    linear(O, L, /):

    Return a linear line.
    First argument can be a point, line or sequence types.
    Second argument must be a line.
    '''
    if type(L) != line:
        raise TypeError(
            f'second argument must be a {line} only')
    if type(O) != point and type(O) != line:
        P = point(*O)
    elif type(O) == line:
        P = O.P
    elif type(O) == point:
        P = O
    else:
        raise TypeError(
            f'first argument must be a {point}, a {line} or sequence types')
    return line(P, m=L.m)
