
from .logic import AND
from .core import QueryBase, Select, Update, Delete


class Where(QueryBase):
    """"""

    def __init__(self, table, terms=None, kw_terms=None):
        """
        The terms will be deal with in AND logic.If you need more 
        complex logic, looking into `logic.AND` and `logic.OR`.
        You can use those logic class to combine all the situation.
        """
        self._tb = table
        if terms or kw_terms:
            logic = AND(*terms, **kw_terms)
            self._clause = f' WHERE {logic.get_str}'
        else:
            self._clause = ''

    def __str__(self):
        return self._clause

    def select(self, *fields, **alias_fields):
        """"""
        return Select(self, fields, alias_fields)

    def order_by(self, *fields):
        return self.select().order_by(*fields)

    def update(self, **field_values):
        """"""
        return Update(self, field_values)

    def delete(self):
        """"""
        return Delete(self)
