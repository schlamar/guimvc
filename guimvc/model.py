# -*- coding: utf-8 -*-
'''
    guimvc.model
    ~~~~~~~~~~~~

    The Model-Part of the MVC Pattern.

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

from fnmatch import fnmatch


class Model(object):
    '''You can specify patterns with wildcard support in
    the class attributes `__exclude__` and `__observe__`
    to define which attributes should be observable.

    Per default all attributes not beginning with an
    underscore are observable.
    '''
    __exclude__ = ('_*',)
    __observe__ = ('*',)

    def __init__(self):
        self.__observers = list()

    def __setattr__(self, name, value):
        '''The "magic" to notify all observers if
        an attribute is observable.
        '''
        if self._is_observable(name):
            try:
                old_value = getattr(self, name)
            except AttributeError:
                object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)
                for obs in self.__observers:
                    obs.notify(name, value, old_value)
        else:
            object.__setattr__(self, name, value)

    def __iter__(self):
        '''Yield all observable attributes.'''

        # Get class attributes
        for attr in self.__class__.__dict__:
            if not attr.startswith('__') and self._is_observable(attr):
                yield attr

        # Get instance attributes
        for attr in self.__dict__:
            if (not attr.startswith('__') and self._is_observable(attr)
                    and attr not in self.__class__.__dict__):
                yield attr

    def _is_observable(self, name):
        '''Matches the patterns in `__exclude__` and
        `__observe__`.
        '''
        if any(fnmatch(name, p) for p in self.__exclude__):
            return False
        return any(fnmatch(name, p) for p in self.__observe__)

    def register_observer(self, obs):
        '''Register a new observer.'''
        self.__observers.append(obs)
