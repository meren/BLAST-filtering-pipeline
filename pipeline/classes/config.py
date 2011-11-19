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
import imp
from ConfigParser import ConfigParser

from pipeline.utils import utils
from pipeline.classes.filter import Filter
from pipeline.utils.logger import debug
from pipeline.utils.logger import error

class ConfigError(Exception):
    def __init__(self, e = None):
        Exception.__init__(self)
        self.e = e
        error(e)
        return
    def __str__(self):
        return 'Config Error: %s' % self.e


class ConfigParserWrapper(ConfigParser):
    """A wrapper class to ConfigParser to override 'sections' function
       in order to get secions sorted by the order they appear in config
       file."""

    def __init__(self, config_file = None):
        ConfigParser.__init__(self)
        self.config_file = config_file
    
    def sections(self):
        _sections = []
        for line in [l.strip() for l in open(self.config_file) if len(l.strip())]:
            if line[0] == '[' and line[-1] == ']':
                _sections.append(line[1:-1])
        return _sections


class Config:
    def __init__(self, args, constants):
        if args:
            self.r1 = args.r1
            self.r2 = args.r2
            self.output_dir = args.output_dir
            self.constants = constants
            self.filters = []
            self.modules = {}

            self.init_modules()
            self.init_filters_config(args.filters_config)
            self.init_chain_of_filters()
            self.init_essential_files_and_directories()

    
    def init_modules(self):
        mod_base = self.constants.dirs['modules']
        for file in os.listdir(mod_base):
            if file.startswith('mod_') and file.endswith('.py'):
                mod_name = file[4:-3]
                self.modules[mod_name] = imp.load_source(mod_name, os.path.join(mod_base, file))
                debug('module "%s" found' % mod_name)


    def init_filters_config(self, config_file_path):
        filters_config = ConfigParserWrapper(config_file_path)
        filters_config.read(config_file_path)
        for section in filters_config.sections():
            filter = Filter(section)
            filter.name = filters_config.get(section, 'filter_name')
            
            filter_module = filters_config.get(section, 'module')
            if not self.modules.has_key(filter_module):
                raise ConfigError, 'Unknown module for filter "%s": "%s".\nAvailable modules:\n%s' \
                                   % (filter.name, filter_module, ', '.join(self.modules.keys()))
            else:
                filter.module = self.modules[filter_module]

            # store command line parameters from the config file
            for option in [o for o in filters_config.options(section) if o.startswith('cmdparam.')]:
                param = '.'.join(option.split('.')[1:])
                opt = filters_config.get(section, option)
                filter.cmdparams.append('%s %s' % (param, opt))
               
            debug('command line params for filter "%s": %s ' % (filter.name, filter.cmdparams))

            # store post-search refinement filters from the config file
            for option in [o for o in filters_config.options(section) if o.startswith('rfnparam.')]:
                param = '.'.join(option.split('.')[1:])
                opt = filters_config.get(section, option)
                if param in filter.get_refinement_params():
                    filter.rfnparams.append((param, filter.module.rfnparams[param](opt)),)
                else:
                    raise ConfigError, 'Unknown refinement parameter for filter "%s": "%s"' \
                                   % (filter.name, param)
            
            debug('refinement line params for filter "%s": %s ' % (filter.name, filter.rfnparams))

            filter.dirs['root']  = self.output_dir
            filter.dirs['base']  = os.path.join(self.output_dir, filter.name)
            filter.dirs['parts'] = os.path.join(filter.dirs['base'], 'parts')
            self.filters.append(filter)

    def init_chain_of_filters(self):
        for i in range(0, len(self.filters)):
            filter = self.filters[i]
           
            # in this context WORK_DIR defines the directory that is dedicated to the 
            # filter, while OUTPUT_DIR returnes the root directory that contains
            # everything including filter directories..
            WORK_DIR   = lambda x: os.path.join(self.output_dir, filter.name, x)
            OUTPUT_DIR = lambda x: os.path.join(self.output_dir, x)
            
            if i == 0:
                # first filter. in_r1, in_r2 should be coming from the command
                # line parameters:
                filter.files['in_r1'] = self.r1
                filter.files['in_r2'] = self.r2
            else:
                # any filter that is not the first one should use the previous filter's
                # output files as input:
                filter.files['in_r1'] = self.filters[i - 1].files['filtered_r1']
                filter.files['in_r2'] = self.filters[i - 1].files['filtered_r2']
          
            filter.files['search_output'] = WORK_DIR('--'.join([os.path.basename(self.r1), filter.name + '.SEARCH-RESULTS']))
            filter.files['refined_search_output'] = WORK_DIR('--'.join([os.path.basename(self.r1), filter.name + '.SEARCH-RESULTS-REFINED']))
            filter.files['out_r1'] = WORK_DIR('--'.join([os.path.basename(self.r1), filter.name]))
            filter.files['out_r2'] = WORK_DIR('--'.join([os.path.basename(self.r2), filter.name]))
            filter.files['filtered_r1'] = OUTPUT_DIR('--'.join([filter.files['in_r1'], filter.name + '_filtered']))
            filter.files['filtered_r2'] = OUTPUT_DIR('--'.join([filter.files['in_r2'], filter.name + '_filtered']))

    def init_essential_files_and_directories(self):
        IS_RELATIVE = lambda d: not d.startswith('/')

        if len([True for item in [self.output_dir, self.r1, self.r2] if IS_RELATIVE(item)]):
            raise ConfigError, 'All paths should be absolute (starting with a "/").'

        if not os.path.exists(self.r1):
            raise ConfigError, 'Pair 1 is not where it is expected to be: "%s"' % self.r1
        
        if not os.path.exists(self.r2):
            raise ConfigError, 'Pair 2 is not where it is expected to be: "%s"' % self.r2

        utils.check_dir(self.output_dir, clean_dir_content = False)

    def init_filter_files_and_directories(self, filter):
        utils.check_dir(filter.dirs['parts'])

    def print_summary(self):
        print('\nSummary of filters and input/output destinations:\n--')
        for filter in self.filters:
            utils.info('Filter name', filter.name)
            utils.info('Module', filter.module.__name__)
            utils.info('Target DB', filter.target_db)
            utils.info('Search Output', filter.files['search_output'])
            utils.info('Inspected Search Output', filter.files['refined_search_output'])
            utils.info('R1 input', filter.files['in_r1'])
            utils.info('R2 input', filter.files['in_r2'])
            utils.info('R1 output', filter.files['out_r1'])
            utils.info('R2 output', filter.files['out_r2'])
            utils.info('Filtered R1', filter.files['filtered_r1'])
            utils.info('Filtered R2', filter.files['filtered_r2'])
            print '\n--\n'

if __name__ == '__main__':
    pass
