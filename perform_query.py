#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# The DIRAC import statements.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Interfaces.API.Dirac import Dirac

#...for the DIRAC File Catalog client interface.
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

if __name__ == "__main__":

    print("")
    print("#############################################")
    print("* GridPP and DIRAC: user metadata - queries *")
    print("#############################################")
    print("")

    ## The DFC client.
    fc = FileCatalogClient()

    ## Base directory for the file uploads.
    dfc_base = "/cernatschool.org/user/t/t.whyntie/diractest003/"

    meta_dict = {\
        #"start_time" : { ">=" : 1371575426 }\
        #"lat" : { ">" : 60.0 }\
        "n_pixel" : { ">" : 700 }\
        #"n_kluster" : { ">" : 40}\
        }

    ## The query result.
    result = fc.findFilesByMetadata(meta_dict, path=dfc_base)

    print "* Metadata query:", meta_dict

    for fn in result["Value"]:
        print("Found: '%s'." % (fn))

    print
    print result
