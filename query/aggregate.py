from .base import AggregateBase


class Count(AggregateBase):
    """Count class for `count` sql function"""


class Max(AggregateBase):
    """Max class for `max` sql function"""


class Min(AggregateBase):
    """Min class for `min` sql function"""


class Sum(AggregateBase):
    """Sum class for `sum` sql function"""


class Avg(AggregateBase):
    """Avg class for `avg` sql function"""
