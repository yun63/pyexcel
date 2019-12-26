# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: excel.py

@Description: excel文档对象

"""

import xlrd  # http://pypi.python.org/pypi/xlrd

from excel import sheet as pysheet
from excel.exceptions import ExcelException
from utils import fileutil


class Excel(object):

    def __init__(self, fullpath):
        self.filename = fullpath
        self.master = None
        self.sheets = {}  # <name:SheetInfo>
        self._fetch_document(self.filename)

    def _fetch_document(self, filename):
        workbook = xlrd.open_workbook(filename)
        for s in workbook.sheets():
            if s.name[0] == '!':
                continue
            print(u'🎤  Processing sheet %s ...' % s.name.split('#')[0])
            try:
                sheet_info = self._do_fetch_one_sheet(s)
            except ExcelException as e:
                print(u'⚠️  Fetch sheet data failed, %s, reason: %s' % (s.name.split('#')[0], e.what))
                continue
            self.sheets[sheet_info.name] = sheet_info

    def _do_fetch_one_sheet(self, xlsheet):
        sheet_info = pysheet.SheetInfo()
        sheet_info.fill_sheet_data(xlsheet, 2)
        return sheet_info

    def dumps(self, outpath):
        success = True
        ok_list, fail_list = [], []
        for name, sheet in self.sheets.iteritems():
            if sheet.meta.format == 'map':
                data = self._format_map_data(sheet.table)
            else:
                data = self._format_list_data(sheet.table)
            outpath2 = fileutil.join_path(outpath, name).encode('utf-8')
            filename = fileutil.join_path(name, '0.json')
            if not fileutil.pathexists(outpath2):
                fileutil.mkdir(outpath2) # 创建多级目录
            try:
                content = fileutil.write_file(outpath2, '0.json', data)
                #print(content)
            except:
                print(u'👿  Generating %s failed' % filename)
                success = False
                fail_list.append(name)
                continue
            ok_list.append(name)
            print(u'🍺  Successfully generate %s' % filename)
        return success, ok_list, fail_list

    @classmethod
    def _format_list_data(cls, sheettable):
        """
        sheettable格式如下:
        {
            '1001': {'id': 1001, 'name': 'xxx'}
            '1002': {'id': 1002, 'name': 'yyy'}
        }
        """
        return sheettable.values()

    @classmethod
    def _format_map_data(cls, sheettable):
        return sheettable


if __name__ == '__main__':
    pass
