# -*- coding: utf-8 -*-
"""
Created before Fri Nov 18 2022
"""

from setuptools import setup

setup(
    name='RPC_server',
    version='0.0.0',
    author='QUANTUM AG Johannes Gutenberg University Mainz',
    author_email='morth@uni-mainz.de',
    packages=[
        'RPC_server',
        'RPC_server.backend',
        'RPC_server.model',
        'RPC_server.JsonInterfaceGeneration',
        ],
    #license='LICENSE.txt',
    description='Structures for RPC servers with different underlying transport layers.',
    long_description=open('README.md').read(),
    python_requires='>= 3.9.0',
    install_requires=[
        #"pyzmq >= 22.2.1",
    ],
)



