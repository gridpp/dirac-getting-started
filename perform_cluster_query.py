#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

DIRAC and GridPP: perform a query on the CERN@school clusters.

"""

#...for the operating system stuff.
import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

# Import the JSON library.
import json

# The DIRAC import statements.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Interfaces.API.Dirac import Dirac

#...for the DIRAC File Catalog client interface.
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

if __name__ == "__main__":

    print("")
    print("########################################################")
    print("* GridPP and DIRAC: CERN@school frame metadata queries *")
    print("########################################################")
    print("")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("queryJson",       help="Path to the query JSON.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("dfcBaseDir",      help="The name of the base directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.queryJson

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## Base directory for the file uploads.
    dfc_base = args.dfcBaseDir

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_perform_cluster_query.log', filemode='w', level=level)

    print("*")
    print("* Input JSON          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("* DFC base directory  : '%s'" % (dfc_base))

    ## The DFC client.
    fc = FileCatalogClient()

    ## The frame query JSON file - FIXME: check it exists...
    qf = open(datapath, "r")
    #
    qd = json.load(qf)
    qf.close()

    meta_dict = {\
        "size" : { ">=" : int(qd[0]["size_min"]) },
        }

    ## The query result.
    result = fc.findFilesByMetadata(meta_dict, path=dfc_base)

    print("*")
    print "* Metadata query:", meta_dict
    print("*")

    #print result
    print("* Number of clusters found      : %d" % len(result["Value"]))
