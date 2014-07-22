# coding: utf-8
from collections import deque


class Cache(object):
    def __init__(self, max_length=0):
        self.max_length = max_length
        self._items = deque()

    def __len__(self):
        return len(self._items)

    def append(self, item):
        self._items.append(item)
        if self.max_length:
            while len(self._items) > self.max_length:
                self._items.popleft()

    @property
    def items(self):
        return self._items

    def consume(self):
        while self._items:
            yield self._items.popleft()
