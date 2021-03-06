# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.


import gc
import os
import sys
import shutil
import inspect
import subprocess

from pipeline.utils.logger import debug
from pipeline.utils.logger import error 
from pipeline.utils.fastalib import SequenceSource
from pipeline.utils.b6lib import B6Source


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

def p_tabular(label, value, label_length = 20, file_obj = None):
    info_line = "%s %s: %s" % (label, '.' * (label_length - len(label)), str(value))
    if file_obj:
        info_file_obj.write(info_line + '\n')
    print info_line

def my_name():
    """a simple function that returns the name of the function from which it was called
       (it was written by Jerry Kindall and was copy-pasted from an online resource)"""
    frame = inspect.currentframe(1)
    code  = frame.f_code
    globs = frame.f_globals
    functype = type(lambda: 0)

    funcs = []

    for func in gc.get_referrers(code):
        if type(func) is functype:
            if getattr(func, "func_code", None) is code:
                if getattr(func, "func_globals", None) is globs:
                    funcs.append(func)
                    if len(funcs) > 1:
                        return None

    return funcs[0].__name__ if funcs else None


def concatenate_files(dest_file, file_list):
    debug('%s; dest: "%s"' % (my_name(), dest_file))
    dest_file_obj = open(dest_file, 'w')
    for chunk_path in file_list:
        for line in open(chunk_path):
            dest_file_obj.write(line)

    return dest_file_obj.close()

def split_file(ids_file, source_file, filtered_dest_file, survived_dest_file, type = 'fasta'):
    """splits reads in input file into two files based on ids_file

       for read_id in input:
           if read_id in list_of_ids:
               --> filtered_dest_file
           else:
               --> survived dest_file

       """
    debug('%s; src: "%s" (%s), filtered_dest: "%s", survived_dest: "%s"'\
        % (my_name(), source_file, type, filtered_dest_file, survived_dest_file))
    
    try:
       ids_to_filter = set([id.strip() for id in open(ids_file).readlines()])
    except IOError:
       raise FilterError, 'Hit IDs file missing ("%s").' \
               % (ids_to_filter)
  
    if type == 'fasta':
        
        STORE = lambda e, f: f.write('>%s\n%s\n' % (e.id, e.seq))

        input  = SequenceSource(source_file)
        filtered_output = open(filtered_dest_file, 'w')
        survived_output = open(survived_dest_file, 'w')
        filtered_count, survived_count = 0, 0

        while input.next():
            if input.pos % 10000 == 0 or input.pos == 1:
                sys.stderr.write('\rSplitting FASTA file: ~ %s' % (pp(input.pos)))
                sys.stderr.flush()

            if input.id in ids_to_filter:
                ids_to_filter.remove(input.id)
                STORE(input, filtered_output)
                filtered_count += 1
            else:
                STORE(input, survived_output)
                survived_count += 1
       
        sys.stderr.write('\n')
        filtered_output.close()
        survived_output.close()

        debug('%s; done. of %s total reads, filtered: %s, survived: %s.'\
                    % (my_name(), pp(filtered_count + survived_count),\
                       pp(filtered_count), pp(survived_count)))
    
    else:
        raise UtilsError, "type '%s' is not implemented" % (type)   
    
    return True


def copy_file(source_file, dest_file):
    debug('%s; dest: "%s", src: "%s"' % (my_name(), source_file, dest_file))
    try:
        return shutil.copyfile(source_file, dest_file)
    except IOError, e:
        raise UtilsError, "copy failed due to the following reason: '%s' (src: %s, dst: %s)" \
                                        % (e, source_file, dest_file)

def run_command(cmdline):
       debug('%s; cmd: %s' % (my_name(), cmdline))
       try:
           if subprocess.call(cmdline, shell = True) < 0:
               raise UtilsError, "command was terminated by signal: %d" % (-retcode)
       except OSError, e:
           raise UtilsError, "command was failed for the following reason: '%s' ('%s')" % (e, cmdline)   


def refine_b6(source_file, dest_file, params):
    # FIXME: check if source_file is a valid m8 output.
    debug('%s; dest: %s' % (my_name(), dest_file))
    try:
        b6 = B6Source(source_file)
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, source_file)

    try:
        output = open(dest_file, 'w')
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, dest_file)

    previous_query_id = None

    while b6.next():
        if b6.pos % 10000 == 0 or b6.pos == 1:
            sys.stderr.write('\rReading B6: ~ %s' % (pp(b6.pos)))
            sys.stderr.flush()

        if params.has_key('unique_hits') and params['unique_hits'] and b6.query_id == previous_query_id:
            continue

        if params.has_key('min_alignment_length') and b6.alignment_length < params['min_alignment_length']:
            continue

        if params.has_key('min_identity') and b6.identity < params['min_identity']:
            continue

        # At this point, this entry must be what we are looking for.
        # We shall store it.
        output.write(b6.entry)
        previous_query_id = b6.query_id

    sys.stderr.write('\n')
    return output.close()

def store_ids_from_b6_output(source_b6_output, dest_file):
    debug('%s; dest: %s' % (my_name(), dest_file))
    try:
        b6 = B6Source(source_b6_output)
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, source_b6_output)

    try:
        output = open(dest_file, 'w')
    except IOError, e:
        raise UtilsError, "open failed due to the following reason: '%s' (src: %s)" \
                                        % (e, dest_file)
    
    while b6.next():
       output.write(b6.query_id + '\n') 


def get_qstat_info(job_identifier):
    try:
        proc = subprocess.Popen(['qstat'], stdout=subprocess.PIPE)
    except OSError, e:
        raise UtilsError, "qstat command was failed for the following reason: '%s' ('%s')" % (e, cmdline)   
    
    qstat_state_codes = {'pending': ['qw', 'hqw', 'hRwq'],
                         'running': ['r', 't', 'Rr', 'Rt'],
                         'suspended': ['s', 'ts', 'S', 'tS', 'T', 'tT'],
                         'error': ['Eqw', 'Ehqw', 'EhRqw'],
                         'deleted': ['dr', 'dt', 'dRr', 'dRt', 'ds', 'dS', 'dT', 'dRs', 'dRS', 'dRT']}
    
    info_dict = {'pending': 0, 'running': 0, 'suspended': 0, 'error': 0, 'deleted': 0}
    line_no = 0
    
    while True:
        line = proc.stdout.readline()
   
        # skip the first two lines
        if line_no < 2:
            line_no += 1
            continue
    
        if line != '':
            id, priority, name, user, state = line.strip().split()[0:5]
            if name == job_identifier:
                found = False
                for s in qstat_state_codes:
                    if state in qstat_state_codes[s]:
                        found = True
                        info_dict[s] += 1
                if not found:
                    raise UtilsError, "unknown state for qstat: '%s' (known states: '%s')"\
                             % (state, ', '.join(info_dict.keys()))   
    
            line_no += 1
        else:
            break
    
    return info_dict


def split_fasta_file(input_file_path, dest_dir, prefix = 'part', number_of_sequences_per_file = 20000):
    debug('%s; src: %s, dest dir: %s' % (my_name(), input_file_path, dest_dir))
    
    input = SequenceSource(input_file_path)
    
    parts = []
    next_part = 1
    part_obj = None

    while input.next():
        if (input.pos - 1) % number_of_sequences_per_file == 0:
            sys.stderr.write('\rCreating part: ~ %s' % (pp(next_part)))
            sys.stderr.flush()

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

    sys.stderr.write('\n')
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
    debug('%s; removing content of "%s"' % (my_name(), dir))
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
        if len(filter.execution_order):
            info('    Special Execution order', filter.execution_order) 
        info('    Target DB', filter.target_db)
        info('    Input File', filter.files['input'])
        info('    Filter Output Direcotory', filter.dirs['output'])
        info('    Search Output', filter.files['search_output'])
        info('    Inspected Search Output', filter.files['refined_search_output'])
        info('    Filtered IDs', filter.files['hit_ids'])
        info('    Filtered Input', filter.files['filtered_reads'])
        info('    Output to the Next Stage', filter.files['survived_reads'])
        print '\n'


