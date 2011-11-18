# -*- coding: utf-8 -*-
# v.110811

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

class SequenceSource:
    def __init__(self, f_name, lazy_init = True):
        self.pos = 0
        self.id  = None
        self.seq = None
        self.file_pointer = open(f_name)
        self.file_pointer.seek(0)
        
        if lazy_init:
            self.total_seq = None
        else:
            self.total_seq = len([l for l in self.file_pointer.readlines() if l.startswith('>')])

    def next(self):
        self.id = self.file_pointer.readline()[1:].strip()
        self.seq = None

        sequence = ''
        while 1:
            line = self.file_pointer.readline()
            if not line:
                if len(sequence):
                    self.seq = sequence
                    return True
                else:
                    return False
            if line.startswith('>'):
                self.file_pointer.seek(self.file_pointer.tell() - len(line))
                break
            sequence += line.strip()

        self.seq = sequence
        self.pos += 1
        return True

    def reset(self):
        self.pos = 0
        self.id  = None
        self.seq = None
        self.file_pointer.seek(0)

