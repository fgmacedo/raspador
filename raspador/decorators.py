# coding: utf-8
import re


class FieldProxy(object):
    def __init__(self, field):
        self.field = field

    def __getattr__(self, attr):
        return getattr(self.field, attr)


class UnionUntilRegexProxy(FieldProxy):
    """
    Does cache of blocks until the provided regex returns a match, then uses
    the ``union_method`` to join blocks that are sent to the decorated field.
    """
    def __init__(self, field, union_method, search_regex):
        super(UnionUntilRegexProxy, self).__init__(field)
        self.cache = []
        self.union_method = union_method
        self.search_regex = re.compile(search_regex, re.UNICODE)

    def parse_block(self, block):
        if hasattr(block, 'rstrip'):
            block = block.rstrip()
        self.cache.append(block)
        if self.search_regex.match(block):
            blocks = self.union_method(self.cache)
            self.cache = []
            return self.field.parse_block(blocks)
