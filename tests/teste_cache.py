#coding: utf-8
import unittest
from raspador.cache import Cache


class Test_Cache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(3)

    def test_deve_manter_ultimos_itens_em_cache(self):
        self.cache.adicionar(1)
        self.cache.adicionar(2)
        self.cache.adicionar(3)
        self.cache.adicionar(4)
        self.assertEqual(self.cache.itens(), [2, 3, 4])

    def test_deve_consumir_cache(self):
        self.cache.adicionar(1)
        self.cache.adicionar(2)
        self.cache.adicionar(3)
        self.cache.adicionar(4)
        self.assertEqual(list(self.cache.consumir()), [2, 3, 4])
        self.cache.adicionar(5)
        self.assertEqual(list(self.cache.consumir()), [5])
        self.cache.adicionar(6)
        self.cache.adicionar(7)
        self.assertEqual(list(self.cache.consumir()), [6, 7])

    def test_deve_retornar_vazio_se_nao_tem_cache(self):
        valor = list(self.cache.consumir())
        self.assertEqual(valor, [])

    def test_deve_retornar_tamanho_da_lista(self):
        self.cache.adicionar(1)
        self.cache.adicionar(2)
        self.assertEqual(len(self.cache), 2)
        self.cache.adicionar(3)
        self.cache.adicionar(4)
        self.cache.adicionar(5)
        self.assertEqual(len(self.cache), 3)
