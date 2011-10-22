
.. _pip: http://www.pip-installer.org/


GuiMVC - Python MVC Framework
=============================

A lightweight MVC Framework in Python for easy and fast GUI development.



Installation and Requirements
-----------------------------

The prefered way to install ``guimvc`` is via pip_::

    pip install guimvc


Observer-Example
----------------

::

    from guimvc import Model, Observer, observemethod

    class MyModel(Model):
        data = 0

    class MyObserver(Observer):

        @observemethod('data')
        def callback(self, name, new, old):
            print 'Attribute "%s" changed from "%s" to "%s"' % (name, old, new)

    model = MyModel()
    obs = MyObserver(model)
    model.data = 1
    #: Attribute "data" changed from "0" to "1"

