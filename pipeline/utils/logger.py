# -*- coding: utf-8 -*-

# Copyright (C) 2010 - 2011, University of New Orleans
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# --
#
# Caller aware logging.
#

import os
import sys
import time
import string

def findCaller():
    if string.lower(__file__[-4:]) in [".pyc", ".pyo"]:
        srcFile = __file__[:-4] + ".py"
    else:
        srcFile = __file__
    srcFile = os.path.normcase(srcFile)

    f = sys._getframe().f_back
    while 1:
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == srcFile:
            f = f.f_back
            continue
        return ":".join([os.path.basename(filename), str(f.f_lineno)])


def __raw(msg, f):
    output = "\n%s\n" % (msg)
    if f:
        open(f, "a").write(output)
    sys.stderr.write(output)

def __log(level, caller, msg, f):
    output = "%s | %-6.6s | %-16.16s | %s\n" %(time.asctime(), level, caller, msg)
    if f:
        open(f, "a").write(output)
    sys.stderr.write(output)


def debug(msg, f = None): 
    caller = findCaller()
    __log("DEBUG", caller, msg, f)

def error(msg, f = None):
    caller = findCaller()
    __log("ERROR", caller, msg, f)

def info(msg, f = None): 
    caller = findCaller()
    __log("INFO", caller, msg, f)

def raw(msg, f = None):
    __raw(msg, f)
