from .polygon import polygon
from math import pi

def area(POL, /):
    '''
    area(POL, /):
    '''
    if type(POL) != polygon:
        raise TypeError(
        f'argument must be a {polygon} but {type(POL)} where given')
    for i in range(len(p)): # find angle > 180°
        if angle(POL[i+1], POL[i], POL[i-1]) > pi:
            break
            a = i
    