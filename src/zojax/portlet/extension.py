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
from BTrees.OOBTree import OOBTree

from zope import interface
from interfaces import IPortletsExtension


class PortletsExtension(object):
    interface.implements(IPortletsExtension)

    def getManagerData(self, manager, name=None):
        if name is None:
            name = manager.__name__

        data = self.data.get(name)
        if not isinstance(data, OOBTree):
            data = OOBTree()
            self.data[name] = data

        return data
