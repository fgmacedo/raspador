#coding: utf-8

import unittest
from datetime import date, datetime

from raspador.fields import BaseField, StringField, FloatField, BRFloatField, \
    IntegerField, DateField, DateTimeField, BooleanField


class TestBaseField(unittest.TestCase):

    def test_should_retornar_valor_no_analizar(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = BaseField(r'COO:(\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, '022734')

    def test_should_retornar_none_sem_search(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = BaseField()
        valor = campo.parse_block(s)
        self.assertEqual(valor, None)

    def test_should_aceitar_callback(self):
        s = "02/01/2013 10:21:51           COO:022734"

        def dobro(valor):
            return int(valor) * 2

        campo = BaseField(r'COO:(\d+)', out_processor=dobro)
        valor = campo.parse_block(s)
        self.assertEqual(valor, 45468)  # 45468 = 2 x 22734

    def test_should_recusar_callback_invalido(self):
        self.assertRaises(
            TypeError,
            lambda: BaseField(r'COO:(\d+)', out_processor='pegadinha')
        )

    def test_should_utilizar_grupo_quando_informado(self):
        s = "Contador de Reduções Z:                     1246"
        campo = BaseField(r'Contador de Reduç(ão|ões) Z:\s*(\d+)', groups=1,
                          out_processor=int)
        valor = campo.parse_block(s)
        self.assertEqual(valor, 1246)


class TestIntegerField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = IntegerField(r'COO:(\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 22734)


class TestFloatField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "VENDA BRUTA DIÁRIA:                    793.00"
        campo = FloatField(r'VENDA BRUTA DIÁRIA:\s+(\d+\.\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 793.0)

    def test_should_obter_valor_com_separador_de_milhar(self):
        s = "VENDA BRUTA DIÁRIA:                  10,036.70"
        campo = FloatField(r'VENDA BRUTA DIÁRIA:\s+([\d,]+.\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 10036.7)


class TestBRFloatField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "VENDA BRUTA DIÁRIA:                    793,00"
        campo = BRFloatField(r'VENDA BRUTA DIÁRIA:\s+(\d+,\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 793.0)

    def test_should_obter_valor_com_separador_de_milhar(self):
        s = "VENDA BRUTA DIÁRIA:                  10.036,70"
        campo = BRFloatField(r'VENDA BRUTA DIÁRIA:\s+([\d.]+,\d+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 10036.7)


class TestStringField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "1   Dinheiro                                       0,00"
        campo = StringField(r'\d+\s+(\w[^\d]+)')
        valor = campo.parse_block(s)
        self.assertEqual(valor, 'Dinheiro')


class TestBooleanField(unittest.TestCase):
    s = "                      CANCELAMENTO                      "

    def test_should_obter_valor_verdadeiro_se_bater_e_capturar(self):
        campo = BooleanField(r'^\s+(CANCELAMENTO)\s+$')
        valor = campo.parse_block(self.s)
        self.assertEqual(valor, True)

    def test_should_retornar_falso_ao_finalizar_quando_regex_nao_bate(self):
        campo = BooleanField(r'^\s+HAH\s+$')
        valor = campo.parse_block(self.s)
        self.assertEqual(valor, None)
        valor = campo.default
        self.assertEqual(valor, False)


class TestDateField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = DateField(r'^(\d+/\d+/\d+)')
        valor = campo.parse_block(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(valor, data_esperada)

    def test_should_obter_respeitando_formato(self):
        s = "2013-01-02T10:21:51           COO:022734"
        campo = DateField(r'^(\d+-\d+-\d+)', formato='%Y-%m-%d')
        valor = campo.parse_block(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(valor, data_esperada)


class TestDateTimeField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        campo = DateTimeField(r'^(\d+/\d+/\d+ \d+:\d+:\d+)')
        valor = campo.parse_block(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(valor, data_esperada)

    def test_should_obter_respeitando_formato(self):
        s = "2013-01-02T10:21:51           COO:022734"
        campo = DateTimeField(r'^(\d+-\d+-\d+T\d+:\d+:\d+)',
                              formato='%Y-%m-%dT%H:%M:%S')
        valor = campo.parse_block(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(valor, data_esperada)

if __name__ == '__main__':
    import logging
    logging.basicConfig(
        # filename='test_parser.log',
        level=logging.DEBUG,
        format='%(asctime)-15s %(message)s'
    )
    unittest.main()
