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
import time
from zope import interface, component
from zope.traversing.api import getPath, getParents
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.cache.tag import Tag, tagging

from interfaces import IPortlet


class PortletId(object):

    prefix = u'portlet: '

    def __init__(self, postfix=u''):
        self.postfix = postfix

    def __call__(self, instance):
        managers = []

        manager = instance.manager
        if manager is not None:
            managers.append(manager)

            while IPortlet.providedBy(manager):
                manager = manager.manager
                if manager is not None:
                    managers.insert(0, manager)

        mid = ':'.join(
            [getattr(manager, '__name__', u'manager') for manager in managers])

        return u'%s:%s%s%s'%(mid, self.prefix, instance.__name__, self.postfix)


class PortletCacheTag(Tag):

    def query(self, instance, default=None):
        global tagging

        name = u'portlet:%s'%instance.__name__
        return tagging.query(name, instance.context, default)

    def update(self, instance):
        global tagging

        name = u'portlet:%s'%instance.__name__
        value = self.genValue()

        # update self
        tagging.update(name, value, instance.context)

        # update in parents
        for context in getParents(instance.context):
            tagging.update(name, value, context)

    def __call__(self, id, instance, *args, **kw):
        global tagging

        name = u'portlet:%s'%instance.__name__
        val = tagging.query(name, instance.context)
        context = getPath(instance.context)

        if val:
            return (('tag:%s'%name, val), ('context', context))
        return (('context', context),)


PortletModificationTag = PortletCacheTag('zojax.portlet')


@component.adapter(IPortlet, IObjectModifiedEvent)
def portletHandler(ob, ev):
    PortletModificationTag.update(ob)
