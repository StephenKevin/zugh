from query.filter import Where
from query.core import Insert, InsertMulti


class Table():
    """model for table"""

    def __init__(self, name: str, db=None):
        self.db = db
        self.name = name
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

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f"Table('{self.name}')"
