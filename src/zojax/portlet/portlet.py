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
from zojax.portlet.browser.portlet import portletAbsoluteURL
"""

$Id$
"""
from zope import interface
from zope.schema import getFields
from zope.location import Location
from zope.security.proxy import removeSecurityProxy
from zope.component import getUtility, queryUtility, queryMultiAdapter
from z3c.pt.pagetemplate import ViewPageTemplateFile

from configproperty import ConfigurationProperty
from interfaces import IPortlet, IPortletView, IPortletManager


class PortletBase(Location):
    interface.implements(IPortlet)

    context = None
    request = None
    manager = None
    template = None

    title = u''
    description = u''
    configuration = None

    __data__ = None
    __schema__ = None

    def __init__(self, context, request, manager, view):
        self.request = request
        self.context = context
        self.manager = manager
        self.view = view

        if self.__schema__ is None or manager is None:
            self.__data__ = {}
        else:
            self.__data__ = removeSecurityProxy(
                manager).getPortletData(self.__name__)

    @property
    def __parent__(self):
        return self.manager or self.context

    def update(self):
        pass

    def updateConfigure(self):
        pass
    
    @property
    def __url(self):
        return portletAbsoluteURL(self, self.request)

    def render(self):
        res = u''
        view = queryMultiAdapter((self, self.request), IPortletView)
        if view is not None:
            view.update()
            res = view.render()
        else:
            if self.template is not None:
                res = self.template()
            else:
                res = u''
        if res and len(self.__schema__):
            return u'<div class="zojax-portlet" kssattr:url="%s">%s</div>'%(self.__url, res)
        else:
            return res

    def isAllowed(self):
        return True

    def isAvailable(self):
        return True

    def updateAndRender(self):
        self.update()
        if self.isAvailable():
            return self.render()
        else:
            return u''


def Portlet(name, class_=None, title='', description='',
            template=None, schema=None, **kw):
    cdict = {}
    cdict.update(kw)
    cdict['__name__'] = name
    cdict['title'] = title
    cdict['description'] = description

    if template:
        cdict['template'] = ViewPageTemplateFile(template)

    if class_ is not None:
        class_name = 'Portlet<%s:%s>'%(class_.__name__, name)
    else:
        class_name = 'Portlet<%s>'%name

    if class_ is None:
        bases = (PortletBase,)
    else:
        bases = (class_, PortletBase)

    PortletClass = type(str(class_name), bases, cdict)

    if schema is not None:
        for f_id in getFields(schema):
            setattr(PortletClass, f_id, ConfigurationProperty(schema[f_id]))

        PortletClass.__schema__ = schema
        interface.classImplements(PortletClass, schema)

    return PortletClass
