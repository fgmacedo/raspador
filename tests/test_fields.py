#coding: utf-8

import unittest
from datetime import date, datetime

from raspador.fields import BaseField, StringField, FloatField, BRFloatField, \
    IntegerField, DateField, DateTimeField, BooleanField


class TestBaseField(unittest.TestCase):

    def test_should_retornar_valor_no_analizar(self):
        s = "02/01/2013 10:21:51           COO:022734"
        field = BaseField(r'COO:(\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, '022734')

    def test_should_retornar_none_sem_search(self):
        s = "02/01/2013 10:21:51           COO:022734"
        field = BaseField()
        value = field.parse_block(s)
        self.assertEqual(value, None)

    def test_should_aceitar_callback(self):
        s = "02/01/2013 10:21:51           COO:022734"

        def dobro(value):
            return int(value) * 2

        field = BaseField(r'COO:(\d+)', input_processor=dobro)
        value = field.parse_block(s)
        self.assertEqual(value, 45468)  # 45468 = 2 x 22734

    def test_should_recusar_callback_invalido(self):
        self.assertRaises(
            TypeError,
            lambda: BaseField(r'COO:(\d+)', input_processor='pegadinha')
        )

    def test_should_utilizar_grupo_quando_informado(self):
        s = "Contador de Reduções Z:                     1246"
        field = BaseField(r'Contador de Reduç(ão|ões) Z:\s*(\d+)', groups=1,
                          input_processor=int)
        value = field.parse_block(s)
        self.assertEqual(value, 1246)


class TestIntegerField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        field = IntegerField(r'COO:(\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, 22734)


class TestFloatField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "VENDA BRUTA DIÁRIA:                    793.00"
        field = FloatField(r'VENDA BRUTA DIÁRIA:\s+(\d+\.\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, 793.0)

    def test_should_obter_valor_com_separador_de_milhar(self):
        s = "VENDA BRUTA DIÁRIA:                  10,036.70"
        field = FloatField(r'VENDA BRUTA DIÁRIA:\s+([\d,]+.\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, 10036.7)


class TestBRFloatField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "VENDA BRUTA DIÁRIA:                    793,00"
        field = BRFloatField(r'VENDA BRUTA DIÁRIA:\s+(\d+,\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, 793.0)

    def test_should_obter_valor_com_separador_de_milhar(self):
        s = "VENDA BRUTA DIÁRIA:                  10.036,70"
        field = BRFloatField(r'VENDA BRUTA DIÁRIA:\s+([\d.]+,\d+)')
        value = field.parse_block(s)
        self.assertEqual(value, 10036.7)


class TestStringField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "1   Dinheiro                                       0,00"
        field = StringField(r'\d+\s+(\w[^\d]+)')
        value = field.parse_block(s)
        self.assertEqual(value, 'Dinheiro')


class TestBooleanField(unittest.TestCase):
    s = "                      CANCELAMENTO                      "

    def test_should_obter_valor_verdadeiro_se_bater_e_capturar(self):
        field = BooleanField(r'^\s+(CANCELAMENTO)\s+$')
        value = field.parse_block(self.s)
        self.assertEqual(value, True)

    def test_should_retornar_falso_ao_finalizar_quando_regex_nao_bate(self):
        field = BooleanField(r'^\s+HAH\s+$')
        value = field.parse_block(self.s)
        self.assertEqual(value, None)
        value = field.default
        self.assertEqual(value, False)


class TestDateField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        field = DateField(r'^(\d+/\d+/\d+)')
        value = field.parse_block(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(value, data_esperada)

    def test_should_obter_respeitando_format_string(self):
        s = "2013-01-02T10:21:51           COO:022734"
        field = DateField(r'^(\d+-\d+-\d+)', format_string='%Y-%m-%d')
        value = field.parse_block(s)
        data_esperada = date(2013, 1, 2)
        self.assertEqual(value, data_esperada)


class TestDateTimeField(unittest.TestCase):
    def test_should_obter_valor(self):
        s = "02/01/2013 10:21:51           COO:022734"
        field = DateTimeField(r'^(\d+/\d+/\d+ \d+:\d+:\d+)')
        value = field.parse_block(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(value, data_esperada)

    def test_should_obter_respeitando_format_string(self):
        s = "2013-01-02T10:21:51           COO:022734"
        field = DateTimeField(r'^(\d+-\d+-\d+T\d+:\d+:\d+)',
                              format_string='%Y-%m-%dT%H:%M:%S')
        value = field.parse_block(s)
        data_esperada = datetime(2013, 1, 2, 10, 21, 51)
        self.assertEqual(value, data_esperada)

if __name__ == '__main__':
    import logging
    logging.basicConfig(
        # filename='test_parser.log',
        level=logging.DEBUG,
        format='%(asctime)-15s %(message)s'
    )
    unittest.main()
