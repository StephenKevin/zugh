# ZughSQL

[WIP] use sql in pythonic way

[TOC]

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
