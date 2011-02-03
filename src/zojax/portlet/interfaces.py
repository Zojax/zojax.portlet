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
from zope import interface, schema
from zope.location.interfaces import ILocation
from zope.tales.interfaces import ITALESExpression
from zope.contentprovider.interfaces import IContentProvider
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.interface.common.sequence import IExtendedReadSequence
from zope.i18nmessageid import MessageFactory

_ = MessageFactory(u'zojax.portlet')

ENABLED = 1
DISABLED = 2
UNSET = 3

statusVocabulary = SimpleVocabulary(
    (SimpleTerm(ENABLED, '1', _('Enabled')),
     SimpleTerm(DISABLED, '2', _('Disabled')),
     SimpleTerm(UNSET, '3', _('Inherit'))))


class ITALESPortletExpression(ITALESExpression):
    """ portlet tales expression  """


class IPortlet(ILocation):
    """ portlet """

    title = schema.TextLine(
        title=u"Title",
        description=u"Portlet title",
        required=True)

    description = schema.Text(
        title=u"Description",
        description=u"Portlet description",
        required=False)

    __schema__ = interface.Attribute('Configuration schema')

    context = interface.Attribute('Context')
    request = interface.Attribute('Request')
    manager = interface.Attribute('Manager')
    view = interface.Attribute('View')

    def update():
        """ update """

    def updateConfigure():
        """ update portlet for configuration """

    def render():
        """ render portlet """

    def isAllowed():
        """ is allowed for configuration """

    def isAvailable():
        """ check is this portlet available in context """

    def updateAndRender():
        """ update and render portlet """


class IPortletManager(IContentProvider):
    """ portlet manager """

    title = schema.TextLine(
        title=u"Title",
        description=u"Portlet title",
        required=True)

    description = schema.Text(
        title=u"Description",
        description=u"Portlet description",
        required=False)

    view = interface.Attribute('View')
    portlets = interface.Attribute('Portlets')
    portlettype = interface.Attribute('Portlet type')
    __schema__ = interface.Attribute('Configuration schema')

    def updateConfigure():
        """ update portlet manager for configuration """

    def isAvailable():
        """ check is this portlet manager available in context """

    def getPortletData(name):
        """ return portlet persistent data container """

    def updateAndRender():
        """ update and render portlet manager """
        

class IPortletManagerConfiguration(interface.Interface):
    """ portlet manager configuration """

    portletIds = schema.Tuple(
        title = _(u'Portlets'),
        value_type=schema.Choice(vocabulary = "zojax portlets"),
        default = (),
        required = True)


class IPortletManagerWithStatus(IPortletManagerConfiguration):
    """ portlet manager with status """

    parentManager = interface.Attribute('Parent manager')

    status = schema.Choice(
        title = _(u'Status'),
        description = _(u""""Enabled" -- set portlets at this level and do not inherit portlets from the manager one level up;
"Disabled" -- don't display portlets that have been set for this manager and don't inherit portlets from the manager one level up. This action will result in no portlets being displayed;
"Unset" -- inherit portlets from the manager one level up"""),
        vocabulary = statusVocabulary,
        default = UNSET,
        required = True)

    def copyDataFromParent():
        """ copy configuration data from parent manager """


class IPortletsExtension(interface.Interface):
    """ portlets extention """

    def getManagerData(manager, name=None):
        """ return portlet manager configuration """


class IPortletView(interface.Interface):
    """ portlet view """


class IPortletManagerView(interface.Interface):
    """ portlet manager view """


class IPortletConfigurationView(interface.Interface):
    """ portlet configuration view """


class IPortletEditLinksLayer(interface.Interface):
    """ portlet edit links layer """