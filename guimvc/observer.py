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
    def __init__(self, model):
        self._callbacks = dict()
        self.model = model
        self.model.register_observer(self)


    def notify(self, name, value, old_value):
        '''Execute all matching callbacks.'''
        for pattern in [p for p in self._callbacks if fnmatch(name, p)]:
            for func, args, kwargs in self._callbacks[pattern]:
                func(name, value, old_value, *args, **kwargs)


    def register_callback(self, pattern, func, *args, **kwargs):
        '''Register a callback function to the pattern.'''
        if pattern in self._callbacks:
            self._callbacks[pattern].append((func, args, kwargs))
        else:
            self._callbacks[pattern] = [(func, args, kwargs)]
