""" 
math function of SQL
"""


from .base import ArithmeticBase, MathFuncBase


class Abs(MathFuncBase):

    def __init__(self, x):
        """abs(x)"""

        return super().__init__(x)


class Sign(MathFuncBase):

    def __init__(self, x):
        """sign(x)"""

        return super().__init__(x)


class Mod(MathFuncBase):

    def __init__(self, x, y):
        """mod(x, y)"""

        return super().__init__(x, y)


class Floor(MathFuncBase):

    def __init__(self, x):
        """floor(x)"""

        return super().__init__(x)


class Ceiling(MathFuncBase):

    def __init__(self, x):
        """ceiling(x)"""

        return super().__init__(x)


Ceil = Ceiling


class Round(MathFuncBase):
    def __init__(self, x, n=None):
        """`round(x)` or `round(x, n)`"""

        super().__init__(x, n)


class Div(ArithmeticBase):

    def __init__(self, x, y):
        """x DIV y"""

        if isinstance(x, ArithmeticBase):
            x = f'({x})'
        if isinstance(y, ArithmeticBase):
            y = f'({y})'
        self._value = f'({x} DIV {y})'


class Exp(MathFuncBase):

    def __init__(self, x):
        """exp(x)"""

        return super().__init__(x)


class Ln(MathFuncBase):

    def __init__(self, x):
        """ln(x)"""

        return super().__init__(x)


class Log(MathFuncBase):

    def __init__(self, x, y=None):
        """If only x, `log(e, x)`; If x and y, `log(x, y)`"""

        return super().__init__(x, y)


class Power(MathFuncBase):

    def __init__(self, x, y):
        """power(x, y)"""

        return super().__init__(x, y)


Pow = Power


class Sqrt(MathFuncBase):

    def __init__(self, x):
        """sqrt(x)"""

        return super().__init__(x)


class Pi(MathFuncBase):

    def __init__(self):
        """PI = 3.141592658..."""

        return super().__init__()


PI = Pi()


class Cos(MathFuncBase):

    def __init__(self, x):
        """cos(x)"""

        return super().__init__(x)


class Sin(MathFuncBase):

    def __init__(self, x):
        """sin(x)"""

        return super().__init__(x)


class Tan(MathFuncBase):

    def __init__(self, x):
        """tan(x)"""

        return super().__init__(x)


class Acos(MathFuncBase):

    def __init__(self, x):
        """acos(x)"""

        return super().__init__(x)


class Asin(MathFuncBase):

    def __init__(self, x):
        """asin(x)"""

        return super().__init__(x)


class Atan(MathFuncBase):

    def __init__(self, x, y=None):
        """atan(x)"""

        return super().__init__(x, y)


class Cot(MathFuncBase):

    def __init__(self, x):
        """cot(x)"""

        return super().__init__(x)


class Rand(MathFuncBase):

    def __init__(self, n=None):
        """`rand()` or `rand(n)`"""

        return super().__init__(n)
