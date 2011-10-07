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
from zojax.portlet.browser.portlet import publicAbsoluteURL
"""

$Id$
"""
import sys
import logging
from datetime import datetime
from pickle import Pickler
from pickle import Unpickler
from StringIO import StringIO
from BTrees.OOBTree import OOBTree
from rwproperty import setproperty, getproperty
from ZODB.POSException import ConflictError

from zope import interface
from zope.schema import getFields
from zope.location import Location
from zope.component import queryMultiAdapter
from zope.cachedescriptors.property import Lazy
from zope.location.pickling import locationCopy

from zojax.extensions.interfaces import IExtensible

from interfaces import DISABLED, ENABLED, UNSET
from interfaces import IPortlet, IPortletsExtension
from interfaces import IPortletManager, IPortletManagerView
from interfaces import IPortletManagerConfiguration
from configproperty import ConfigurationProperty
from browser.portlet import portletAbsoluteURL

logger = logging.getLogger('zojax.portlet')


class PortletManagerBase(Location):
    interface.implements(IPortletManager)

    context = None
    request = None
    view = None
    template = None
    portlettype = IPortlet
    portlets = ()

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    @Lazy
    def __data__(self):
        data = {}
        parent = self.context

        while True:
            if IExtensible.providedBy(parent):
                extension = IPortletsExtension(parent, None)
                if extension is not None:
                    data = extension.getManagerData(self)
                    break

            parent = getattr(parent, '__parent__', None)
            if parent is None:
                break

        return data

    @property
    def __parent__(self):
        return self.context

    def update(self):
        context = self.context
        request = self.request

        portlets = []
        for portletId in self.portletIds:
            portlet = queryMultiAdapter(
                (context,request,self,self.view), self.portlettype, portletId)
            if portlet is not None:
                portlets.append(portlet)

        self.portlets = portlets

    def updateConfigure(self):
        self.portlets = []

    @property
    def __url(self):
        return portletAbsoluteURL(self, self.request)

    @property
    def __checkUrl(self):
        return '%s/check'%publicAbsoluteURL(self, self.request)

    def render(self):
        try:
            res = ''
            if not self.portlets or not self.isAvailable():
                return u''
            else:
                view = queryMultiAdapter((self, self.request), IPortletManagerView)
                if view is not None:
                    res = view.updateAndRender()
                res = u'\n'.join([portlet.updateAndRender()
                                   for portlet in self.portlets])
            return u'<div class="zojax-portlet-manager" kssattr:url="%s" kssattr:checkurl="%s">%s</div>'%(self.__url, self.__checkUrl, res)
        except Exception, e:
            logger.exception('Portlets Rendering Error: ')
            return u'<div class="zojax-portlet-manager" kssattr:url="%s" kssattr:checkurl="%s">Portlets Rendering Error</div>' % \
                (self.__url, self.__checkUrl)

    def isAvailable(self):
        return True

    def getPortletData(self, name):
        data = self.__data__.get('__portlets_data__')
        if data is None:
            data = OOBTree()
            self.__data__['__portlets_data__'] = data

        pdata = data.get(name)
        if pdata is None:
            pdata = OOBTree()
            data[name] = pdata

        return pdata

    def updateAndRender(self):
        self.update()
        if self.isAvailable():
            return self.render()
        else:
            return u''


class PortletManagerWithStatus(object):

    parentManager = None

    def update(self):
        if self.status == UNSET:
            view = self.view
            name = self.__name__
            context = self.context
            request = self.request
            while True:
                context = context.__parent__
                if context is None:
                    self.portlets = ()
                    return

                manager = queryMultiAdapter(
                    (context, request, view), IPortletManager, name)
                if manager is not None:
                    manager.update()
                    self.parentManager = manager
                    return

        elif self.status == DISABLED:
            self.portlets = ()
            return

        super(PortletManagerWithStatus, self).update()

    def render(self):
        if self.parentManager is not None:
            return self.parentManager.render()

        return super(PortletManagerWithStatus, self).render()


    def copyDataFromParent(self):
        data = locationCopy(self.parentManager.__data__)
        self.__data__.update(data)
        self.status = self.parentManager.status


def PortletManager(
    name, class_=None, provides=(),
    title='', description='', schema=None, portlettype=IPortlet, **kw):

    # configuration schema
    if schema is None:
        schema = IPortletManagerConfiguration

    cdict = {}
    cdict.update(kw)
    cdict['__name__'] = name
    cdict['__schema__'] = schema
    cdict['title'] = title
    cdict['description'] = description
    cdict['portlettype'] = portlettype

    class_name = 'PortletManager<%s>'%name

    if class_ is None:
        bases = (PortletManagerBase,)
    else:
        bases = (class_, PortletManagerBase)

    ManagerClass = type(str(class_name), bases, cdict)

    if provides:
        interface.classImplements(ManagerClass, *provides)

    for f_id in getFields(schema):
        if not hasattr(ManagerClass, f_id):
            setattr(ManagerClass, f_id, ConfigurationProperty(schema[f_id]))

    interface.classImplements(ManagerClass, schema)

    return ManagerClass
