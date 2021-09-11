from . import decimal, DC, dec
from math import pi, atan2, acos, cos, sin, gcd

_pi = dec(pi, string=False)

class point:
    '''
    point(x, y)

    2D Cartesian Coordinate System.
    Basic class contains 2 decimal value.

    Construct a new point object. With no argument, point() will create
    point(0, 0).
    '''
    # I'm not sure about __rtruediv__, and below its
    __slots__ = 'x', 'y'

    def __init__(self, x=0, y=0, /):
        self.x = dec(x).normalize()
        self.y = dec(y).normalize()
    ###########################################################################
    def __call__(self, /):
        return point(self.x, self.y)

    def __str__(self, /):
        return f'({self.x}, {self.y})'

    def __repr__(self, /):
        return f'point({self.x}, {self.y})'
    ###########################################################################
    def __iter__(self, /):
        return iter((self.x, self.y))

    def __len__(self, /):
        return 2

    def __getitem__(self, key, /):
        if key == 0 or key == 'x':
            return self.x
        if key == 1 or key == 'y':
            return self.y
        if type(key) == str:
            raise KeyError(
                f'{point} object has no key {key}')
        elif type(key) == int:
            raise IndexError(
                'index out of range')
        else:
            raise TypeError(
                'key must be string or integers')

    def __contains__(self, item, /):
        return True if item == self.x or item == self.y else False
    ###########################################################################
    def __bool__(self, /):
        return True if self.x and self.y else False

    def __eq__(self, other, /):
        if hasattr(other, '__len__') and len(self) == len(other):
            x, y = other
        else:
            return False
        return True if self.x == x and self.y == y else False

    def __ne__(self, other, /):
        if hasattr(other, '__len__') and len(self) == len(other):
            x, y = other
        else:
            return True
        return False if self.x == x and self.y == y else True
    ###########################################################################
    def __pos__(self, /):
        return point(+self.x, +self.y)

    def __neg__(self, /):
        return point(self.x.copy_negate(), self.y.copy_negate())

    def __abs__(self, /):
        return point(self.x.copy_abs(), self.y.copy_abs())

    def __ceil__(self, /):
        return point(
            self.x.to_integral_value(rounding=decimal.ROUND_CEIL),
            self.y.to_integral_value(rounding=decimal.ROUND_CEIL))

    def __floor__(self, /):
        return point(
            self.x.to_integral_value(rounding=decimal.ROUND_FLOOR),
            self.y.to_integral_value(rounding=decimal.ROUND_FLOOR))

    def __round__(self, ndigits=None, /):
        if not ndigits:
            return point(
                self.x.to_integral_value(),
                self.y.to_integral_value())
        e = dec(f'0e-{ndigits}')
        return point(
            self.x.quantize(e).normalize(),
            self.y.quantize(e).normalize())
    ###########################################################################
    def __add__(self, obj, /):
        x, y = point._get_value(obj)
        return point(self.x + x, self.y + y)

    def __sub__(self, obj, /):
        x, y = point._get_value(obj)
        return point(self.x - x, self.y - y)

    def __mul__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(self.x * value, self.y * value)

    def __truediv__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(self.x / value, self.y / value)

    def __floordiv__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(self.x // value, self.y // value)

    def __mod__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(self.x % value, self.y % value)

    def __divmod__(self, value, /):
        raise TypeError(
            'unsupported operand type(s) '
            f'for divmod(): {point} and {type(value)}')

    def __pow__(self, value, mod=None, /):
        if type(value) == float:
            value = dec(value)
        return point(
            DC.power(self.x, value, mod),
            DC.power(self.y, value, mod))
    ###########################################################################
    def __radd__(self, obj, /):
        x, y = point._get_value(obj)
        return point(x + self.x, y + self.y)

    def __rsub__(self, obj, /):
        x, y = point._get_value(obj)
        return point(x - self.x, y - self.y)

    def __rmul__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(value * self.x, value * self.y)

    def __rtruediv__(self, value, /):
        if type(value) == float:
            value = dec(value)
        return point(value / self.x, value / self.y)

    def __rfloordiv__(self, value, /):
        raise TypeError(
            'unsupported operand type(s) '
            f'for //: {type(value)} and {point}')

    def __rmod__(self, value, /):
        raise TypeError(
            'unsupported operand type(s) '
            f'for %: {type(value)} and {point}')

    def __rdivmod__(self, value, /):
        raise TypeError(
            'unsupported operand type(s) '
            f'for divmod(): {type(value)} and {point}')

    def __rpow__(self, value, mod=None, /):
        raise TypeError(
            'unsupported operand type(s) '
            f'for ** or pow(): {type(value)} and {point}')
    ###########################################################################
    @staticmethod
    def _get_value(obj, /):
        if type(obj) == point:
            x, y = obj
        elif type(obj) == int or type(obj) == decimal:
            x = y = obj
        elif type(obj) == float:
            x = y = dec(obj)
        # elif type(obj) == complex: # currently looking for it
        else:
            raise TypeError(
                f'unsupported operations + or - for {type(obj)}')
        return x, y

###############################################################################

class quadrant:
    '''
    obj can be a point or int in range -4 <= obj <= 4.
    O = origin, default is None, if given, then obj = obj - O.

    Create a class that return a value representing Quadrant of a point:

        -4 = x-Axis +
        -3 = y-Axis +
        -2 = x-Axis -
        -1 = y-Axis -
        0 = origin
        1-4 = the four Quadrants
    '''
    __slots__ = 'P', 'O', 'q'

    def __init__(self, obj, O=None, /):
        if type(obj) == int:
            if not -4 <= obj <= 4:
                raise ValueError(
                    f'value out of range, -4 <= {q} <= 4')
            self.q = obj
            self.P = self.O = None
        else:
            P = point(*obj) if type(obj) != point else obj
            if O != None:
                if type(O) != point:
                    O = point(*O)
                P -= O
            else:
                O = point()
            x, y = P
            if x == 0 == y:
                self.q = 0
            else:
                if x != 0 != y:
                    j = y > 0
                    if x > 0:
                        if j: self.q = 1
                        else: self.q = 4
                    else:
                        if j: self.q = 2
                        else: self.q = 3
                else:
                    j = y > 0 if x == 0 else x > 0
                    if x == 0:
                        if j: self.q = -3
                        else: self.q = -1
                    else:
                        if j: self.q = -4
                        else: self.q = -2
            self.P = P
            self.O = O
        assert -4 <= self.q <= 4, f'value out of range, -4 <= {self.q} <= 4'
    ###########################################################################
    def __call__(self, /):
        return quadrant(self.q)

    def __str__(self, /):
        if not self.q:
            return '"Origin"'
        elif self.q == 1:
            return f'"Quadrant I"'
        elif self.q == 2:
            return f'"Quadrant II"'
        elif self.q == 3:
            return f'"Quadrant III"'
        elif self.q == 4:
            return f'"Quadrant IV"'
        elif self.q == -4:
            return '"x-Axis +"'
        elif self.q == -3:
            return '"y-Axis +"'
        elif self.q == -2:
            return '"x-Axis -"'
        elif self.q == -1:
            return '"y-Axis -"'

    def __repr__(self, /):
        return str(self) # ¯\_(ツ)_/¯
    ###########################################################################
    def __bool__(self, /):
        return self.q != 0

    def __eq__(self, obj, /):
        q = obj.q if type(obj) == quadrant else obj
        if self.q == q:
            return True
        elif not self.q:
            return self.q == q
        elif self.q == 1:
            return True if q == -4 or q == -3 else False
        elif self.q == 2:
            return True if q == -3 or q == -2 else False
        elif self.q == 3:
            return True if q == -2 or q == -1 else False
        elif self.q == 4:
            return True if q == -1 or q == -4 else False
        elif self.q == -4:
            return True if q in (1, 4, -1, -3) else False
        elif self.q == -3:
            return True if q in (2, 1, -2, -4) else False
        elif self.q == -2:
            return True if q in (3, 2, -3, -1) else False
        elif self.q == -1:
            return True if q in (4, 3, -4, -2) else False

    def __ne__(self, obj, /):
        q = obj.q if type(obj) == quadrant else obj
        if self.q == q:
            return False
        elif not self.q:
            return self.q != q
        elif self.q == 1:
            return False if q == -4 or q == -3 else True
        elif self.q == 2:
            return False if q == -3 or q == -2 else True
        elif self.q == 3:
            return False if q == -2 or q == -1 else True
        elif self.q == 4:
            return False if q == -1 or q == -4 else True
        elif self.q == -4:
            return False if q in (1, 4, -1, -3) else True
        elif self.q == -3:
            return False if q in (2, 1, -2, -4) else True
        elif self.q == -2:
            return False if q in (3, 2, -3, -1) else True
        elif self.q == -1:
            return False if q in (4, 3, -4, -2) else True

    # def __lt__(self, obj, /):
        # return self.q < (obj.q if isinstance(obj, quadrant) else obj)

    # def __le__(self, obj, /):
        # return self.q <= (obj.q if isinstance(obj, quadrant) else obj)

    # def __gt__(self, obj, /):
        # return self.q > (obj.q if isinstance(obj, quadrant) else obj)

    # def __ge__(self, obj, /):
        # return self.q >= (obj.q if isinstance(obj, quadrant) else obj)
    ###########################################################################
    def __add__(self, value, /):
        if type(value) != int:
            raise TypeError(
                'value must be integers')
        if not self.q:
            return self
        else:
            q = self.q + value
            if self.q > 0:
                return quadrant((q%4) if q%4 else 4)
            else:
                return quadrant((q%-4) if q%4 else -4)

    def __sub__(self, value, /):
        return self + (-value)
    ###########################################################################
    def __radd__(self, value, /):
        return value + self.q

    def __rsub__(self, value, /):
        return value - self.q
###############################################################################
def angle(A, B, C, /):
    '''
    Returns angle B in radian.
    '''
    if type(A) != point: A = point(*A)
    if type(B) != point: B = point(*B)
    if type(C) != point: C = point(*C)
    # if B == A or B == C: # ??? None or 0°
        # return None
    A -= B
    C -= B
    with decimal.localcontext() as ctx:
        ctx.prec = decimal.RX
        a = decimal.Decimal(atan2(A.y, A.x))
        c = decimal.Decimal(atan2(C.y, C.x))
        if a < 0: a += _pi*2
        if c < 0: c += _pi*2
        ang = (_pi*2 + c - a) if a > c else (c - a)
    return +ang

def distance(A, B, /):
    '''
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
            with decimal.localcontext() as ctx:
                ctx.prec = decimal.RX
                d = abs(A.c - B.c)\
                  / DC.sqrt(DC.power(A.a, 2) + DC.power(A.b, 2))
        else:
            d = dec()
    elif type(A) == line or type(B) == line:
        P, L = (A, B) if type(B) == line else (B, A)
        if 0 == L.a == L.b:
            return None
        a, b, c = L
        x, y = P
        with decimal.localcontext() as ctx:
            ctx.prec = decimal.RX
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
        with decimal.localcontext() as ctx:
            ctx.prec = decimal.RX
            if x1 == x2 and y1 == y2:
                d = dec()
            elif x1 != x2 and y1 == y2:
                d = abs(x1 - x2)
            elif x1 == x2 and y1 != y2:
                d = abs(y1 - y2)
            else:
                d = DC.sqrt(DC.power(x2-x1, 2) + DC.power(y2-y1, 2))
    return +d.normalize()

def midpoint(A, B, /):
    if type(A) != point: A = point(*A)
    if type(B) != point: B = point(*B)
    return (A + B)/2

def intersect(A, B, /):
    '''
    Intersect of 2 lines:
        a₁x + b₁y + c₁ = 0
        a₂x + b₂y + c₂ = 0
            x' = (c₁b₂ - c₂b₁) / (a₁b₂ - a₂b₁)
            y' = (a₁c₂ - a₂c₁) / (a₁b₂ - a₂b₁)
    '''
    if isinstance(A, line) and isinstance(B, line):
        a1, b1, c1 = dec((A.a, A.b, -A.c))
        a2, b2, c2 = dec((B.a, B.b, -B.c))
        x = (c1*b2 - c2*b1)
        y = (a1*c2 - a2*c1)
        n = (a1*b2 - a2*b1)
        if 0 == n == x == y:
            return dec('inf')
        elif n == 0:
            return None
        I = point(x/n, y/n)
        return I if (I in A) and (I in B) else None
    raise TypeError(
        'both of arguments must be line, ray, or segment')

def point_F2pointWdist(A, B, d, /):
    '''
    point_F2pointWdist(A, B, d, /)

    point from 2 points with distance

    Method:
        d = distance(A, B)
        r = dt/d
        C = A + (B-A)*r
    '''
    if type(A) != point: A = point(*A)
    if type(B) != point: B = point(*B)
    return A + (B-A)*(dec(d)/distance(A, B))

###############################################################################
###############################################################################
###############################################################################

class line:
    '''
    line(A, B)
    line(A, m=x)
    line(A, m=dec('inf'))
    line(A, m=None)

    Will give something like this:
        ax + by + c = 0
            where is:
                a always positive
                a, b, c always int

    P = base point
    Q = 2nd point, ignored if m specified
    m = slope
    a = x coefficient, if any
    b = y coefficient, if any
    c = constants

    note:
        m value can become 0 or -0; inf or -inf
        indicates the direction of the line, but it useless,
        if None, that indicates this is not a line at all

        about Membership test operations: x in line,
        return True if type(x) == point and point lies in line else False

    '''
    #### Line from 2 points:
    ####     (x₁, y₁)
    ####     (x₂, y₂)
    ####         (x₂ - x₁)·(y - y₁) = (y₂ - y₁)·(x - x₁)
    ####         (x₂ - x₁)·(y - y₁) - (y₂ - y₁)·(x - x₁) = 0
    ####             a = -(y2 - y1)
    ####             b = (x2 - x1)
    ####             c = (-y1)*(x2 - x1) - (-x1)*(y2 - y1)

    #### Line from a gradient:
    ####     (x₁, y₁)
    ####     m
    ####         y - y₁ = m(x - x₁)
    ####         mx - y + y₁ - mx₁ = 0
    ####             a = m
    ####             b = -1
    ####             c = y1 - mx1
    __slots__ = 'P', 'Q', 'm', 'a', 'b', 'c', '_arg'

    def __init__(self, A=point(), B=None, /, *, m=1):
        self._arg = A, B, m
        self.P = A if type(A) == point else point(*A)
        if B != None:
            self.Q = B if type(B) == point else point(*B)
            self.m = slope(self.P, self.Q)
        else:
            self.m = dec(m) if m != None else None
            self.Q = None
        is_int = lambda x: x.as_integer_ratio()[1] == 1
        # linear to x/y axis
        if self.m == 0 or (self.m and self.m.is_infinite()):
            a, b, c = (0, dec(1), 'y') if self.m == 0 else (dec(1), 0, 'x')
            c = -(self.P[c])
            w = True if a else False
            if not is_int(c): # always int
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
            if any([not is_int(i) for i in (a,b,c)]): # always int
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
    def __call__(self, /):
        return self.a, self.b, self.c, self.m, self.P, self.Q

    def __str__(self, /):
        a, b, c = self.a, self.b, self.c
        if 0 == a == b == c:
            return 'not a line'
        A = '' if not a else (('' if a == 1 else str(a)) + 'x ')
        B = '' if not b else (
            ((('+ ' if b > 0 else '- ') + ('' if abs(b) == 1 else str(abs(b))))
            if A else ('' if b == 1 else (str(b) if b != -1 else '-'))) + 'y ')
        C = '' if not c else (('+ ' if c > 0 else '- ') + f'{abs(c)} ')
        return f'{A}{B}{C}= 0'

    def __repr__(self, /):
        P, Q, m = self._arg
        O = Q if Q else (f'm={m}')
        return f'line({P}, {O})'
    ###########################################################################
    def __iter__(self, /):
        return iter((self.a, self.b, self.c))

    def __len__(self, /):
        return 3

    def __getitem__(self, key, /):
        return getattr(self, key)

    def __contains__(self, item, /):
        x, y = item
        return True if self.a*x + self.b*y + self.c == 0 else False
    ###########################################################################
    def __bool__(self, /):
        return True if self.m != None else False

    def __eq__(self, other, /):
        return False if type(other) != line else (True
        if abs(self.m) == abs(other.m)
        and other.P in self else False)

    def __ne__(self, other, /):
        return True if type(other) != line else (False
        if abs(self.m) == abs(other.m)
        and other.P in self else True)
    ###########################################################################
    def _preview(self, /):
        Px, Py = self.P
        Qx, Qy = self.Q if self.Q else (None, None)
        Q = f'({Qx}, {Qy})' if self.Q else self.Q
        m = self.m
        a, b, c = self.a, self.b, self.c
        return f'P = ({Px}, {Py})\nQ = {Q}\nm = {m}\na:{a} b:{b} c:{c}\n'
    ###########################################################################
    def x_from(self, y, /):
        y = dec(y)
        m = self.m
        if m and m.is_infinite():
            x = -self.c/self.a
        elif m == 0:
            if y == -self.c:
                return dec('inf')
            else:
                return None
        else:
            x1, y1 = self.P
            x = (y + m*x1 - y1)/m
        return point(x, y)

    def y_from(self, x, /):
        x = dec(x)
        m = self.m
        if m == 0:
            y = -self.c/self.b
        elif m and m.is_infinite():
            if x == -self.c:
                return dec('inf')
            else:
                return None
        else:
            x1, y1 = self.P
            y = m*x - m*x1 + y1
        return point(x, y)

    @staticmethod
    def lies_in(P, O, /):
        '''
        Check whether point P lies in line O. O must be a line, ray or segment.
        Checked without creating new instance.
        '''
        if not isinstance(O, line):
            raise TypeError(
                'second argument must be line, ray, or segment')
        return P in O

class ray(line):
    '''
    Same like line, except in Membership test operations, ==, and !=.
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
            self._con = (f'x >= {self.P.x}' if dx else f'x <= {self.P.x}')\
                + ', ' + (f'y >= {self.P.y}' if dy else f'x <= {self.P.y}')
            if dx and dy:
                self._ctr = lambda A: A[0] >= self.P.x and A[1] >= self.P.y
            elif dx:
                self._ctr = lambda A: A[0] >= self.P.x and A[1] <= self.P.y
            elif dy:
                self._ctr = lambda A: A[0] <= self.P.x and A[1] >= self.P.y
            else:
                self._ctr = lambda A: A[0] <= self.P.x and A[1] <= self.P.y
    ###########################################################################
    def __str__(self, /):
        s = super().__str__()
        return f'{s}, {self._con}' if s != 'not a line' else s

    def __repr__(self, /):
        return f'ray({self._arg[0]}, {self._arg[1]})'
    ###########################################################################
    def __contains__(self, item, /):
        return self._ctr(item) and super().__contains__(item)
    ###########################################################################
    def __eq__(self, other, /):
        return False if type(other) != ray else (True
        if self.P == other.P
        and abs(self.m) == abs(other.m) else False)

    def __ne__(self, other, /):
        return True if type(other) != ray else (False
        if self.P == other.P
        and abs(self.m) == abs(other.m) else True)
    ###########################################################################
    def x_from(self, y, /):
        P = super().x_from(y)
        return P if P in self else None

    def y_from(self, x, /):
        P = super().y_from(y)
        return P if P in self else None

    @staticmethod
    def lies_in(P, O, /):
        '''
        Check whether point P lies in O. O must be a line, ray or segment.
        Then, return True if point P lies in ray O else False,
        or None if O is line and line constructed using gradient
        (there is no way to determine the line direction).
        Checked without creating new instance.
        '''
        if not isinstance(O, line):
            raise TypeError(
                'second argument must be line, ray, or segment')
        elif type(O) == ray:
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
                    ctr = lambda A: A[0] >= O.P.x and A[1] >= O.P.y
                elif d[0]:
                    ctr = lambda A: A[0] >= O.P.x and A[1] <= O.P.y
                elif d[1]:
                    ctr = lambda A: A[0] <= O.P.x and A[1] >= O.P.y
                else:
                    ctr = lambda A: A[0] <= O.P.x and A[1] <= O.P.y
            return ctr(P) and P in O

class segment(ray):
    '''
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
        P = super(ray, self).x_from(y)
        return P if P in self else None

    def y_from(self, x, /):
        P = super(ray, self).y_from(y)
        return P if P in self else None

    @staticmethod
    def lies_in(P, O, /):
        '''
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
            return ctr(P) and P in O
###############################################################################
def slope(A, B, /):
    '''
    Slope of 2 points. Use line.m for slope of line object instead.
    '''
    x1, y1 = A if type(A) == point else point(*A)
    x2, y2 = B if type(B) == point else point(*B)
    if x1 == x2 and y1 == y2:
        return None
    with decimal.localcontext() as ctx:
        ctx.prec = decimal.RX
        ctx.traps[decimal.DivisionByZero] = False
        m = (y2 - y1)/(x2 - x1)
    return +m.normalize()

def linear(O, L, /):
    '''
    Return a linear line.
    First argument can be a point, line or sequence types.
    Second argument must be a line.
    '''
    if type(L) != line:
        raise TypeError(
            f'second argument must be a {line} only')
    if type(O) != point and type(O) != line:
        P = point(*O)
    elif type(O) == line:
        P = O.P
    elif type(O) == point:
        P = O
    else:
        raise TypeError(
            f'first argument must be a {point}, '
            f'a {line} or sequence types')
    return line(P, m=L.m)

def perpendicular(O, L, /):
    '''
    Return a perpendicular line.
    First argument can be a point, line or sequence types.
    Second argument must be a line.
    '''
    if type(L) != line:
        raise TypeError(
            f'second argument must be a {line} only')
    if type(O) != point and type(O) != line:
        P = point(*O)
    elif type(O) == point:
        P = O
    elif type(O) == line:
        P = O.P
    else:
        raise TypeError(
            f'First argument must be a {point}, a {line} or sequence types')
    if L.m and L.m.is_infinite():
        m = dec().copy_sign(-L.m)
    elif L.m == 0:
        m = dec('inf').copy_sign(-L.m)
    else:
        m = DC.divide(*L.m.as_integer_ratio()[::-1]).copy_sign(-L.m)\
            if L.m else None
    return line(P, m=m)

###############################################################################
###############################################################################
###############################################################################

class polygon:
    '''
    '''
    __slots__ = (
        'points',
        'convexity',
        'side_lengths',
        'angles',
        'perimeter',
        'area',
        )

    def __new__(cls, *P):
        if len(P) < 3:
            raise IndexError(
                f'argument take at least 3 items but {len(P)} were given')
        elif len(P) == 3:
            return triangle(*P)
        return super().__new__(cls)

    def __init__(self, *P):
        self.points = tuple(
            (e if type(e) == point else point(*e) for e in P))
        self.side_lengths = tuple(
            (distance(*self[i:i+2]) for i in range(len(self))))
        j, k = [], dec()
        for a in (angle(*self[i-1:i+2]) for i in range(len(self))):
            j.append(a)
            k += a
        a = _pi*2
        k = k == (len(self)-2)*(a/2)
        self.angles = tuple(j if k else (a - e for e in j))
        self.perimeter = polygon.get_perimeter(self)
        self.convexity = polygon.convexity_type(self)
        self.area = polygon.get_area(self)
    ###########################################################################
    def __str__(self, /):
        return f'polygon{self.points}'

    def __repr__(self, /):
        return str(self)
    ###########################################################################
    def __iter__(self, /):
        return iter(self.points)

    def __len__(self, /):
        return len(self.points)

    def __getitem__(self, i, /):
        if type(i) == slice:
            step = i.step if i.step != None else 1
            return [self[i] for i in range(i.start, i.stop, step)]
        return self.points[i%len(self)]
    ###########################################################################
    def geogebra(self):
        p = ', '.join((str(v) for v in self.points))
        v = ', '.join([f'Vector({self.points[i-1]}, {self.points[i]})'
            for i in range(1, len(self.points))]
            + [f'Vector({self.points[-1]}, {self.points[0]})'])
        s = f'Polygon({p})'
        return 'PyPol = {'f'{p}, {v}, {s}''}'
    ###########################################################################
    @staticmethod
    def get_perimeter(POL, /):
        return sum(POL.side_lengths)

    @staticmethod
    def get_area(POL, /):
        if not POL.convexity:
            raise NotImplementedError
        elif POL.convexity == 1:
            pass
        elif POL.convexity == 2:
            pass
        else:
            raise SystemExit('unexpected convexity_type')

    @staticmethod
    def convexity_type(POL, /):
        '''
        self_intersecting = 0
        simple
            convex        = 1
            concave       = 2
            star          = 3
            star_shaped   = 4
        '''
        for a in POL.angles:
            if a > _pi:
                return 2
        else:
            return 1

class regular_polygon(polygon):
    __slots__ = ()

    def __new__(cls, A, B, n, /):
        return super(polygon, cls).__new__(cls)

    def __init__(self, A, B, n, /):
        pass

class triangle(polygon):
    '''
    Triangle base class.
    '''
    __slots__ = ()

    def __new__(cls, A, B, C, /):
        a, b, c = distance(B, C), distance(C, A), distance(A, B)
        if a == b == c:
            return equilateral_triangle(A, B, a)
        elif a != b != c != a:
            return scalene_triangle(A, B, C, a, b, c)
        elif a == b:
            return isoceles_triangle(A, B, a, c)
        elif b == c:
            return isoceles_triangle(B, C, b, a)
        elif c == a:
            return isoceles_triangle(C, A, c, b)

    def __init__(self, /, *args):
        self.perimeter = self.get_perimeter(self)
        self.area = self.get_area(self)
        self.convexity = 1
    ###########################################################################
    def __str__(self, /):
        return f'triangle{self.points}'
    ###########################################################################
    @staticmethod
    def get_perimeter(POL, /):
        return super().get_perimeter(POL)

    @staticmethod
    def get_area(POL, /):
        a, b, c = POL.side_lengths
        return DC.sqrt((a + b - c)*(a - b + c)*(-a + b + c)*(a + b + c))/4

class equilateral_triangle(triangle):
    __slots__ = ()

    def __new__(cls, A, B, /, *args):
        if type(A) != point: A = point(*A)
        if type(B) != point: B = point(*B)
        r = _pi/3
        C = A.x + (B.x-A.x) * dec(cos(r)) - (B.y-A.y) * dec(sin(r)),\
            A.y + (B.x-A.x) * dec(sin(r)) + (B.y-A.y) * dec(cos(r))
        obj = super(polygon, cls).__new__(cls)
        obj.points = A, B, point(*C)
        obj.angles = (r,)*3
        obj.side_lengths = (args if args else (distance(A, B),))*3
        return obj
    ###########################################################################
    @staticmethod
    def get_perimeter(POL, /):
        return POL.side_lengths[0]*3

    @staticmethod
    def get_area(POL, /):
        return POL.side_lengths[0]**2 * DC.sqrt(3)/4

class isoceles_triangle(triangle):
    __slots__ = ()

    def __new__(cls, A, B, length, /, *args):
        if type(A) != point: A = point(*A)
        if type(B) != point: B = point(*B)
        l = *(dec(length),)*2, args[0] if args else distance(A, B)
        #### using trigonometry
        T = point_F2pointWdist(A, B, length)
        r = dec(acos((l[2]/2)/l[0]))
        C = A.x + (T.x-A.x) * dec(cos(r)) - (T.y-A.y) * dec(sin(r)),\
            A.y + (T.x-A.x) * dec(sin(r)) + (T.y-A.y) * dec(cos(r))
        #### using intersect
        # h = DC.sqrt(4 * l[0]**2 - l[2]**2)/2
        # M = midpoint(A, B)
        # p = perpendicular(M, line(A, B))
        # P = p.x_from(l[0]), p.y_from(l[0])
        # if P[0]:
            # P = P[0]
        # else:
            # P = P[1]
        # C = point_F2pointWdist(M, P, h)
        if l[0] == l[2]:
            obj = super(polygon, cls).__new__(equilateral_triangle)
            obj.angles = (r,)*3
            obj.side_lengths = (l[2],)*3
        else:
            a = _pi - r*2
            if a == _pi/2:
                obj = super(polygon, cls).__new__(right_triangle)
                obj.right_angle = 2
            else:
                obj = super(polygon, cls).__new__(cls)
            obj.angles = r, r, a
            obj.side_lengths = l
        obj.points = A, B, point(*C)
        return obj
    ###########################################################################
    @staticmethod
    def get_perimeter(POL, /):
        return POL.side_lengths[2] + POL.side_lengths[0]*2

    @staticmethod
    def get_area(POL, /):
        a, b, c = POL.side_lengths
        return DC.sqrt((a + b - c)*(a - b + c)*(-a + b + c)*(a + b + c))/4

class scalene_triangle(triangle):
    __slots__ = ()

    def __new__(cls, A, B, C, /, *args):
        if not args:
            triangle(A, B, C)
        if type(A) != point: A = point(*A)
        if type(B) != point: B = point(*B)
        if type(C) != point: C = point(*C)
        a = angle(C, A, B), angle(A, B, C), angle(B, C, A)
        if sum(a) != _pi:
            a = tuple((_pi*2 - e for e in a))
        r = _pi/2
        for i in range(2):
            if a[i] == r:
                obj = super(polygon, cls).__new__(right_triangle)
                obj.right_angle = i
                break
        else:
            obj = super(polygon, cls).__new__(cls)
        obj.points = A, B, C
        obj.angles = a
        obj.side_lengths = args if args else\
            (distance(B, C), distance(C, A), distance(A, B))
        return obj

class right_triangle(triangle):
    __slots__ = ('right_angle',)

    def __new__(cls, /):
        return None
    ###########################################################################
    @staticmethod
    def get_area(POL, /):
        t = POL.side_lengths[(POL.right_angle+1)%3]
        h = POL.side_lengths[(POL.right_angle-1)%3]
        return (t*h)/2

class quadrilateral(polygon):
    '''
    Quadrilateral base class.
    '''
    __slots__ = ()

    def __new__(cls, /):
        pass

    def __init__(self, /, *args):
        self.perimeter = self.get_perimeter(self)
        self.area = self.get_area(self)
        self.convexity = quadrilateral.convexity_type(self)
###############################################################################
def polygon_F2points(A, B, /, w=1):
    '''
    polygon from 2 points

    Return a polygon object from 2 given point and width, aka rectangle.

    rotating (x,y) with center point (a,b) and v° rotating angle:
        x' = a + (x-a) * cos(v°) - (y-b) * sin(v°)
        y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
    '''
    if A == B:
        return None
    m = slope(A, B)
    wid = dec(w)/2
    Ax, Ay = dec(A)
    Bx, By = dec(B)
    if m == 0 or (m and m.is_infinite()):
        j, k, s = ('x', 'y', False) if m == 0 else ('y', 'x', True)
        v = False if A[j] - B[j] > 0 else True
        q1, q2, q3, q4 = A[k]-wid, B[k]-wid, B[k]+wid, A[k]+wid
        if s:
            if v: a, b, c, d = (q4,Ay), (q3,By), (q2,By), (q1,Ay)
            else: a, b, c, d = (q1,Ay), (q2,By), (q3,By), (q4,Ay)
        else:
            if v: a, b, c, d = (Ax,q1), (Bx,q2), (Bx,q3), (Ax,q4)
            else: a, b, c, d = (Ax,q4), (Bx,q3), (Bx,q2), (Ax,q1)
    else:
        q = quadrant(B)
        if q == 1:
            C = Bx, Ay
            x0, y0 = Ax+wid, Ay
            x1, y1 = Bx-wid, By
        elif q == 2:
            C = Ax, By
            x0, y0 = Ax, Ay+wid
            x1, y1 = Bx, By-wid
        elif q == 3:
            C = Bx, Ay
            x0, y0 = Ax-wid, Ay
            x1, y1 = Bx+wid, By
        elif q == 4:
            C = Ax, By
            x0, y0 = Ax, Ay-wid
            x1, y1 = Bx, By+wid
        an = dec(acos(distance(A,C)/distance(A,B)))
        an0, an1 = an-dec(pi)/2, an+dec(pi)/2
        a = Ax + (x0-Ax) * dec(cos(an0)) - (y0-Ay) * dec(sin(an0)),\
            Ay + (x0-Ax) * dec(sin(an0)) + (y0-Ay) * dec(cos(an0))
        b = Bx + (x1-Bx) * dec(cos(an1)) - (y1-By) * dec(sin(an1)),\
            By + (x1-Bx) * dec(sin(an1)) + (y1-By) * dec(cos(an1))
        c = Bx + (x1-Bx) * dec(cos(an0)) - (y1-By) * dec(sin(an0)),\
            By + (x1-Bx) * dec(sin(an0)) + (y1-By) * dec(cos(an0))
        d = Ax + (x0-Ax) * dec(cos(an1)) - (y0-Ay) * dec(sin(an1)),\
            Ay + (x0-Ax) * dec(sin(an1)) + (y0-Ay) * dec(cos(an1))
    return polygon(a, b, c, d)

def polygon_Fpoints(*P, w=1, sm=False, lvl=0):
    '''
    rotating (x, y) with center point (a, b) and v° rotating angle:
        x' = a + (x-a) * cos(v°) - (y-b) * sin(v°)
        y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
    '''
    if sm or lvl:
        raise SystemExit('not yet')
    if len(P) < 2:
        raise IndexError(
            f'argument take at least 2 items but {len(P)} were given')
    elif len(P) == 2:
        print('need fix')
        return polygon_F2points(*P, w=w)
    if P.count(P[0]) == len(P):
        return None
    PT = iter(P)
    A, B = next(PT), next(PT)
    def nested_func_1():
        nonlocal B
        while PT.__length_hint__() and A == B:
            B = next(PT)
            if A != B:
                return False
        return True
    nested_func_1()
    def nested_func_2(A, B):
        m = slope(A, B)
        a, b = point(*A)
        x, y = point_F2pointWdist(A, B, wid)
        ang = -dec(pi)/2
        P = a + (x-a) * dec(cos(ang)) - (y-b) * dec(sin(ang)),\
            b + (x-a) * dec(sin(ang)) + (y-b) * dec(cos(ang))
        ang = -ang
        Q = a + (x-a) * dec(cos(ang)) - (y-b) * dec(sin(ang)),\
            b + (x-a) * dec(sin(ang)) + (y-b) * dec(cos(ang))
        return line(P, m=m), line(Q, m=m)
    wid = dec(w)/2
    la0, la1 = nested_func_2(A, B)
    ls0, ls1 = [la0.P], [la1.P]
    while True:
        A = B
        if nested_func_1():
            break
        lb1, lb0 = nested_func_2(B, A)
        it0, it1 = intersect(la0, lb0), intersect(la1, lb1)
        assert type(it0) == type(it1), f'how? {type(it0)} {type(it1)}'
        if type(it0) == point == type(it1):
            ls0.append(it0)
            ls1.append(it1)
        else:
            ls0.append(la0.P)
            ls1.append(la1.P)
        la0, la1 = lb0, lb1
    ls0.append(la0.P)
    ls1.append(la1.P)
    return polygon(*ls0, *reversed(ls1))

