# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: sheet.py

@Description: Excel Sheet对象(表单)

"""

import collections
from datetime import datetime

from xlrd import xldate_as_tuple

from excel import type_register
from excel.exceptions import ExcelException, PrimaryKeyIgnoreException


# Sheet表级联符
SHEET_CONNECT_SYMBOL = '##'

"""
#################################################################################################################

Excel:
               ----------------------------------------------------------------------------------------
     第1行 -> | 这里可以写一些注释，给产品看的，代码里直接跳过                                         |
               ----------------------------------------------------------------------------------------
 第2行表头 -> |  *id#int  | name#string  |   attr#list   |   data#map    | !sex#enum#{1,2}|  open#bool |
               ----------------------------------------------------------------------------------------    =>>
 第3行数据 -> |   10001   |   诸葛亮     |   [1,2,3,4]   | {'a':1,'b':2} |       1        |     No     |
               ----------------------------------------------------------------------------------------
              |   10002   |   貂蝉       |   [1,2,3,4]   | {'a':5,'b':8} |       2        |     Yes    |
               ----------------------------------------------------------------------------------------
 |hero#map|!equip#list#zip|

~~~~~~~~~~~~
Json:

 {
    "1001": {
        "id": 10001,
        "name": "诸葛亮"，
        "attr": [1,2,3,4],
        "data": {'a': 1, 'b': 2},
        "sex": 1,
        "open": false
    },
    "1002": {
        "id": 1002,
        "name": "貂蝉",
        "attr": [1,2,3,4],
        "data": {'a': 5, 'b': 8},
        "sex": 2,
        "open": true
    }
 }

#################################################################################################################
"""

class ColMark(object):

    PRIMARY_KEY_MARK = '*'  # 主键标识符 *id
    DATA_TYPE_MARK = '#'  # 数据类型标识符 name#string
    IGNORE_COL_MARK = '!' # 屏蔽列标识符 !ignore
    ENUM_SEP_MARK = '@' # 枚举值分隔符


class Meta(object):
    """
    Sheet表头信息
    """

    class Column(object):

        def __init__(self, name, ctype):
            self.name = name
            self.type = ctype


    def __init__(self):
        self.nrows = 0
        self.ncols = 0
        self.keys = []  # 主键可以多个, 这里存放主键列index
        self.cols = {}  # 列
        self.ignore_cols = []  # 忽略的列
        self.format = 'list'  # 默认输出格式为列表
        self.compress = False  # 是否做json数据压缩处理，暂时不做

    def get_col(self, col):
        """
        获取列
        """
        return self.cols.get(col)

    def padding(self, colvals):
        """
        填充表头
        """
        enum = None

        for icol, vcol in enumerate(colvals):
            if not vcol:
                continue
            print('padding, icol, vcol', icol, vcol)
            key, ctype = vcol.strip().split('#')
            if key[:2] == '!*':
                raise PrimaryKeyIgnoreException(2, icol, vcol)

            if key[0] == '!':  # 忽略
                self.ignore_cols.append(icol)
                continue

            if key[0] == '*':  # 主键
                key = key[1:]
                self.keys.append(icol)

            pair = ctype.split('@')  # 处理枚举
            if len(pair) == 2:
                ctype = pair[0]
                enum = pair[1]
            mytype = type_register.BaseTypeRegister.as_type(ctype, enum)
            mycol = Meta.Column(key, mytype)
            self.cols[icol] = mycol

        if not self.keys:
            self.keys.append(0)  # 默认第1列为主键，推荐每个sheet都设置主键

    def as_value(self, col, val):
        """
        单元格数据类型转换
        """
        col = self.get_col(col)
        return col.type.as_value(val)


class SheetInfo(object):

    NORMAL = 0  # 普通表
    MASTER = 1  # 主表
    SLAVE = 2  # 有主从关系的子表

    def __init__(self):

        self.type = SheetInfo.NORMAL

        self.meta = None  # 元数据

        self.slave_sheets = {}  # 所有的从属表

        self.table = collections.OrderedDict()  # 单元格数据

    @property
    def name(self):
        return self.meta.name

    @classmethod
    def make_meta(cls, xlsheet):
        """
        生成元数据信息
        """
        meta = Meta()

        meta.nrows = xlsheet.nrows
        meta.ncols = xlsheet.ncols

        name = xlsheet.name
        nameparts = name.strip().split('#')
        length = len(nameparts)

        if length == 1:
            meta.name = name
            meta.format = 'list'
            meta.compress = False
        elif length == 2:
            meta.name = nameparts[0]
            meta.format = nameparts[1]
            assert meta.format in ['list', 'map'], u'输出格式只支持list或map'
            meta.compress = False
        elif length == 3:
            meta.name = nameparts[0]
            meta.format = nameparts[1]
            meta.compress = True
            assert meta.format in ['list', 'map']
            assert nameparts[2].lower() == 'zip', u'压缩参数必须是zip'
        else:
            assert False, u'sheet格式错误, %s' % name

        meta.padding(xlsheet.row_values(1))  # 第2行是表头信息
        return meta 

    def add_slave_sheet(self, sheet):
        assert isinstance(sheet, SheetInfo)
        self.slave_sheets[sheet.name] = sheet

    def set_meta(self, meta):
        assert isinstance(meta, Meta)
        self.meta = meta 

    @classmethod
    def make_key(self, keys):
        """
        生成主键
        """
        _iter = map(lambda x: str(x).strip(), keys)
        return '_'.join(list(_iter))

    def fill_sheet_data(self, xlsheet, start_rowx=2):
        """
        sheet的第1行是注释，跳过
        sheet的第2行是表头，从第3行开始才是数据
        """
        #import pdb
        #pdb.set_trace()
        meta = self.make_meta(xlsheet)
        self.set_meta(meta)
        # 开始读取数据
        self._do_fetch_data(xlsheet, start_rowx)

    def _do_fetch_data(self, xlsheet, start_rowx):
        for row in range(start_rowx, self.meta.nrows):
            key, data = self._do_fetch_one_row(xlsheet, row)
            self.table.update({key: data})

    def _do_fetch_one_row(self, xlsheet, row):
        key_vals = list()
        row_vals_dict = collections.OrderedDict()
        row_values = xlsheet.row_values(row, 0, self.meta.ncols)
        for col in range(len(self.meta.cols)):
            if col in self.meta.ignore_cols:
                continue
            cellval = row_values[col]
            try:
                mycol = self.meta.get_col(col)
                myval = mycol.type.as_value(cellval)
                if col in self.meta.keys:
                    key_vals.append(myval)
                row_vals_dict[mycol.name] = myval
            except:
                raise ExcelException(-10000, u'数据格式错误', row + 1, col + 1, cellval)
        return self.make_key(key_vals), row_vals_dict

