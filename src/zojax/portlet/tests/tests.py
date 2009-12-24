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
"""

$Id$
"""
import os
import unittest, doctest
from zope import interface, component
from zope.app.testing import setup
from zope.app.testing.functional import ZCMLLayer
from zope.app.rotterdam import Rotterdam
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import getVocabularyRegistry
from zope.annotation.attribute import AttributeAnnotations

from z3c.pt import expressions
from zojax.extensions import storage, extensiontype
from zojax.extensions.interfaces import IExtensible
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.content.type.interfaces import IItem
from zojax.content.type.container import ContentContainer

from zojax.portlet import vocabulary, extension, interfaces



class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxPortlet = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxPortlet', allow_teardown=True)


class ITestContent(IItem):
    pass

class TestContent(ContentContainer):
    interface.implements(ITestContent)


def setUp(test):
    site = setup.placefulSetUp(True)
    component.provideAdapter(storage.Storage)
    component.provideAdapter(AttributeAnnotations)
    component.provideUtility(expressions.path_translator, name='path')

    ext = extensiontype.ExtensionType(
        'portlets', interfaces.IPortletsExtension,
        extension.PortletsExtension, 'Portlets', u'')
    component.provideAdapter(ext, (IExtensible,), interfaces.IPortletsExtension)

    setup.setUpTestAsModule(test, name='zojax.portlet.TESTS')

    getVocabularyRegistry().register('zojax portlets', vocabulary.Portlets())


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)


def test_suite():
    manager = doctest.DocFileSuite(
        '../manager.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    portlet = doctest.DocFileSuite(
        '../portlet.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    tales = doctest.DocFileSuite(
        '../tales.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    configuration = doctest.DocTestSuite(
        'zojax.portlet.configproperty',
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    cache = doctest.DocFileSuite(
        'cache.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    testbrowser = doctest.DocFileSuite(
        "tests.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxPortlet

    return unittest.TestSuite((manager, tales, cache,
                               configuration, portlet, testbrowser))
