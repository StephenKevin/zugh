from .base import ExpBase, ArithmeticBase


class F(ArithmeticBase):

    def __init__(self, field):
        """F object for complex query. F object mean it is field instead str"""
        self._value = f'{field}'


class distinct(ExpBase):
    """distinct"""

    def __init__(self, field):
        """distinct object for DISTINCT keyword"""
        self._value = f'DISTINCT {field}'


class values(ArithmeticBase):
    def __init__(self, field):
        """values object for VALUES keyword"""
        self._value = f'VALUES({field})'


class As(ExpBase):

    def __init__(self, entity, name: str):
        self._value = f'{entity} AS {name}'