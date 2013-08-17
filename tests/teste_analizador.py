#coding: utf-8
import unittest
import re
from .teste_uteis import full_path, assertDicionario
from raspador.analizador import Analizador, Dicionario
from raspador.campos import CampoBase, CampoNumerico, \
    CampoInteiro, CampoBooleano


class CampoItem(CampoBase):
    def _iniciar(self):
        self.mascara = (r"(\d+)\s(\d+)\s+([\w.#\s/()]+)\s+(\d+)(\w+)"
                        "\s+X\s+(\d+,\d+)\s+(\w+)\s+(\d+,\d+)")

    def _para_python(self, r):
        return Dicionario(
            Item=int(r[0]),
            Codigo=r[1],
            Descricao=r[2],
            Qtd=float(re.sub(r'[,.]', '.', r[3])),
            Unidade=r[4],
            ValorUnitario=float(re.sub(r'[,.]', '.', r[5])),
            Aliquota=r[6],
            ValorTotal=float(re.sub(r'[,.]', '.', r[7])),
        )


class ExtratorDeDados(Analizador):
    inicio = r'^\s+CUPOM FISCAL\s+$'
    fim = r'^FAB:.*BR$'
    qtd_linhas_cache = 1
    COO = CampoInteiro(r'COO:\s?(\d+)')
    Cancelado = CampoBooleano(r'^\s+(CANCELAMENTO)\s+$')
    Total = CampoNumerico(r'^TOTAL R\$\s+(\d+,\d+)')
    Itens = CampoItem(lista=True)


class TotalizadoresNaoFiscais(Analizador):
    class CampoNF(CampoBase):
        def _iniciar(self):
            self.mascara = r'(\d+)\s+([\w\s]+)\s+(\d+)\s+(\d+,\d+)'

        def _para_python(self, v):
            return Dicionario(
                N=int(v[0]),
                Operacao=v[1].strip(),
                CON=int(v[2]),
                ValorAcumulado=float(re.sub('[,.]', '.', v[3])),
            )

    inicio = r'^\s+TOTALIZADORES NÃO FISCAIS\s+$'
    fim = r'^[\s-]*$'
    Totalizador = CampoNF(lista=True)

    def processar_retorno(self):
        self.retorno = self.retorno.Totalizador


class AnalizadorDeReducaoZ(Analizador):
    inicio = r'^\s+REDUÇÃO Z\s+$'
    fim = r'^FAB:.*BR$'
    qtd_linhas_cache = 1
    COO = CampoInteiro(r'COO:\s*(\d+)')
    CRZ = CampoInteiro(r'Contador de Redução Z:\s*(\d+)')
    Totalizadores = TotalizadoresNaoFiscais()


class BaseParaTestesComApiDeArquivo(unittest.TestCase):
    fazer_cache_itens = True
    codificacao_arquivo = 'latin1'
    cache_itens = None

    def setUp(self):
        self.analizador = self.criar_analizador()
        self.arquivo = self.obter_arquivo()

        # verificando se analizador foi criado
        self.assertTrue(hasattr(self.analizador, 'analizar'))

        if self.cache_itens:
            self.itens = self.cache_itens
            self.itens_dict = self.cache_itens_dict
            return

        self.itens = self.analizar()
        cupom_or_reduz = lambda x: x.get('Cupom', x.get('ReducaoZ'))
        self.itens_dict = {cupom_or_reduz(item).COO: cupom_or_reduz(item) for
                           item in self.itens if cupom_or_reduz(item)}
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
        return list(self.analizador.analizar(
            self.arquivo,
            codificacao=self.codificacao_arquivo) or [])

    assertDicionario = assertDicionario


class TesteDeExtrairDadosDeCupom(BaseParaTestesComApiDeArquivo):
    codificacao_arquivo = 'utf-8'

    def obter_arquivo(self):
        return open(full_path('arquivos/cupom.txt'))

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
        return open(full_path('arquivos/cupom.txt'))

    def criar_analizador(self):
        class ExtratorDeDados(Analizador):
            inicio = r'^\s+CUPOM FISCAL\s+$'
            fim = r'^FAB:.*BR$'
            Total = CampoNumerico(r'^TOTAL R\$\s+(\d+,\d+)')

        return ExtratorDeDados()

    def teste_deve_retornar_valores(self):
        self.assertEqual(len(self.itens), 1)


class TesteExtrairDadosComAnalizadoresAlinhados(BaseParaTestesComApiDeArquivo):
    codificacao_arquivo = 'utf-8'

    def obter_arquivo(self):
        "sobrescrever retornando arquivo"
        return open(full_path('arquivos/reducaoz.txt'))

    def criar_analizador(self):
        return AnalizadorDeReducaoZ()

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
        self.assertDicionario(reducao[0], self.itens[0])
