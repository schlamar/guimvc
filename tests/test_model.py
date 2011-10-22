# -*- coding: utf-8 -*-
'''
    Model tests
    ~~~~~~~~~~~

    :copyright: (c) 2011 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''


import unittest

from mock import Mock

from guimvc import Model, Observer


class TestModel(Model):
    attr1 = 0
    attr2 = 0


class WildcardModel(TestModel):
    __observe__ = ('attr?', 'test*', 'data1')
    __exclude__ = ('attr2',)

    test_attr = 0
    data1 = 0


class ModelTest(unittest.TestCase):

    def test_get_observable_attributes(self):
        model = TestModel()
        self.assertEqual(set(model), set(['attr1', 'attr2']))

        model.attr3 = 0
        print model.__dict__
        self.assertEqual(set(model), set(['attr1', 'attr2', 'attr3']))

        del model.attr3
        self.assertEqual(set(model), set(['attr1', 'attr2']))

    def test_notify(self):
        model = TestModel()
        obs = Observer(model)
        obs.notify = Mock()

        model.attr1 = 1
        obs.notify.assert_called_with('attr1', 1, 0)  # name, new, old

        model.attr1 = 1
        obs.notify.assert_called_with('attr1', 1, 1)

    def test_wildcards(self):
        model = WildcardModel()
        obs = Observer(model)
        obs.notify = Mock()

        model.attr1 = 1
        obs.notify.assert_called_with('attr1', 1, 0)

        obs.notify.reset_mock()
        model.attr2 = 2
        self.assertFalse(obs.notify.called)

        model.test_attr = 1
        obs.notify.assert_called_with('test_attr', 1, 0)

        model.data1 = 1
        obs.notify.assert_called_with('data1', 1, 0)
