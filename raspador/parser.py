#coding: utf-8
import re
import weakref
import collections
import logging

from .cache import Cache
from .item import Dictionary

logger = logging.getLogger(__name__)


class ParserMixin(object):
    """
    Classe auxiliar para definir comportamentos que serão adicionados
    em todos os analizadores através de herança múltipla.
    Padrão mix-in.
    """

    number_of_blocks_in_cache = 0
    default_item_class = Dictionary

    def __init__(self):
        self.tem_busca_inicio = hasattr(self, '_inicio')
        self.tem_busca_fim = hasattr(self, '_fim')
        self.inicio_encontrado = not self.tem_busca_inicio
        self.cache = Cache(self.number_of_blocks_in_cache + 1)
        self._assign_parser_on_fields()

    def _assign_parser_on_fields(self):
        """
        Assigns an weak parser reference to fields.
        """
        ref = weakref.ref(self)
        for item in list(self._campos.values()):
            if hasattr(item, 'assign_parser'):
                item.assign_parser(ref)

    def parse(self, iterator):
        for item in self.parse_iterator(iterator):
            yield item

    @property
    def tem_retorno(self):
        return hasattr(self, 'retorno') and self.retorno is not None

    def parse_iterator(self, iterator):
        try:
            while True:
                block = next(iterator)
                res = self.parse_block(block)
                if res:
                    yield res
        except StopIteration:
            res = self.finalizar()
            if res:
                yield res

    def parse_block(self, block):
        logger.debug('parse_block: %s:%s', type(block), block)
        self.cache.adicionar(block)

        if self.tem_busca_inicio and not self.inicio_encontrado:
            self.inicio_encontrado = bool(self._inicio.match(block))

        if self.inicio_encontrado:
            logger.debug('init found: %r', self.inicio_encontrado)
            if not self.tem_retorno:
                self.retorno = self.default_item_class()
            if self.tem_busca_fim:
                self.inicio_encontrado = not bool(self._fim.match(block))

            for block in self.cache.consumir():
                for nome, campo in list(self._campos.items()):
                    if nome in self.retorno and \
                            hasattr(campo, 'lista') and not campo.lista:
                        continue
                    valor = campo.parse_block(block)
                    if valor is not None:
                        self.atribuir_valor_ao_retorno(nome, valor)
                        if self.retornar_ao_obter_valor:
                            return self.finalizar_retorno()

            if not self.inicio_encontrado:
                return self.finalizar_retorno()

    def finalizar(self):
        if not self.tem_retorno:
            return None
        if self.retornar_ao_obter_valor:
            return None
        return self.finalizar_retorno()

    def finalizar_retorno(self):
        for nome, campo in list(self._campos.items()):
            if not nome in self.retorno:
                valor = None
                if hasattr(campo, 'finalizar') and \
                        isinstance(campo.finalizar, collections.Callable):
                    valor = campo.finalizar()
                if valor is None:
                    valor = campo.default
                if valor is not None:
                    self.atribuir_valor_ao_retorno(nome, valor)

        self.processar_retorno()
        res = self.retorno
        self.retorno = None
        return res

    def atribuir_valor_ao_retorno(self, nome, valor):
        if isinstance(valor, list) and not nome in self.retorno:
            self.retorno[nome] = valor
        elif isinstance(valor, list) and hasattr(self.retorno[nome], 'extend'):
            self.retorno[nome].extend(valor)
        else:
            self.retorno[nome] = valor

    def processar_retorno(self):
        "Permite modificações finais ao objeto sendo retornado"
        pass


class ParserMetaclass(type):
    """
    Collect data-extractors into a field collection and injects ParserMixin.
    """
    def __new__(self, name, bases, attrs):
        if object in bases:
            bases = tuple([c for c in bases if c != object])

        return type.__new__(self, name, bases + (ParserMixin,), attrs)

    def __init__(cls, name, bases, attrs):
        super(ParserMetaclass, cls).__init__(name, bases, attrs)

        cls._campos = dict((k, v) for k, v in list(attrs.items())
                           if hasattr(v, 'parse_block')
                           and not isinstance(v, type))

        cls.adicionar_atributo_re(cls, attrs, 'inicio')
        cls.adicionar_atributo_re(cls, attrs, 'fim')

        if not hasattr(cls, 'retornar_ao_obter_valor'):
            cls.retornar_ao_obter_valor = False

        for nome, atributo in list(cls._campos.items()):
            if hasattr(atributo, 'anexar_na_classe'):
                atributo.anexar_na_classe(cls, nome)

    def adicionar_atributo_re(self, cls, atributos, nome):
        if nome in atributos:
            expressao = atributos[nome]
            setattr(cls, '_' + nome, re.compile(expressao, re.UNICODE))


Parser = ParserMetaclass('Parser', (object,), {})
