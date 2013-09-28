#coding: utf-8

"""
Os fields são simples extratores de dados baseados em expressões regulares.

Ao confrontar uma block recebida para análise com sua expressão regular, o
campo verifica se há groups de dados capturados, e então pode realizar algum
processamento e validações nestes dados. Se o campo considerar os dados
válidos, retorna o(s) dado(s). """

import re
from datetime import datetime
import collections


class BaseField(object):
    """
    Contém lógica de processamento para extrair dados através de expressões
    regulares, além de prover métodos utilitários que podem ser sobrescritos
    para customizações no tratamento dos dados.

    O comportamento do Campo pode ser ajustado através de diversos parâmetros:

    search

        O requisito mínimo para um campo é uma máscara em expressão regular,
        onde deve-se especificar um grupo para captura::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> campo = BaseField(search=r'COO:(\d+)')
            >>> campo.parse_block(s)
            '022734'

        O parâmetro search é o único posicional, e deste modo, seu nome pode
        ser omitido::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> campo = BaseField(r'COO:(\d+)')
            >>> campo.parse_block(s)
            '022734'


    out_processor

        Recebe um callback para tratar o value antes de ser retornado pelo
        campo.

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> def dobro(value):
            ...     return int(value) * 2
            ...
            >>> campo = BaseField(r'COO:(\d+)', out_processor=dobro)
            >>> campo.parse_block(s)  # 45468 = 2 x 22734
            45468

    groups

        Permite escolher quais groups capturados o campo deve processar como
        dados de entrada, utilizado para expressões regulares que utilizam
        groups para correspondência da expressão regular, mas que apenas parte
        destes groups possui informação útil.

        Pode-se informar um número inteiro, que será o índice do grupo,
        inicando em 0::

            >>> s = "Contador de Reduções Z:                     1246"
            >>> campo = BaseField(r'Contador de Reduç(ão|ões) Z:\s*(\d+)', \
                groups=1, out_processor=int)
            >>> campo.parse_block(s)
            1246

        Ou uma lista de inteiros::

            >>> s = "Data do movimento: 02/01/2013 10:21:51"
            >>> c = BaseField(r'^Data .*(movimento|cupom): (\d+)/(\d+)/(\d+)',\
                groups=[1, 2, 3])
            >>> c.parse_block(s)
            ['02', '01', '2013']


    default

        Valor que será utilizado no :py:class:`~raspador.parser.Parser`
        , quando o campo não retornar value após a análise das
        linhas recebidas.


    is_list

        Quando especificado, retorna o value como uma lista::

            >>> s = "02/01/2013 10:21:51           COO:022734"
            >>> campo = BaseField(r'COO:(\d+)', is_list=True)
            >>> campo.parse_block(s)
            ['022734']

        Por convenção, quando um campo retorna uma lista, o
        :py:class:`~raspador.parser.Parser` acumula os valores
        retornados pelo campo.
    """
    def __init__(self, search=None, default=None, is_list=False,
                 out_processor=None, groups=[]):
        self.search = search
        self.default = default
        self.is_list = is_list
        self.out_processor = out_processor
        self.groups = groups

        if self.out_processor and \
                not isinstance(self.out_processor, collections.Callable):
            raise TypeError('out_processor is not callable.')

        if not hasattr(self.groups, '__iter__'):
            self.groups = (self.groups,)

        self._setup()

    @property
    def _search_method(self):
        return self.search.findall

    def _setup(self):
        "Hook to special setup required on child classes"
        pass

    def assign_parser(self, parser):
        """
        Receives a weak reference of
        :py:class:`~raspador.parser.Parser`
        """
        self.parser = parser

    def _is_valid_result(self, value):
        return bool(value)

    def _process_value(self, value):
        if self.groups:
            if len(value) == 1:   # take first, if only one item
                value = value[0]
            length = len(value)
            value = [value[i] for i in self.groups if i < length]

        if len(value) == 1:   # take first, if only one item
            value = value[0]
        return value

    def to_python(self, value):
        """
        Converts parsed data to native python type.
        """
        return value

    @property
    def search(self):
        return self._search

    @search.setter
    def search(self, value):
        self._search = re.compile(value, re.UNICODE) if value else None

    def assign_class(self, cls, name):
        self.cls = cls

    def parse_block(self, block):
        if self.search:
            value = self._search_method(block)
            if self._is_valid_result(value):
                value = self._process_value(value)
                value = self.to_python(value)
                if self.out_processor:
                    value = self.out_processor(value)
                if value is not None and self.is_list \
                        and not isinstance(value, list):
                    value = [value]
                return value


class StringField(BaseField):
    def to_python(self, value):
        return str(value).strip()


class FloatField(BaseField):
    "Removes thousand separator and converts to float."
    def to_python(self, value):
        value = value.replace(',', '')
        return float(value)


class BRFloatField(BaseField):
    "Removes thousand separator and converts to float (Brazilian format)"
    def to_python(self, value):
        value = value.replace('.', '')
        value = value.replace(',', '.')
        return float(value)


class IntegerField(BaseField):
    def to_python(self, value):
        return int(value)


class BooleanField(BaseField):
    """
    Retorna verdadeiro se a Regex bater com uma block completa, e
    se ao menos algum value for capturado.
    """
    def _setup(self):
        self.default = False

    @property
    def _search_method(self):
        return self.search.match

    def _process_value(self, value):
        res = value.groups() if value else False
        return super(BooleanField, self)._process_value(res)

    def _is_valid_result(self, value):
        return value and (value.groups())

    def to_python(self, value):
        return bool(value)


class DateField(BaseField):
    """
    Campo que mantém dados no formato de data,
    representado em Python por datetine.date.

    Formato:
        Veja http://docs.python.org/library/datetime.html para detalhes.
    """

    default_format_string = '%d/%m/%Y'
    convertion_function = lambda self, date: datetime.date(date)

    def __init__(self, search=None, formato=None, **kwargs):
        self.formato = formato if formato else self.default_format_string
        super(DateField, self).__init__(search=search, **kwargs)

    def to_python(self, value):
        date_value = datetime.strptime(value, self.formato)
        return self.convertion_function(date_value)


class DateTimeField(DateField):
    """
    Campo que mantém dados no formato de data/hora,
    representado em Python por datetine.datetime.

    Formato:
        Veja http://docs.python.org/library/datetime.html para detalhes.
    """

    default_format_string = '%d/%m/%Y %H:%M:%S'
    convertion_function = lambda self, date: date


if __name__ == '__main__':
    import doctest
    doctest.testmod()
