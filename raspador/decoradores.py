#coding: utf-8
import re


class ProxyDeCampo(object):
    def __init__(self, campo):
        self.campo = campo

    def __getattr__(self, atributo):
        return getattr(self.campo, atributo)


class ProxyConcatenaAteRE(ProxyDeCampo):
    """
    Proxy que faz cache de linhas recebidas. Quando recebe uma linha para
    análise, envia a linha ao cache, até encontrar um match da linha recebida
    com a expressão regular de término, e então envia o acumulado das linhas
    recebidas para o decorado.
    """
    def __init__(self, campo, uniao, re_fim):
        super(ProxyConcatenaAteRE, self).__init__(campo)
        self.cache = []
        self.uniao = uniao
        self.re_fim = re.compile(re_fim)

    def analizar_linha(self, linha):
        linha = linha.rstrip()
        self.cache.append(linha)
        if self.re_fim.match(linha):
            acumulado = self.uniao(self.cache)
            self.cache = []
            return self.campo.analizar_linha(acumulado)
