#!/usr/bin/env python
#coding: utf-8

from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='raspador',
    author='Fernando Macedo',
    author_email='fgmacedo@gmail.com',
    description='Biblioteca para extração de dados em documentos',
    long_description=long_description,
    license='MIT',
    url="http://github.org/fgmacedo/raspador",
    version='0.1.0',
    packages=['raspador'],
)