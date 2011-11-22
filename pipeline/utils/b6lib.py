# -*- coding: utf-8 -*-
# v.112211

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

class B6Source:
    def __init__(self, f_name, lazy_init = True):
        self.init()
        
        self.file_pointer = open(f_name)
        self.file_pointer.seek(0)
        
        self.conversion = [str, str, float, int, int, int, int, int, int, int, float, float]
        
        if lazy_init:
            self.total_seq = None
        else:
            self.total_seq = len([l for l in self.file_pointer.readlines() if not l.startswith('#')])

    def init(self):
        self.pos = 0
        self.entry = None

        #b6 columns..
        self.query_id = None
        self.subject_id = None
        self.identity = None
        self.alignment_length = None
        self.mismatches = None
        self.gaps = None
        self.q_start = None
        self.q_end = None
        self.s_start = None
        self.s_end = None
        self.e_value = None
        self.bit_score = None

    def next(self):
        while 1:
            self.entry = self.file_pointer.readline()
            
            if self.entry == '':
                return False

            self.entry = self.entry.strip()
            
            if not (self.entry.startswith('#') or len(self.entry) == 0):
                break
       
        self.query_id, self.subject_id, self.identity, self.alignment_length,\
        self.mismatches, self.gaps, self.q_start, self.q_end, self.s_start,\
        self.s_end, self.e_value, self.bit_score =\
            [self.conversion[x](self.entry.split('\t')[x]) for x in range(0, 12)]

        self.pos   += 1
        self.entry += '\n'
        
        return True

    def reset(self):
        self.init()
        self.file_pointer.seek(0)
