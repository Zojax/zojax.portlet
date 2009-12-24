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
from zope import interface, component
from zope.location import LocationProxy
from zope.component import getAdapters, queryMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin

from zojax.extensions.interfaces import IExtensible
from zojax.portlet.interfaces import IPortletManager, IPortletsExtension

from interfaces import IPortletManagerConfigMarker


class ExtensionView(object):

    def update(self):
        context = self.context
        request = self.request

        while not IExtensible.providedBy(context):
            context = getattr(context, '__parent__')

        terms = []
        for id, manager in getAdapters((context, request, None), IPortletManager):
            terms.append((manager.title, manager.description, id))

        terms.sort()
        self.managers = [
            {'name': name, 'title': title,
             'description': desc} for title, desc, name in terms]


class PublisherPlugin(object):
    interface.implements(ITraverserPlugin)
    component.adapts(IPortletsExtension, interface.Interface)

    def __init__(self, context, request):
        self.context = context.context
        self.request = request
        self.extension = context

    def publishTraverse(self, request, name):
        manager = queryMultiAdapter(
            (self.context, self.request, None), IPortletManager, name)
        if manager is None:
            raise NotFound(self.context, name, request)

        manager.__data__ = removeSecurityProxy(self.extension).getManagerData(manager)
        manager.update()

        interface.alsoProvides(manager, IPortletManagerConfigMarker)
        return LocationProxy(manager, self.extension, name)
