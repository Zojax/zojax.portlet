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
from zope.component import getMultiAdapter
from zope.proxy import removeAllProxies
from zope.traversing.browser import absoluteURL, AbsoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL

from zojax.layoutform import Fields, PageletEditForm

from zojax.portlet.interfaces import IPortlet


class PortletConfiguration(PageletEditForm):

    @property
    def fields(self):
        return Fields(self.context.__schema__)

    @property
    def label(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    def nextURL(self):
        return self.request.getURL()


def publicAbsoluteURL(ob, request):
    return getMultiAdapter((ob, request), IAbsoluteURL, name="public_absolute_url")()


class PortletPublicAbsoluteURL(AbsoluteURL):

    def __str__(self):
        return '%s/%s'%(getMultiAdapter(
                (self.context.manager, self.request),
                name='public_absolute_url'), self.context.__name__)

    __call__ = __str__


class PortletManagerPublicAbsoluteURL(AbsoluteURL):

    def __str__(self):
        return '%s/portlets/%s'%(
            absoluteURL(self.context.context, self.request), \
            removeAllProxies(self.context).__name__)

    __call__ = __str__
