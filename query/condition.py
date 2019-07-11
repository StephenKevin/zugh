
from datetime import date, datetime
from decimal import Decimal

from .base import ExpBase
from .core import Select


class ConditionBase(ExpBase):

    _operator = '='

    def __init__(self, condition):
        """"""
        if isinstance(condition, (str, Decimal, datetime, date)):
            c_str = f"'{condition}'"
        else:
            c_str = str(condition)
        self._value = f'{self._operator} {c_str}'


class eq(ConditionBase):
    _operator = '='


class ne(ConditionBase):
    _operator = '!='


class gt(ConditionBase):
    _operator = '>'


class ge(ConditionBase):
    _operator = '>='


class lt(ConditionBase):
    _operator = '<'


class le(ConditionBase):
    _operator = '<='


class like(ConditionBase):
    _operator = 'LIKE'


class unlike(ConditionBase):
    _operator = 'NOT LIKE'


class InBase(ConditionBase):
    """"""

    def __init__(self, *conditions):
        """`conditions` must be a `iterable` or a `query.Select` object"""
        c_str_list = []
        if isinstance(conditions[0], Select):
            cc = str(conditions)
        else:
            for c in conditions:
                if isinstance(c, (str, Decimal, datetime, date)):
                    c_str = f"'{c}'"
                else:
                    c_str = str(c)
                c_str_list.append(c_str)
            cc = ','.join(c_str_list)

        self._value = f'{self._operator} ({cc})'


class In(InBase):
    _operator = 'IN'


class NIn(InBase):
    _operator = 'NOT IN '
