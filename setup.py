#!/usr/bin/env python

from setuptools import setup

setup(
      name = 'guimvc',
      version = '0.1-dev',
      description=('A lightweight MVC Framework in Python for '
                   'easy and fast GUI development.'),
      author='Marc Schlaich',
      license='MIT',
      author_email='marc.schlaich@gmail.com',
      url='http://ms4py.github.com/guimvc/',

      platforms = 'any',

      packages = ['guimvc'],

      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Topic :: Software Development :: Libraries :: Python Modules'],


      )
