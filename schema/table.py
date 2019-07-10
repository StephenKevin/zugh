from query.filter import Where
from query.core import Insert, InsertMulti
from query.others import As


class Table():
    """model for table"""

    def __init__(self, name: str, db=None, alias=None):

        self.db = db
        self.name = name
        self.alias = As(self, alias)
        if db:
            self.full_name = db.name + self.name
        else:
            self.full_name = self.name

    def where(self, *terms, **kw_terms):
        """return a `Where` query object"""
        return Where(self, terms, kw_terms)

    def select(self, *fields, **alias_fields):
        """select fields from table"""
        return Where(self).select(*fields, *alias_fields)

    def insert(self, **field_values):
        """insert a row into table"""
        return Insert(self, field_values)

    def insert_ignore(self, **field_values):
        return Insert(self, field_values, True)

    def insert_multi(self, rows):
        """insert multi-lines into table"""
        return InsertMulti(self, rows)

    def insert_multi_ignore(self, rows):
        return InsertMulti(self, rows, True)

    def upsert(self, row: dict, update_fv: dict):
        """insert a row or update it when duplicate key"""
        return Insert(self, row, duplicate_update=update_fv)

    def upsert_multi(self, rows):
        """"""
        # TODO

    def join(self, table, on):
        return JoinTable(self, Join(table, on))

    def inner_join(self, table, on):
        return JoinTable(self, InnerJoin(table, on))

    def left_join(self, table, on):
        return JoinTable(self, LeftJoin(table, on))

    def right_join(self, table, on):
        return JoinTable(self, RightJoin(table, on))

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f"Table('{self}')"


class Join:

    join_type = 'JOIN'

    def __init__(self, table, on):
        self.table = table
        self.on = on

    def __str__(self):
        return f'{self.join_type} {self.table.alias} ON {self.on}'


class InnerJoin(Join):
    join_type = 'INNER JOIN'


class LeftJoin(Join):
    join_type = 'LEFT JOIN'


class RightJoin(Join):
    join_type = 'RIGHT JOIN'


class JoinTable(Table):
    """"""

    def __init__(self, primary, join):
        """"""
        if isinstance(primary, JoinTable):
            self.primary = primary.primary
            self.join_list = []
            self.join_list.extend(primary.join_list)
            self.join_list.append(join)
        else:
            self.primary = primary
            self.join_list = [join]

        j_strs = [str(j) for j in self.join_list]
        self.name = f"{self.primary.alias} {' '.join(j_strs)}"
        self.full_name = self.name
