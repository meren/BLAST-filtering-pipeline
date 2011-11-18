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
from ConfigParser import ConfigParser

from utils import utils

class Filter:
    def __init__(self, target_db):
        self.target_db = target_db
        self.name = None
        self.dirs = {}
        self.files = {}
        self.in_r1 = None
        self.in_r2 = None
        self.out_r1 = None
        self.out_r2 = None

    def run(self):
        pass
