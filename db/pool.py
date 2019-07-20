from collections import deque
from datetime import datetime, timedelta

import pymysql


class PoolConnectContext:

    def __init__(self, config: dict, pool):
        self.config = config
        self.connection = pymysql.connect(**config)
        self.pool = pool
        self.pool._idle.append(self)

    def __enter__(self):

        self.pool._used.append(self)
        self.pool._idle.remove(self)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.last_used = datetime.now()
        self.pool._used.remove(self)
        self.pool._idle.append(self)
        self.pool.clear_idle()


class ConnectionPool:

    def __init__(self, timeout=60):

        self.conn_timeout = timedelta(seconds=timeout)
        self._idle = deque()
        self._used = deque()

    def connect_config(self, config: dict):
        """Params for connect to DB"""

        self.conn_config = config

    def clear_idle(self):

        refer = datetime.now() - self.conn_timeout
        idle = deque()
        for conn_context in self._idle:
            if conn_context.connection.open:
                if refer < conn_context.last_used:
                    idle.append(conn_context)
                else:
                    conn_context.connection.close()
        self._idle = idle

    def connect(self):
        """Return a PoolConnectContext instance"""

        refer = datetime.now() - self.conn_timeout
        for conn_context in self._idle:
            if refer < conn_context.last_used and conn_context.connection.open:
                return conn_context

        conn_context = PoolConnectContext(self.conn_config, self)
        return conn_context
