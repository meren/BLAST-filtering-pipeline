# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

from pipeline.utils.logger import debug
from pipeline.utils.fastalib import SequenceSource

import os
import sys

def split_fasta_file(input_file_path, dest_dir, prefix = 'part', number_of_sequences_per_file = 100):
    debug('split file: %s' % input_file_path)
    debug('into dest dir: %s' % dest_dir)
    
    input = SequenceSource(input_file_path)
    
    parts = []
    next_part = 1
    part_obj = None

    while input.next():
        if (input.pos - 1) % number_of_sequences_per_file == 0:
            if part_obj:
                part_obj.close()
            file_path = os.path.join(dest_dir, prefix + '-%08d' % next_part)
            parts.append(file_path)
            next_part += 1
            part_obj = open(file_path, 'w')

        part_obj.write('>%s\n' % input.id)
        part_obj.write('%s\n' % input.seq)
  
    if part_obj:
        part_obj.close()

    return parts
        

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
    debug('removing content of "%s"' % dir)
    for f in os.listdir(dir):
        os.unlink(os.path.join(dir, f))

def info(label, value, mlen = 30, file_obj = None):
    info_line = "%s %s: %s" % (label, '.' * (mlen - len(label)), str(value))
    if file_obj:
        info_file_obj.write(info_line + '\n')
    print info_line
