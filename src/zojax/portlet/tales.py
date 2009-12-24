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
""" 'portlet' tales expression

$Id$
"""
from zope import interface
from zope.component import queryMultiAdapter
from zope.tales.expressions import StringExpr

from chameleon.core import types
from chameleon.zpt import expressions

from interfaces import IPortlet, ITALESPortletExpression


class PortletExpression(object):

    def __call__(self, context, request, view, name):
        # Try to look up the portlet.
        portlet = queryMultiAdapter(
            (context, request, None, view), IPortlet, name)

        # if the portlet is not found, don't do anything
        if portlet is None:
            return u''

        # Stage 2: Render the HTML content.
        return portlet.updateAndRender()


class TALESPortletExpression(StringExpr, PortletExpression):
    interface.implements(ITALESPortletExpression)

    def __call__(self, econtext):
        name = StringExpr.__call__(self, econtext)
        context = econtext.vars['context']
        request = econtext.vars['request']
        view = econtext.vars['view']

        return PortletExpression.__call__(self, context, request, view, name)


class PortletTranslator(expressions.ExpressionTranslator):

    symbol = '_get_zojax_portlet'
    portlet_traverse = PortletExpression()

    def translate(self, string, escape=None):
        value = types.value("%s(context, request, view, '%s')" % \
                                (self.symbol, string))
        value.symbol_mapping[self.symbol] = self.portlet_traverse
        return value
