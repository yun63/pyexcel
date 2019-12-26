# -*- coding:utf-8 -*-

####################################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
####################################################################################

"""

@File: exceptions.py

@Description: 异常

"""

class ExcelException(Exception):

    def __init__(self, error_code, message, row, col, val):
        message = message + u', 第%s行: 第%s列: 值: %s' % (row, col, val)
        super(Exception, self).__init__(error_code, message)

    @property
    def error_code(self):
        return self.args[0]

    @property
    def what(self):
        return self.args[1]

    def __str__(self):
        return '%s: %s' % (self.error_code, self.what)

    __repr__ = __str__

    def __unicode__(self):
        return u'%s: %s' % (self.error_code, self.what)


class ExcelTypeErrorException(TypeError):
    pass


class ExcelValueErrorException(ValueError):
    pass


class PrimaryKeyIgnoreException(ExcelException):

    def __init__(self, row, col, key):
        super(PrimaryKeyIgnoreException, self).__init__(-100, u'主键不能设置忽略', row, col, key)

