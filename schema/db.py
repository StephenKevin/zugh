from zugh.db.connection import ConnectConfigError, connect
from zugh.db.pool import ConnectionPool
from zugh.db.query import execute


class DataBase:

    conn_config = None
    conn_pool = None

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def connect_config(self, config: dict = None, pool: ConnectionPool = None):
        """connection configuration"""

        self.conn_config = config
        self.conn_pool = pool

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
