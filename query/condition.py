
from datetime import date, datetime
from decimal import Decimal

from .base import ExpBase
from .core import SelectBase
from .others import F


class ConditionBase(ExpBase):

    def __init__(self, condition, operator=None):
        """"""

        if operator is not None:
            self._operator = operator
        if isinstance(condition, (str, Decimal, datetime, date)):
            self._value = f"{self._operator} '{condition}'"
        else:
            self._value = f'{self._operator} {condition}'


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


class In(ConditionBase):
    """IN"""

    _operator = 'IN'

    def __init__(self, *conditions):
        """ condition could be str, int as well as `query.SelectBase` instance"""
        
        if isinstance(conditions[0], SelectBase):
            cc = str(conditions[0])
        else:
            c_str_list = []
            for c in conditions:
                if isinstance(c, (str, Decimal, datetime, date)):
                    c_str = f"'{c}'"
                else:
                    c_str = str(c)
                c_str_list.append(c_str)
            cc = ','.join(c_str_list)

        self._value = f'{self._operator} ({cc})'


class NIn(In):
    """NOT IN"""

    _operator = 'NOT IN'


NULL = ConditionBase(F('NULL'), 'IS')

NOT_NULL = ConditionBase(F('NOT NULL'), 'IS')
