#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

GridPP and DIRAC: get the CERN@school cluster data.

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

from DIRAC.Interfaces.API.Dirac import Dirac

from DIRAC.Interfaces.API.Job import Job

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

#...for the grid site information.
from gridcfg.gridvals import *

#...for the CERN@school dataset wrapper.
from cernatschool.dataset import Dataset

if __name__ == "__main__":

    print("")
    print("###################################################")
    print("* GridPP and DIRAC: get CERN@school cluster files *")
    print("###################################################")
    print("")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonPath",        help="Path to the cluster query JSON.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("jobNum",          help="User-specified job number (for ref.).")
    parser.add_argument("siteName",        help="The site name.")
    parser.add_argument("dfcBaseDir",      help="The name of the base directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    jsonpath = args.jsonPath

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The user-specified job number.
    jobnum = int(args.jobNum)

    ## The job name.
    jobname = "CERNatschool-get-clusters_%05d" % (jobnum)

    ## The site name.
    sitename = args.siteName
    #
    if sitename not in UK_GRID_SITES:
        raise IOError("* ERROR: invalid grid site.")

    ## Base directory for the file uploads.
    dfc_base = args.dfcBaseDir

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_get_clusters.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (jsonpath))
    print("* Output path         : '%s'" % (outputpath))
    print("* Job name            : '%s'" % (jobname))
    print("* Site                : '%s'" % (sitename))
    print("*")

    ## The DFC client.
    fc = FileCatalogClient()

    ## The frame query JSON file - FIXME: check it exists...
    qf = open(jsonpath, "r")
    #
    qd = json.load(qf)
    qf.close()

    ## The metadata search (more fields can be added).
    meta_dict = {\
        "size" : { ">=" : int(qd[0]["size_min"]) },
        }

    ## The query result.
    result = fc.findFilesByMetadata(meta_dict, path=dfc_base)

    print("*")
    print "* Metadata query:", meta_dict
    print("*")

    ## The frames retrieved from the metadata query.
    retrieved_clusters = ['LFN:%s' % fn for fn in sorted(result["Value"])]
    #
    if len(retrieved_clusters) == 0:
        raise IOError("* ERROR: no frames found. Quitting.")

    #print retrieved_clusters

    ## The files to retrieve.
    outputfiles = []

    for fn in retrieved_clusters:
        print("*--> Retrieving: '%s'" % (os.path.basename(fn)))
        outputfiles.append(os.path.basename(fn))

    outputfiles.append("StdOut")
    outputfiles.append("StdErr")

    ## The DIRAC job to submit.
    j = Job(stdout='StdOut', stderr='StdErr')

    # Set the name of the job (viewable in the web portal).
    j.setName(jobname)

    # As we're just copying the input sandbox to the storage element
    # via OutputData, we'll just list the files as a check for the
    # output written to StdOut.
    j.setExecutable('/bin/ls -l')

    # Here we add the names of the temporary copies of the frame data
    # files in the dataset to the input sandbox. These will be uploaded
    # to the grid with the job...
    j.setInputSandbox(retrieved_clusters)

    # These are the files retrieved with the local job output.
    j.setOutputSandbox(outputfiles)

    # You can set your preferred site here.
    j.setDestination(sitename)

    ## The DIRAC instance.
    dirac = Dirac()

#    # Submit the job and print the result.
#    result = dirac.submit(j)
#    print 'Submission result: ', result
