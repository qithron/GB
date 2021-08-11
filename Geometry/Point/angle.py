from ... import dec
from .point import point
from math import atan2, pi

def angle(A, B, C, /):
    '''
    angle(A, B, C, /):

    Returns angle B in radian.
    '''
    if type(A) != point: point(*A)
    if type(B) != point: point(*B)
    if type(C) != point: point(*C)
    # if B == A or B == C: # ??? None or 0°
        # return None
    A -= B
    C -= B
    a = dec(atan2(A.y, A.x))
    c = dec(atan2(C.y, C.x))
    if a < 0: a += dec(pi)*2
    if c < 0: c += dec(pi)*2
    return (dec(pi)*2 + c - a) if a > c else (c - a)
