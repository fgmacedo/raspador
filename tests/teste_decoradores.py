#coding: utf-8
import unittest
import iniciar_testes
from raspador import ProxyDeCampo, ProxyConcatenaAteRE, Cache


class CampoFake(object):
    def __init__(self, valor_padrao=None, lista=False, retornar=False):
        self.valor_padrao = valor_padrao
        self.lista = lista
        self.linhas = []
        self.retornar = retornar

    def analizar_linha(self, linha):
        self.linhas.append(linha)
        if self.retornar:
            return linha

    def anexar_na_classe(self, cls, nome, informacoes):
        self.classe = cls
        self.nome = nome
        self.informacoes = informacoes


class TesteDeProxyChamandoMetodosSemIntervencao(unittest.TestCase):
    def teste_decorador_deve_retornar_valor_padrao(self):
        mock = CampoFake(valor_padrao=1234)
        p = ProxyDeCampo(mock)
        self.assertEqual(
            p.valor_padrao,
            1234
        )

    def teste_decorador_deve_retornar_valor_lista(self):
        mock = CampoFake(lista=True)
        p = ProxyDeCampo(mock)
        self.assertEqual(
            p.lista,
            True
        )

    def teste_decorador_deve_passar_linhas(self):
        mock = CampoFake()
        p = ProxyDeCampo(mock)
        p.analizar_linha('teste1')
        p.analizar_linha('teste2')
        self.assertEqual(
            mock.linhas,
            ['teste1', 'teste2']
        )


class TesteDeDecoradorConcatenaAteRE(unittest.TestCase):

    def teste_deve_chamar_decorado_acumulando_linhas(self):
        mock = CampoFake()
        p = ProxyConcatenaAteRE(mock, ' '.join, 'l4|l6')
        p.analizar_linha('l1')
        p.analizar_linha('l2')
        p.analizar_linha('l3')
        p.analizar_linha('l4')
        p.analizar_linha('l5')
        p.analizar_linha('l6')
        self.assertEqual(
            [
                'l1 l2 l3 l4',
                'l5 l6',
            ],
            mock.linhas
        )

    def teste_deve_chamar_decorado_retornando_primeiro_valor(self):
        mock = CampoFake(retornar=True)
        p = ProxyConcatenaAteRE(mock, ' '.join, 'l\d')
        p.analizar_linha('l1')
        p.analizar_linha('l2')
        p.analizar_linha('l3')
        p.analizar_linha('l4')
        p.analizar_linha('l5')
        p.analizar_linha('l6')
        self.assertEqual(
            [
                'l1',
                'l2',
                'l3',
                'l4',
                'l5',
                'l6',
            ],
            mock.linhas
        )


if __name__ == '__main__':
    unittest.main()
