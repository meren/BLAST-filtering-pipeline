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

from pipeline.utils import utils

class Filter:
    def __init__(self, target_db):
        self.target_db = target_db
        self.name = None
        self.module = None
        self.cmdparams = []
        self.rfnparams = {}
        self.execution_order = []
        self.dirs = {}
        self.files = {}

    def execute(self):
        if not self.execution_order:
            self.execution_order = self.module.FUNCTIONS_ORDER
        
        for func in self.execution_order:
            self.module.FUNCTION_MAP[func](self)

        self.split()

    def get_refinement_params(self):
        if hasattr(self.module, 'ALLOWED_RFNPARAMS'):
            return self.module.ALLOWED_RFNPARAMS.keys()
        else:
            return {}

    def split(self):
        """this function creates 04_filtered.fa and 05_survived.fa
           files from self.files['input'] file, using ids in
           self.files['hit_ids'] provided by the filter"""

        # FIXME: user should be able to change the default behavior of
        # this function (for instance user may require one filter not
        # to split the content of the input file and the same input 
        # to be used by the next filter.
        
        pass
