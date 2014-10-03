#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# The DIRAC imports.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Interfaces.API.Dirac import Dirac

from DIRAC.Interfaces.API.Job import Job

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

#...for the CERN@school dataset wrapper.
from cernatschool.dataset import Dataset

# Set this if you want to modify the job/dataset number.
jobnum = 1

if __name__ == "__main__":

    print("")
    print("#################################################")
    print("* GridPP and DIRAC: user metadata - file upload *")
    print("#################################################")
    print("")


    ## The test dataset to upload.
    ds = Dataset("testdata/ASCIIxyC")

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
        fn = "%s_%d-%6d.txt" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create a temporary file for the frame data.
        with open(fn, "w") as of:
            for X, C in f.getPixelMap().iteritems():
                of.write("%d\t%d\t%d\n" % (X%256, X/256, C))

        # Create the DIRAC metadata dictionary for the frame.
        metadata = {
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
            "ismc"        : int(g.isMC())
            }

        file_dict[fn] = metadata

        # Add the file metadata based on the frame information.


    # Update the user.
    print("* Uploading the following files:")
    for fn in file_dict.keys():
        print("*-> '%s'" % (fn))

    ## The DIRAC job to submit.
    j = Job(stdout='StdOut', stderr='StdErr')

    # Set the name of the job (viewable in the web portal).
    j.setName("CERNatschool_test_%03d" % (jobnum))

    # As we're just copying the input sandbox to the storage element
    # via OutputData, we'll just list the files as a check for the
    # output written to StdOut.
    j.setExecutable('/bin/ls -l')

    # Here we add the names of the temporary copies of the frame data
    # files in the dataset to the input sandbox. These will be uploaded
    # to the grid with the job...
    j.setInputSandbox(file_dict.keys())

    #...and added to the desried storage element with the corresponding
    # LFN via the job's OutputData. You may wish to change:
    # * The Storage Element - by changing the outputSE parameter;
    # * The LFN base name   - by changing the outputPath parameter.
    j.setOutputData(file_dict.keys(), \
                    outputSE='GLASGOW-disk', \
                    outputPath='/diractest%03d/' % (jobnum)\
                   )

    # These are the files retrieved with the local job output.
    j.setOutputSandbox(['StdOut', 'StdErr'])

    # You can set your preferred site here.
    j.setDestination('LCG.Glasgow.uk')

    ## The DIRAC instance.
    dirac = Dirac()

    # Submit the job and print the result.
    result = dirac.submit(j)
    print 'Submission result: ', result

    # Delete the (temporary) data files.
    for fn in file_dict.keys():
        os.remove(fn)
