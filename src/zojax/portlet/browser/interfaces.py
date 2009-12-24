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

from zojax.portlet.interfaces import IPortletManager


class IPortletConfigMarker(interface.Interface):
    """ portlet config """


class IPortletPublicMarker(interface.Interface):
    """ portlet public """


class IPortletManagerConfigMarker(interface.Interface):
    """ portlet manager config """


class IPortletManagerPublicMarker(interface.Interface):
    """ portlet manager public """


class IPortletManagerPortlets(interface.Interface):
    """ portlets of portlet manager """

    def __iter__():
        """ """
