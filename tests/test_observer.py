# -*- coding: utf-8 -*-
'''
    Observers tests
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''

import unittest

from mock import Mock

from guimvc import Observer


def _get_mock(obs, attr):
    return obs._Observer__callbacks[attr][0][0]


class TestObserver(Observer):

    __callbacks__ = [('attr1', Mock()),
                     ('attr2', Mock(), ('arg1', 'arg2')),
                     ('attr3', Mock(), ('arg1',), dict(kwarg1=1))
                    ]


class ObserverTest(unittest.TestCase):

    def test_callbacks(self):
        obs = TestObserver(Mock())

        mock = _get_mock(obs, 'attr1')
        args = ('attr1', 0, 1)
        obs.notify(*args)
        mock.assert_called_with(*args)

        mock = _get_mock(obs, 'attr2')
        args = ['attr2', 0, 1]
        obs.notify(*args)
        args = args + ['arg1', 'arg2']
        mock.assert_called_with(*args)

        mock = _get_mock(obs, 'attr3')
        args = ['attr3', 0, 1]
        obs.notify(*args)
        args = args + ['arg1']
        kwargs = dict(kwarg1=1)
        mock.assert_called_with(*args, **kwargs)

        mock = Mock()
        obs.register_callback('attr4', mock, 'arg1', kwarg1=1)
        args = ['attr4', 0, 1]
        obs.notify(*args)
        args = args + ['arg1']
        mock.assert_called_with(*args, **kwargs)

    def test_wildcards(self):
        obs = TestObserver(Mock())
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
