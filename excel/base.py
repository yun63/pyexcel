# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: base.py

@Description: Excel单元格支持的基本数据类型

"""

import re
from datetime import datetime

from utils import strutil
from excel.exceptions import ExcelTypeErrorException, ExcelValueErrorException


class base(object):

    def __init__(self, reserved):
        self.reserved = reserved

    def as_value(self, val):
        """
        转换对应类型数据，val可能是字符串
        """
        raise NotImplementedError


class Int(base):

    TYPE_NAME = 'int'
    DEFAULT_VAL = 0

    def as_value(self, val):
        if isinstance(val, (unicode, str)):
            val = val.strip()
        try:
            return int(val)
        except ValueError:
            raise ExcelValueErrorException('Invalid IntValue: %s' % val)


class String(base):

    TYPE_NAME = 'string'
    DEFAULT_VAL = ''

    def as_value(self, val):
        #print('### String: %s, unicode: %s' % (val, isinstance(val, unicode)))
        return val


class Float(base):

    TYPE_NAME = 'float'
    DEFAULT_VAL = 0.0

    def as_value(self, val):
        if isinstance(val, (unicode, str)):
            val = val.strip()
        return float(val)


class List(base):

    TYPE_NAME = 'list'
    DEFAULT_VAL = []

    def as_value(self, val):
        """
        TODO: 正则检测val符合list模式的字符串
        """
        if not isinstance(val, (unicode, str)):
            raise ExcelValueErrorException('Invalid ListValue: %s' % val)
        #print('### List: %s, unicode: %s' % (val, isinstance(val, unicode)))
        try:
            return eval(val.strip())
        except Exception:
            raise ExcelValueErrorException('Invalid ListValue: %s' % val)


class Dict(base):

    TYPE_NAME = 'map'
    DEFAULT_VAL = {}

    def as_value(self, val):
        """
        TODO: 正则检测val是否是dict模式的字符串
        """
        if not isinstance(val, (unicode, str)):
            raise ExcelValueErrorException('Invalid MapValue: %s' % val)
        #print('### Dict: %s, unicode: %s' % (val, isinstance(val, unicode)))
        try:
            return eval(val.replace(' ', ''))
        except Exception:
            raise ExcelValueErrorException('Invalid MapValue: %s' % val)



class Bool(base):

    TYPE_NAME = 'bool'
    DEFAULT_VAL = False

    def as_value(self, val):
        val = val.strip()
        if val in ['Yes', 'YES', 'Y']:
            return True
        if val in ['No', 'NO', 'N']:
            return False
        raise ExcelValueErrorException('Invalid BoolValue: %s' % val)


class Enum(base):

    TYPE_NAME = 'enum'
    DEFAULT_VAL = None

    def __init__(self, reserved):
        super(Enum, self).__init__(reserved)
        _iter = map(lambda x: x.strip(), reserved.strip('{}<> ').split(','))
        self.enums = list(map(int, _iter))

    def as_value(self, val):
        """
        枚举值必须是int，不支持其他类型的枚举
        """
        if isinstance(val, (unicode, str)):
            val = val.strip()
        val = int(val)
        if val not in self.enums:
            raise ExcelValueErrorException('Invalid EnumValue: %s' % val)
        return val


class DateTime(base):

    TYPE_NAME = 'datetime'
    DEFAULT_VAL = None

    def as_value(self, val):
        val = val.strip()
        try:
            dt = datetime.strptime(val, '%Y-%m-%d %H:%M')
            return datetime.strftime(dt, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ExcelValueError('Invalid DateTimeValue: %s' % val)

