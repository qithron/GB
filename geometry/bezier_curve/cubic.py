'''Bezier Curve Cubic
(1-𝓉)³P₀ + 3(1-𝓉)²𝓉P₁ + 3(1-𝓉)𝓉²P₂ + 𝓉³P₃, 0 <= 𝓉 <= 1
(1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3
'''

from ... import RD

def bcc_simple(P0, P1, P2, P3, step=100):
    return tuple([(
        round((1-n/step)**3*P0[0] + 3*(1-n/step)**2*(n/step)*P1[0]
        + 3*(1-n/step)*(n/step)**2*P2[0] + (n/step)**3*P3[0], RD),
        round((1-n/step)**3*P0[1] + 3*(1-n/step)**2*(n/step)*P1[1]
        + 3*(1-n/step)*(n/step)**2*P2[1] + (n/step)**3*P3[1], RD))
        for n in range(0, step+1)])

def bcc():
    pass