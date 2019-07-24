# Zugh

**[WIP] Access to database in pythonic way**

- [Zugh](#zugh)
  - [Status](#status)
  - [Required](#required)
  - [Licence](#licence)
  - [Install](#install)
- [Usage](#usage)
  - [Connection](#connection)
    - [Config](#config)
    - [Pool](#pool)
  - [Database](#database)
  - [Table](#table)
  - [Query Object](#query-object)
  - [Insert](#insert)
    - [Insert a Row](#insert-a-row)
    - [Insert Ignore](#insert-ignore)
    - [Insert Or Update](#insert-or-update)
    - [Insert Multi Rows](#insert-multi-rows)
  - [Select](#select)
    - [Filter](#filter)
      - [Logic Express](#logic-express)
      - [Compare](#compare)
    - [Alias](#alias)
    - [Sort](#sort)
    - [Limit](#limit)
    - [Aggregate](#aggregate)
    - [Distinct](#distinct)
    - [Subquery](#subquery)
    - [Join In](#join-in)
    - [Union](#union)
  - [Update](#update)
    - [F Object](#f-object)
  - [Delete](#delete)
  - [Decorator](#decorator)
    - [db.query.query](#dbqueryquery)
    - [db.query.transaction](#dbquerytransaction)
  - [String](#string)
    - [S Object](#s-object)
  - [Math](#math)

**Zugh** is a tool for access to databases flexibly in pythonic way. It empower you use complex SQL, but didn't need to write them directly.

## Status

Work in progress.

Now we support MySQL only.

## Required

- Python >= 3.6
- PyMySQL >= 0.9.3

## Licence

MIT.

## Install

Use pip:

```sh
pip install zugh
```

# Usage

>Note !\
>The time of writing each part of this document is out of order. So the results before and after the execution of SQL may not match. Nevertheless, I recommend that you start reading from scratch and try the code.

## Connection

### Config

```py
>>> from zugh.db.connection import connect_config
>>> conn_config = connect_config('localhost', 'your_username', 'your_password')
# You can use conn_config dict to configure connection for DdataBase object
# or initial a connection pool
```

### Pool

```py
>>> from zugh.db.pool import ConnectionPool
>>> pool = ConnectionPool(conn_config)
```

## Database

Create a databses:

```py
>>> from zugh.schema.db import DataBase
>>> db = DataBase('zugh', conn_config=conn_config)
# or db = DataBase('zugh', pool=pool)
>>> db.create()
```

## Table

Create a table.

We haven't implemented those APIs to create a table yet, so just execute SQL in a connection:

```py
>>> from zugh.db import connect
>>> sql = """
CREATE TABLE zugh.users (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age` int(11) NOT NULL,
  `score` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;
"""
>>> conn = connect(conn_config) # return a connection context
>>> with conn as cn:
        with cn.cursor() as cursor:
            cursor.execute(sql)
```

Initial a `Table` object:

```py
>>> from zugh.schema.table import Table
>>> tb = Table('users', db)
```

## Query Object

`zugh.query.core.QueryBase` provide a base class for Query class below:

- `zugh.query.core.SelectBase`
- `zugh.query.core.Update`
- `zugh.query.core.Insert`
- `zugh.query.core.Delete`
- or subclass of above class

`Query object` is a instance of above class. If they were printed, a string of SQL statement would output.If configure properly, they can call `.exe()` method to execute. Usually, you don't use them
directly.

Mostly, you would initial a `zugh.schema.table.Table` instance and call relative method, then will return a new `Query object`.

Dangerous queries, such as `update`, `delete` or similar mothed are expose after `Table.where()` method.

```py
>>> q_1 = tb.where().select()
>>> type(q_1)
<class 'zugh.query.core.Select'>
>>> q_2 = tb.where().update(age=10)
>>> type(q_2)
<class 'zugh.query.core.Update'>
>>> q_3 = tb.where().delete()
>>> type(q_3)
<class 'zugh.query.core.Delete'>
>>> q_4 = tb.insert(dict(age=10, score=18))
>>> type(q_4)
<class 'zugh.query.core.Insert'>
>>> q_5 = q_1.order_by()
>> type(q_5)
<class 'zugh.query.core.OrderBy'>
```

## Insert

### Insert a Row

```py
>>> q1 = tb.insert(age=16, score=7)
>>> print(q1)
INSERT INTO zugh.users (age, score) VALUES (16, 7)
>>> q2 = tb.where().select()
>>> print(q2)
SELECT * FROM zugh.users
>>> q2.exe() # execute q2
((), 0)
>>> q1.exe() # execute q1
1
>>> q2.exe() # execute q2 again
(((1, 16, 7),), 1)
```

### Insert Ignore

```py
>>> q3 = tb.insert_ignore(id=1, age=16, score=7)
>>> print(q3)
INSERT IGNORE INTO zugh.users (id, age, score) VALUES (1, 16, 7)
>>> q3.exe() # would show a duplicate key warning
```

### Insert Or Update

You can use `F` object or `values` object to complete complex query.

```py
from zugh.query.others import F, values
>>> row = dict(id=1, age=16, score=7)
>>> q4 = tb.upsert(row, dict(age=9))
>>> print(q4)
INSERT INTO zugh.users (id, age, score) VALUES (1, 16, 7) ON DUPLICATE UPDATE age = 9
>>> update_fv = dict(age=F('age')-1, score=values('age')+1)
>>> q5 = tb.upsert(row, update_fv=update_fv)
>>> print(q5)
INSERT INTO zugh.users (id, age, score) VALUES (1, 16, 7) ON DUPLICATE UPDATE age = age - 1, score = VALUES(age) + 1
```

### Insert Multi Rows

```py
>>> rows = [
    dict(age=9, score=8),
    dict(age=7, score=9),
    dict(age=17, score=7),
    dict(age=23, score=7),
  ]

>>> q6 = tb.insert_multi(rows)
>>> print(q6)
INSERT INTO zugh.users (age, score) VALUES (9, 8), (7, 9), (17, 7), (23, 7)
>>> q6.exe() # execute q6
4
>>> q2.exe()
(((1, 16, 7), (2, 9, 8), (3, 7, 9), (4, 17, 7), (5, 23, 7)), 5)
```

## Select

```py
>>> q7 = tb.where(id=3).select()
>>> print(q7)
SELECT * FROM zugh.users WHERE id = 3
>>> q7.exe()
(((3, 7, 9),), 1)
>>> q8 = tb.where().select('id', 'age')
>>> print(q8)
SELECT id, age FROM zugh.users
>>> q8.exe()
(((1, 16), (2, 9), (3, 7), (4, 17), (5, 23)), 5)
```

### Filter

the `Table.where()` method of Table instance act as a filter.

If don't need to filter table, You can call `Table.select()` directly. It is a shortup of `Table.where().select()`.

#### Logic Express

```py
>>> from zugh.query.logic import AND, OR, L
>>> q9 = tb.where('id>3', 'id<7').select()
>>> print(q9)
SELECT * FROM zugh.users WHERE id>3 AND id<7
>>> q9.exe()
(((4, 17, 7), (5, 23, 7)), 2)

>>> w1 = L('id<3')|L('id>7') # equal to OR('id<3', 'id>7')
>>> w2 = OR('id<3', 'id>7')
>>> w1
OR(L(id<3),L(id>7))
>>> w2
OR(L(id<3),L(id>7))
>>> print(w1)
id<3 OR id>7
>>> print(w2)
id<3 OR id>7

>>> q10 = tb.where(w2).select()
>>> print(q10)
SELECT * FROM zugh.users WHERE (id<3 OR id>7)
>>> q10.exe()
(((1, 16, 7), (2, 9, 8)), 2)

# you can combine complex Logic object use L, OR and AND

>>> w3 = L('id>3') & L('id<7') # equal to AND('id>3', 'id<7')
>>> print(w3)
id>3 AND id<7
>>> w4 = L('age>3') & L('age<20')
>>> print(w4)
age>3 AND age<20

>>> print(OR(w3, w4))
(id>3 AND id<7) OR (age>3 AND age<20)
>>> print(w3|w4)
(id>3 AND id<7) OR (age>3 AND age<20)
```

#### Compare

We use class or their instance to deal with compare express.You can find them in `zugh.query.condition` module.

| SQL Operator | Python Class/Instance/Operator |           example            |
| ------------ | ------------------------------ | ---------------------------- |
| =            | `eq`, `=`                      | .where(name='lisa')          |
| !=           | `ne`                           | .where(name=ne('lisa'))      |
| >            | `gt`                           | .where(amount=gt(9))         |
| >=           | `ge`                           | .where(amount=ge(9))         |
| <            | `lt`                           | .where(amount=lt(6))         |
| <=           | `le`                           | .where(amount=le(5))         |
| IN           | `In`                           | .where(id=In(1,2,3,4))       |
| NOT IN       | `NIn`                          | .where(id=NIn(98,34,2))      |
| LIKE         | `like`                         | .where(name=like('lisa%'))   |
| NOT LIKE     | `unlike`                       | .where(name=unlike('john%')) |
| IS NULL      | `NULL`                         | .where(age=NULL)             |
| IS NOT NULL  | `NOT_NULL`                     | .where(age=NOT_NULL)         |

Though works, `eq` is meaningless. For convenience, you would always use `=` .

```py
>>> from zugh.query.condition import NOT_NULL, NULL, In, NIn, ge, gt, le, like, lt, ne, unlike
>>> q11 = tb.where(id=gt(3)).select()
>>> print(q11)
SELECT * FROM zugh.users WHERE id > 3

>>> q12 = tb.where(id=gt(3), age=lt(18)).select()
>>> print(q12)
SELECT * FROM zugh.users WHERE id > 3 AND age < 18
>>> q12.exe()
(((4, 17, 7),), 1)

>>> q13 = tb.where(id=In(1,3,5,7,9)).select('id', 'score')
>>> print(q13)
SELECT id, score FROM zugh.users WHERE id IN (1,3,5,7,9)
>>> q13.exe()
(((1, 7), (3, 9), (5, 7)), 3)

>>> q14 = tb.where(score=NULL).select()
>>> print(q14)
SELECT * FROM zugh.users WHERE score IS NULL
```

### Alias

```py
>>> from zugh.query.others import As
>>> from zugh.query.aggregate import Max
>>> qa = tb.where().select(max_age=Max('age'))
>>> print(qa)
SELECT max(age) AS max_age FROM zugh.users
>>> print(tb.where().select(As(Max('age'), 'max_age')))
SELECT max(age) AS max_age FROM zugh.users
```

We support alias, but the default `cursorclass` of PyMySQL will return query set in tuple. In this case, alias is useless.
If you want to return dict, you need to configure connection parameter `cursorclass=pymysql.cursors.DictCursor`. For more information, please refer PyMySQL's documents.

### Sort

```py
>>> q15 = tb.where().select().order_by('age')
>>> print(q15)
SELECT * FROM zugh.users  ORDER BY age
>>> q15.exe()
(((3, 7, 9), (2, 9, 8), (1, 16, 7), (4, 17, 7), (5, 23, 7)), 5)

# You can use prefix '-' to sort reverse.
>>> q16 = tb.where().select().order_by('-age', 'score')
>>> print(q16)
SELECT * FROM zugh.users  ORDER BY age DESC, score
>>> q16.exe()
(((5, 23, 7), (4, 17, 7), (1, 16, 7), (2, 9, 8), (3, 7, 9)), 5)
```

### Limit

We use a magical `slice` to act limit/offset, `Select Query`' slice will return a instance of
`zugh.query.core.Limit`, which is a subclass of `zugh.query.core.SelectBase`.

```py
>>> qm = tb.where().select()
>>> qm1 = qm[:3] # fetch frist three
>>> print(qm1)
SELECT * FROM zugh.users LIMIT 3
>>> qm2 = qm[2:4]
>>> print(qm2)
SELECT * FROM zugh.users LIMIT 2, 2
>>> qm3 = qm[2:]
>>> print(qm3)
SELECT * FROM zugh.users LIMIT 2, 18446744073709551614
```

Except for instances of `Limit`, all the others instance of `SelectBase` could use slice to return a instance of `Limit`.

The slice here don't accept negative numbers.

### Aggregate

We provide some aggregation functions in `zugh.query.aggregate` moulde.

```py
>>> from zugh.query.aggregate import Avg, Count, Max, Min, Sum
>>> q17 = tb.where().select(Avg('age'))
>>> print(q17)
SELECT avg(age) FROM zugh.users
>>> q17.exe()
(((Decimal('14.4000'),),), 1)

>>> q18 = tb.where().select('score', Count('id')).group_by('score')
>>> print(q18)
SELECT score, count(id) FROM zugh.users GROUP BY score
>>> q18.exe()
(((7, 3), (8, 1), (9, 1)), 3)
```

You can also use write 'raw' functions as long as you like it, such as:

```py
q17 = tb.where().select('avg(age)')
```

### Distinct

```py
from zugh.query.others import distinct
>>> q19 = tb.where().select('distinct age', 'score')
>>> print(q15)
SELECT distinct age, score FROM zugh.users
>>> q19.exe()
(((16, 7), (9, 8), (7, 9), (17, 7), (23, 7)), 5)

>>> q20 = tb.where().select(distinct('age'), 'score')
>>> print(q20)
SELECT DISTINCT age, score FROM zugh.users

>>> q21 = tb.where().select(Count(distinct('age')))
>>> print(q21)
SELECT count(DISTINCT age) FROM zugh.users
```

### Subquery

At present, `In` and `NIn` express support subquery, it could accept a instance of `SelectBase` as a parameter.But they can not accept instance of `zugh.schema.table.TempTable` as a parameter.

`TempTable` accept a `Select Query` as frist parameter and a alias string as second parameter. It would act like a normal read-only table, you could join it with others, or query data as a new instance `TempTable`.

```py
>>> from zugh.schema.table import TempTable
>>> q22 = tb.where().select(Max('age'))
>>> print(q22)
SELECT max(age) FROM zugh.users

>>> q23 = tb.where(age=In(q18)).select()
>>> print(q23)
SELECT * FROM zugh.users WHERE age IN (SELECT max(age) FROM zugh.users )
>>> q23.exe()
(((5, 23, 7),), 1)

>>> q_t = tb.where(id=gt(2)).select()
>>> tb_t1 = q_t.as_table('ak') # equal to tb_t1 = TempTable(q_t, 'ak')
>>> tb_t1
TempTable(SELECT * FROM zugh.users WHERE id > 2)
>>> tb_t2 = tb_t1.inner_join(tb2, on='a.user_id = ak.id')
>>> q_t2 = tb_t2.select()
>>> print(q_t2)
SELECT * FROM (SELECT * FROM zugh.users WHERE id > 2) AS ak INNER JOIN zugh.account AS a ON a.user_id = ak.id
>>> q_t2.exe()
(((3, 7, 8, 3, 3, Decimal('299.89')), (4, 17, 8, 4, 4, Decimal('192.10'))), 2)
```

### Join In

Let's add a new table and query from the join table:

```py
>>> from zugh.db import connect
>>> sql2  = """
CREATE TABLE zugh.account (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `amount` decimal(11,2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;
"""
>>> conn = connect(conn_config) # return a connection context
>>> with conn as cn:
        with cn.cursor() as cursor:
            cursor.execute(sql2)

>>> tb2 = Table('account', db, alias='a') # If tend to join table, alias is necessary
>>> rows2 = (
  dict(user_id=1, amount='99.89'),
  dict(user_id=2, amount='292.2'),
  dict(user_id=3, amount='299.89'),
  dict(user_id=4, amount='192.1'),
  dict(user_id=5, amount='183.7'),
)
>>> tb2.insert_multi(rows2).exe()
>>> tb3 = Table('users', db, alias='b') # If tend to join table, alias is necessary
>>> tb_i = tb2.inner_join(tb3, on='a.user_id=b.id')
>>> q_i = tb_i.where(a__id=gt(2)).select('a.id', 'a.user_id', 'a.amount', 'b.score', 'b.age')
>>> print(q_i)
SELECT a.id, a.user_id, a.amount, b.score, b.age FROM zugh.account AS a INNER JOIN zugh.users AS b ON a.user_id=b.id WHERE a.id > 2
>>> q_i.exe()
(((3, 3, Decimal('299.89'), 8, 7), (4, 4, Decimal('192.10'), 8, 17)), 2)
```

If two underscores are used in the keyword of `where` method, the two underscores will be replaced by solid point.
For example, a__id will be replaced with a.id. This idea was copied from the Django project.

We provide `Table.inner_join()`, `Table.left_join()` and `Table.right_join()` methods to support Table join.

### Union

Not implement yet.

## Update

```py
>>> tb.where(id=1).select().exe()
(((1, 16, 7),), 1)
>>> q24 = tb.where(id=1).update(age=28)
>>> print(q24)
UPDATE zugh.users SET age = 28 WHERE id = 1
>>> q24.exe()
1
>>> tb.where(id=1).select().exe()
(((1, 28, 7),), 1)
```

### F Object

Use F object to update on field or filter. F object means that it is a field, not a string.
F class is a subclass of `ArithmeticBase`. So F objects can perform mathematical operations, and it will return a new `ArithmeticBase` instance.

```py
>>> from zugh.query.others import F
>>> tb.where(id=1).select().exe()
(((1, 28, 7),), 1)

>>> q25 = tb.where(id=1).update(age=F('age') - 2, score=F('score') + 6)
>>> print(q25)
UPDATE zugh.users SET age = age - 2, score = score + 6 WHERE id = 1
>>> q25.exe()
1
>>> tb.where(id=1).select().exe()
(((1, 26, 13),), 1)

# F object also use in filter
>>> q26 = tb.where(score=gt(F('age')*2)).select()
>>> print(q26)
SELECT * FROM zugh.users WHERE score > age * 2
>>> q26.exe()
((), 0)
```

## Delete

```py
>>> tb.where(id=5).select().exe()
(((5, 23, 7),), 1)
>>> q23 = tb.where(id=5).delete()
>>> print(q23)
DELETE FROM zugh.users WHERE id = 5
>>> q23.exe()
1
>>> tb.where(id=5).select().exe()
((), 0)
```

## Decorator

### db.query.query

`query` decorator wrap a function which return a Query object. When call the wrapped function,
it would execute a Query object. For example:

```py
>>> from zugh.query.aggregate import Max
>>> from zugh.db.query import query

>>> @query()
    def query_max_score():
      q1 = tb.where().select(Max('score'))
      q2 = tb.where(score=In(q1)).select()
      return q2

>>> query_max_score()
(((1, 26, 13),), 1)
```

`query` accept 2 parameters, `conn_config` and `conn_pool`. If the Query object returned don't
configure connection, you can pass a `conn_config` dict  or a connection pool to it.

### db.query.transaction

`transaction` decorator wrap a function which return a list of `Query ojbect`. When call the wrapped
function, it would execute them as a transaction. If transaction succeed, return True, otherwise
return False.

For example:

```py
from zugh.db.query import transaction
from zugh.query.others import F

@transaction(conn_pool=pool)
def mv_score():
    q1 = tb.where(id=3).update(score=F('score') - 1)
    q2 = tb.where(id=4).update(score=F('score') + 1)
    return (q1, q2)

>>> mv_score()
True
```

## String

Some string function awailable in `zugh.query.string` module.

concat 2 field:

```py
from zugh.query.string import Concat, S, Substring
>>> q24 = tb.where().select(Concat('age', 'score'))
>>> print(q24)
SELECT concat(age, score) FROM zugh.users
```

### S Object

In string functions, str meaning field name instead of string. You should use S object to represent string.

```py
from zugh.query.string import Concat, S, Substring
>>> q25 = tb.where().select(Concat(S('PRI-'), 'age'))
>>> print(q24)
SELECT concat('PRI-', age) FROM zugh.users
>>> q25.exe()
((('PRI-26',), ('PRI-9',), ('PRI-7',), ('PRI-17',)), 4)

>>> print(tb.where().select(Substring('age', 2)))
SELECT substring(age, 2) FROM zugh.users
```

## Math

Some math functions are awailable in `zugh.query.math` module.
