#coding: utf-8
# from __future__ import unicode_literals
import re
import weakref
import collections
import logging

from .cache import Cache
from .item import Dictionary

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ParserMixin(object):
    """
    A mixin that holds all base parser implementation.
    """

    number_of_blocks_in_cache = 0
    default_item_class = Dictionary
    yield_item_to_each_field_value_found = False
    begin = None
    end = None

    def __init__(self):
        self.begin_found = not self.has_search_begin
        self.cache = Cache(self.number_of_blocks_in_cache + 1)
        self._assign_parser_to_fields()

    def _assign_parser_to_fields(self):
        """
        Assigns an weak parser reference to fields.
        """
        ref = weakref.ref(self)
        for item in list(self.fields.values()):
            if hasattr(item, 'assign_parser'):
                item.assign_parser(ref)

    def parse(self, iterator):
        for item in self.parse_iterator(iterator):
            yield item

    @property
    def has_item(self):
        return hasattr(self, 'item') and self.item is not None

    def parse_iterator(self, iterator):
        try:
            while True:
                block = next(iterator)
                res = self.parse_block(block)
                if res:
                    yield res
        except StopIteration:
            res = self.finalize()
            if res:
                yield res

    def parse_block(self, block):
        logger.debug('%s.block: %r:%s', self.__class__.__name__, type(block),
                     block)
        self.cache.append(block)

        if self.has_search_begin and not self.begin_found:
            self.begin_found = bool(self._begin.match(block))

        if self.begin_found:
            logger.debug('%s.begin_found: %r', self.__class__.__name__,
                         self.begin_found)
            if not self.has_item:
                self.item = self.default_item_class()
            if self.has_search_end:
                self.begin_found = not bool(self._end.match(block))

            for block in self.cache.consume():
                for name, field in list(self.fields.items()):
                    if name in self.item and \
                            hasattr(field, 'is_list') and not field.is_list:
                        continue
                    value = field.parse_block(block)
                    if value is not None:
                        self.assign_value_into_item(name, value)
                        if self.yield_item_to_each_field_value_found:
                            return self.finalize_item()

            if not self.begin_found:
                return self.finalize_item()

    def finalize(self):
        if not self.has_item:
            return None
        if self.yield_item_to_each_field_value_found:
            return None
        return self.finalize_item()

    def finalize_item(self):
        for name, field in list(self.fields.items()):
            if not name in self.item:
                value = None
                if hasattr(field, 'finalize') and \
                        isinstance(field.finalize, collections.Callable):
                    value = field.finalize()
                if value is None and hasattr(field, 'default'):
                    value = field.default
                if value is not None:
                    self.assign_value_into_item(name, value)

        res = self.process_item(self.item)
        self.item = None
        return res

    def assign_value_into_item(self, name, value):
        logger.debug('%s.%s = %r', self.__class__.__name__, name, value)
        if isinstance(value, list) and not name in self.item:
            self.item[name] = value
        elif isinstance(value, list) and hasattr(self.item[name], 'extend'):
            self.item[name].extend(value)
        else:
            self.item[name] = value

    def process_item(self, item):
        "Allows final modifications at the object being returned"
        return item


class ParserMetaclass(type):
    """
    Collect data-extractors into a field collection and injects ParserMixin.
    """
    def __new__(self, name, bases, attrs):
        if object in bases:
            bases = tuple([c for c in bases if c != object])

        return type.__new__(self, name, bases + (ParserMixin,), attrs)

    def __init__(cls, name, bases, attrs):
        super(ParserMetaclass, cls).__init__(name, bases, attrs)

        cls.fields = dict((k, v) for k, v in list(attrs.items())
                          if hasattr(v, 'parse_block')
                          and not isinstance(v, type))

        cls.add_regex_attr(cls, attrs, 'begin')
        cls.add_regex_attr(cls, attrs, 'end')

        for name, attr in list(cls.fields.items()):
            if hasattr(attr, 'assign_class'):
                attr.assign_class(cls, name)

    def add_regex_attr(self, cls, attrs, name):
        has_attr = name in attrs
        setattr(cls, 'has_search_'+name, has_attr)
        if has_attr:
            regex = attrs[name]
            logger.error('add_regex_attr %s: %s', name, regex)
            setattr(cls, '_' + name, re.compile(regex, re.UNICODE))


Parser = ParserMetaclass('Parser', (object,), {})
