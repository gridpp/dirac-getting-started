#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

GridPP and DIRAC: processing CERN@school test data on the grid.

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

if __name__ == "__main__":

    print("")
    print("*##############################################################*")
    print("* GridPP and DIRAC: process CERN@school data files on the grid *")
    print("*##############################################################*")
    print("*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("queryJsonPath",   help="Path to the frame query JSON file.")
    parser.add_argument("dfcQueryDir",     help="The name of the query directory on the DFC.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("jobNum",          help="User-specified job number (for ref.).")
    parser.add_argument("siteName",        help="The site name.")
    parser.add_argument("storageElement",  help="The Storage Element name.")
    parser.add_argument("gridOutputDir",   help="The name of the output directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the frame query JSON file.
    datapath = args.queryJsonPath

    ## The path to query on the DFC.
    dfc_query_path = args.dfcQueryDir

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The user-specified job number.
    jobnum = int(args.jobNum)

    ## The job name.
    jobname = "CERNatschool-process-test_%05d" % (jobnum)

    ## The site name.
    sitename = args.siteName
    #
    if sitename not in UK_GRID_SITES:
        raise IOError("* ERROR: invalid grid site.")

    ## The Storage Element name.
    se = args.storageElement
    #
    if se not in UK_STORAGE_ELEMENTS:
        raise IOError("* ERROR: invalid Storage Element name.")

    ## The output directory on the DFC.
    gridoutdir = args.gridOutputDir

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_process_frames.log', filemode='w', level=level)

    print("*")
    print("* Query JSON path     : '%s'" % (datapath))
    print("* DFC query path      : '%s'" % (dfc_query_path))
    print("* Output path         : '%s'" % (outputpath))
    print("* Job name            : '%s'" % (jobname))
    print("* Site                : '%s'" % (sitename))
    print("* Storage Element     : '%s'" % (se))
    print("* DFC output dir.     : '%s'" % (gridoutdir))
    print("*")

    # Get the frames from the DIRAC DFC metadata query.

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
    result = fc.findFilesByMetadata(meta_dict, path=dfc_query_path)

    print("*")
    print "* Metadata query:", meta_dict
    print("*")

    ## The frames retrieved from the metadata query.
    retrieved_frames = ['LFN:%s' % fn for fn in sorted(result["Value"])]
    #
    if len(retrieved_frames) == 0:
        raise IOError("* ERROR: no frames found. Quitting.")

    # Get the expected cluster file names from metadata interface.

    ## Kluster file names.
    kluster_file_names = []

    for fn in retrieved_frames:
        #print("* Frame: '%s'." % (fn))
        # Ah - LFN: needs to be removed from the start...
        filemetadata = fc.getFileUserMetadata(fn[4:])
        #print filemetadata
        frameid = str(filemetadata['Value']['frameid'])
        n_kluster = int(filemetadata['Value']['n_kluster'])
        #print("*--> Frame ID           : '%s'" % (frameid))
        #print("*--> Number of clusters = %d" % (n_kluster))
        #print("*")
        for i in range(n_kluster):
            kn = "%s_k%05d.png" % (frameid, i)
            kluster_file_names.append(kn)
    print("*")

    #lg.info(" * Clusters to be downloaded:")
    #for kn in kluster_file_names:
    #    lg.info(" *--> '%s'" % (kn))

    ## The input sandbox files.
    inputfiles = ['run.sh']

    # Update the user with the frames found.
    for fn in retrieved_frames:
        #print("* Found: '%s'." % (fn))
        inputfiles.append(fn)
    print("*")

    ## The DIRAC job to submit.
    j = Job(stdout='StdOut', stderr='StdErr')

    # Set the name of the job (viewable in the web portal).
    j.setName(jobname)

    #
    j.setExecutable('/bin/sh', arguments='%s %s %s' % ('run.sh', '/cvmfs/cernatschool.gridpp.ac.uk/grid-klustering-001-00-07/', 'process-frames.py'))

    #
    j.setInputSandbox(inputfiles)

    #...and added to the desired storage element with the corresponding
    # LFN via the job's OutputData. You may wish to change:
    # * The Storage Element - by changing the outputSE parameter;
    # * The LFN base name   - by changing the outputPath parameter.
    j.setOutputData(kluster_file_names, \
                    outputSE='%s' % (se), \
                    outputPath='/%s/' % (gridoutdir)\
                   )

    # These are the files retrieved with the local job output.
    j.setOutputSandbox(['StdOut', 'StdErr', 'klusters.json', 'log_process_frames.log'])

    # You can set your preferred site here.
    j.setDestination(sitename)

    ## The DIRAC instance.
    dirac = Dirac()

#    # Submit the job and print the result.
#    result = dirac.submit(j)
#    print 'Submission result: ', result
