
class F:

    def __init__(self, field):
        """F object for complex query"""
        self._field = field

    def __str__(self):
        return self._field

    def __neg__(self):
        return self.__class__(f'-{self._field}')

    def __add__(self, value):
        return self.__class__(f'{self._field} + {value}')

    def __radd__(self, value):
        return self.__class__(f'{value} + {self._field}')

    def __sub__(self, value):
        return self.__class__(f'{self} - {value}')

    def __rsub__(self, value):
        return self.__class__(f'{value} - {self}')


class distinct:
    """distinct"""

    def __init__(self, field):
        """distinct object for DISTINCT keyword"""
        self._field = field

    def __str__(self):
        return f'DISTINCT {self._field}'


class values:
    def __init__(self, field):
        """values object for VALUES keyword"""
        self._field = field

    def __str__(self):
        return f'VALUES({self._field})'

    def __neg__(self):
        return f'-VALUES({self._field})'

    def __add__(self, value):
        return f'{self} + {value}'

    def __radd__(self, value):
        return f'{value} + {self}'

    def __sub__(self, value):
        return f'{self} - {value}'

    def __rsub__(self, value):
        return f'{value} - {self}'
