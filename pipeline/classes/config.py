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
            self.args = args
            self.constants = constants
            self.base_work_dir = self.args.base_work_dir
            self.dataset_name  = self.args.dataset_name
            self.input = self.args.input
            
            self.dataset_root_dir = os.path.join(self.base_work_dir, self.dataset_name)
            self.filters = []
            self.modules = {}

            self.init_modules()
            self.init_essential_files_and_directories()
            self.init_filters_config(args.filters_config)
            self.init_chain_of_filters()
            debug('Config class is initialized with %d modules and %d filters'\
                                % (len(self.modules), len(self.filters)))

    
    def init_modules(self):
        mod_base = self.constants.dirs['modules']
        for file in os.listdir(mod_base):
            if file.startswith('mod_') and file.endswith('.py'):
                mod_name = file[4:-3]
                self.modules[mod_name] = imp.load_source(mod_name, os.path.join(mod_base, file))
                debug('module "%s" found' % mod_name)


    def init_essential_files_and_directories(self):
        IS_RELATIVE = lambda d: not d.startswith('/')

        if len([True for item in [self.base_work_dir, self.input] if IS_RELATIVE(item)]):
            raise ConfigError, 'All paths should be absolute (starting with a "/").'

        if not os.path.exists(self.input):
            raise ConfigError, 'Input file is not where it is expected to be: "%s"' % self.input
        
        utils.check_dir(self.base_work_dir, clean_dir_content = False)
        utils.check_dir(self.dataset_root_dir, clean_dir_content = False)


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
                    filter.rfnparams[param] = filter.module.allowed_rfnparams[param](opt)
                else:
                    raise ConfigError, 'Unknown refinement parameter for filter "%s": "%s"' \
                                   % (filter.name, param)
            
            debug('refinement line params for filter "%s": %s ' % (filter.name, filter.rfnparams))
            
            
            # take care of file paths and directories
            J = lambda x: os.path.join(filter.dirs['output'], x)
            
            filter.dirs['output']  = os.path.join(self.dataset_root_dir, filter.name)
            filter.dirs['parts'] = J('parts')
            filter.files['search_output'] = J('01_raw_hits.txt')
            filter.files['refined_search_output'] = J('02_refined_hits.txt')
            filter.files['hit_ids'] = J('03_hits.ids')
            filter.files['filtered_reads'] = J('04_filtered.fa')
            filter.files['survived_reads'] = J('05_survived.fa') 

            self.filters.append(filter)

    def init_chain_of_filters(self):
        for i in range(0, len(self.filters)):
            filter = self.filters[i]

            if i == 0:
                # first filter. input should be coming from the command
                # line parameters:
                filter.files['input'] = self.input
            else:
                # any filter that is not the first one should use the previous filter's
                # output files as input:
                filter.files['input'] = self.filters[i - 1].files['filtered_reads']
          

    def init_filter_files_and_directories(self, filter):
        utils.check_dir(filter.dirs['parts'])

if __name__ == '__main__':
    pass
