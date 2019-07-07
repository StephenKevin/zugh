
class AggregateBase:

    def __init__(self, field):
        self._field = str(field)

    def __str__(self):
        return f'{self._name}({self._field})'


class Count(AggregateBase):
    """Count class for `count` sql function"""
    _name = 'count'


class Max(AggregateBase):
    """Max class for `max` sql function"""
    _name = 'max'


class Min(AggregateBase):
    """Min class for `min` sql function"""
    _name = 'min'


class Sum(AggregateBase):
    """Sum class for `sum` sql function"""
    _name = 'sum'


class Avg(AggregateBase):
    """Avg class for `avg` sql function"""
    _name = 'avg'
