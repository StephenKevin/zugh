import pymysql


def connect_config(host: str, user: str, password: str = "", database: str = None, **kwargs):
    """Return a dict including config for connection. For more parameters, please refer to `pymysql.connect()`"""

    config = dict(host=host, user=user)
    if password:
        config['password'] = password
    if database:
        config['database'] = database
    config.update(kwargs)
    return config


class ConnectionContext():

    def __init__(self, config: dict):

        self.config = config

    def __enter__(self):

        self.connection = pymysql.connect(**self.config)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.connection.close()


connect = ConnectionContext


class ConnectError(Exception):

    def __init__(self, name):

        self.name = name


ConnectConfigError = ConnectError(
    'No configurations info for DB connection, and no pool to use')
