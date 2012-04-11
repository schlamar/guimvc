# -*- coding: utf-8 -*-
'''
    Model tests
    ~~~~~~~~~~~

    :copyright: (c) 2012 by Marc Schlaich
    :license: MIT, see LICENSE for more details.
'''


import unittest

from mock import Mock

from guimvc import Model, Observer, List, Dict


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


class ContainerTest(unittest.TestCase):

    def test_list(self):
        class ListModel(Model):
            data = List([1, 2, 3])

        model = ListModel()
        obs = Observer(model)
        obs.notify = Mock()

        model.data.append(4)
        assert obs.notify.called

        obs.notify.reset_mock()
        del model.data[0]
        assert obs.notify.called

        obs.notify.reset_mock()
        assert model.data[0] == 2  # no modification
        assert not obs.notify.called

        obs.notify.reset_mock()
        model.data[0] = 1
        assert model.data[0] == 1
        assert obs.notify.called

        obs.notify.reset_mock()
        model.data.pop()  # remove last item
        assert model.data[-1] == 3
        assert obs.notify.called

    def test_dict(self):
        class DictModel(Model):
            data = Dict({1: 'blub', 'test': True})

        model = DictModel()
        obs = Observer(model)
        obs.notify = Mock()

        model.data[0] = 'new'
        assert model.data[0] == 'new'
        assert obs.notify.called

        obs.notify.reset_mock()
        del model.data[0]
        assert obs.notify.called

        obs.notify.reset_mock()
        assert 0 not in model.data  # no modification
        assert not obs.notify.called

        obs.notify.reset_mock()
        model.data.popitem()
        assert obs.notify.called
