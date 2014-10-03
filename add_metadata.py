#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# The DIRAC imports.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

#...for the CERN@school dataset wrapper.
from cernatschool.dataset import Dataset

# Set this if you want to modify the job/dataset number.
jobnum = 1

if __name__ == "__main__":

    print("")
    print("#################################################")
    print("* GridPP and DIRAC: user metadata - add metadata *")
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

    ## The File Catalog client object.
    fc = FileCatalogClient()

    ## Base directory for the LFNs.
    lfn_base = "/cernatschool.org/user/t/t.whyntie/diractest%03d/" % (jobnum)

    # Loop over the filenames and add the metadata.
    for fn, metadata in file_dict.iteritems():

        ## The full LFN for the datafile.
        lfn = lfn_base + fn

        metadataresult = fc.setMetadata(lfn, metadata)
        print("*--> '%s'" % (lfn))
        print metadataresult
