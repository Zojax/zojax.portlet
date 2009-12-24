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
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from zope.security.proxy import removeSecurityProxy
from zope.component import getAdapters, queryMultiAdapter
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.portlet.interfaces import IPortletManager, IPortletsExtension
from zojax.portlet.browser.interfaces import IPortletManagerConfigMarker


class ContentPortletManagers(object):

    def update(self):
        request = self.request
        context = self.context

        terms = []
        for id, manager in getAdapters((context,request,None), IPortletManager):
            terms.append((manager.title, manager.description, id))

        terms.sort()
        self.managers = [
            {'name': 'pm-%s'%name, 'title': title,
             'description': desc} for title, desc, name in terms]

    def isAvailable(self):
        return bool(self.managers)

    def postUpdate(self):
        pass


class ContentPortletManagersPublisher(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if name.startswith('pm-'):
            context = self.context.getContent()

            manager = queryMultiAdapter(
                (context, self.request, None), IPortletManager, name[3:])
            if manager is not None:
                extension = IPortletsExtension(context)
                manager.__data__ = \
                    removeSecurityProxy(extension).getManagerData(manager)
                manager.updateConfigure()

                interface.alsoProvides(manager, IPortletManagerConfigMarker)
                return LocationProxy(manager, self.context, name)

        raise NotFound(self.context, name, request)
