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
from zope.publisher.interfaces import IPublishTraverse
from zope.security.proxy import removeSecurityProxy
from zope.component import getAdapters, queryMultiAdapter

from zojax.statusmessage.interfaces import IStatusMessage

from zojax.portlet.interfaces import IPortletManager, IPortletsExtension
from zojax.portlet.browser.interfaces import IPortletManagerPublicMarker


class Portlets(object):

    interface.implements(IPublishTraverse)

    __name__ = 'portlets'
    __parent__ = None

    def __init__(self, context, request):
        self.__parent__ = self.context = context
        self.request = request
        
    def publishTraverse(self, request, name):
        context = self.context

        manager = queryMultiAdapter(
            (context, request, None), IPortletManager, name)
        if manager is not None:
            manager.update()
            interface.alsoProvides(manager, IPortletManagerPublicMarker)
            return LocationProxy(manager, self.context, name)
    
        raise NotFound(self.context, self.__name__, request)

    def __call__(self):
	raise NotFound(self.context, self.__name__, request)
