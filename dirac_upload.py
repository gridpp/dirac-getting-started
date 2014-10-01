#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

#...for the CERN@school dataset wrapper.
from cernatschool.dataset import Dataset

if __name__ == "__main__":

    print("")
    print("###############################################")
    print("* GridPP and DIRAC: file upload with metadata *")
    print("###############################################")
    print("")

    ## Base directory for the file uploads.
    dfc_base = "/cernatschool.org/users/t/t.whyntie/diractest/"

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

    # Loop over the frames and upload them to the DFC.
    for f in frames:
        fn = "%s_%d-%6d.txt" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create a temporary file for the frame data.
        with open(fn, "w") as of:
            for X, C in f.getPixelMap().iteritems():
                of.write("%d\t%d\t%d\n" % (X%256, X/256, C))

        ## The LFN for the file being uploaded.
        outfile = dfc_base + fn

        # Upload the file to the DFC.
        print("* Uploading: '%s'." % (outfile))

        # Create the DIRAC metadata dictionary for the frame.
        meta_dict = {
            "chipid"     : f.getChipId(),
            "starttime"  : f.getStartTime(),
            "endtime"    : f.getEndTime(),
            "n_klusters" : f.getNumberOfKlusters()
            }

        print meta_dict

        # Add the file metadata based on the frame information.

        # Delete the (temporary) file.
        os.remove(fn)
