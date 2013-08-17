raspador
========

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
------------------------------

O raspador é compatível com Python 2 e 3, testado em Python2.7.5 e Python3.2.3.

Não há dependências externas.

Testes
------

Os testes dependem de algumas bibliotecas externas:

.. include:: requirements_dev.txt
    :literal:


Você pode executar os testes com ``nosetests``:

.. code-block:: bash

    $ nosetests

E adicionalmente, verificar a compatibilidade com o PEP8:

.. code-block:: bash

    $ flake8 raspador testes

Ou por conveniência, executar os dois em sequência com invoke:

.. code-block:: bash

    $ invoke test