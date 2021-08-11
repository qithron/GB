from .Geometry.Line import *
from .Geometry.Point import *
# from .Geometry.Polygon import *
from time import perf_counter_ns

def timeexe(func, /):
    st = perf_counter_ns()
    fs = eval(func)
    ed = perf_counter_ns()
    print(f'{(ed-st)/10**6} ms elapsed for: {func}')
    return fs

# comment this if not needed
for v in (m for m in dir() if not (m.startswith('_'))): print(f'{v:25} {eval(v)}')

# do other test here
A = timeexe('point()')
B = timeexe('point(2,4)')
AB = timeexe('line(A,B)')
print(AB)
