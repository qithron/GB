from ... import decimal, DC, dec

class point:
    '''
    point(x=0, y=0, /)

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
    def __call__(self):
        self.x.normalize()
        self.y.normalize()
        return point(self.x, self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'point({self.x}, {self.y})'

    def __bool__(self):
        return True if self.x and self.y else False

    def __eq__(self, other, /):
        return False if type(other) != point else \
        (True if self.x == other.x and self.y == other.y else False)

    def __ne__(self, other, /):
        return True if type(other) != point else \
        (True if self.x != other.x or self.y != other.y else False)

    def __pos__(self):
        return point(+self.x, +self.y)

    def __neg__(self):
        return point(self.x.copy_negate(), self.y.copy_negate())

    def __abs__(self):
        return point(self.x.copy_abs(), self.y.copy_abs())

    def __ceil__(self):
        return point(
            self.x.to_integral_value(rounding=decimal.ROUND_CEIL),
            self.y.to_integral_value(rounding=decimal.ROUND_CEIL))

    def __floor__(self):
        return point(
            self.x.to_integral_value(rounding=decimal.ROUND_FLOOR),
            self.y.to_integral_value(rounding=decimal.ROUND_FLOOR))

    def __round__(self, ndigits=None, /):
        if not ndigits:
            return self.x.to_integral_value(), self.y.to_integral_value()
        e = dec(f'0e-{ndigits}')
        return point(
            self.x.quantize(e).normalize(),
            self.y.quantize(e).normalize())
    ###########################################################################
    def __iter__(self):
        return iter((self.x, self.y))

    def __len__(self):
        return 2

    def __getitem__(self, key, /):
        return getattr(self, key)
    
    def __contains__(self, item, /):
        return True if item == self.x or item == self.y else False
    ###########################################################################
    def __add__(self, obj, /):
        x, y = self.__get_value(obj)
        return point(self.x + x, self.y + y)

    def __sub__(self, obj, /):
        x, y = self.__get_value(obj)
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
        x, y = self.__get_value(obj)
        return point(x + self.x, y + self.y)

    def __rsub__(self, obj, /):
        x, y = self.__get_value(obj)
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
    def __get_value(self, obj, /):
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
