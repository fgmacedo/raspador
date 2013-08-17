#coding: utf-8

import unittest
from datetime import date, datetime

from raspador.campos import CampoBase, CampoString, CampoNumerico, \
    CampoInteiro, CampoData, CampoDataHora, CampoBooleano


class TesteDeCampoBase(unittest.TestCase):
    def teste_deve_retornar_valor_no_analizar(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = CampoBase(r'COO:(\d+)', nome='COO')
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, '022734')

    def teste_deve_aceitar_callback(self):
        s = "02/01/2013 10:21:51           COO:022734"

        def dobro(valor):
            return int(valor) * 2

        campo = CampoBase(r'COO:(\d+)', nome='COO', ao_atribuir=dobro)
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 45468)  # 45468 = 2 x 22734

    def teste_deve_recusar_callback_invalido(self):
        self.assertRaises(
            TypeError,
            lambda: CampoBase(r'COO:(\d+)', ao_atribuir='pegadinha')
        )

    def teste_deve_utilizar_grupo_quando_informado(self):
        s = "Contador de Reduções Z:                     1246"
        campo = CampoBase(r'Contador de Reduç(ão|ões) Z:\s*(\d+)', grupos=1,
                          ao_atribuir=int)
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 1246)


class TesteDeCampoInteiro(unittest.TestCase):
    def teste_deve_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = CampoInteiro(r'COO:(\d+)', nome='COO')
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 22734)


class TesteDeCampoNumerico(unittest.TestCase):
    def teste_deve_obter_valor(self):
        s = "VENDA BRUTA DIÁRIA:                    793,00"
        campo = CampoNumerico(r'VENDA BRUTA DIÁRIA:\s+(\d+,\d+)')
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 793.0)

    def teste_deve_obter_valor_com_separador_de_milhar(self):
        s = "VENDA BRUTA DIÁRIA:                  10.036,70"
        campo = CampoNumerico(r'VENDA BRUTA DIÁRIA:\s+([\d.]+,\d+)')
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 10036.7)


class TesteDeCampoString(unittest.TestCase):
    def teste_deve_obter_valor(self):
        s = "1   Dinheiro                                       0,00"
        campo = CampoString(r'\d+\s+(\w[^\d]+)', nome='Meio')
        valor = campo.analizar_linha(s)
        self.assertEqual(valor, 'Dinheiro')


class TesteDeCampoBooleano(unittest.TestCase):
    s = "                      CANCELAMENTO                      "

    def teste_deve_obter_valor_verdadeiro_se_bater_e_capturar(self):
        campo = CampoBooleano(r'^\s+(CANCELAMENTO)\s+$', nome='Cancelado')
        valor = campo.analizar_linha(self.s)
        self.assertEqual(valor, True)

    def teste_deve_retornar_falso_ao_finalizar_quando_regex_nao_bate(self):
        campo = CampoBooleano(r'^\s+HAH\s+$', nome='Cancelado')
        valor = campo.analizar_linha(self.s)
        self.assertEqual(valor, None)
        valor = campo.valor_padrao
        self.assertEqual(valor, False)


class TesteDeCampoData(unittest.TestCase):
    def teste_deve_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = CampoData(r'^(\d+/\d+/\d+)', nome='Data')
        valor = campo.analizar_linha(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(valor, data_esperada)

    def teste_deve_obter_respeitando_formato(self):
        s = "2013-01-02T10:21:51           COO:022734"
        campo = CampoData(r'^(\d+-\d+-\d+)', nome='Data', formato='%Y-%m-%d')
        valor = campo.analizar_linha(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(valor, data_esperada)


class TesteDeCampoDataHora(unittest.TestCase):
    def teste_deve_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = CampoDataHora(r'^(\d+/\d+/\d+ \d+:\d+:\d+)')
        valor = campo.analizar_linha(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(valor, data_esperada)

    def teste_deve_obter_respeitando_formato(self):
        s = "2013-01-02T10:21:51           COO:022734"
        campo = CampoDataHora(r'^(\d+-\d+-\d+T\d+:\d+:\d+)',
                              formato='%Y-%m-%dT%H:%M:%S')
        valor = campo.analizar_linha(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(valor, data_esperada)
