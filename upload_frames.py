#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

GridPP and DIRAC: uploading CERN@school test data.

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
    print("* GridPP and DIRAC: upload CERN@school data files *")
    print("###################################################")
    print("")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("jobNum",          help="User-specified job number (for ref.).")
    parser.add_argument("siteName",        help="The site name.")
    parser.add_argument("storageElement",  help="The Storage Element name.")
    parser.add_argument("gridOutputDir",   help="The name of the output directory on the DFC.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The user-specified job number.
    jobnum = int(args.jobNum)

    ## The job name.
    jobname = "CERNatschool-test_%05d" % (jobnum)

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
    lg.basicConfig(filename='log_upload_frames.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("* Job name            : '%s'" % (jobname))
    print("* Site                : '%s'" % (sitename))
    print("* Storage Element     : '%s'" % (se))
    print("* DFC output dir.     : '%s'" % (gridoutdir))

    ## The test dataset to upload.
    ds = Dataset(datapath)

    ## Latitude of the test dataset [deg.].
    lat = 51.509915

    ## Longitude of the test dataset [deg.].
    lon = -0.142515 # [deg.]

    ## Altitude of the test dataset [m].
    alt = 34.02

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt))

    ## A dictionary mapping the file names to the metadata dictionary.
    file_dict = {}

    # Loop over the frames and upload them to the DFC.
    for f in frames:

        ## The filename for the data frame, based on frame information.
        fn = "%s_%d-%06d" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create a temporary file for the frame data.
        with open(fn+".txt", "w") as of:
            for X, C in f.getPixelMap().iteritems():
                of.write("%d\t%d\t%d\n" % (X%256, X/256, C))

        # Create the DIRAC metadata dictionary for the frame.
        metadata = {
            "frameid"     : fn,
            "chipid"      : f.getChipId(),
            "hv"          : f.getBiasVoltage(),
            "ikrum"       : f.getIKrum(),
            #
            "lat"         : f.getLatitude(),
            "lon"         : f.getLongitude(),
            "alt"         : f.getAltitude(),
            #
            "start_time"  : f.getStartTimeSec(),
            "end_time"    : f.getEndTimeSec(),
            "acqtime"     : f.getAcqTime(),
            #
            "n_pixel"     : f.getNumberOfUnmaskedPixels(),
            "occ"         : f.getOccupancy(),
            "occ_pc"      : f.getOccupancyPc(),
            #
            "n_kluster"   : f.getNumberOfKlusters(),
            "n_gamma"     : f.getNumberOfGammas(),
            "n_non_gamma" : f.getNumberOfNonGammas(),
            #
            "ismc"        : int(f.isMC())
            }

        file_dict["%s.txt" % (fn)] = metadata

    # Update the user.
    print("*")
    print("* Uploading the following files:")
    for fn in file_dict.keys():
        print("*-> '%s'" % (fn))
    print("*")

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
    j.setInputSandbox(file_dict.keys())

    #...and added to the desired storage element with the corresponding
    # LFN via the job's OutputData. You may wish to change:
    # * The Storage Element - by changing the outputSE parameter;
    # * The LFN base name   - by changing the outputPath parameter.
    j.setOutputData(file_dict.keys(), \
                    outputSE='%s' % (se), \
                    outputPath='/%s/' % (gridoutdir)\
                   )

    # These are the files retrieved with the local job output.
    j.setOutputSandbox(['StdOut', 'StdErr'])

    # You can set your preferred site here.
    j.setDestination(sitename)

    ## The DIRAC instance.
    dirac = Dirac()

    # Submit the job and print the result.
    result = dirac.submit(j)
    print 'Submission result: ', result

    # Delete the (temporary) data files.
    for fn in file_dict.keys():
        os.remove(fn)

    ## The dataset name (chip ID + start time).
    dn = sorted(file_dict.keys())[0][:-4]

    # Write out the frame information to a JSON file.
    with open("%s/%s.json" % (outputpath, dn), "w") as jf:
        json.dump(file_dict.values(), jf)
