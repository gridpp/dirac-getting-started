#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the Pixelman dataset wrapper.
from dataset import Dataset

class FrameTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_asciixyc_frame(self):

        self.assertEqual(1, 1)

        ## The dataset wrapper.
        ds = Dataset("testdata/ASCIIxyC")

        ## The frames from the dataset.
        frames = ds.getFrames((51.509915, -0.142515, 34.02))

        # The tests
        #-----------
        #
        # The number of frames.
        self.assertEqual(len(frames), 5)
        #
        # Spatial information.
        self.assertEqual(frames[0].getLatitude(), 51.509915)
        self.assertEqual(frames[0].getLongitude(), -0.142515)
        self.assertEqual(frames[0].getAltitude(), 34.02)
        #
        self.assertEqual(frames[0].getRoll(), 0.0)
        self.assertEqual(frames[0].getPitch(), 0.0)
        self.assertEqual(frames[0].getYaw(), 0.0)
        #
        self.assertEqual(frames[0].getOmegax(), 0.0)
        self.assertEqual(frames[0].getOmegay(), 0.0)
        self.assertEqual(frames[0].getOmegaz(), 0.0)
        #
        # Temporal information.
        self.assertEqual(frames[0].getStartTime(), 1371575424.293207)
        self.assertEqual(frames[0].getStartTimeSec(), 1371575424)
        self.assertEqual(frames[0].getStartTimeSubSec(), 293207)
        self.assertEqual(frames[0].getEndTime(), 1371575425.293207)
        self.assertEqual(frames[0].getEndTimeSec(), 1371575425)
        self.assertEqual(frames[0].getEndTimeSubSec(), 293207)
        self.assertEqual(frames[0].getAcqTime(), 1.0)
        #
        # Detector information.
        self.assertEqual(frames[0].getChipId(), "B06-W0212")
        #
        self.assertEqual(frames[0].getBiasVoltage(), 18.0)
        self.assertEqual(frames[0].getIKrum(), 1)
        #
        self.assertEqual(frames[0].getDetx(), 0.0)
        self.assertEqual(frames[0].getDety(), 0.0)
        self.assertEqual(frames[0].getDetz(), 0.0)
        self.assertEqual(frames[0].getDetEulera(), 0.0)
        self.assertEqual(frames[0].getDetEulerb(), 0.0)
        self.assertEqual(frames[0].getDetEulerc(), 0.0)
        #
        # Payload information.
        self.assertEqual(frames[0].getWidth(), 256)
        self.assertEqual(frames[0].getHeight(), 256)
        self.assertEqual(frames[0].getFormat(), 4114)
        self.assertEqual(frames[0].getRawNumberOfPixels(), 735)
        self.assertEqual(frames[0].getOccupancy(), 735)
        self.assertAlmostEqual(frames[0].getOccupancyPc(), 0.011215, places=6)
        self.assertEqual(frames[0].getNumberOfUnmaskedPixels(), 735)
        self.assertEqual(frames[0].getNumberOfMaskedPixels(), 0)
        #
        self.assertEqual(frames[0].isMC(), False)
        #
        # Cluster information.
        self.assertEqual(frames[0].getNumberOfKlusters(), 34)
        self.assertEqual(frames[0].getNumberOfGammas(), 12)
        self.assertEqual(frames[0].getNumberOfMonopixels(), 4)
        self.assertEqual(frames[0].getNumberOfBipixels(), 2)
        self.assertEqual(frames[0].getNumberOfTripixelGammas(), 4)
        self.assertEqual(frames[0].getNumberOfTetrapixelGammas(), 2)
        self.assertEqual(frames[0].getNumberOfNonGammas(), 22)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_frame.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("===============================================")
    lg.info(" Logger output from cernatschool/test_frame.py ")
    lg.info("===============================================")
    lg.info("")

    unittest.main()
