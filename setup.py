#!/usr/bin/env python
#coding: utf-8

from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='raspador',
    author='Fernando Macedo',
    author_email='fgmacedo@gmail.com',
    description='Library to extract data from semi-structured text documents',
    long_description=long_description,
    license='MIT',
    url="http://github.org/fgmacedo/raspador",
    version='0.2.2',
    packages=['raspador'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
