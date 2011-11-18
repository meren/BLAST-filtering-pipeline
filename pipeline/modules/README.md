Modules
=======

This file will explain how a new module can be implemented so it can be called as a filter from the pipeline.

Here is a 'FIXME' label so I wouldn't forget to come back to this.

Sample
======

An empty module frame:

     # -*- coding: utf-8 -*-
     
     # Copyright (C) YEAR, NAME/INSTITUTE
     #
     # This program is free software; you can redistribute it and/or modify it under
     # the terms of the GNU General Public License as published by the Free
     # Software Foundation; either version 2 of the License, or (at your option)
     # any later version.
     #
     # Please read the docs/COPYING file.
     
     description = "Module description line"
     
     def init(f_object):
         """Initialize files and directories, split input file
            into smaller pieces if necessary, check binaries and
            parameters, etc."""
         pass
     
     def run(f_object):
         """Perform the actual run, implement nested funcitons
         or classes to handle intricate run-time tasks."""
         pass
     
     def finalize(f_object):
         """Based on the criteria defined in the config file,
         refine search results to finally come up with a list
         of IDs to specify which reads are not going to go to
         the next filter in the chain."""
         pass

