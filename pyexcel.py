# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019  All Rights Reserved.
#
###############################################################################

"""

@File: pyexcel.py

@Description:

"""

import sys
import json
import argparse

from excel import exceldoc
from utils import fileutil


global config, excelpath, outpath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool can convert excel sheets to json files')
    parser.add_argument('--excel', type=str,
                        help='specified excel file to convert')
    args = parser.parse_args()
    xlsxfile = args.excel
    if not xlsxfile or not xlsxfile.endswith('.xlsx'):
        parser.error('❌  Only convert excel file!')
        sys.exit(1)

    global excelpath, outpath, config
    config = fileutil.read_json('config.json', 'utf-8')
    excelpath = config.get('excel_path', '.').encode('utf-8')
    outpath = config.get('output_path', '.').encode('utf-8')

    xlsxfullname = fileutil.join_path(excelpath, xlsxfile).encode('utf-8')
    if not fileutil.fileexists(xlsxfullname):
        parser.error('❌  %s not exist!' % xlsxfile)
        sys.exit(1)

    ret, succs, fails = exceldoc.Excel(xlsxfullname).dumps(outpath)
    if ret:
        #print(u'🍺 Done %s' % (', '.join(succs)))
        pass
    else:
        print(u'💔 请检查你的配置 %s' % (', '.join(fails)))

    sys.exit(0)

