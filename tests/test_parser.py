#coding: utf-8
from __future__ import unicode_literals
import os
import sys
import unittest
import io
import re

sys.path.append('../')

from raspador.parser import Parser, Dictionary
from raspador.fields import BaseField, IntegerField, BooleanField
from raspador.fields import BRFloatField as FloatField


full_path = lambda x: os.path.join(os.path.dirname(__file__), x)


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)
        ]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        return self.current_keys - self.intersect

    def removed(self):
        return self.past_keys - self.intersect

    def changed(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])


def assertDictionary(self, a, b, mensagem=''):
    d = DictDiffer(a, b)

    def diff(msg, fn):
        q = getattr(d, fn)()
        if mensagem:
            msg = mensagem + '. ' + msg
        m = 'chaves %s: %r, esperado:%r != encontrado:%r' % \
            (msg, q, a, b,) if q else ''
        self.assertFalse(q, m)

    diff('adicionadas', 'added')
    diff('removidas', 'removed')
    diff('alteradas', 'changed')


class CampoItem(BaseField):
    def setup(self):
        self.search = (r"(\d+)\s(\d+)\s+([\w.#\s/()]+)\s+(\d+)(\w+)"
                        "\s+X\s+(\d+,\d+)\s+(\w+)\s+(\d+,\d+)")

    def to_python(self, r):
        return Dictionary(
            Item=int(r[0]),
            Codigo=r[1],
            Descricao=r[2],
            Qtd=float(re.sub(r'[,.]', '.', r[3])),
            Unidade=r[4],
            ValorUnitario=float(re.sub(r'[,.]', '.', r[5])),
            Aliquota=r[6],
            ValorTotal=float(re.sub(r'[,.]', '.', r[7])),
        )


class ExtratorDeDados(Parser):
    begin = r'^\s+CUPOM FISCAL\s+$'
    end = r'^FAB:.*BR$'
    number_of_blocks_in_cache = 1
    COO = IntegerField(r'COO:\s?(\d+)')
    Cancelado = BooleanField(r'^\s+(CANCELAMENTO)\s+$')
    Total = FloatField(r'^TOTAL R\$\s+(\d+,\d+)')
    Itens = CampoItem(is_list=True)


class TotalizadoresNaoFiscais(Parser):
    class CampoNF(BaseField):
        def setup(self):
            self.search = r'(\d+)\s+([\w\s]+)\s+(\d+)\s+(\d+,\d+)'

        def to_python(self, v):
            return Dictionary(
                N=int(v[0]),
                Operacao=v[1].strip(),
                CON=int(v[2]),
                ValorAcumulado=float(re.sub('[,.]', '.', v[3])),
            )

    begin = r'^\s+TOTALIZADORES NÃO FISCAIS\s+$'
    end = r'^[\s-]*$'
    Totalizador = CampoNF(is_list=True)

    def process_item(self, item):
        return item.Totalizador


class ParserDeReducaoZ(Parser):
    begin = r'^\s+REDUÇÃO Z\s+$'
    end = r'^FAB:.*BR$'
    number_of_blocks_in_cache = 1
    COO = IntegerField(r'COO:\s*(\d+)')
    CRZ = IntegerField(r'Contador de Redução Z:\s*(\d+)')
    Totalizadores = TotalizadoresNaoFiscais()


class BaseParaTestesComApiDeArquivo(unittest.TestCase):
    fazer_cache_itens = True
    codificacao_arquivo = 'latin1'
    cache_itens = None

    def setUp(self):
        self.parser = self.criar_analizador()
        self.arquivo = self.obter_arquivo()

        # verificando se parser foi criado
        self.assertTrue(hasattr(self.parser, 'parse'))

        if self.cache_itens:
            self.itens = self.cache_itens
            self.itens_dict = self.cache_itens_dict
            return

        self.itens = self.analizar()
        cupom_or_reduz = lambda x: x.get('Cupom', x.get('ReducaoZ'))
        self.itens_dict = dict(
            (cupom_or_reduz(item).COO, cupom_or_reduz(item)) for
            item in self.itens if cupom_or_reduz(item)
        )
        if self.fazer_cache_itens:
            self.__class__.cache_itens = self.itens
            self.__class__.cache_itens_dict = self.itens_dict

    def tearDown(self):
        self.arquivo = None

    def criar_analizador(self):
        return None

    def obter_arquivo(self):
        "sobrescrever retornando arquivo"
        raise NotImplementedError('Return an file-like object')

    def analizar(self):
        return list(self.parser.parse(self.arquivo) or [])

    @classmethod
    def open_file(cls, filename):
        return io.open(full_path(filename), encoding=cls.codificacao_arquivo)

    assertDictionary = assertDictionary


