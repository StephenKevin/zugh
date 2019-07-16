
from .base import ExpBase, FuncBase


class S(ExpBase):

    def __init__(self, s):
        """S object mean it is str instead field. It is useful in string function.
        """
        self._value = f"'{s}'"


class Ascii(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


class Concat(FuncBase):

    def __init__(self, *s):
        """
        If you want to concat(field, string), you should use S class to
        wrap the string. For example, `concat('field1', S('_ex'))` will generate
        SQL snippet `concat(field1, '_ex')`
        """
        return super().__init__(*s)


Cat = Concat


class Upper(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


class Lower(FuncBase):
    
    def __init__(self, s):
        return super().__init__(s)


class Substring(FuncBase):

    def __init__(self, s, start, length=None):
        return super().__init__(s, start, length)


substr = Substring


class Substring_Index(FuncBase):

    def __init__(self, s, delimiter, cnt):
        return super().__init__(s, delimiter, cnt)


class Left(FuncBase):

    def __init__(self, s, n=None):
        return super().__init__(s, n)


class Right(FuncBase):

    def __init__(self, s, n=None):
        return super().__init__(s, n)


class Lpad(FuncBase):

    def __init__(self, s, n, pad):
        return super().__init__(s, n, pad)


class Rpad(FuncBase):

    def __init__(self, s, n, pad):
        return super().__init__(s, n, pad)



class Repeat(FuncBase):

    def __init__(self, s, n):
        return super().__init__(s, n)


class Replace(FuncBase):

    def __init__(self, s1, s2):
        return super().__init__(s1, s2)


class Strcmp(FuncBase):

    def __init__(self, s1, s2):
        return super().__init__(s1, s2)


class Trim(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


class Ltrim(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


class Rtrim(FuncBase):

    def __init__(self, s):
        return super().__init__(s)



class Length(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


Len = Length


class Char_Length(FuncBase):

    def __init__(self, s):
        return super().__init__(s)


class Reverse(FuncBase):

    def __init__(self, s):
        return super().__init__(s)