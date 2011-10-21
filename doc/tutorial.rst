
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



Observer
--------

You have to initialize the Observer with the specific
model as first attribute::

    from guimvc import Observer

    class MyObserver(Observer):

        def __init__(self, model):
            Observer.__init__(self, model)


Now you can register callbacks on the change of an attribute.
Wildcards are allowed, too::

    def callback(name, new, old):
        print 'attribute "%s" changed from "%s" to "%s"' % (name, old, new)


    class MyActivatedObserver(Observer):

        __callbacks__ = [('data*', callback)]

    obs = MyActivatedObserver(RestrictiveModel())
    obs.model.data1 = 2
    #: attribute "data1" changed from "0" to "2"


