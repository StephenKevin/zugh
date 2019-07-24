

from datetime import date, datetime
from decimal import Decimal

from .base import ExpBase
from .condition import ConditionBase


class LogicBase(ExpBase):
    """Logic class to deal with logic relation"""

    def __or__(self, term):
        """use `|` to act OR"""
        return OR(self, term)

    def __and__(self, term):
        """use `&` to act AND"""
        return AND(self, term)


class L(LogicBase):
    """Convert express to Logic object"""

    def __init__(self, *terms, **kw_terms):
        """Logic object"""
        if len(terms)+len(kw_terms) != 1:
            raise Exception(
                'param error: L class must receive at least one and only one parameter')
        if terms:
            if not isinstance(terms[0], str):
                raise Exception('only accept string')
            self._value = terms[0]
        else:
            k, v = kw_terms.popitem()
            k = k.replace('__', '.')
            if isinstance(v, ConditionBase):
                self._value = f'{k} {v}'
            elif isinstance(v, (str, Decimal, datetime, date)):
                self._value = f"{k} = '{v}'"
            else:
                self._value = f'{k} = {v}'

    def __eq__(self, item):
        return self._value == str(item)

    def __repr__(self):
        return f'L({self})'


class ComplexLogicBase(LogicBase):

    def __init__(self, *terms, **kw_terms):

        self._terms = []

        for term in terms:
            self._add(term)
        for k, v in kw_terms.items():
            self._add(L(**{k: v}))

        t_list = []
        if len(self)==1:
            self._value = f'{self[0]}'
        else:
            for t in self:
                if isinstance(t, ComplexLogicBase):
                    t_str = f'({t})'
                else:
                    t_str = f'{t}'
                t_list.append(t_str)
            oper = f' {self.__class__.__name__} '
            self._value = oper.join(t_list)

    def __iter__(self):
        return iter(self._terms)

    def __len__(self):
        return len(self._terms)

    def __getitem__(self, key):
        return self._terms[key]

    def _add(self, term):
        if term not in self:
            if isinstance(term, LogicBase):
                if isinstance(term, self.__class__):
                    for t in term:
                        self._terms.append(t)
                else:
                    self._terms.append(term)
            else:
                self._terms.append(L(term))

    def __repr__(self):
        term_list = [repr(c) for c in self]
        v = ','.join(term_list)
        return f'{self.__class__.__name__}({v})'


class AND(ComplexLogicBase):
    """Logic AND"""


class OR(ComplexLogicBase):
    """Logic OR"""
