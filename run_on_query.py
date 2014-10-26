#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# The DIRAC import statements.

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Interfaces.API.Dirac import Dirac

from DIRAC.Interfaces.API.Job import Job

#...for the DIRAC File Catalog client interface.
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

# Set this if you want to modify the job/dataset number.
jobnum = 1

if __name__ == "__main__":

    print("")
    print("#############################################")
    print("* GridPP and DIRAC: user metadata - queries *")
    print("#############################################")
    print("")

    ## The DFC client.
    fc = FileCatalogClient()

    ## Base directory for the file uploads.
    dfc_base = "/cernatschool.org/user/t/t.whyntie/diractest003/"

    meta_dict = {\
        #"start_time" : { ">=" : 1371575426 }\
        #"lat" : { ">" : 60.0 }\
        "n_pixel" : { ">" : 700 }\
        #"n_kluster" : { ">" : 40}\
        }

    ## The query result.
    result = fc.findFilesByMetadata(meta_dict, path=dfc_base)

    ## The LFNs found by the query.
    lfns = ["LFN:" + x for x in result["Value"]]

    #print lfns

    #print "* Metadata query:", meta_dict

    for fn in lfns:
        print("Found: '%s'." % (fn))

    print
    #print result

    # Setup the job.

    ## The DIRAC job to submit.
    j = Job(stdout='StdOut', stderr='StdErr')

    # Set the name of the job (viewable in the web portal).
    j.setName("CERNatschool_test_%03d" % (jobnum))

    # As we're just copying the input sandbox to the storage element
    # via OutputData, we'll just list the files as a check for the
    # output written to StdOut.
    j.setExecutable('/bin/ls -l')

    # Here we add the list of LFNs we have obtained from the metadata
    # query.
    j.setInputSandbox(lfns)

    #...and added to the desried storage element with the corresponding
    # LFN via the job's OutputData. You may wish to change:
    # * The Storage Element - by changing the outputSE parameter;
    # * The LFN base name   - by changing the outputPath parameter.
    #j.setOutputData(file_dict.keys(), \
    #                outputSE='GLASGOW-disk', \
    #                outputPath='/diractest%03d/' % (jobnum)\
    #               )

    # These are the files retrieved with the local job output.
    j.setOutputSandbox(['StdOut', 'StdErr'])

    # You can set your preferred site here.
    #j.setDestination('LCG.Liverpool.uk')
    #j.setDestination('LCG.Glasgow.uk')
    j.setDestination('LCG.UKI-LT2-QMUL.uk')

    ## The DIRAC instance.
    dirac = Dirac()

    # Submit the job and print the result.
    #result = dirac.submit(j)
    print
    print 'Submission result: ', result
    print
