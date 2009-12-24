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
from zope.proxy import removeAllProxies
from zope.location import LocationProxy
from zope.component import queryMultiAdapter
from zope.publisher.interfaces import NotFound

from zojax.layoutform import Fields, PageletEditForm, button
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.portlet.interfaces import \
    IPortlet, IPortletManager, IPortletManagerWithStatus, _

from interfaces import \
    IPortletConfigMarker, IPortletManagerConfigMarker, \
    IPortletManagerPublicMarker, IPortletPublicMarker, IPortletManagerPortlets


class PortletManagerConfiguration(PageletEditForm):

    buttons = PageletEditForm.buttons.copy()
    handlers = PageletEditForm.handlers.copy()

    @property
    def fields(self):
        return Fields(self.context.__schema__)

    @property
    def label(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    def applyChanges(self, data):
        changes = super(PortletManagerConfiguration, self).applyChanges(data)

        if changes:
            self.redirect('.')

        return changes

    def canCopy(self):
        if IPortletManagerWithStatus.providedBy(self.context):
            self.context.update()
            return getattr(self.context, 'parentManager', None) is not None
        return False

    @button.buttonAndHandler(
        _(u'Copy portlet settings from parent manager'),
        name='copy', condition=canCopy)
    def handleCopyFromParent(self, action):
        self.context.copyDataFromParent()
        IStatusMessage(self.request).add(_(u'Setting has been copied'))
        self.redirect('.')


class PublisherPlugin(object):
    component.adapts(IPortletManagerConfigMarker, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context

        if name in context.portletIds:
            portlet = queryMultiAdapter(
                (context.context, request, context, None), IPortlet, name)

            if portlet is not None:
                portlet.updateConfigure()
                if portlet.isAllowed():
                    interface.alsoProvides(portlet, IPortletConfigMarker)
                    return LocationProxy(portlet, context, name)

        raise NotFound(self.context, name, request)


class PublicPublisherPlugin(object):
    component.adapts(IPortletManagerPublicMarker, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context
        for portlet in IPortletManagerPortlets(context):
            if name == portlet.__name__:
                portlet = removeAllProxies(portlet)
                interface.alsoProvides(portlet, IPortletPublicMarker)
                return LocationProxy(portlet, context, name)

        raise NotFound(self.context, name, request)


class ModifyPortlets(object):

    def listPortlets(self):
        portlets = []
        for portlet in self.portlets:
            portlets.append(
                (portlet.title, portlet.__name__,
                 {'name': portlet.__name__,
                  'title': portlet.title,
                  'description': portlet.description,
                  'schema': portlet.__schema__ is not None}))

        portlets.sort()
        return [info for t,n,info in portlets]

    def update(self):
        context = self.context

        portlets = []
        for pid in self.context.portletIds:
            portlet = queryMultiAdapter(
                (context.context, self.request, context, None), IPortlet, pid)
            if portlet is not None:
                portlet.updateConfigure()
                if portlet.isAllowed():
                    portlets.append((portlet.title, pid, portlet))

        portlets.sort()
        self.portlets = [portlet for t,i,portlet in portlets]

    def isAvailable(self):
        for portlet in self.portlets:
            if portlet.__schema__ is not None:
                return True

        return False

    def postUpdate(self): pass


@component.adapter(IPortletManager)
@interface.implementer(IPortletManagerPortlets)
def portletManagerPortlets(context):
    return context.portlets

@component.adapter(IPortletManagerWithStatus)
@interface.implementer(IPortletManagerPortlets)
def portletManagerWithStatusPortlets(context):
    if context.parentManager is not None:
        return IPortletManagerPortlets(context.parentManager)
    return context.portlets
