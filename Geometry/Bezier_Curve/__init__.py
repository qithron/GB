'''
Bezier Curve.
Based on https://en.wikipedia.org/wiki/B%C3%A9zier_curve

Bezier Curve Linear
    (1-𝓉)P₀ + 𝓉P₁, 0 <= 𝓉 <= 1
    (1-t)*P0 + t*P1

Bezier Curve Quadratic
    (1-𝓉)²P₀ + 2(1-𝓉)𝓉P₁ + 𝓉²P₂, 0 <= 𝓉 <= 1
    (1-t)**2*P0 + 2*(1-t)*t*P1 + t**2*P2

Bezier Curve Cubic
    (1-𝓉)³P₀ + 3(1-𝓉)²𝓉P₁ + 3(1-𝓉)𝓉²P₂ + 𝓉³P₃, 0 <= 𝓉 <= 1
    (1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3
'''

from .cubic import bcc
from .linear import bcl_v4 as bcl
from .quadratic import bcq
