# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: strutil.py

@Description: 字符串操作接口

"""

import json
import copy
import base64
import hashlib
import urllib
import uuid as _uuid


def clone(data):
    """
    克隆，即深拷贝
    """
    return copy.deepcopy(data)


def deepcopy(data):
    """
    数据深拷贝
    """
    return copy.deepcopy(data)


def uuid():
    """
    返回唯一uuid
    """
    return str(_uuid.uuid4()).replace('-', '')


def urlencode(params):
    return urllib.urlencode(params)


def md5digest(md5str):
    """
    MD5摘要
    """
    m = hashlib.md5()
    m.update(md5str)
    md5code = m.hexdigest()
    return md5code.lower()


def dumps_lock(obj):
    return json.dumps(obj, indent=2, separators=(', ', ' : '), sort_keys=True, ensure_ascii=False)


def dumps(obj):
    return json.dumps(obj, separators=(',', ':'))


def decode_utf8(datas):
    if isinstance(datas, dict):
        ndatas = {}
        for key, val in datas.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            ndatas[key] = decode_utf8(val)
        return ndatas

    if isinstance(datas, list):
        ndatas = []
        for val in datas:
            ndatas.append(decode_utf8(val))
        return ndatas

    if isinstance(datas, unicode):
        return datas.encode('utf-8')

    return datas


def unicode_to_ascii(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return str(s)


def loads(jstr, decodeutf8=False, ignore_exception=False, exception=None):
    if ignore_exception:
        try:
            datas = json.loads(jstr)
        except:
            datas = exception
    else:
        datas = json.loads(jstr)
    if datas and decodeutf8:
        datas = decode_utf8(datas)
    return datas


def dumps_base64(obj):
    jstr = json.dumps(obj, separators=(',', ':'))
    return base64.b64encode(jstr)


def loads_base64(base64jstr, decodeutf8=False):
    jstr = base64.b64decode(base64jstr)
    datas = json.loads(jstr)
    if decodeutf8:
        datas = decode_utf8(datas)
    return datas


def loads_json_val(jstr, key, defaultval=''):
    key = '"' + key + '":'
    begin = jstr.find(key)
    if begin > 0:
        x = jstr.find('"', begin + len(key))
        y = jstr.find('"', x + 1)
        return jstr[x + 1: y]
    return defaultval

