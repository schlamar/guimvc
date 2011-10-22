# -*- coding: utf-8 -*-
'''
    Observers tests
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

import unittest

from mock import Mock

from guimvc import Observer, observemethod


class BaseObserver(Observer):
    pass


class TestObserver(BaseObserver):
    pass

# This tests the inspection of the base classes
BaseObserver.attr1 = observemethod('attr1')(Mock())
TestObserver.attr2 = observemethod('attr2', 'arg1', 'arg2')(Mock())
TestObserver.attr3 = observemethod('attr3', 'arg1', kwarg1=1)(Mock())


class ObserverTest(unittest.TestCase):

    def test_callbacks(self):
        obs = TestObserver(Mock())

        args = ('attr1', 0, 1)
        obs.notify(*args)
        obs.attr1.assert_called_with(*args)

        args = ['attr2', 0, 1]
        obs.notify(*args)
        args = args + ['arg1', 'arg2']
        obs.attr2.assert_called_with(*args)

        args = ['attr3', 0, 1]
        obs.notify(*args)
        args = args + ['arg1']
        kwargs = dict(kwarg1=1)
        obs.attr3.assert_called_with(*args, **kwargs)

        mock = Mock()
        obs.register_callback('attr4', mock, 'arg1', kwarg1=1)
        args = ['attr4', 0, 1]
        obs.notify(*args)
        args = args + ['arg1']
        mock.assert_called_with(*args, **kwargs)

    def test_wildcards(self):
        obs = Observer(Mock())
        mock = Mock()
        obs.register_callback('*', mock)

        args = ['attr1', 0, 1]
        obs.notify(*args)
        mock.assert_called_with(*args)

        args = ['test_attr', 0, 1]
        obs.notify(*args)
        mock.assert_called_with(*args)

        mock = Mock()
        obs.register_callback('attr?', mock)

        args = ['attr1', 0, 1]
        obs.notify(*args)
        mock.assert_called_with(*args)

        mock.reset_mock()
        args = ['test_attr', 0, 1]
        obs.notify(*args)
        self.assertFalse(mock.called)
