from .line import line
from .point import point

def linear(O, L, /):
    '''\
    Return a linear line.
    First argument can be a point, line or sequence types.
    Second argument must be a line.
    '''
    if type(L) != line:
        raise TypeError(f'Second argument must be a {line}')
    if type(O) != point and type(O) != line:
        P = point(*O)
    elif type(O) == line:
        P = O.P
    elif type(O) == point:
        P = O
    else:
        raise TypeError(
            f'First argument must be a {point}, {line} or sequence types')
    return line(P, m=L.m)
