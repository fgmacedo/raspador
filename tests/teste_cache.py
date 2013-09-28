#coding: utf-8
import unittest
from raspador.cache import Cache


class Test_Cache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(3)

    def test_deve_manter_ultimos_itens_em_cache(self):
        self.cache.append(1)
        self.cache.append(2)
        self.cache.append(3)
        self.cache.append(4)
        self.assertEqual(list(self.cache.itens()), [2, 3, 4])

    def test_deve_consume_cache(self):
        self.cache.append(1)
        self.cache.append(2)
        self.cache.append(3)
        self.cache.append(4)
        self.assertEqual(list(self.cache.consume()), [2, 3, 4])
        self.cache.append(5)
        self.assertEqual(list(self.cache.consume()), [5])
        self.cache.append(6)
        self.cache.append(7)
        self.assertEqual(list(self.cache.consume()), [6, 7])

    def test_deve_retornar_vazio_se_nao_tem_cache(self):
        valor = list(self.cache.consume())
        self.assertEqual(valor, [])

    def test_deve_retornar_tamanho_da_lista(self):
        self.cache.append(1)
        self.cache.append(2)
        self.assertEqual(len(self.cache), 2)
        self.cache.append(3)
        self.cache.append(4)
        self.cache.append(5)
        self.assertEqual(len(self.cache), 3)
