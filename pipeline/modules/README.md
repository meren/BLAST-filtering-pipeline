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
    
     def clean(m):
        """Clean directory module work directory content"""
        pass

     def init(m):
         """Initialize files and directories"""
         pass
     
     def run(m):
         """Run time task"""
         pass
    
     def refine(m):
         """Refine search output"""
         pass

     def finalize(f_object):
         """Generate the list of IDs that will not go to the next filter"""
         pass

