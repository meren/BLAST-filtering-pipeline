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
    parser.add_argument('-s', '--filters-config', required=True, metavar = 'STAGES_CONFIG',
                                        help = 'File in which BLAST filtering targets are defined')
    parser.add_argument('--r1', required=True, metavar = 'FASTA_FILE',
                            help = 'First pair of the input Illumina file')
    parser.add_argument('--r2', required=True, metavar = 'FASTA_FILE',
                            help = 'Second pair of the input Illumina file')
    parser.add_argument('-o', '--output_dir', required=True, metavar = 'OUTPUT_DIR',
                            help = 'Root directory for output to be stored')

    return parser

