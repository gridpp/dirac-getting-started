#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

DIRAC and GridPP: perform a query on the CERN@school frames.

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
    lg.basicConfig(filename='log_perform_frame_query.log', filemode='w', level=level)

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
        "start_time" : { ">=" : int(qd[0]["start_time"]) },
        "end_time"   : { "<=" : int(qd[0]["end_time"  ]) }
#        #"lat" : { ">" : 60.0 }\
#        #"n_pixel" : { ">" : 700 }\
#        #"n_kluster" : { ">" : 40}\
        }

    ## The query result.
    result = fc.findFilesByMetadata(meta_dict, path=dfc_base)

    print("*")
    print "* Metadata query:", meta_dict
    print("*")
    print("* Number of frames found     : %d" % (len(result["Value"])))
    print("*")

    # Get the cluster file names from the metadata query.

#    ## Kluster file names.
#    kluster_file_names = []

    for fn in sorted(result["Value"]):
        #print("* Found: '%s'." % (fn))
        filemetadata = fc.getFileUserMetadata(fn)
        frameid = str(filemetadata['Value']['frameid'])
        n_kluster = int(filemetadata['Value']['n_kluster'])
        print("*--> Frame ID           : '%s'" % (frameid))
        print("*--> Number of clusters = %d" % (n_kluster))
        #print("*")
#        for i in range(n_kluster):
#            kn = "%s_k%05d.png" % (frameid, i)
#            kluster_file_names.append(kn)
#    print("*")
#
#    #lg.info(" * Clusters to be downloaded:")
#    #for kn in kluster_names:
#    #    lg.info(" *--> '%s'" % (kn))
#
#    print("* Number of clusters found   : %d" % (len(kluster_file_names)))
