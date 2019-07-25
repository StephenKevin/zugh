from datetime import datetime, timedelta
from queue import Queue

import pymysql


class PoolConnectContext:

    def __init__(self, config: dict, pool):
        self.config = config
        self.connection = pymysql.connect(**config)
        self.pool = pool
        self.life_until = datetime.now() + pool.conn_lifetime

    def __enter__(self):

        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.pool._put(self)

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            pass


class ConnectionPool:

    def __init__(self, conn_config: dict, max_size=256, conn_lifetime=512):

        self.conn_config = conn_config
        self._pool = Queue(max_size)
        self.conn_lifetime = timedelta(seconds=conn_lifetime)

    def _put(self, conn_context):
        """Put conn_context into pool if it still life"""

        if datetime.now() > conn_context.life_until:
            del conn_context
            return False
        if not conn_context.connection.open:
            del conn_context
            return False
        try:
            self._pool.put_nowait(conn_context)
        except Exception as e:
            del conn_context
            return False
        return True

    def connect(self):
        """Return a PoolConnectContext instance"""

        try:
            conn_context = self._pool.get_nowait()
            if datetime.now() > conn_context.life_until:
                del conn_context
            elif not conn_context.connection.open:
                del conn_context
            else:
                conn_context = PoolConnectContext(self.conn_config, self)
        except Exception as e:
            conn_context = PoolConnectContext(self.conn_config, self)

        return conn_context

    def size(self):
        return self._pool.qsize()

    def __del__(self):
        while not self._pool.empty():
            conn_context = self._pool.get_nowait()
            del conn_context
