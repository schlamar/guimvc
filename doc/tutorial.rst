
Tutorial
========

Model
-----

Defining a model is really easy. Just define the observable
attributes in the class attribute ``__observe__``, wildcards
are allowed::

    from guimvc import Model

    class MyModel(Model):

        __observe__ = ('data*',)

        # This attribute will be observed
        data1 = 0


You can make your wildcard patterns more restrictive
by defining the ``__exclude__`` attribute::

    class RestrictiveModel(MyModel):

        __exclude__ = ('data0',)

        # This attribute will be observed
        data1 = 0
        # This attribute will not be observed
        data0 = 'default'



Per default all non-private attributes are observed. No configuration
of observable attributes means the same as defining::

    class DefaultModel(Model):

        __observe__ = ('*',)
        __exclude__ = ('_*',)


You can get all observed attributes of a model by iterating
over it::

    >>> list(RestrictiveModel())
    ['data1']


The Model usually detect modifications if you reassign a
value. If you want to track changes of container datatypes
such as ``list`` or ``dict`` you have to use the custom
implementations::

    from guimvc import List, Dict

    class ContainerModel(Model):

        data1 = List([1, 2, 3])
        data2 = Dict({1: 'value', 'test': True})


Observer
--------

You have to initialize the Observer with the specific
model as first attribute. You can register methods as callbacks
on the change of an attribute with the decorator ``observemethod``.
Wildcards are allowed, too::

    from guimvc import Observer, observemethod

    class MyObserver(Observer):

        @observemethod('data*')
        def callback(self, name, new, old):
            print 'Attribute "%s" changed from "%s" to "%s"' % (name, old, new)

    obs = MyObserver(MyModel())
    obs.model.data1 = 2
    #: Attribute "data1" changed from "0" to "2"


