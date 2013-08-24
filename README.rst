========
raspador
========

.. image:: https://api.travis-ci.org/fgmacedo/raspador.png
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
automaticamente a partir dos grupos capturados.


O analisador é implementado como um gerador, onde cada item encontrado pode ser
consumido antes do final da análise, caracterizando uma pipeline.


A análise é foward-only, o que o torna extremamente rápido, e deste modo
qualquer iterador que retorne uma string pode ser analisado, incluindo streams
infinitos.


Com uma base sólida e enxuta, é fácil construir seus próprios extratores.

Além da utilidade da ferramenta, o raspador é um exemplo prático e simples da
utilização de conceitos e recursos como iteradores, geradores, meta-programação
e property-descriptors.


Compatibilidade e dependências
===============================

O raspador é compatível com Python 2.6, 2.7, 3.2, 3.3 e pypy.

Desenvolvimento realizado em Python 2.7.5 e Python 3.2.3.

Não há dependências externas.

.. note:: Python 2.6

    Em Python 2.6, a biblioteca `ordereddict
    <https://pypi.python.org/pypi/ordereddict/>`_ é necessária.

    Você pode instalar com pip::

        pip install ordereddict

Testes
======

Os testes dependem de algumas bibliotecas externas:

.. code-block:: text

    coverage==3.6
    nose==1.3.0
    flake8==2.0
    invoke==0.5.0


Você pode executar os testes com ``nosetests``:

.. code-block:: bash

    $ nosetests

E adicionalmente, verificar a compatibilidade com o PEP8:

.. code-block:: bash

    $ flake8 raspador testes

Ou por conveniência, executar os dois em sequência com invoke:

.. code-block:: bash

    $ invoke test


Exemplos
========

Extrator de dados em logs
-------------------------

.. code-block:: python

    import json
    from raspador import Analizador, CampoString

    out = """
    PART:/dev/sda1 UUID:423k34-3423lk423-sdfsd-43 TYPE:ext4
    PART:/dev/sda2 UUID:74928389-852893-sdfdf-g8 TYPE:ext4
    PART:/dev/sda3 UUID:sdkj9d93-sdf9df-3kr3l-d8 TYPE:swap
    """


    class AnalizadorDeLog(Analizador):
        inicio = r'^PART.*'
        fim = r'^PART.*'
        PART = CampoString(r'PART:([^\s]+)')
        UUID = CampoString(r'UUID:([^\s]+)')
        TYPE = CampoString(r'TYPE:([^\s]+)')


    a = AnalizadorDeLog()

    # res é um gerador
    res = a.analizar(linha for linha in out.splitlines())

    print (json.dumps(list(res), indent=2))

    # Saída:
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