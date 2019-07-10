
from datetime import date, datetime
from decimal import Decimal
from .others import As


class QueryBase:
    """abstract Query class"""

    def commit():
        """"""
        # TODO


class SelectBase(QueryBase):

    def __getitem__(self, key):
        """support slice for select query"""
        if not isinstance(key, slice):
            raise Exception(
                'unsupport index, please condiser using slice instead')
        if key.start < 0 or key.stop < 0:
            raise Exception('unsupport negative slice')
        if key.stop <= key.start:
            raise Exception('slice.stop must great than slice.start')

        offset = key.start
        length = key.stop - key.start - 1
        return Limit(self, length, offset)


class Select(SelectBase):
    """"""

    def __init__(self, where, fields: tuple = None, alias_fields: dict = None):
        """"""
        self._where = where
        if fields or alias_fields:
            fs = [str(f) for f in fields]
            af = [f'{As(f, a)}' for a, f in alias_fields.items()]
            fs.extend(af)
            self.fields_str = ', '.join(fs)
        else:
            self.fields_str = '*'

        self._clause = f'SELECT {self.fields_str} FROM {self._where._tb}'

    def __str__(self):
        return self._clause + self._where._clause

    def order_by(self, *fields):
        return OrderBy(self, fields)

    def group_by(self, *fields):
        return GroupBy(self, fields)

    def __getitem__(self, key):
        """support slice for select query"""
        if not isinstance(key, slice):
            raise Exception(
                'unsupport index, please condiser using slice instead')
        if key.start < 0 or key.stop < 0:
            raise Exception('unsupport negative slice')
        if key.stop <= key.start:
            raise Exception('slice.stop must great than slice.start')

        offset = key.start
        length = key.stop - key.start - 1
        return Limit(self, length, offset)


class OrderBy(SelectBase):

    def __init__(self, select, fields):
        self._select = select
        f_str = []
        for f in fields:
            if f.startswith('-'):
                f = f[1:]
                f_str.append(f'{f} DESC')
            else:
                f_str.append(f)
        self._clause = f"ORDER BY {', '.join(f_str)}"

    def __str__(self):
        return f'{self._select} {self._clause}'


class GroupBy(SelectBase):
    """"""

    def __init__(self, select, fields):
        self._select = select
        self._clause = f"GROUP BY {','.join(fields)}"

    def __str__(self):
        return f'{self._select} {self._clause}'

    def order_by(self, *fields):
        return OrderBy(self, fields)


class Limit(QueryBase):

    def __init__(self, select, length, offset=None):
        self._select = select
        if offset:
            self._clause = f'LIMIT {offset}, {length}'
        else:
            self._clause = f'LIMIT {length}'

    def __str__(self):
        return f'{self._select} {self._clause}'


class Update(QueryBase):
    """"""

    def __init__(self, where, kwargs):
        self._where = where
        kv = []
        for k, v in kwargs.items():
            if isinstance(v, (str, Decimal, datetime, date)):
                kv.append(f"{k} = '{v}'")
            else:
                kv.append(f'{k} = {v}')
        kv_str = ', '.join(kv)
        self._clause = f"UPDATE TABLE {self._where._tb} SET {kv_str}"

    def __str__(self):
        return self._clause + self._where._clause


class Delete(QueryBase):
    """"""

    def __init__(self, where):
        self._where = where
        self._clause = f"DELETE FROM {self._where._tb}"

    def __str__(self):
        return self._clause + self._where._clause


class InsertBase(QueryBase):

    @staticmethod
    def fields_str(fields):
        return f"({', '.join(fields)})"

    @staticmethod
    def values_str(values):
        vs = []
        for v in values:
            if isinstance(v, (str, Decimal, datetime, date)):
                vs.append(f"'{v}'")
            else:
                vs.append(str(v))
        return f"({', '.join(vs)})"


class Insert(InsertBase):
    """"""

    def __init__(self, table, row: dict, ignore=False, duplicate_update=None):
        self._tb = table
        f_str = self.fields_str(row.keys())
        v_str = self.values_str(row.values())
        ignore_word = ' IGNORE ' if ignore else ' '
        if duplicate_update:
            up_list = []
            for k, v in duplicate_update.items():
                up_list.append(f'{k} = {v}')
            up_str = ', '.join(up_list)
            up_clause = f' ON DUPLICATE UPDATE {up_str}'
        else:
            up_clause = ''
        self._clause = f'INSERT{ignore_word}INTO {self._tb} {f_str} VALUES {v_str}{up_clause}'

    def __str__(self):
        return self._clause


class InsertMulti(InsertBase):
    """query object which insert mutil-rows into table"""

    def __init__(self, table, rows: list, ignore=False):
        self._tb = table

        f_str = self.fields_str(rows[0].keys())
        v_str_list = [self.values_str(r.values()) for r in rows]
        v_str = ', '.join(v_str_list)
        ignore_word = ' IGNORE ' if ignore else ' '
        self._clause = f'INSERT{ignore_word}INTO {self._tb} {f_str} VALUES {v_str}'

    def __str__(self):
        return self._clause
