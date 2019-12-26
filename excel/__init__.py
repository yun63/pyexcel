# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: __init__.py

@Description:

"""

from excel.base import Int, Float, String, List, Dict, Bool, Enum
from excel.type_register import BaseTypeRegister

BaseTypeRegister.register_class(Int.TYPE_NAME, Int)
BaseTypeRegister.register_class(Float.TYPE_NAME, Float)
BaseTypeRegister.register_class(String.TYPE_NAME, String)
BaseTypeRegister.register_class(List.TYPE_NAME, List)
BaseTypeRegister.register_class(Dict.TYPE_NAME, Dict)
BaseTypeRegister.register_class(Bool.TYPE_NAME, Bool)
BaseTypeRegister.register_class(Enum.TYPE_NAME, Enum)

