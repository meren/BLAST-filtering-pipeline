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
from pipeline.utils import fastalib as u
from pipeline.utils.logger import debug
from pipeline.utils.logger import error


class FilterError(Exception):
    def __init__(self, e = None):
        Exception.__init__(self)
        self.e = e
        error(e)
        return
    def __str__(self):
        return 'Filter Error: %s' % self.e

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
        try:
            ids_to_filter = set([id.strip() for id in open(self.files['hit_ids']).readlines()])
        except IOError:
            raise FilterError, 'Hit IDs file missing ("%s").' \
                    % (self.files['hit_ids'])

        input  = u.SequenceSource(self.files['input'])
        filtered_output = open(self.files['filtered_reads'], 'w')
        survived_output = open(self.files['survived_reads'], 'w')

        debug('input file is being splitted.')        

        while input.next():
            #if input.pos % 10000 == 0:
            #    sys.stderr.write('\rSplitting FASTA file: ~ %s' % (utils.pp(input.pos)))
            #    sys.stderr.flush()

            if input.id in ids_to_filter:
                ids_to_filter.remove(input.id)
                filtered_output.write('>%s\n' % input.id)
                filtered_output.write('%s\n' % input.seq)
            else:
                survived_output.write('>%s\n' % input.id)
                survived_output.write('%s\n' % input.seq)
        
        filtered_output.close()
        survived_output.close()

        debug('filter "%s" is done; filtered reads: "%s"; survived reads: "%s"'\
                 % (self.name, self.files['filtered_reads'], self.files['survived_reads']))        
