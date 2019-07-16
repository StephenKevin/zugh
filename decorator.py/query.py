

def commit(func):
    """decorator to generate query function from query object"""

    statement = str(func())

    def query():
        """"""
        statement = statement

        # TODO

    return query



def transaction(func):

    statements = [str(q) for q in func()]

    def query():

        statements = statements

    return query

