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


class Constants:
    def __init__(self, base_dir = None):
        self.dirs = {}
        
        if base_dir:
            self.dirs['base'] = base_dir
        else:
            self.dirs['base'] = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-2])
        
        self.dirs['modules'] = os.path.join(self.dirs['base'], 'pipeline/modules')
