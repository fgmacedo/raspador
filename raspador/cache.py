# coding: utf-8
from collections import deque


class Cache(object):
    def __init__(self, max_length=0):
        self.max_length = max_length
        self.items = deque()

    def __len__(self):
        return len(self.items)

    def append(self, item):
        self.items.append(item)
        if self.max_length:
            while len(self.items) > self.max_length:
                self.items.popleft()

    def itens(self):
        return self.items

    def consume(self):
        while self.items:
            yield self.items.popleft()
