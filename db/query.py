"""Some functions or decorators about commit SQL Query"""

from .connection import ConnectConfigError, connect


def execute(connection, query):

    sql = str(query)
    with connection.cursor() as cursor:
        row = cursor.execute(sql)
    return row


def execute_commit(connection, query):
    """Execute INSERT, UPDATE, DELETE sql"""

    sql = str(query)
    try:
        with connection.cursor() as cursor:
            row = cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    return row


def execute_insert(connection, query):
    """Execute INSERT sql and fetch last_insert_id"""

    sql = str(query)
    try:
        with connection.cursor() as cursor:
            row = cursor.execute(sql)
            last = cursor.execute('SELECT last_insert_id()')
            last_id = cursor.fetchone()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    if isinstance(last_id, tuple):
        return last_id[0]
    else:
        return last_id['last_insert_id()']


def execute_fetch(connection, query):
    """Execute SELECT sql"""
    sql = str(query)
    with connection.cursor() as cursor:
        row = cursor.execute(sql)
        result = cursor.fetchall()
    return result, row


def execute_transaction(connection, queries):
    """Execute multi sql in a transaction"""

    sqls = [str(query) for query in queries]

    connection.begin()
    try:
        with connection.cursor() as cursor:
            for sql in sqls:
                cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

    return True


def query(conn_config=None, conn_pool=None):
    """Decorate a func which return a Query object. When call the func, it will execute the Query"""

    def decorator(func):

        query = func()

        def execute():

            if conn_config:
                query.connect_config(conn_config=conn_config)
            elif conn_pool:
                query.connect_config(pool=conn_pool)

            return query.exe()

        return execute

    return decorator


def transaction(conn_config=None, conn_pool=None):
    """Decorate a func which return a list of Query object. When call the func, execute 
    Queries in order as a transaction. It won't use the connection configration of any Query , So one of params is necessary.
    """

    if not conn_config and not conn_pool:
        raise ConnectConfigError

    def decorator(func):

        queries = func()

        def execute():

            if conn_config:
                with connect(conn_config) as conn:
                    result = execute_transaction(conn, queries)
            elif conn_pool:
                with conn_pool.connect() as conn:
                    result = execute_transaction(conn, queries)
            else:
                raise ConnectConfigError
            return result

        return execute

    return decorator
