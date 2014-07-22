# coding: utf-8
import unittest

from raspador import FieldProxy, UnionUntilRegexProxy


class CampoFake(object):
    def __init__(self, default=None, is_list=False, retornar=False):
        self.default = default
        self.is_list = is_list
        self.lines = []
        self.retornar = retornar

    def parse_block(self, linha):
        self.lines.append(linha)
        if self.retornar:
            return linha

    def assign_class(self, cls, nome, informacoes):
        self.classe = cls
        self.nome = nome
        self.informacoes = informacoes


class TesteDeProxyChamandoMetodosSemIntervencao(unittest.TestCase):
    def teste_decorador_deve_retornar_default(self):
        mock = CampoFake(default=1234)
        p = FieldProxy(mock)
        self.assertEqual(
            p.default,
            1234
        )

    def teste_decorador_deve_retornar_valor_lista(self):
        mock = CampoFake(is_list=True)
        p = FieldProxy(mock)
        self.assertEqual(
            p.is_list,
            True
        )

    def teste_decorador_deve_passar_linhas(self):
        mock = CampoFake()
        p = FieldProxy(mock)
        p.parse_block('teste1')
        p.parse_block('teste2')
        self.assertEqual(
            mock.lines,
            ['teste1', 'teste2']
        )


class TesteDeDecoradorConcatenaAteRE(unittest.TestCase):

    def teste_deve_chamar_decorado_acumulando_linhas(self):
        mock = CampoFake()
        p = UnionUntilRegexProxy(mock, ' '.join, 'l4|l6')
        p.parse_block('l1')
        p.parse_block('l2')
        p.parse_block('l3')
        p.parse_block('l4')
        p.parse_block('l5')
        p.parse_block('l6')
        self.assertEqual(
            [
                'l1 l2 l3 l4',
                'l5 l6',
            ],
            mock.lines
        )

    def teste_deve_chamar_decorado_retornando_primeiro_valor(self):
        mock = CampoFake(retornar=True)
        p = UnionUntilRegexProxy(mock, ' '.join, 'l\d')
        p.parse_block('l1')
        p.parse_block('l2')
        p.parse_block('l3')
        p.parse_block('l4')
        p.parse_block('l5')
        p.parse_block('l6')
        self.assertEqual(
            [
                'l1',
                'l2',
                'l3',
                'l4',
                'l5',
                'l6',
            ],
            mock.lines
        )


if __name__ == '__main__':
    unittest.main()
