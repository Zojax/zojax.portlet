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
import os.path
from zope import schema, interface
from zope.component import getUtility
from zope.component.zcml import handler, utility, adapter
from zope.schema.interfaces import IField
from zope.configuration import fields
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.security.checker import defineChecker, Checker, CheckerPublic
from zope.app.security.protectclass import protectName, protectSetAttribute

from portlet import Portlet
from manager import PortletManager
from interfaces import IPortlet, IPortletManager, IPortletManagerConfiguration


class IPortletDirective(interface.Interface):

    for_ = fields.GlobalObject(
        title = u"For",
        required = False)

    name = fields.PythonIdentifier(
        title = u"Name",
        description = u"Name of the portlet.",
        required = True)

    template = fields.Path(
        title=u'Template.',
        description=u"Refers to a file containing a page template (should "
                     "end in extension ``.pt`` or ``.html``).",
        required=False)

    title = fields.MessageID(
        title = u"Title",
        description = u"Title of the portlet used in UIs.",
        required = True)

    description = fields.MessageID(
        title = u"Description",
        description = u"Description of the portlet used in UIs.",
        required = False)

    class_ = fields.GlobalObject(
        title = u"Class",
        description = u'Custom portlet class.',
        required = False)

    provides = fields.GlobalInterface(
        title=u"Interface the portlet provides",
        description=u"This attribute specifies the interface the portlet"
                     " instance will provide.",
        default=IPortlet,
        required=False)

    schema = fields.GlobalInterface(
        title = u"Schema",
        description = u'Portlet configuration schema.',
        required = False)

    type = fields.GlobalInterface(
        title = u"Type",
        description = u'Portlet type.',
        required = False)

    manager = fields.GlobalObject(
        title = u"Manager",
        description = u'Portlets manager.',
        required = False)


class IPortletManagerDirective(interface.Interface):

    for_ = fields.GlobalObject(
        title = u"For",
        description = u'The content interface or class this manager is for.',
        required = False)

    name = fields.PythonIdentifier(
        title = u"Name",
        description = u"Name of the portlet manager.",
        required = True)

    title = fields.MessageID(
        title = u"Title",
        description = u"Title of the portlet manager used in UIs.",
        required = True)

    description = fields.MessageID(
        title = u"Description",
        description = u"Description of the portlet manager used in UIs.",
        required = False)

    class_ = fields.GlobalObject(
        title = u"Class",
        description = u'Custom portlet manager class.',
        required = False)

    schema = fields.GlobalInterface(
        title = u"Schema",
        description = u'Portlet manager configuration schema.',
        required = False)

    layer = fields.GlobalObject(
        title = u'Layer',
        description = u'The layer for which the portlet manager should be available',
        required = False,
        default = IDefaultBrowserLayer)

    provides = fields.Tokens(
        title = u"The interface this portlet manager provides.",
        description = u"""This would be used for support other views.""",
        required = False,
        value_type = fields.GlobalInterface())

    portlettype = fields.GlobalInterface(
        title = u"Portlet type",
        description = u'Portlet type.',
        required = False)


def portletDirective(
    _context, name, title, for_=None, template=u'',
    description=u'', class_=None, provides=IPortlet,
    schema=None, type=IPortlet, manager=None, **kw):

    # Make sure that the template exists
    if template:
        template = os.path.abspath(str(_context.path(template)))
        if not os.path.isfile(template):
            raise ConfigurationError("No such file", template)

    # Build a new class.
    PortletClass = Portlet(
        name, class_, title, description, template, schema, **kw)

    if provides is not IPortlet:
        interface.classImplements(PortletClass, provides)

    # Set up permission mapping for various accessible attributes
    required = {'__call__': CheckerPublic,
                'browserDefault': CheckerPublic,
                'publishTraverse': CheckerPublic}

    for iface in (IPortlet, provides):
        for iname in iface:
            required[iname] = CheckerPublic

    # security checker
    defineChecker(PortletClass, Checker(required))

    # portlet schema
    if schema is not None:
        # security for configuration
        for f_id in schema:
            field = schema[f_id]
            if IField.providedBy(field) and not field.readonly:
                protectSetAttribute(PortletClass, f_id, 'zojax.ManagePortlets')
            protectName(PortletClass, f_id, CheckerPublic)

    # register the portlet
    adapter(_context, (PortletClass,), type,
            (for_, None, manager, None), name=name)


def portletManagerDirective(
    _context, name, title, for_=None, description=u'',
    class_=None, schema=None, layer=IDefaultBrowserLayer,
    provides=(), portlettype=IPortlet, **kw):

    # Build a new class
    ManagerClass = PortletManager(
        name, class_, provides, title, description, schema, portlettype, **kw)

    # Set up permission mapping for various accessible attributes
    required = {'__call__': CheckerPublic,
                'browserDefault': CheckerPublic,
                'publishTraverse': CheckerPublic}

    for iname in IPortletManager:
        required[iname] = CheckerPublic

    # security checker
    defineChecker(ManagerClass, Checker(required))

    # security for schema fields
    for iface in (IPortletManagerConfiguration, schema):
        if iface is None:
            continue
        for f_id in iface:
            field = iface[f_id]
            if IField.providedBy(field) and not field.readonly:
                protectSetAttribute(ManagerClass, f_id, 'zojax.ManagePortlets')
            protectName(ManagerClass, f_id, 'zope.Public')

    # register the portlet manager
    adapter(_context, (ManagerClass,),
            IPortletManager, (for_, layer, None), name=name)
