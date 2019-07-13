
from datetime import date, datetime
from decimal import Decimal

from .base import ExpBase
from .others import As


class QueryBase(ExpBase):
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
        length = key.stop - key.start
        return Limit(self, length, offset)


class Select(SelectBase):
    """"""

    def __init__(self, where, fields: tuple = None, alias_fields: dict = None):
        """"""
        if fields or alias_fields:
            fs = [str(f) for f in fields]
            af = [str(As(f, a)) for a, f in alias_fields.items()]
            fs.extend(af)
            fields_str = ', '.join(fs)
        else:
            fields_str = '*'

        self._value = f'SELECT {fields_str} FROM {where._tb} {where}'

    def order_by(self, *fields):
        return OrderBy(self, fields)

    def group_by(self, *fields):
        return GroupBy(self, fields)


class OrderBy(SelectBase):

    def __init__(self, select, fields):
        f_str = []
        for f in fields:
            if f.startswith('-'):
                f = f[1:]
                f_str.append(f'{f} DESC')
            else:
                f_str.append(f)
        self._value = f"{select} ORDER BY {', '.join(f_str)}"


class GroupBy(SelectBase):
    """"""

    def __init__(self, select, fields):
        self._value = f"{select} GROUP BY {','.join(fields)}"

    def order_by(self, *fields):
        return OrderBy(self, fields)


class Limit(QueryBase):

    def __init__(self, select, length, offset=None):
        if offset:
            self._value = f'{select} LIMIT {offset}, {length}'
        else:
            self._value = f'{select} LIMIT {length}'


class Update(QueryBase):
    """"""

    def __init__(self, where, kwargs):
        kv = []
        for k, v in kwargs.items():
            k = k.replace('__', '.')
            if isinstance(v, (str, Decimal, datetime, date)):
                kv.append(f"{k} = '{v}'")
            else:
                kv.append(f'{k} = {v}')
        kv_str = ', '.join(kv)
        self._value = f"UPDATE {where._tb} SET {kv_str} {where}"


class Delete(QueryBase):
    """"""

    def __init__(self, where, tables):
        if tables:
            tables_str = ','.join([str(tb) for tb in tables])
            self._value = f"DELETE {tables_str} FROM {where._tb} {where}"
        else:
            self._value = f"DELETE FROM {where._tb} {where}"


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
        f_str = self.fields_str(row.keys())
        v_str = self.values_str(row.values())
        if ignore:
            self._value = f'INSERT IGNORE INTO {table} {f_str} VALUES {v_str}'
        elif duplicate_update:
            up_list = [f'{k} = {v}' for k, v in duplicate_update.items()]
            up_str = ', '.join(up_list)
            self._value = f'INSERT INTO {table} {f_str} VALUES {v_str} ON DUPLICATE UPDATE {up_str}'
        else:
            self._value = f'INSERT INTO {table} {f_str} VALUES {v_str}'


class InsertMulti(InsertBase):
    """query object which insert mutil-rows into table"""

    def __init__(self, table, rows: list, ignore=False):
        
        f_str = self.fields_str(rows[0].keys())
        v_str_list = [self.values_str(r.values()) for r in rows]
        v_str = ', '.join(v_str_list)
        if ignore:
            self._value = f'INSERT IGNORE INTO {table} {f_str} VALUES {v_str}'
        else:
            self._value = f'INSERT INTO {table} {f_str} VALUES {v_str}'
