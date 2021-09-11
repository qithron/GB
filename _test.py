from .Geometry import *

# all func/class
#for v in (v for v in dir() if not v.startswith('_')): print(v)

A = point()
B = point(5, 6)
C = point(-4, 3)

print(f'A : {A}')
print(f'B : {B}')
print(f'C : {C}')
print(f'type(B), type(C) : {type(B)}, {type(C)}')
print(f'B + C: {B + C}')

ab = line(A, B)
print('line ab:', ab)

print()
p = polygon_Fpoints(A, B, C)
print(p)
print('\noutput visual untuk Geogebra:')
print(p.geogebra())
