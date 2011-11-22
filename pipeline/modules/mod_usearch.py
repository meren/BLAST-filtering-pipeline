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

searchcmd = "usearch -query %(input)s -blast6out %(output)s -wdb %(target)s %(cmdparams)s &> %(log)s"

allowed_rfnparams = {'min_alignment_length': int, 
                     'min_identity': float,
                     'unique_hits': int}


from pipeline.utils import utils
from pipeline.utils.logger import debug
from pipeline.utils.logger import error

class ModuleError(Exception):
    def __init__(self, e = None):
        Exception.__init__(self)
        self.e = e
        error(e)
        return
    def __str__(self):
        return 'Module Error: %s' % self.e

def clean(m):
    utils.check_dir(m.dirs['parts'], clean_dir_content = True)

def init(m):
    m.files['parts'] = utils.split_fasta_file(m.files['input'], m.dirs['parts'], prefix = 'part')

def run(m):
    parts = m.files['parts']
    for part in parts:
        params = {'input': part, 'output': part + '.b6', 'target': m.target_db, 
                  'log': part + '.log', 'cmdparams': ' '.join(m.cmdparams)}
        debug('running part %d/%d (log: %s)' % (parts.index(part) + 1, len(parts), params['log']))
        cmdline = searchcmd % params
        utils.run_command(cmdline)
    
    dest_file = m.files['search_output']
    utils.concatenate_files(dest_file, [part + '.b6' for part in m.files['parts']])

def refine(m):
    utils.refine_b6(m.files['search_output'], m.files['refined_search_output'], m.rfnparams)
    
def finalize(m):
    utils.store_ids_from_b6_output(m.files['refined_search_output'], m.files['hit_ids'])
