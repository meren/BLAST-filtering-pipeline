#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

#
# bpline.py: user command line interface.
#

# standard python modules
import os
import sys

# non-standard python modules
from pipeline.utils.cmdlinehandler import get_parser_obj
from pipeline.classes.constants import Constants as c
from pipeline.classes.config import Config

def main(config):
    for filter in config.filters:
        config.init_filter_files_and_directories(filter)
        filter.execute()
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(Config(get_parser_obj().parse_args(), c(os.path.dirname(os.path.abspath(__file__))))))
