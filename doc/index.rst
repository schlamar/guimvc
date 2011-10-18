
.. _pip: http://www.pip-installer.org/

=============================
GuiMVC - Python MVC Framework
=============================

A lightweight MVC Framework in Python for easy and fast GUI development.



Installation and Requirements
=============================

The prefered way to install ``guimvc`` is via pip_::

    pip install guimvc


Observer-Example
================

::

    >>> from guimvc import Model, Observer
    >>> m = Model()
    >>> m.data = 1
    >>> o = Observer(m)
    >>> def callback(name, new, old):
    ...     print 'attribute "%s" changed from "%s" to "%s"' % (name, old, new)
    ...
    >>> o.register_callback('*', callback)
    >>> m.data = 2
    attribute "data" changed from "1" to "2"


Tutorial
========

.. toctree::
   :maxdepth: 2

   tutorial


License
=======

Code and documentation are available according to the MIT License:

.. include:: ../LICENSE
  :literal:

