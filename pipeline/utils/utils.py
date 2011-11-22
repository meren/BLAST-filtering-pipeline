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
from pipeline.utils.logger import error 
from pipeline.utils.fastalib import SequenceSource

import os
import sys
import shutil
import subprocess


class UtilsError(Exception):
    def __init__(self, e = None):
        Exception.__init__(self)
        self.e = e
        error(e)
        return
    def __str__(self):
        return 'Utils Error: %s' % self.e


def pp(n):
    """Pretty print function for very big numbers.."""
    ret = []
    n = str(n)
    for i in range(len(n) - 1, -1, -1):
        ret.append(n[i])
        if (len(n) - i) % 3 == 0:
            ret.append(',')
    ret.reverse()
    return ''.join(ret[1:]) if ret[0] == ',' else ''.join(ret)


def concatenate_files(dest_file, file_list):
    debug('concatenate; dest: %s' % dest_file)
    dest_file_obj = open(dest_file, 'w')
    for chunk_path in file_list:
        for line in open(chunk_path):
            dest_file_obj.write(line)

    return dest_file_obj.close()


def copy_file(source_file, dest_file):
    debug('copy file; dest: "%s", src: "%s"' % (source_file, dest_file))
    try:
        return shutil.copyfile(source_file, dest_file)
    except IOError, e:
        raise UtilsError, "copy failed due to the following reason: '%s' (src: %s, dst: %s)" \
                                        % (e, source_file, dest_file)

def run_command(cmdline):
       try:
           if subprocess.call(cmdline, shell = True) < 0:
               raise UtilsError, "command was terminated by signal: %d" % (-retcode)
       except OSError, e:
           raise UtilsError, "command was failed for the following reason: '%s' ('%s')" % (e, cmdline)   


def refine_b6(source_file, dest_file, params):
    # FIXME: check if source_file is a valid m8 output.
    debug('refine b6; dest: %s' % (dest_file))
    try:
        b6 = open(source_file)
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, source_file)

    try:
        output = open(dest_file, 'w')
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, dest_file)

    QUERY_ID, SUBJECT_ID, IDENTITY, ALIGNMENT_LENGTH,\
    MISMATCHES, GAPS, Q_START, Q_END, S_START,\
    S_END, E_VALUE, BIT_SCORE = range(0, 12)

    conversion = [str, str, float, int, int, int, int, int, int, int, float, float]
    CONV = lambda x, i: conversion[i](x)

    counter, previous_query_id = 0, None

    for line in (l for l in b6 if not l.startswith('#')):
        #if counter % 10000 == 0:
        #    sys.stderr.write('\rReading B6: ~ %s' % (pp(counter)))
        #    sys.stderr.flush()
        counter += 1

        s = line.split(('\t'))

        if params.has_key('unique_hits') and params['unique_hits'] and CONV(s[QUERY_ID], QUERY_ID) == previous_query_id:
            continue

        if params.has_key('min_alignment_length') and CONV(s[ALIGNMENT_LENGTH], ALIGNMENT_LENGTH) < params['min_alignment_length']:
            continue

        if params.has_key('min_identity') and CONV(s[IDENTITY], IDENTITY) < params['min_identity']:
            continue

        # At this point, this entry must be what we are looking for.
        # We shall store it.
        output.write(line)
        previous_query_id = CONV(s[QUERY_ID], QUERY_ID)

    return output.close()


def split_fasta_file(input_file_path, dest_dir, prefix = 'part', number_of_sequences_per_file = 100):
    debug('split fasta file; src: %s, dest dir: %s' % (input_file_path, dest_dir))
    
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

def print_config_summary(config):
    print('\nSummary of filters and intended input/output destinations:\n')
    info('Dataset name', config.dataset_name)
    info('Working Direcotory', config.base_work_dir)
    print('\n')
    for filter in config.filters:
        info('  Filter name', filter.name)
        info('    Module', filter.module.__name__)
        info('    Target DB', filter.target_db)
        info('    Input file', filter.files['input'])
        info('    Filter Output Direcotory', filter.dirs['output'])
        info('    Search Output', filter.files['search_output'])
        info('    Inspected Search Output', filter.files['refined_search_output'])
        info('    Filtered IDs', filter.files['hit_ids'])
        info('    Filtered Input', filter.files['filtered_reads'])
        info('    Output to the next Stage', filter.files['survived_reads'])
        print '\n'


