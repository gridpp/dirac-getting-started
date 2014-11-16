#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

GridPP and DIRAC: adding CERN@school cluster metadata.

"""

import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

# Import the JSON library.
import json

# The DIRAC imports.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

if __name__ == "__main__":

    print("")
    print("*###############################=########*")
    print("* GridPP and DIRAC: add cluster metadata *")
    print("*########################################*")
    print("")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the cluster dataset's JSON.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("dfcBaseDir",      help="The name of the base directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the cluster JSON file.
    datapath = args.inputPath

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The target directory on the DFC.
    dfcbasedir = args.dfcBaseDir

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_add_cluster_metadata.log', filemode='w', level=level)

    print("*")
    print("* Input JSON          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("* DFC base dir.       : '%s'" % (dfcbasedir))
    print("*")

    ## The frame properties JSON file - FIXME: check it exists...
    kf = open(datapath, "r")
    #
    kd = json.load(kf)
    kf.close()

    ## The File Catalog client object.
    fc = FileCatalogClient()

    # Loop over the clusters and upload the metadata to the DFC.
    for k in kd:

        ## The cluster file name.
        fn = k["id"] + ".png"

        print("* Found           : '%s'" % (fn))

        ## The full LFN for the datafile.
        lfn = dfcbasedir + "/" + fn

        print("*--> Adding to    : '%s'" % (lfn))

        metadataresult = fc.setMetadata(lfn, k)
        #print("*--> '%s'" % (lfn))
        print metadataresult
