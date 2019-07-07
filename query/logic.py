

from datetime import date, datetime
from decimal import Decimal

from .condition import ConditionBase


class LogicBase:
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
            self.value = terms[0]
        else:
            for k, v in kw_terms.items():
                if isinstance(v, ConditionBase):
                    self.value = f'{k}{v}'
                elif isinstance(v, (str, Decimal, datetime, date)):
                    self.value = f"{k} = '{v}'"
                else:
                    self.value = f'{k} = {v}'

    def __eq__(self, item):
        return self.value == str(item)

    def __str__(self):
        return self.value

    @property
    def get_str(self):
        return self.value

    def __repr__(self):
        return f'L({self.value})'


class ComplexLogicBase(LogicBase):

    def __init__(self, *terms, **kw_terms):
        self.terms = []
        for term in terms:
            if isinstance(term, LogicBase):
                self._add(term)

        for k, v in kw_terms.items():
            self._add(L(**{k: v}))

    def __iter__(self):
        return iter(self.terms)

    def __len__(self):
        return len(self.terms)

    def __getitem__(self, key):
        return self.terms[key]

    def _add(self, term):
        if term not in self:
            if isinstance(term, LogicBase):
                if isinstance(term, self.__class__):
                    for t in terms:
                        self.terms.append(term)
                else:
                    self.terms.append(term)
            else:
                self.terms.append(L(term))

    def __str__(self):
        """return the logic statement"""
        return f'({self.get_str})'

    @property
    def get_str(self):
        if len(self) == 1:
            return self[0].get_str
        else:
            term_list = [str(c) for c in self]
            op = f' {self.__class__.__name__} '
            v = op.join(term_list)
            return f'{v}'

    def __repr__(self):
        term_list = [repr(c) for c in self]
        v = ','.join(term_list)
        return f'{self.__class__.__name__}({v})'


class AND(ComplexLogicBase):
    """Logic AND"""


class OR(ComplexLogicBase):
    """Logic OR"""
