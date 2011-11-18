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

class Constants:
    def __init__(self, base_dir):
        self.dirs = {}
        self.dirs['base'] = base_dir
        self.dirs['modules'] = os.path.join(self.dirs['base'], 'pipeline/modules')
