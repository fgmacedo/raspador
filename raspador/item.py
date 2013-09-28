#coding: utf-8
try:
    from collections import OrderedDict
except ImportError:
    # Python 2.6 alternative
    from ordereddict import OrderedDict


class Dictionary(OrderedDict):
    """
    Dictionary that exposes keys as properties for easy read access.
    """
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError("%s without attr '%s'" %
                             (type(self).__name__, name))
