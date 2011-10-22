# -*- coding: utf-8 -*-
'''
    guimvc.observer
    ~~~~~~~~~~~~~~~

    The Observer-Part of the MVC Pattern.

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

from fnmatch import fnmatch


class Observer(object):
    '''You can specify callbacks as patterns with wildcard
    support. They are executed when a changed attribute
    matches the pattern.

    Signature of the callback function::

        callback(attr_name, new_value, old_value, *args, **kwargs)
    '''

    __callbacks__ = ()

    def __init__(self, model):
        self.__callbacks = dict()
        self.model = model
        self.model.register_observer(self)

        for data in self.__callbacks__:
            if len(data) == 2:
                pattern, callback = data
                self.register_callback(pattern, callback)
            elif len(data) == 3:
                pattern, callback, args = data
                self.register_callback(pattern, callback, *args)
            elif len(data) == 4:
                pattern, callback, args, kwargs = data
                self.register_callback(pattern, callback, *args, **kwargs)


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
