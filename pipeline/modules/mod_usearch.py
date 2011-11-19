# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

description = "USEARCH module"

cmdline = "usearch -query %(input)s -blast6out %(output)s -wdb %(target_db)s %(params_from_config)s &> %(log)s"
rfnparams = {'min_alignment_length': int, 
             'min_identity': float}

from pipeline.utils import utils


class ModuleError(Exception):
    def __init__(self, e = None):
        Exception.__init__(self)
        self.e = e
        return
    def __str__(self):
        return 'Config Error: %s' % self.e

def init(f_object):
    # split input file into numerous smaller pieces:
    utils.check_dir(f_object.dirs['parts'], clean_dir_content = True)
    f_object.files['r1_parts'] = utils.split_fasta_file(f_object.files['in_r1'], f_object.dirs['parts'], prefix = 'r1-part')
    
    if not len(f_object.files['r1_parts']):
        raise ModuleError, 'split_fasta_file returned 0 for "%s"' % f_object.files['in_r1']

def run(f_object):
    for part in f_object.files['r1_parts']:
        cmdline % {
                            'input': part,
                            'output': part + '.b6',
                            'target_db': f_object.target_db,
                            'log': part + '.log',
                            'params_from_config': None,

                        }
                

def finalize(f_object):
    pass
