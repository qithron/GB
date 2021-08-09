from ... import dec
from ..Line import line, ray, perpendicular
from .distance import distance
from .intersect import intersect
from .point import point
from .quadrant import quadrant
from math import acos, pi

def angle(A, B, C, /):
    '''
    angle(A, B, C, /):

    Returns angle B in radian.

    note:
        angle(P, Q, R) != angle(R, Q, P)
    '''
    # this code maybe too long and not efficient :(
    # but, i think its better to avoid complicated calculations
    # and, i think too, this is advantages using algorithm vs math formula
    # or not?
    if type(A) != point:
        point(*A)
    if type(B) != point:
        point(*B)
    if type(C) != point:
        point(*C)
    if B == A or B == C:
        return None
    A-=B ; C-=B ; B-=B
    qa, qc = quadrant(A), quadrant(C)
    if qa.q < 0 and qc.q < 0:
        if qa == qc+2:
            return dec(pi) # 180°
        if qa == qc+1:
            return dec(pi) + dec(pi)/2 # 270°
        if qa == qc-1:
            return dec(pi)/2 # 90°
        if qa == qc:
            return dec() # 0°
    BA = line(B, A)
    BC = line(B, C)
    AC = perpendicular(A, BA)
    CA = perpendicular(C, BA)
    IA = intersect(BC, AC)
    IC = intersect(BA, CA)
    if IC in ray(B, A):
        return dec() # 0°
    elif IC in BA:
        return dec(pi) # 180°
    if qa < 0 or qc < 0: # one of them lies in axis
        j, k, s = (qc, qa, False) if qa < 0 else (qa, qc, True)
        if j == 5 + k:
            if s: ang = lambda x: dec(pi)*2 - dec(x)
            else: ang = lambda x: dec(x)
        elif j == 5 + (k+1):
            if s: ang = lambda x: dec(pi) + dec(x)
            else: ang = lambda x: dec(pi) - dec(x)
        elif j == 5 + (k+2):
            if s: ang = lambda x: dec(pi) - dec(x)
            else: ang = lambda x: dec(pi) + dec(x)
        elif j == 5 + (k+3):
            if s: ang = lambda x: dec(x)
            else: ang = lambda x: dec(pi)*2 - dec(x)
    else:
        if qa == 1:
            if qc == 1:
                ang = lambda x: dec(x)
            s = IC in ray(B, A)
            if qc == 2:
                if s: ang = lambda x: dec(x)
                else: ang = lambda x: dec(pi) - dec(x)
            else qc == 3:
    print(qa, qc, end=' | ', sep=' | ')
    if IA == None:
        return ang(90)
    if distance(B, IC) < distance(B, A):
        samping = distance(B, IC)
        miring = distance(B, C)
    else:
        samping = distance(B, A)
        miring = distance(B, IA)
    assert IA != dec('inf'), f'{A}, {B}, {C}'
    return ang(acos(samping/miring))
