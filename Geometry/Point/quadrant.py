from .point import point

class quadrant:
    '''
    quadrant(P, O=None, /):

    O = origin, default is None, if given, then P = P - O.
    Create a class that return a value representing Quadrant of a point:

        -4 = x-Axis +
        -3 = y-Axis +
        -2 = x-Axis -
        -1 = y-Axis -
        0 = origin
        1-4 = the four Quadrants
    '''
    __slots__ = 'P', 'O', 'q', 'next', 'prev', 'mirr'

    def __init__(self, P, O=None, /):
        if type(P) != point:
            point(*P)
        if O != None:
            if type(O) != point:
                O = point(*O)
            P -= O
        x, y = P
        if x == 0 == y:
            self.q = 0
        else:
            if x != 0 != y:
                if x > 0:
                    if y > 0:
                        self.q = 1
                    else:
                        self.q = 4
                else:
                    if y > 0:
                        self.q = 2
                    else:
                        self.q = 3
            else:
                if x == 0:
                    if y > 0:
                        self.q = -3
                    else:
                        self.q = -1
                else:
                    if x > 0:
                        self.q = -4
                    else:
                        self.q = -2
        self.P = P
        self.O = point() if O == None else O
        assert -4 <= self.q <= 4, f'{self.P} {self.O}'
    ###########################################################################
    def __call__(self, /):
        return quadrants(self.q)

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
        q = obj.q if isinstance(obj, quadrant) else obj
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
        q = obj.q if isinstance(obj, quadrant) else obj
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
                return quadrants((q%4) if q%4 else 4)
            else:
                return quadrants((q%-4) if q%4 else -4)

    def __sub__(self, value, /):
        return self + (-value)
    ###########################################################################
    def __radd__(self, value, /):
        return value + self.q

    def __rsub__(self, value, /):
        return value - self.q

class quadrants(quadrant):
    '''
    quadrants(q, /)

    -4 <= q <= 4

    Create new quadrant object from a value.
    '''
    def __init__(self, q, /):
        if type(q) != int:
            raise TypeError(
                f'value must be integers')
        elif not -4 <= q <= 4:
            raise ValueError(
                f'value out of range, -4 <= {q} <= 4')
        self.q = q
