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
    A mixin that holds all base parser implementation.
    """

    number_of_blocks_in_cache = 0
    default_item_class = Dictionary

    def __init__(self):
        self.has_search_begin = hasattr(self, '_begin')
        self.has_search_end = hasattr(self, '_end')
        self.begin_found = not self.has_search_begin
        self.cache = Cache(self.number_of_blocks_in_cache + 1)
        self._assign_parser_on_fields()

    def _assign_parser_on_fields(self):
        """
        Assigns an weak parser reference to fields.
        """
        ref = weakref.ref(self)
        for item in list(self.fields.values()):
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

        if self.has_search_begin and not self.begin_found:
            self.begin_found = bool(self._begin.match(block))

        if self.begin_found:
            logger.debug('init found: %r', self.begin_found)
            if not self.tem_retorno:
                self.retorno = self.default_item_class()
            if self.has_search_end:
                self.begin_found = not bool(self._end.match(block))

            for block in self.cache.consumir():
                for name, field in list(self.fields.items()):
                    if name in self.retorno and \
                            hasattr(field, 'lista') and not field.lista:
                        continue
                    value = field.parse_block(block)
                    if value is not None:
                        self.atribuir_valor_ao_retorno(name, value)
                        if self.retornar_ao_obter_valor:
                            return self.finalizar_retorno()

            if not self.begin_found:
                return self.finalizar_retorno()

    def finalizar(self):
        if not self.tem_retorno:
            return None
        if self.retornar_ao_obter_valor:
            return None
        return self.finalizar_retorno()

    def finalizar_retorno(self):
        for name, field in list(self.fields.items()):
            if not name in self.retorno:
                value = None
                if hasattr(field, 'finalizar') and \
                        isinstance(field.finalizar, collections.Callable):
                    value = field.finalizar()
                if value is None:
                    value = field.default
                if value is not None:
                    self.atribuir_valor_ao_retorno(name, value)

        self.processar_retorno()
        res = self.retorno
        self.retorno = None
        return res

    def atribuir_valor_ao_retorno(self, name, value):
        if isinstance(value, list) and not name in self.retorno:
            self.retorno[name] = value
        elif isinstance(value, list) and hasattr(self.retorno[name], 'extend'):
            self.retorno[name].extend(value)
        else:
            self.retorno[name] = value

    def processar_retorno(self):
        "Allows final modifications at the object being returned"
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

        cls.fields = dict((k, v) for k, v in list(attrs.items())
                          if hasattr(v, 'parse_block')
                          and not isinstance(v, type))

        cls.adicionar_atributo_re(cls, attrs, 'begin')
        cls.adicionar_atributo_re(cls, attrs, 'end')

        if not hasattr(cls, 'retornar_ao_obter_valor'):
            cls.retornar_ao_obter_valor = False

        for name, atributo in list(cls.fields.items()):
            if hasattr(atributo, 'anexar_na_classe'):
                atributo.anexar_na_classe(cls, name)

    def adicionar_atributo_re(self, cls, atributos, name):
        if name in atributos:
            expressao = atributos[name]
            setattr(cls, '_' + name, re.compile(expressao, re.UNICODE))


Parser = ParserMetaclass('Parser', (object,), {})
