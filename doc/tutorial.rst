
========
Tutorial
========

Model
=====

Defining a model is really easy. Just define the observable
attributes in the class attribute ``__observe__``, wildcards
are allowed::

    from guimvc import Model

    class MyModel(Model):

        __observe__ = ('data*',)

        def __init__(self):
            Model.__init__(self)
            # This attribute will be observed
            self.data1 = 0


You can make your wildcard patterns more restrictive
by defining the ``__exclude__`` attribute::

    class RestrictiveModel(MyModel):

        __exclude__ = ('data0',)

        def __init__(self):
            MyModel.__init__(self)
            # This attribute will be observed
            self.data1 = 0
            # This attribute will not be observed
            self.data0 = 'default'


Per default all non-private attributes are observed. No configuration
of observable attributes means the same as defining::

    class DefaultModel(Model):

        __observe__ = ('*',)
        __exclude__ = ('_*',)

        def __init__(self):
            Model.__init__(self)



Observer
========

You have to initialize the Observer with the specific
model::

    from guimvc import Observer

    class MyObserver(Observer):

        def __init__(self, model):
            Observer.__init__(self, model)


Now you can register a callback on the change of an attribute.
Wildcards are allowed, too::

    class MyActivatedObserver(Observer):

        def __init__(self):
            Observer.__init__(self, MyModel())
            self.register_callback('data*', callback)

    def callback(name, new, old):
        print 'notification of attribute "%s", new value: "%s"' % (name, new)



