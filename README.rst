========
raspador
========

.. image:: https://api.travis-ci.org/fgmacedo/raspador.png?branch=master
        :target: https://travis-ci.org/fgmacedo/raspador

.. image:: https://coveralls.io/repos/fgmacedo/raspador/badge.png
        :target: https://coveralls.io/r/fgmacedo/raspador

.. image:: https://pypip.in/v/raspador/badge.png
        :target: https://pypi.python.org/pypi/raspador

.. image:: https://pypip.in/d/raspador/badge.png
        :target: https://crate.io/packages/raspador/


Biblioteca para extração de dados em documentos semi-estruturados.

A definição dos extratores é feita através de classes como modelos, de forma
semelhante ao ORM do Django. Cada extrator procura por um padrão especificado
por expressão regular, e a conversão para tipos primitidos é feita
automaticamente a partir dos groups capturados.


O analisador é implementado como um gerador, onde cada item encontrado pode ser
consumido antes do final da análise, caracterizando uma pipeline.


A análise é foward-only, o que o torna extremamente rápido, e deste modo
qualquer iterador que retorne uma string pode ser analisado, incluindo streams
infinitos.


Com uma base sólida e enxuta, é fácil construir seus próprios extratores.

Além da utilidade da ferramenta, o raspador é um exemplo prático e simples da
utilização de conceitos e recursos como iteradores, geradores, meta-programação
e property-descriptors.


Compatibility and dependencies
==============================

raspador runs on Python 2.6+, 3.2+ and pypy.

There are no external dependencies.

.. note:: Python 2.6

    With Python 2.6, you must install `ordereddict
    <https://pypi.python.org/pypi/ordereddict/>`_.

    You can install it with pip::

        pip install ordereddict

Tests
======

To automate tests with all supported Python versions at once, we use `tox
<http://tox.readthedocs.org/en/latest/>`_.

Run all tests with:

.. code-block:: bash

    $ tox

Tests depends on several third party libraries, but these are installed by tox
on each Python's virtualenv:

.. code-block:: text

    nose==1.3.0
    coverage==3.6
    flake8==2.0


Examples
========

Extract data from logs
----------------------

.. code-block:: python

    from __future__ import print_function
    import json
    from raspador import Parser, StringField

    out = """
    PART:/dev/sda1 UUID:423k34-3423lk423-sdfsd-43 TYPE:ext4
    PART:/dev/sda2 UUID:74928389-852893-sdfdf-g8 TYPE:ext4
    PART:/dev/sda3 UUID:sdkj9d93-sdf9df-3kr3l-d8 TYPE:swap
    """


    class LogParser(Parser):
        begin = r'^PART.*'
        end = r'^PART.*'
        PART = StringField(r'PART:([^\s]+)')
        UUID = StringField(r'UUID:([^\s]+)')
        TYPE = StringField(r'TYPE:([^\s]+)')


    a = LogParser()

    # res is a generator
    res = a.parse(iter(out.splitlines()))

    out_as_json = json.dumps(list(res), indent=2)
    print (out_as_json)

    # Output:
    """
    [
      {
        "PART": "/dev/sda1",
        "TYPE": "ext4",
        "UUID": "423k34-3423lk423-sdfsd-43"
      },
      {
        "PART": "/dev/sda2",
        "TYPE": "ext4",
        "UUID": "74928389-852893-sdfdf-g8"
      },
      {
        "PART": "/dev/sda3",
        "TYPE": "swap",
        "UUID": "sdkj9d93-sdf9df-3kr3l-d8"
      }
    ]
    """