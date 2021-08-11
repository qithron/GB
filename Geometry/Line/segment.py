from .ray import ray
from ..Point import quadrant

class segment(ray):
    '''
    ray(A, B, /)

    Same like ray, except in Membership test operations, ==, and !=.
    '''
    __slots__ = '_arg', '_con', '_ctr'

    def __init__(self, A, B, /):
        self._arg = A, B
        super().__init__(A, B)
        if self.m == None:
            self._ctr = lambda A: A == self.P
        else:
            qd = quadrant(B, A)
            dx = qd.q in (1, 4, -4, -3, -1)
            dy = qd.q in (1, 2, -4, -3, -2)
            sx = ('>=' if dx else '<=')
            sy = ('>=' if dy else '<=')
            self._con = f'{self.Q.x} {sx} x {sx} {self.P.x}, ' \
                         f'{self.Q.y} {sy} y {sy} {self.P.y}'
            if dx and dy:
                self._ctr = lambda A: self.Q.x >= A[0] >= self.P.x\
                                   and self.Q.y >= A[1] >= self.P.y
            elif dx:
                self._ctr = lambda A: self.Q.x >= A[0] >= self.P.x\
                                   and self.Q.y <= A[1] <= self.P.y
            elif dy:
                self._ctr = lambda A: self.Q.x >= A[0] <= self.P.x\
                                   and self.Q.y >= A[1] >= self.P.y
            else:
                self._ctr = lambda A: self.Q.x <= A[0] <= self.P.x\
                                   and self.Q.y <= A[1] <= self.P.y
    ###########################################################################
    def __str__(self, /):
        s = super(ray, self).__str__()
        return f'{s}, {self._con}' if s != 'not a line' else s

    def __repr__(self, /):
        return f'segment({self._arg[0]}, {self._arg[1]})'
    ###########################################################################
    def __contains__(self, item, /):
        return self._ctr(item) and super(ray, self).__contains__(item)
    ###########################################################################
    def __eq__(self, other, /):
        return False if type(other) != segment else (True
        if self.P == other.P and self.Q == other.Q
        and abs(self.m) == abs(other.m) else False)

    def __ne__(self, other, /):
        return True if type(other) != segment else (False
        if self.P == other.P and self.Q == other.Q
        and abs(self.m) == abs(other.m) else True)
    ###########################################################################
    def x_from(self, y, /):
        x = super(ray, self).x_from(y)
        return x if (x, y) in self else None

    def y_from(self, x, /):
        y = super(ray, self).y_from(y)
        return y if (x, y) in self else None

    @staticmethod
    def lies_in(P, O, /):
        '''
        lies_in(P, O, /)
        
        Check whether point P lies in O. O must be a line, ray or segment.
        Then, return True if point P lies in segment O else False,
        or None if O is line and line constructed using gradient
        (there is no way to determine the line direction).
        Checked without creating new instance.
        '''
        if not isinstance(O, line):
            raise TypeError(
                'second argument must be line, ray, or segment')
        elif type(O) == segment:
            return O.__contains__(P)
        else:
            if O.Q == None:
                return None
            if O.m == None:
                ctr = lambda A: A == O.P
            else:
                qd = quadrant(O.Q, O.P)
                d = qd.q in (1, 4, -4, -3, -1), qd.q in (1, 2, -4, -3, -2)
                if all(d):
                    ctr = lambda A: O.Q.x >= A[0] >= O.P.x\
                                and O.Q.y >= A[1] >= O.P.y
                elif d[0]:
                    ctr = lambda A: O.Q.x >= A[0] >= O.P.x\
                                and O.Q.y <= A[1] <= O.P.y
                elif d[1]:
                    ctr = lambda A: O.Q.x >= A[0] <= O.P.x\
                                and O.Q.y >= A[1] >= O.P.y
                else:
                    ctr = lambda A: O.Q.x <= A[0] <= O.P.x\
                                and O.Q.y <= A[1] <= O.P.y
            return ctr(P) and line.__contains__(O, P)
