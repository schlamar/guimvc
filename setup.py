#!/usr/bin/env python

from setuptools import setup

setup(
      name='guimvc',
      version='0.1a.dev',
      license='MIT',

      author='Marc Schlaich',
      author_email='marc.schlaich@gmail.com',
      url='http://guimvc.readthedocs.org/',
      download_url=('http://github.com/ms4py/guimvc/tarball/master'
                    '#egg=guimvc-dev'),

      platforms='any',
      packages=['guimvc'],
      test_suite='nose.collector',

      description=('A lightweight MVC Framework in Python for '
                   'easy and fast GUI development.'),

      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      )
