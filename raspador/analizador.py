#coding: utf-8
import re
import weakref

from .cache import Cache
from .colecoes import Dicionario
import collections
import logging

logger = logging.getLogger(__name__)


class ParserMixin(object):
    """
    Classe auxiliar para definir comportamentos que serão adicionados
    em todos os analizadores através de herança múltipla.
    Padrão mix-in.
    """

    qtd_linhas_cache = 0
    default_item_class = Dicionario

    def __init__(self):
        self.tem_busca_inicio = hasattr(self, '_inicio')
        self.tem_busca_fim = hasattr(self, '_fim')
        self.inicio_encontrado = not self.tem_busca_inicio
        self.cache = Cache(self.qtd_linhas_cache + 1)
        self._atribuir_analizador_nos_campos()

    def _atribuir_analizador_nos_campos(self):
        """
        Atribui uma referência fraca do analizador para seus campos.
        Não foi utilizada referência forte para não gerar dependência ciclica,
            impedindo a liberação de memória do analizador.
        """
        ref = weakref.ref(self)
        for item in list(self._campos.values()):
            if hasattr(item, 'atribuir_analizador'):
                item.atribuir_analizador(ref)

    def analizar(self, arquivo, codificacao='latin1'):
        for item in self.analizar_arquivo(arquivo, codificacao):
            yield item

    @property
    def tem_retorno(self):
        return hasattr(self, 'retorno') and self.retorno is not None

    def converter_linha(self, linha, codificacao):
        logger.debug('converter_linha (%s): %s', codificacao, linha)
        if codificacao == 'utf-8':
            return linha
        try:
            return linha.decode(codificacao).encode('utf-8')
        except:
            return linha

    def analizar_arquivo(self, arquivo, codificacao='latin1'):
        try:
            while True:
                linha = next(arquivo)
                linha = self.converter_linha(linha, codificacao)
                res = self.analizar_linha(linha)
                if res:
                    yield res
        except StopIteration:
            res = self.finalizar()
            if res:
                yield res

    def analizar_linha(self, linha):
        self.cache.adicionar(linha)

        if self.tem_busca_inicio and not self.inicio_encontrado:
            self.inicio_encontrado = bool(self._inicio.match(linha))

        if self.inicio_encontrado:
            if not self.tem_retorno:
                self.retorno = self.default_item_class()
            if self.tem_busca_fim:
                self.inicio_encontrado = not bool(self._fim.match(linha))

            for linha in self.cache.consumir():
                for nome, campo in list(self._campos.items()):
                    if nome in self.retorno and \
                            hasattr(campo, 'lista') and not campo.lista:
                        continue
                    valor = campo.analizar_linha(linha)
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
                           if hasattr(v, 'analizar_linha')
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
            setattr(cls, '_' + nome, re.compile(expressao))

    @classmethod
    def __prepare__(self, name, bases):
        return self.default_item_class()


Parser = ParserMetaclass('Parser', (object,), {})
