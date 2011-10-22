# -*- coding: utf-8 -*-
'''
    guimvc.observer
    ~~~~~~~~~~~~~~~

    The Observer-Part of the MVC Pattern.

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

import inspect
from fnmatch import fnmatch

_OBS_ATTR = 'observe_method'


def observemethod(pattern, *args, **kwargs):
    def decorator(func):
        setattr(func, _OBS_ATTR, (pattern, args, kwargs))
        return func
    return decorator


class Observer(object):
    '''You can specify callbacks as patterns with wildcard
    support. They are executed when a changed attribute
    matches the pattern.

    Signature of the callback function::

        callback(attr_name, new_value, old_value, *args, **kwargs)
    '''

    def __init__(self, model):
        self.__callbacks = dict()
        self.model = model
        self.model.register_observer(self)

        # check for observe methods in this class and
        # all base classes between ``Observer`` and this
        # class as well
        for cls in inspect.getmro(self.__class__):
            if cls is Observer:
                break
            for attr in cls.__dict__:
                func = getattr(self, attr)
                if callable(func) and hasattr(func, _OBS_ATTR):
                    pattern, args, kwargs = getattr(func, _OBS_ATTR)
                    self.register_callback(pattern, func, *args, **kwargs)

    def notify(self, name, value, old_value):
        '''Execute all matching callbacks.'''
        for pattern in [p for p in self.__callbacks if fnmatch(name, p)]:
            for func, args, kwargs in self.__callbacks[pattern]:
                func(name, value, old_value, *args, **kwargs)

    def register_callback(self, pattern, func, *args, **kwargs):
        '''Register a callback function to the pattern.'''
        if pattern in self.__callbacks:
            self.__callbacks[pattern].append((func, args, kwargs))
        else:
            self.__callbacks[pattern] = [(func, args, kwargs)]
