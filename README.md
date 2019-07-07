# ZughSQL

[WIP] use sql in pythonic way

- [ZughSQL](#ZughSQL)
  - [table](#table)
  - [select](#select)
    - [filter](#filter)
      - [logic express](#logic-express)
      - [compare](#compare)
    - [sort](#sort)
    - [aggregate](#aggregate)
    - [distinct](#distinct)
    - [subquery](#subquery)
    - [union](#union)
  - [update](#update)
    - [F object](#F-object)
    - [values object](#values-object)
  - [insert](#insert)
    - [insert a row](#insert-a-row)
    - [insert multi rows](#insert-multi-rows)
    - [insert ignore](#insert-ignore)
    - [insert or update](#insert-or-update)
  - [delete](#delete)

## table

initial a `Table` object:

```py
>>> from schema.table import Table

>>> tb = Table('name')
```

## select

```py
>>> s1 = tb.where(c4).select('id')
>>> print(s1)
```

### filter

#### logic express

#### compare

### sort

### aggregate

### distinct

### subquery

### union

## update

### F object

### values object

## insert

### insert a row

### insert multi rows

### insert ignore

### insert or update

## delete
