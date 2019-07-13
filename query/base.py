class ExpBase:

    def __str__(self):
        return self._value


class ArithmeticBase(ExpBase):
    """Base for arithmetic operation"""

    def __neg__(self):
        return NEG(self)

    def __add__(self, other):
        return ADD(self, other)

    def __radd__(self, other):
        return ADD(other, self)

    def __sub__(self, other):
        return SUB(self, other)

    def __rsub__(self, other):
        return SUB(other, self)

    def __mul__(self, other):
        return MUL(self, other)

    def __rmul__(self, other):
        return MUL(other, self)

    def __div__(self, other):
        return DIV(self, other)

    def __rdiv__(self, other):
        return DIV(other, self)


class NEG(ArithmeticBase):

    def __init__(self, x):

        self._value = f'-{x}'


class ADD(ArithmeticBase):

    def __init__(self, x, y):

        if isinstance(x, NEG):
            x = f'({x})'
        if isinstance(x, NEG):
            y = f'({y})'

        self._value = f'{x} + {y}'


class SUB(ArithmeticBase):

    def __init__(self, x, y):

        if isinstance(x, NEG):
            x = f'({x})'
        if isinstance(x, NEG):
            y = f'({y})'
        self._value = f'{x} - {y}'


class MUL(ArithmeticBase):

    def __init__(self, x, y):

        if isinstance(x, (NEG, ADD, SUB)):
            x = f'({x})'
        if isinstance(x, (NEG, ADD, SUB)):
            y = f'({y})'
        self._value = f'{x} * {y}'


class DIV (ArithmeticBase):

    def __init__(self, x, y):

        if isinstance(x, (NEG, ADD, SUB)):
            x = f'({x})'
        if isinstance(x, (NEG, ADD, SUB)):
            y = f'({y})'
        self._value = f'{x} / {y}'


class MathFuncBase(ArithmeticBase):
    """Base for SQL-Function"""

    def __init__(self, *values):

        params = ', '.join([str(v) for v in values if v is not None])
        self._value = f'{self.__class__.__name__.lower()}({params})'


class FuncBase(ExpBase):

    def __init__(self, *values):

        params = ', '.join([str(v) for v in values if v is not None])
        self._value = f'{self.__class__.__name__.lower()}({params})'


class AggregateBase(ExpBase):

    def __init__(self, field):
        self._value = f'{self.__class__.__name__.lower()}({field})'