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
from zojax.portlet.interfaces import _

_marker = object()


class ConfigurationProperty(object):
    """ Special property thats reads and writes values from
    instance's 'data' attribute

    Let's define simple schema field

    >>> from zope import schema
    >>> field = schema.TextLine(
    ...    title = u'Test',
    ...    default = u'default value')
    >>> field.__name__ = 'attr1'

    Now we need content class

    >>> class Content(object):
    ...
    ...    attr1 = ConfigurationProperty(field)

    Lets create class instance and add field values storage

    >>> ob = Content()

    If content instance __data__ attribute is None we get default
    value for field and exception on write

    >>> ob.attr1
    u'default value'

    >>> ob.attr1 = u'test'
    Traceback (most recent call last):
    ...
    ValueError: ('attr1', u"Can't set field")

    >>> ob.__data__ = {}

    By default we should get field default value

    >>> ob.attr1
    u'default value'

    We can set only valid value

    >>> ob.attr1 = 'value1'
    Traceback (most recent call last):
    ...
    WrongType: ('value1', <type 'unicode'>)

    >>> ob.attr1 = u'value1'
    >>> ob.attr1
    u'value1'

    If storage contains field value we shuld get it

    >>> ob.__data__['attr1'] = u'value2'
    >>> ob.attr1
    u'value2'

    Remove attribute

    >>> del ob.attr1
    >>> ob.attr1
    u'default value'

    We can't set value for readonly fields

    >>> field.readonly = True

    But we can set readonly first time
    >>> ob.attr1 = u'value1'

    Next time we will get exception

    >>> ob.attr1 = u'value1'
    Traceback (most recent call last):
    ...
    ValueError: ('attr1', u'Field is readonly')

    """

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if getattr(inst, '__data__', None) is None:
            return self.__field.default

        value = inst.__data__.get(self.__name, _marker)
        if value is _marker:
            return self.__field.default

        return value

    def __set__(self, inst, value):
        if getattr(inst, '__data__', None) is None:
            raise ValueError(self.__name, _(u"Can't set field"))

        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and self.__name in inst.__data__:
            raise ValueError(self.__name, _(u'Field is readonly'))
        inst.__data__[self.__name] = value

    def __delete__(self, inst):
        if inst.__data__ is not None:
            if self.__name in inst.__data__:
                del inst.__data__[self.__name]
