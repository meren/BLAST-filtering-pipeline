# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.

import pipeline.modules.usearch as usearch
import pipeline.modules.blast   as blast

modules_dict = {'usearch'    : usearch,
                'blast'      : blast}

def available_modules():
    return '\n'.join([' - "%s" (%s)' % (m, modules_dict[m].description) for m in modules_dict])

if __name__ == '__main__':
    print 'Available modules:'
    print available_modules()
