from .. import dec
from .point import point
from .slope import slope
from math import gcd

class line:
    '''\
    Will give something like this:
        ax + by - c = 0
            where is:
                a always positive
                a, b, c always int.

    line(point, point) -> line
    line(point, m=x) -> line

    P = base point
    Q = 2nd point, ignored if m specified
    m = slope
    a = x coefficient, if any
    b = y coefficient, if any
    c = constants
        note: m value can become 0 or -0; inf or -inf
              indicates the direction of the line
    '''

    #### Line from 2 points:
    ####     (x₁, y₁)
    ####     (x₂, y₂)
    ####         (x₂ - x₁)·(y - y₁) = (y₂ - y₁)·(x - x₁)
    ####         (x₂ - x₁)·(y - y₁) - (y₂ - y₁)·(x - x₁) = 0
    ####             a = -(y2 - y1)
    ####             b = (x2 - x1)
    ####             c = (-y1)*(x2 - x1) - (-x1)*(y2 - y1)
    ####
    #### Line from a gradient:
    ####     (x₁, y₁)
    ####     m
    ####         y - y₁ = m(x - x₁)
    ####         mx - y + y₁ - mx₁ = 0
    ####             a = m
    ####             b = -1
    ####             c = y1 - mx1

    __slots__ = 'P', 'Q', 'm', 'a', 'b', 'c', '__arg'
    def __init__(self, A, B=None, /, *, m=None):
        self.__arg = A, B, m
        self.P = A if type(A) == point else point(*A)
        if B:
            self.Q = B if type(B) == point else point(*B)
            self.m = slope(self.P, self.Q)
        else:
            self.m = dec(m) if m != None else None
            self.Q = None
        # linear to x/y axis
        if self.m == 0 or self.m.is_infinite():
            a, b, c = (0, dec(1), 'y') if self.m == 0 else (dec(1), 0, 'x')
            c = -(self.P[c])
            w = True if a else False
            if not self.__is_int(c): # always int
                z = 10**len(str(c)[str(c).find('.')+1:])
                if w: a *= z
                else: b *= z
                c *= z
            s = gcd(*[abs(int(v)) for v in ((a if w else b),c) if v])
            if s > 1: # simplify
                if w: a /= s
                else: b /= s
                c /= s
            if w: a = int(a)
            else: b = int(b)
            c = int(c)
        # has slope
        elif self.m:
            x1, y1 = self.P
            if self.Q: # 2 points
                x2, y2 = self.Q
                a = -(y2 - y1)
                b = (x2 - x1)
                c = (-y1)*(x2 - x1) - (-x1)*(y2 - y1)
            else: # gradient
                m = self.m
                a = m
                b = dec(-1)
                c = y1 - m*x1
            if any([not self.__is_int(i) for i in (a,b,c)]): # always int
                z = 10**max(len(str(a)[str(a).find('.')+1:]),
                            len(str(b)[str(b).find('.')+1:]),
                            len(str(c)[str(c).find('.')+1:]))
                a *= z
                b *= z
                c *= z
            if a < 0: # a always positive
                a *= -1
                b *= -1
                c *= -1
            s = gcd(*[abs(int(v)) for v in (a,b,c) if v])
            if s > 1: # simplify
                a /= s
                b /= s
                c /= s
            a, b, c = int(a), int(b), int(c)
        # P == Q, this is not a line at all
        else: # self.m == None
            a = b = c = 0
        self.a, self.b, self.c = a, b, c
    ###########################################################################
    def __call__(self):
        return self.a, self.b, self.c, self.m, self.P, self.Q

    def __str__(self):
        a, b, c = self.a, self.b, self.c
        if None == a == b == c:
            return None
        A = '' if not a else (('' if a == 1 else str(a)) + 'x ')
        B = '' if not b else (
            ((('+ ' if b > 0 else '- ') + ('' if abs(b) == 1 else str(abs(b))))
            if A else ('' if b == 1 else (str(b) if b != -1 else '-'))) + 'y ')
        C = '' if not c else (('+ ' if c > 0 else '- ') + f'{abs(c)} ')
        return f'{A}{B}{C}= 0'

    def __repr__(self):
        P, Q, m = self.__arg
        O = Q if Q else (f'm={m}')
        return f'line({P}, {O})'

    def __iter__(self):
        return iter((self.a, self.b, self.c))

    def __len__(self):
        return 3

    def __getitem__(self, key):
        return getattr(self, key)
    ###########################################################################
    def _preview(self):
        Px, Py = self.P
        Qx, Qy = self.Q
        Q = f'({Qx}, {Qy})' if self.Q else self.Q
        m = self.m
        a, b, c = self.a, self.b, self.c
        return f'P = ({Px}, {Py})\nQ = {Q}\nm = {m}\na:{a} b:{b} c:{c}\n'

    def __is_int(self, value):
        return True if value.as_integer_ratio()[1] == 1 else False
    ###########################################################################
    def x_from(self, y):
        y = dec(y)
        m = self.m
        if m == None:
            return -self.c
        elif m == 0:
            if y == -self.c:
                return dec('inf')
            else:
                return None
        x1, y1 = self.P
        x = (y + m*x1 - y1)/m
        return x

    def y_from(self, x):
        x = dec(x)
        m = self.m
        if m == 0:
            return -self.c
        elif m == None:
            if x == -self.c:
                return dec('inf')
            else:
                return None
        x1, y1 = self.P
        y = m*x - m*x1 + y1
        return y
