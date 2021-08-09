from ... import dec
from ..Bezier_Curve import bcl
from ..Point import point

class polygon:
    '''
    polygon(P0, P1, P2, /, *Pn)
    '''
    __slots__ = 'points',

    def __init__(self, P0, P1, P2, /, *Pn):
        tmp = (e if type(e) == point else point(*e)
               for e in [P0,P1,P2] + list(Pn))
        self.points = tuple(tmp)
    ###########################################################################
    def __call__(self, /):
        return self.points

    def __str__(self, /):
        return f'polygon{self.points}'

    def __repr__(self, /):
        return f'polygon{self.points}'
    ###########################################################################
    def __iter__(self, /):
        return iter(self.points)

    def __len__(self, /):
        return len(self.points)

    def __getitem__(self, i, /):
        return self.points[i%len(self)]
    ###########################################################################
    def get_points(self, /):
        return tuple(
            [bcl((self.points[v-1], self.points[v]))
            for v in range(1, len(self.points))]
            + list(bcl((self.points[-1], self.points[0]))))

    def geogebra(self, d=0.3):
        c = f'Circle({self.points[0]}, {d})'
        p = ', '.join((f'({v.x}, {v.y})' for v in self.points))
        v = ', '.join([f'Vector({self.points[i-1]}, {self.points[i]})'
              for i in range(1,len(self.points))]
              + [f'Vector({self.points[-1]},{self.points[0]})'])
        return 'PyPolygon = {' + f'{c}, {p}, {v}' + '}'
