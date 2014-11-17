#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

GridPP and DIRAC: adding CERN@school frame metadata.

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

#...for the CERN@school dataset wrapper.
from cernatschool.dataset import Dataset

if __name__ == "__main__":

    print("")
    print("########################################")
    print("* GridPP and DIRAC: add frame metadata *")
    print("########################################")
    print("")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonPath",        help="Path to the input dataset's JSON.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("gridOutputDir",   help="The name of the output directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the metadata JSON file.
    datapath = args.jsonPath

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The output directory on the DFC.
    gridoutdir = args.gridOutputDir

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_add_frame_metadata.log', filemode='w', level=level)

    print("*")
    print("* Input JSON          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("* DFC output dir.     : '%s'" % (gridoutdir))
    print("*")

    ## The frame properties JSON file - FIXME: check it exists...
    ff = open(datapath, "r")
    #
    fd = json.load(ff)
    ff.close()

    ## The File Catalog client object.
    fc = FileCatalogClient()

    # Loop over the frames and upload them to the DFC.
    for f in fd:

        ## The file name.
        fn = f["frameid"] + ".txt"

        print("* Found           : '%s'" % (fn))

        ## The full LFN for the datafile.
        lfn = gridoutdir + "/" + fn

        metadataresult = fc.setMetadata(lfn, f)
        print("*--> '%s'" % (lfn))
        print metadataresult
