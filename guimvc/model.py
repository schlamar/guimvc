# -*- coding: utf-8 -*-
'''
    guimvc.model
    ~~~~~~~~~~~~

    The Model-Part of the MVC Pattern.

    :copyright: (c) 2012 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

import inspect
from fnmatch import fnmatch
from functools import partial


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
        self.__proxies = dict()

        # search for class attributes which
        # are containers and register them
        for cls in inspect.getmro(self.__class__):
            if cls is Model:
                break
            for name in cls.__dict__:
                attr = getattr(self, name)
                if isinstance(attr, Container):
                    attr._func = partial(self._notify, name)

    def __setattr__(self, name, value):
        '''The "magic" to notify all observers if
        an attribute is observable.
        '''
        if self._is_observable(name):
            try:
                old_value = object.__getattribute__(self, name)
            except AttributeError:
                print value, name
                if isinstance(value, Container):
                    value._func = partial(self._notify, name)
                object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)
                self._notify(name, value, old_value)
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

    def _notify(self, name, value=None, old_value=None):
        for obs in self.__observers:
            obs.notify(name, value, old_value)

    def register_observer(self, obs):
        '''Register a new observer.'''
        self.__observers.append(obs)


class Container(object):
    '''Base class for container types such as
    ``list`` or ``dict`` to track modifications.

    '''
    _modify_methods = list()

    def __init__(self):
        self._func = None

    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_modify_methods'):
            object.__getattribute__(self, '_func')()
        return object.__getattribute__(self, name)


class List(Container, list):
    '''List implementation usable as an attribute of a
    :class:``Model`` instance.

    '''
    _modify_methods = ('append', 'extend', 'insert', 'pop', 'remove',
                       'reverse', 'sort')

    def __init__(self, obj):
        Container.__init__(self)
        list.__init__(self, obj)

    def __delitem__(self, index):
        object.__getattribute__(self, '_func')()
        list.__delitem__(self, index)

    def __setitem__(self, index, value):
        object.__getattribute__(self, '_func')()
        list.__setitem__(self, index, value)
