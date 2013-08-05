#coding: utf-8


class Cache(object):
    def __init__(self, tamanho=0):
        self.tamanho = tamanho
        self.lista = []

    def __len__(self):
        return len(self.lista)

    def adicionar(self, item):
        self.lista.append(item)
        if self.tamanho:
            while len(self.lista) > self.tamanho:
                self.lista.pop(0)

    def itens(self):
        return self.lista

    def consumir(self):
        while self.lista:
            yield self.lista.pop(0)
