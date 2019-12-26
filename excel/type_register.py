# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: type_register.py

@Description: excel单元格类型注册器

"""

from utils import object_register
from excel.exceptions import ExcelException 


class BaseTypeRegister(object_register.ClassRegister):

    @classmethod
    def as_type(cls, tname, reserved=None):
        clz = cls.find_class(tname)
        if not clz:
            raise ExcelException(-1, 'Unregister type name %s' % tname)
        instance = clz(reserved)
        return instance 

