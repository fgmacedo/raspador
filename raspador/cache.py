#coding: utf-8
from collections import deque


class Cache(object):
    def __init__(self, length=0):
        self.length = length
        self.items = deque()

    def __len__(self):
        return len(self.items)

    def append(self, item):
        self.items.append(item)
        if self.length:
            while len(self.items) > self.length:
                self.items.popleft()

    def itens(self):
        return self.items

    def consume(self):
        while self.items:
            yield self.items.popleft()
