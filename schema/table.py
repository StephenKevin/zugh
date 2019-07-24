from typing import List

from zugh.query.core import Insert, InsertMulti, SelectBase, Update
from zugh.query.filter import Where
from zugh.query.others import As

from .db import DataBase


class Table():
    """model for table"""

    read_only = False

    def __init__(self, name: str, db: DataBase = None, alias: str = None):

        self.db = db
        self.name = name
        if db:
            self.full_name = f'{db.name}.{self.name}'
            self.conn_config = db.conn_config
            self.conn_pool = db.conn_pool
        else:
            self.full_name = self.name
            self.conn_config = None
            self.conn_pool = None
        if alias:
            self.alias = As(self, alias)
        else:
            self.alias = ''

    def where(self, *terms, **kw_terms):
        """return a `Where` query object"""
        return Where(self, terms, kw_terms)

    def select(self, *fields, **alias_fields):
        """select fields from table"""
        return self.where().select(*fields, *alias_fields)

    def insert(self, **field_values):
        """insert a row into table"""
        return Insert(self, field_values)

    def insert_ignore(self, **field_values):
        return Insert(self, field_values, True)

    def insert_multi(self, rows: List[dict]):
        """insert multi-lines into table"""
        return InsertMulti(self, rows)

    def insert_multi_ignore(self, rows: List[dict]):
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
        return f"Table({self})"


class TempTable(Table):

    read_only = True

    def __init__(self, query: SelectBase, alias: str):
        """TempTable class to support subquery"""
        self.db = None
        self.name = f'({query})'
        self.full_name = self.name
        self.alias = As(self, alias)
        self.conn_config = query.conn_config
        self.conn_pool = query.conn_pool

    def __repr__(self):
        return f"TempTable{self}"


class Join:

    join_type = 'JOIN'

    def __init__(self, table: Table, on):
        assert table.alias, f'Joined Table({table}) must have a alias.'
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
    """class for Join tables"""

    read_only = False

    def __init__(self, primary: Table, join: Join):
        """"""
        self.conn_config = primary.conn_config
        self.conn_pool = primary.conn_pool
        if isinstance(primary, JoinTable):
            self.primary = primary.primary
            self.join_list = []
            self.join_list.extend(primary.join_list)
            self.join_list.append(join)
        else:
            assert primary.alias, f'Joined Table({primary}) must have a alias.'
            self.primary = primary
            self.join_list = [join]

        j_strs = [str(j) for j in self.join_list]
        self.name = f"{self.primary.alias} {' '.join(j_strs)}"
        self.full_name = self.name

    def __repr__(self):
        return f"JoinTable({self})"
