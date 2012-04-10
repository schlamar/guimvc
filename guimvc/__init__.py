# -*- coding: utf-8 -*-
'''
    guimvc
    ~~~~~~

    A lightweight MVC Framework in Python for easy
    and fast GUI development.

    :copyright: (c) 2012 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

__version__ = '0.1dev'

__all__ = ['Observer', 'observemethod', 'Model', 'List']

from observer import Observer, observemethod
from model import Model, List
