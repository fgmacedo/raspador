========
raspador
========

.. image:: https://api.travis-ci.org/fgmacedo/raspador.svg?branch=master
        :target: https://travis-ci.org/fgmacedo/raspador

.. image:: https://coveralls.io/repos/fgmacedo/raspador/badge.png
        :target: https://coveralls.io/r/fgmacedo/raspador

.. image:: https://img.shields.io/pypi/v/raspador.svg
        :target: https://pypi.python.org/pypi/raspador

.. image:: https://img.shields.io/pypi/dm/raspador.svg
        :target: https://pypi.python.org/pypi/raspador


Library to extract data from semi-structured text documents.

It's best suited for data-processing in files that do not have a formal
structure and are in plain text (or that are easy to convert). Structured files
like XML, CSV and HTML doesn't fit a good use case for Raspador, and have
excellent alternatives to get data extracted, like lxml_, html5lib_,
BeautifulSoup_, and PyQuery_.

The extractors are defined through classes as models, something similar to the
Django ORM. Each field searches for a pattern specified by the regular
expression, and captured groups are converted automatically to primitives.

The parser is implemented as a generator, where each item found can be consumed
before the end of the analysis, featuring a pipeline.

The analysis is forward-only, which makes it extremely quick, and thus any
iterator that returns a string can be analyzed, including infinite streams.

.. _lxml: http://lxml.de
.. _html5lib: https://github.com/html5lib/html5lib-python
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
.. _PyQuery: https://github.com/gawel/pyquery/


Install
=======

Raspador works on CPython 2.6+, CPython 3.2+ and PyPy. To install it, use::

    pip install raspador

or easy install::

    easy_install raspador


From source
-----------

Download and install from source::

    git clone https://github.com/fgmacedo/raspador.git
    cd raspador
    python setup.py install


Dependencies
------------

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

Tests depend on several third party libraries, but these are installed by tox
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
