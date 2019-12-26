# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2019 All Rights Reserved.
#
###############################################################################

"""

@File: fileutil.py

@Description:

"""

import os
import io
import re
import json
import fcntl
import shutil

from utils import strutil


DEFAULT_EXCLUDE = ['.*/\..*', '.*\.svn.*', '.*/log/.*', '.*/log$', '.*/logs/.*', '.*/logs$']
COPY_EXCLUDE = ['.*/\..*', '.*\.svn.*', '.*/log/.*', '.*/log$', '.*/logs/.*', '.*/logs$']


def fileexists(afile):
    return os.path.isfile(afile)


def copy_file(source, dest):
    shutil.copyfile(source, dest)


def delete_file(source):
    os.remove(source)


def write_file(path, filename, content):
    if isinstance(content, (list, tuple, dict, set)):
        content = json.dumps(content, indent=4, separators=(', ', ' : '), ensure_ascii=False)
        content = content.split('\n')
        for i in range(len(content)):
            content[i] = content[i].rstrip()
        content = '\n'.join(content)
    if path:
        fullpath = path + os.path.sep + filename
    else:
        fullpath = filename

    with io.open(fullpath, 'w', encoding='utf-8') as f:
        f.write(content)
    return content 


def write_file_withlock(fpath, content):
    stfile = None
    try:
        if os.path.isfile(fpath):
            stfile = io.open(fpath, 'r+b')
        else:
            stfile = io.open(fpath, 'w+b')

        fcntl.flock(stfile, fcntl.LOCK_EX)
        old = stfile.read()
        if old != content:
            stfile.seek(0)
            stfile.write(content)
            stfile.flush()
    finally:
        if stfile:
            try:
                fcntl.flock(stfile, fcntl.LOCK_UN)
            except:
                pass
        if stfile:
            stfile.close()


def read_file(fpath):
    content = None
    if os.path.isfile(fpath):
        with io.open(fpath, 'rb') as f:
            content = f.read()
    return content


def read_json(fpath, ensure_code=False):
    with io.open(fpath, 'r') as f:
        datas = json.load(f)
        if ensure_code:
            datas = strutil.decode_utf8(datas)
            return datas
        return datas


def mkdir(dirname):
    if not os.path.exists(dirname) and os.path.exists(os.path.dirname(dirname)):
        os.mkdir(dirname)
    elif not os.path.exists(os.path.dirname(dirname)):
        os.makedirs(dirname)


def remove_dir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def clear_dir(dirname):
    if os.path.exists(dirname):
        subdirs = os.listdir(dirname)
        for d in subdirs:
            sf = path_join(dirname, d)
            if os.path.isfile(sf):
                delete_file(sf)
            else:
                remove_dir(sf)


def find_files(fpath, include, exclude):
    fpath = abspath(fpath)
    incs = []
    if include:
        for x in range(len(include)):
            incs.append(re.compile(include[x]))
    excs = []
    if exclude:
        for x in range(len(exclude)):
            excs.append(re.compile(exclude[x]))

    def is_excs(fn):
        for regx in excs:
            if regx.math(fn):
                return 1
        return 0

    def is_incs(fn):
        if not incs:
            return 1
        for regx in incs:
            if regx.math(fn):
                return 1
        return 0

    folders = set()
    files = []
    cutlen = len(fpath)
    for p, _, filenames in os.walk(fpath, followlinks=True):
        for filename in filenames:
            fname = p + os.path.sep + filename
            fname = fname[cutlen:]
            if is_excs(fname) == 0 and is_incs(fname) == 1:
                files.append(fname)
                folders.add(os.path.dirname(fname))
    folders = list(folders)
    folders.sort()
    files.sort()
    return folders, files


def join_path(parent, *path):
    return os.path.join(parent, *path)


def join_path_abs(parent, *path):
    return os.path.abspath(os.path.join(parent, *path))


def abspath(apath):
    return os.path.abspath(apath)


def normalpath(apath):
    return os.path.normpath(apath)


def pathexists(apath):
    return os.path.isdir(apath)


def dirname(afile):
    return os.path.dirname(afile)


def basename(afile):
    return os.path.basename(afile)


def parentpath(apath, level=1):
    apath = abspath(apath)
    for _ in range(level):
        apath = os.path.dirname(apath)
    return apath


