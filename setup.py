##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Setup for zojax.portlet package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.6.5'


setup(name = 'zojax.portlet',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Portlets system.",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'rwproperty',
                          'zope.schema',
                          'zope.component',
                          'zope.interface',
                          'zope.security',
                          'zope.configuration',
                          'zope.cachedescriptors',
                          'zope.publisher',
                          'zope.tales',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.app.component',
                          'zope.app.security',
                          'zope.app.pagetemplate',
                          'z3c.pt',
                          'z3c.traverser',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.extensions',
                          'zojax.resourcepackage',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zope.securitypolicy',
                                  'zope.app.zcmlfiles',
                                  'zojax.cache',
                                  'zojax.autoinclude',
                                  'zojax.content.type',
                                  'zojax.content.forms',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
