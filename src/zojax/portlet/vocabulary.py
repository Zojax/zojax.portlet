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
from zope import interface
from zope.component import getAdapters, getUtilitiesFor, ComponentLookupError
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.security.management import queryInteraction

from interfaces import IPortlet, IPortletManager


class Portlets(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        manager = context
        context = manager.context

        portlets = list(getAdapters(
                (context, getRequest(), manager, None), manager.portlettype))

        portlets = []
        for name, portlet in getAdapters(
            (context, getRequest(), manager, None), manager.portlettype):
            portlet.updateConfigure()
            if portlet.isAllowed():
                portlets.append((portlet.title, name))

        portlets.sort()
        return SimpleVocabulary(
            [SimpleTerm(name, name, title) for title, name in portlets])


def getRequest():
    interaction = queryInteraction()

    if interaction is not None:
        for request in interaction.participations:
            if request is not None:
                return request

    return TestRequest()
