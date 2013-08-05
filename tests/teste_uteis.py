#coding: utf-8
import os
import sys

OBTER_CAMINHO = lambda x: os.path.join(os.path.dirname(__file__), x)


def incluir_diretorio_raiz():
    sys.path.append(os.path.realpath('../'))


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


def assertDicionario(self, a, b, mensagem=''):
    d = DictDiffer(a, b)

    def diff(msg, fn):
        q = getattr(d, fn)()
        if mensagem:
            msg = mensagem +'. '+ msg
        m = 'chaves %s: %r, esperado:%r != encontrado:%r' % (msg, q, a, b,) if q else ''
        self.assertFalse(q, m)

    diff('adicionadas', 'added')
    diff('removidas', 'removed')
    diff('alteradas', 'changed')
