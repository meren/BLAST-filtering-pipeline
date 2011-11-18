# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

import os
import sys

def check_dir(dir, create=True, clean_dir_content = False):
    if os.path.exists(dir):
        pass
    elif create:
        os.makedirs(dir)
    else:
        return False

    if clean_dir_content:
        delete_files_in_dir(dir)

    return True

def delete_files_in_dir(dir):
    for f in os.listdir(dir):
        print 'remove,', os.path.join(dir, f)
        #os.unlink(os.path.join(dir, f))

def info(label, value, mlen = 30, file_obj = None):
    info_line = "%s %s: %s" % (label, '.' * (mlen - len(label)), str(value))
    if file_obj:
        info_file_obj.write(info_line + '\n')
    print info_line
