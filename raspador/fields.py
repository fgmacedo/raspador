# coding: utf-8

"""

Fields define how and what data will be extracted. The parser does not expect
the fields explicitly inherit from :py:class:`~raspador.fields.BaseField`, the
minimum expected is that a field has at least a method `parse_block`.

The fields in this file are based on regular expressions and provide conversion
for primitive types in Python.
"""

import re
from datetime import datetime
import collections


class BaseField(object):
    """
    Contains processing logic to extract data using regular expressions, and
    provide utility methods that can be overridden for custom data processing.


    Default behavior can be adjusted by parameters:

    search

        Regular expression that must specify a group of capture. Use
        parentheses for capturing::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> field = BaseField(search=r'COO:(\d+)')
            >>> field.parse_block(s)
            '022734'

        The `search` parameter is the only by position and hence its name can
        be omitted::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> field = BaseField(r'COO:(\d+)')
            >>> field.parse_block(s)
            '022734'


    input_processor

        Receives a function to handle the captured value before being returned
        by the field.

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> def double(value):
            ...     return int(value) * 2
            ...
            >>> field = BaseField(r'COO:(\d+)', input_processor=double)
            >>> field.parse_block(s)  # 45468 = 2 x 22734
            45468

    groups

        Specify which numbered capturing groups do you want do process in.


        You can enter a integer number, as the group index::

            >>> s = "Contador de Reduções Z:                     1246"
            >>> regex = r'Contador de Reduç(ão|ões) Z:\s*(\d+)'
            >>> field = BaseField(regex, groups=1, input_processor=int)
            >>> field.parse_block(s)
            1246

        Or a list of integers::

            >>> s = "Data do movimento: 02/01/2013 10:21:51"
            >>> regex = r'^Data .*(movimento|cupom): (\d+)/(\d+)/(\d+)'
            >>> c = BaseField(regex, groups=[1, 2, 3])
            >>> c.parse_block(s)
            ['02', '01', '2013']

        .. note::

            If you do not need the group to capture its match, you can optimize
            the regular expression putting an `?:` after the opening
            parenthesis::

            >>> s = "Contador de Reduções Z:                     1246"
            >>> field = BaseField(r'Contador de Reduç(?:ão|ões) Z:\s*(\d+)')
            >>> field.parse_block(s)
            '1246'

    default

        If assigned, the :py:class:`~raspador.parser.Parser` will query this
        default if no value was returned by the field.

    is_list

        When specified, returns the value as a list::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> field = BaseField(r'COO:(\d+)', is_list=True)
            >>> field.parse_block(s)
            ['022734']

        By convention, when a field returns a list, the
        :py:class:`~raspador.parser.Parser` accumulates values
         returned by the field.

    """
    def __init__(self, search=None, default=None, is_list=False,
                 input_processor=None, groups=[]):
        self.search = search
        self.default = default
        self.is_list = is_list
        self.input_processor = input_processor
        self.groups = groups

        if self.input_processor and \
                not isinstance(self.input_processor, collections.Callable):
            raise TypeError('input_processor is not callable.')

        if not hasattr(self.groups, '__iter__'):
            self.groups = (self.groups,)

        self.setup()

    @property
    def _search_method(self):
        return self.search.findall

    def setup(self):
        "Hook to special setup required on child classes"
        pass

    def assign_parser(self, parser):
        """
        Receives a weak reference of
        :py:class:`~raspador.parser.Parser`
        """
        self.parser = parser

    def _is_valid_result(self, value):
        return bool(value)

    def _process_value(self, value):
        if self.groups:
            if len(value) == 1:   # take first, if only one item
                value = value[0]
            length = len(value)
            value = [value[i] for i in self.groups if i < length]

        if len(value) == 1:   # take first, if only one item
            value = value[0]
        return value

    def to_python(self, value):
        """
        Converts parsed data to native python type.
        """
        return value

    @property
    def search(self):
        return self._search

    @search.setter
    def search(self, value):
        self._search = re.compile(value, re.UNICODE) if value else None

    def assign_class(self, cls, name):
        self.cls = cls

    def parse_block(self, block):
        if self.search:
            value = self._search_method(block)
            if self._is_valid_result(value):
                value = self._process_value(value)
                value = self.to_python(value)
                if self.input_processor:
                    value = self.input_processor(value)
                if value is not None and self.is_list \
                        and not isinstance(value, list):
                    value = [value]
                return value


class StringField(BaseField):
    def to_python(self, value):
        return str(value).strip()


class FloatField(BaseField):
    """
    Sanitizes captured value according to thousand and decimal separators and
    converts to float.
    """
    default_thousand_separator = ','
    default_decimal_separator = '.'

    def __init__(self, search, thousand_separator=None, decimal_separator=None,
                 **kwargs):
        super(FloatField, self).__init__(search, **kwargs)
        self.thousand_separator = thousand_separator if thousand_separator \
            else self.default_thousand_separator
        self.decimal_separator = decimal_separator if decimal_separator \
            else self.default_decimal_separator

    def to_python(self, value):
        value = value.replace(self.thousand_separator, '')
        value = value.replace(self.decimal_separator, '.')
        return float(value)


class BRFloatField(FloatField):
    """
    Removes thousand separator and converts to float (Brazilian format).

    .. deprecated:: 0.2.2

        Use :py:class:`~raspador.fields.FloatField` instead.
    """
    default_thousand_separator = '.'
    default_decimal_separator = ','


class IntegerField(BaseField):
    def to_python(self, value):
        return int(value)


class BooleanField(BaseField):
    """
    Returns true if the block is matched by Regex, and is at least some value
    is captured.
    """
    def setup(self):
        self.default = False

    @property
    def _search_method(self):
        return self.search.match

    def _process_value(self, value):
        res = value.groups() if value else False
        return super(BooleanField, self)._process_value(res)

    def _is_valid_result(self, value):
        return value and (value.groups())

    def to_python(self, value):
        return bool(value)


class DateField(BaseField):
    """

    Field that holds data in date format, represented in Python by
    datetine.date.

        http://docs.python.org/library/datetime.html
    """

    default_format_string = '%d/%m/%Y'

    def convertion_function(self, date):
        return datetime.date(date)

    def __init__(self, search=None, format_string=None, **kwargs):
        self.format_string = format_string \
            if format_string else self.default_format_string
        super(DateField, self).__init__(search=search, **kwargs)

    def to_python(self, value):
        date_value = datetime.strptime(value, self.format_string)
        return self.convertion_function(date_value)


class DateTimeField(DateField):
    """
    Field that holds data in hour/date format, represented in Python by
    datetine.datetime.

        http://docs.python.org/library/datetime.html
    """

    default_format_string = '%d/%m/%Y %H:%M:%S'

    def convertion_function(self, date):
        return date


if __name__ == '__main__':
    import doctest
    doctest.testmod()