class TesteDeExtrairDadosDeCupom(BaseParaTestesComApiDeArquivo):
    codificacao_arquivo = 'utf-8'

    def obter_arquivo(self):
        return self.open_file('files/cupom.txt')

    def criar_analizador(self):
        return ExtratorDeDados()

    def teste_deve_encontrar_cupom(self):
        self.assertEqual(len(self.itens), 1)

    def teste_deve_emitir_dicionario_com_valores(self):
        item = {
            "COO": 24422,
            "Cancelado": False,
            "Total": 422.2,
            "Itens": [
                {
                    "Item": 1,
                    "Codigo": "872",
                    "Descricao": "#POLENTA FINA",
                    "Qtd": 2,
                    "Unidade": "UN",
                    "ValorUnitario": 11.00,
                    "Aliquota": "Te",
                    "ValorTotal": 22.00
                },
                {
                    "Item": 2,
                    "Codigo": "1352",
                    "Descricao": "SUCO DE UVA",
                    "Qtd": 1,
                    "Unidade": "UN",
                    "ValorUnitario": 5.50,
                    "Aliquota": "F1",
                    "ValorTotal": 5.50
                },
                {
                    "Item": 3,
                    "Codigo": "1280",
                    "Descricao": "AGUA FONTE IJUI S/G",
                    "Qtd": 1,
                    "Unidade": "UN",
                    "ValorUnitario": 3.20,
                    "Aliquota": "F1",
                    "ValorTotal": 3.20
                },
                {
                    "Item": 4,
                    "Codigo": "119",
                    "Descricao": "#LINGUICA CASEIRA",
                    "Qtd": 2,
                    "Unidade": "UN",
                    "ValorUnitario": 12.00,
                    "Aliquota": "Te",
                    "ValorTotal": 24.00
                },
                {
                    "Item": 5,
                    "Codigo": "464",
                    "Descricao": "#CARRETEIRO DE FILET",
                    "Qtd": 1,
                    "Unidade": "UN",
                    "ValorUnitario": 45.00,
                    "Aliquota": "Te",
                    "ValorTotal": 45.00
                },
                {
                    "Item": 6,
                    "Codigo": "117",
                    "Descricao": "#SALADA (POR PESSOA)",
                    "Qtd": 6,
                    "Unidade": "UN",
                    "ValorUnitario": 12.00,
                    "Aliquota": "Te",
                    "ValorTotal": 72.00
                },
                {
                    "Item": 7,
                    "Codigo": "1202",
                    "Descricao": "COCA COLA ZERO LT.",
                    "Qtd": 1,
                    "Unidade": "UN",
                    "ValorUnitario": 3.50,
                    "Aliquota": "F1",
                    "ValorTotal": 3.50
                },
                {
                    "Item": 8,
                    "Codigo": "324",
                    "Descricao": "#PICANHA ANGUS",
                    "Qtd": 2,
                    "Unidade": "UN",
                    "ValorUnitario": 47.00,
                    "Aliquota": "Te",
                    "ValorTotal": 94.00
                },
                {
                    "Item": 9,
                    "Codigo": "990",
                    "Descricao": "#CAFE EXPRESSO",
                    "Qtd": 1,
                    "Unidade": "UN",
                    "ValorUnitario": 3.00,
                    "Aliquota": "Tc",
                    "ValorTotal": 3.00
                },
                {
                    "Item": 10,
                    "Codigo": "1400",
                    "Descricao": "CHOPP CL. BRAHMA 300",
                    "Qtd": 25,
                    "Unidade": "UN",
                    "ValorUnitario": 6.00,
                    "Aliquota": "F1",
                    "ValorTotal": 150.00
                },
            ]
        }
        self.assertEqual(self.itens[0], item)


class TesteExtrairDadosDeCupomCancelado(BaseParaTestesComApiDeArquivo):
    def obter_arquivo(self):
        return self.open_file('files/cupom.txt')

    def criar_analizador(self):
        class ExtratorDeDados(Parser):
            begin = r'^\s+CUPOM FISCAL\s+$'
            end = r'^FAB:.*BR$'
            Total = FloatField(r'^TOTAL R\$\s+(\d+,\d+)')

        return ExtratorDeDados()

    def teste_deve_retornar_valores(self):
        self.assertEqual(len(self.itens), 1)


class TesteExtrairDadosComParseresAlinhados(BaseParaTestesComApiDeArquivo):
    codificacao_arquivo = 'utf-8'

    def obter_arquivo(self):
        "sobrescrever retornando arquivo"
        return self.open_file('files/reducaoz.txt')

    def criar_analizador(self):
        return ParserDeReducaoZ()

    def teste_deve_retornar_dados(self):
        reducao = [
            {
                "COO": 24152,
                "CRZ": 1389,
                "Totalizadores": [
                    {
                        "N": 1,
                        "Operacao": "Sangria",
                        "CON": 10,
                        "ValorAcumulado": 100.0
                    }, {
                        "N": 2,
                        "Operacao": "Fundo de Troco",
                        "CON": 20,
                        "ValorAcumulado": 200.0
                    }, {
                        "N": 3,
                        "Operacao": "Assinada",
                        "CON": 30,
                        "ValorAcumulado": 300.0
                    },
                ]
            }
        ]
        self.assertDictionary(reducao[0], self.itens[0])

if __name__ == '__main__':
    import logging
    logging.basicConfig(
        # filename='test_parser.log',
        level=logging.DEBUG,
        format='%(asctime)-15s %(message)s'
    )
    unittest.main()
