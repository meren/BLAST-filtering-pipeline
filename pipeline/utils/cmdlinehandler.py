# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.


import argparse

def get_parser_obj():
    parser = argparse.ArgumentParser(description='Metagenomics BLAST Filtering Pipeline')
    parser.add_argument('-s', '--filters-config', required=True, metavar = 'CONFIG FILE PATH',
                                        help = 'File in which BLAST filtering targets are defined')
    parser.add_argument('-i', '--input', required=True, metavar = 'FILE PATH',
                            help = 'Input file in FASTA format')
    parser.add_argument('-o', '--base-work-dir', required=True, metavar = 'DIRECTORY',
                            help = 'Base working directory (in which new directories for datasets\
                                    will be created to store output files)')
    parser.add_argument('-d', '--dataset-name', required=True, metavar = 'NAME',
                            help = 'Dataset name for file and directory names')

    return parser

