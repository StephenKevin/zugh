from .base import ExpBase


class F(ExpBase):

    def __init__(self, field):
        """F object for complex query. F object mean it is field instead str"""
        self._value = f'{field}'

    def __neg__(self):
        return self.__class__(f'-{self}')

    def __add__(self, other):
        return self.__class__(f'{self} + {other}')

    def __radd__(self, other):
        return self.__class__(f'{other} + {self}')

    def __sub__(self, other):
        return self.__class__(f'{self} - {other}')

    def __rsub__(self, other):
        return self.__class__(f'{other} - {self}')


class distinct(ExpBase):
    """distinct"""

    def __init__(self, field):
        """distinct object for DISTINCT keyword"""
        self._value = f'DISTINCT {field}'


class values(ExpBase):
    def __init__(self, field):
        """values object for VALUES keyword"""
        self._value = f'VALUES({field})'

    def __neg__(self):
        return f'-{self}'

    def __add__(self, other):
        return f'{self} + {other}'

    def __radd__(self, other):
        return f'{other} + {self}'

    def __sub__(self, other):
        return f'{self} - {other}'

    def __rsub__(self, other):
        return f'{other} - {self}'


class As(ExpBase):

    def __init__(self, entity, name: str):
        self._value = f'{entity} AS {name}'