from .base import ExpBase
from .core import Delete, Select, Update
from .logic import AND


class WhereBasic(ExpBase):
    """Filter which have basic method, can not operate `update` or `delete`"""

    def __init__(self, table, terms=None, kw_terms=None):
        """
        The terms will be deal with in AND logic.If you need more 
        complex logic, looking into `logic.AND` and `logic.OR`.
        You can use those logic class to combine all the situation.
        """

        self.table = table
        self.conn_config = table.conn_config
        self.conn_pool = table.conn_pool
        if terms or kw_terms:
            logic = AND(*terms, **kw_terms)
            self._value = f'WHERE {logic}'
        else:
            self._value = ''

    def select(self, *fields, **alias_fields):
        """"""
        return Select(self, fields, alias_fields)

    def order_by(self, *fields):
        return self.select().order_by(*fields)

    def exe(self):
        """Shortcut to call `where().select().exe()`. You should always know that `Where` object isn't `Query` object"""
        return self.select().exe()


class Where(WhereBasic):
    """Filter which have full method"""

    def update(self, **field_values):
        """"""
        return Update(self, field_values)

    def delete(self, *tables):
        """"""
        return Delete(self, tables)
