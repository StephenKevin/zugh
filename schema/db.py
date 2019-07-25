from zugh.db.connection import ConnectConfigError, connect
from zugh.db.pool import ConnectionPool
from zugh.db.query import execute


class DataBase:

    conn_config = None
    conn_pool = None

    def __init__(self, name: str, conn_config: dict = None, pool: ConnectionPool = None):

        self.name = name
        self.conn_config = conn_config
        self.conn_pool = pool

    def __str__(self):
        return self.name

    def create(self):
        """Create database"""

        sql = f'CREATE DATABASE {self}'
        if self.conn_config:
            with connect(self.conn_config) as conn:
                result = execute(conn, sql)
        elif self.conn_pool:
            with self.conn_pool.connect() as conn:
                result = execute(conn, sql)
        else:
            raise ConnectConfigError
        return result
