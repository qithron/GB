from ... import decimal, DC, dec
from ..Line import line
from .point import point

def distance(A, B, /):
    '''
    distance(A, B, /)

    Distance point/line to point/line.

    Point-Point:
        (x₁, y₁)
        (x₂, y₂)
            d = √(x₂ - x₁)² + (y₂ - y₁)²

    Point-Line:
        (x₀, y₀)
        ax + by + c = 0
            d = |ax₀ + by₀ + c| / √a²+b², m ≠ 0 or m ≠ ∞
            d = |by₀ + c| / |b|, a = 0
            d = |ax₀ + c| / |a|, b = 0
            Point on the line closest to (x₀, y₀):
                x' = (b(bx₀ - ay₀) - ac) / (a²+b²)
                y' = (a(ay₀ - bx₀) - bc) / (a²+b²)

    Line-Line:
        ax + by + c₁ = 0
        ax + by + c₂ = 0
            d = |c₂ - c₁| / √a²+b²
        y = mx + b₁
        y = mx + b₂
            d = |b₂ - b₁| / √m²+1
    '''
    if type(A) == line == type(B):
        if 0 == A.a == A.b == B.a == B.b:
            return None
        if A.m == B.m:
            d = abs(A.c - B.c) / DC.sqrt(DC.power(A.a, 2) + DC.power(A.b, 2))
        else:
            d = dec()
    elif type(A) == line or type(B) == line:
        P, L = (A, B) if type(B) == line else (B, A)
        if 0 == L.a == L.b:
            return None
        a, b, c = L
        x, y = P
        if a == 0:
            d = abs(b*y + c) / abs(b)
        elif b == 0:
            d = abs(a*x + c) / abs(a)
        else:
            d = abs(a*x + b*y + c)\
              / abs(DC.sqrt(DC.power(a, 2) + DC.power(b, 2)))
    else:
        x1, y1 = A if type(A) == point else point(*A)
        x2, y2 = B if type(B) == point else point(*B)
        if x1 == x2 and y1 == y2:
            d = dec()
        elif x1 != x2 and y1 == y2:
            d = abs(x1 - x2)
        elif x1 == x2 and y1 != y2:
            d = abs(y1 - y2)
        else:
            d = DC.sqrt(DC.power(x2-x1, 2) + DC.power(y2-y1, 2))
    return d.normalize()
