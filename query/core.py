
from datetime import date, datetime
from decimal import Decimal
from typing import List, Tuple

from zugh.db.connection import ConnectConfigError, connect
from zugh.db.query import execute_commit, execute_fetch, execute_insert

from .base import ExpBase
from .others import As


class QueryBase(ExpBase):
    """abstract Query class"""

    def connect_config(self, conn_config: dict = None, pool=None):
        """A hook for Query object to configure connection"""

        self.conn_config = conn_config
        self.conn_pool = pool

    def exe(self):
        """"""
        if self.conn_config:
            with connect(self.conn_config) as conn:
                result = execute_commit(conn, self)
        elif self.conn_pool:
            with self.conn_pool.connect() as conn:
                result = execute_commit(conn, self)
        else:
            raise ConnectConfigError
        return result


class SelectBase(QueryBase):
    """Base for retrieve"""

    def exe(self):
        """"""

        if self.conn_config:
            with connect(self.conn_config) as conn:
                result = execute_fetch(conn, self)
        elif self.conn_pool:
            with self.conn_pool.connect() as conn:
                result = execute_fetch(conn, self)
        else:
            raise ConnectConfigError
        return result

    def as_table(self, alias: str):
        """Return a instance of TempTable"""

        from zugh.schema.table import TempTable
        return TempTable(self, alias)

    def union(self, other):
        return Union(self, other)

    def union_all(self, other):
        return Union(self, other, distinct=False)


class LimitMixin(SelectBase):

    def __getitem__(self, key):
        """support slice for select query"""

        if not isinstance(key, slice):
            raise Exception(
                'unsupport index, please condiser using slice instead')
        start = key.start or 0
        stop = key.stop or 18446744073709551616
        if start < 0 or stop < 0:
            raise Exception('unsupport negative slice')
        if stop <= start:
            raise Exception('slice.stop must great than slice.start')

        return Limit(self, stop - start, start)


class Select(LimitMixin):
    """"""

    def __init__(self, where, fields: tuple = None, alias_fields: dict = None):
        """"""
        self.conn_config = where.conn_config
        self.conn_pool = where.conn_pool
        if fields or alias_fields:
            fs = [str(f) for f in fields]
            af = [str(As(f, a)) for a, f in alias_fields.items()]
            fs.extend(af)
            fields_str = ', '.join(fs)
        else:
            fields_str = '*'

        if str(where):
            self._value = f'SELECT {fields_str} FROM {where.table} {where}'
        else:
            self._value = f'SELECT {fields_str} FROM {where.table}'

    def order_by(self, *fields):
        return OrderBy(self, fields)

    def group_by(self, *fields):
        return GroupBy(self, fields)


class OrderBy(LimitMixin):

    def __init__(self, select, fields):

        self.conn_config = select.conn_config
        self.conn_pool = select.conn_pool
        f_str = []
        for f in fields:
            if f.startswith('-'):
                f = f[1:]
                f_str.append(f'{f} DESC')
            else:
                f_str.append(f)
        self._value = f"{select} ORDER BY {', '.join(f_str)}"


class GroupBy(LimitMixin):
    """"""

    def __init__(self, select, fields):

        self.conn_config = select.conn_config
        self.conn_pool = select.conn_pool
        self._value = f"{select} GROUP BY {','.join(fields)}"

    def order_by(self, *fields):
        return OrderBy(self, fields)


class Limit(SelectBase):

    def __init__(self, select, length, offset=None):
        """Limit"""

        self.conn_config = select.conn_config
        self.conn_pool = select.conn_pool
        if offset:
            self._value = f'{select} LIMIT {offset}, {length}'
        else:
            self._value = f'{select} LIMIT {length}'


class Union(LimitMixin):

    def __init__(self, select, other, distinct=True):

        self.conn_config = select.conn_config
        self.conn_pool = select.conn_pool
        if distinct:
            self._value = f'{select} UNION {other}'
        else:
            self._value = f'{select} UNION ALL {other}'

    def order_by(self, *fields):
        return OrderBy(self, fields)


class Update(QueryBase):
    """"""

    def __init__(self, where, kwargs):

        assert kwargs, 'Update() params error. No field to update!'
        self.conn_config = where.conn_config
        self.conn_pool = where.conn_pool
        kv = []
        for k, v in kwargs.items():
            k = k.replace('__', '.')
            if isinstance(v, (str, Decimal, datetime, date)):
                kv.append(f"{k} = '{v}'")
            else:
                kv.append(f'{k} = {v}')
        kv_str = ', '.join(kv)
        self._value = f"UPDATE {where.table} SET {kv_str} {where}"


class Delete(QueryBase):
    """"""

    def __init__(self, where, tables=None):

        self.conn_config = where.conn_config
        self.conn_pool = where.conn_pool
        if tables:
            tables_str = ','.join([str(tb) for tb in tables])
            self._value = f"DELETE {tables_str} FROM {where.table} {where}"
        else:
            self._value = f"DELETE FROM {where.table} {where}"


class Insert(QueryBase):
    """Insert row/rows"""

    fetch_last_id = False

    def __init__(self, table, row: dict = None, rows: List[dict] = None, ignore=False, duplicate_update=None):

        self.conn_config = table.conn_config
        self.conn_pool = table.conn_pool
        if row:
            self.fetch_last_id = True
            f_str = self.fields_str(row.keys())
            v_str = self.values_str(row.values())
        elif rows:
            f_str = self.fields_str(rows[0].keys())
            v_str_list = [self.values_str(r.values()) for r in rows]
            v_str = ', '.join(v_str_list)
        else:
            raise Exception('Insert() params error. No content to insert.')

        if ignore:
            self.fetch_last_id = False
            self._value = f'INSERT IGNORE INTO {table} {f_str} VALUES {v_str}'
        elif duplicate_update:
            self.fetch_last_id = False
            up_list = [f'{k} = {v}' for k, v in duplicate_update.items()]
            up_str = ', '.join(up_list)
            self._value = f'INSERT INTO {table} {f_str} VALUES {v_str} ON DUPLICATE KEY UPDATE {up_str}'
        else:
            self._value = f'INSERT INTO {table} {f_str} VALUES {v_str}'

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

    def exe(self):

        if self.conn_config:
            with connect(self.conn_config) as conn:
                if self.fetch_last_id:
                    result = execute_insert(conn, self)
                else:
                    result = execute_commit(conn, self)
        elif self.conn_pool:
            with self.conn_pool.connect() as conn:
                if self.fetch_last_id:
                    result = execute_insert(conn, self)
                else:
                    result = execute_commit(conn, self)
        else:
            raise ConnectConfigError
        return result


class InsertQuery(Insert):
    """Insert rows from a subquery"""

    def __init__(self, table, fields: Tuple[str], query):

        self.conn_config = table.conn_config
        self.conn_pool = table.conn_pool
        f_str = self.fields_str(fields)
        self._value = f'INSERT INTO {table} {f_str} {query}'
