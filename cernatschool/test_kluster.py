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

#...for the klusters.
from kluster import KlusterFinder

class KlusterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_asciixyc_frame(self):

        self.assertEqual(1, 1)

        ## The dataset wrapper.
        ds = Dataset("testdata/ASCIIxyC")

        ## The frames from the test dataset.
        frames = ds.getFrames((51.509915, -0.142515, 34.02))

        # The tests
        #-----------
        ## The cluster finder from the first frame.
        kf = KlusterFinder(frames[0].getPixelMap(), frames[0].getWidth(), frames[0].getHeight(), frames[0].isMC())

        # The number of clusters in the first frame.
        #
        # This frame has 34 clusters.
        self.assertEqual(kf.getNumberOfKlusters(), 34)
        self.assertEqual(kf.getNumberOfGammas(), 12)
        self.assertEqual(kf.getNumberOfMonopixels(), 4)
        self.assertEqual(kf.getNumberOfBipixels(), 2)
        self.assertEqual(kf.getNumberOfTripixelGammas(), 4)
        self.assertEqual(kf.getNumberOfTetrapixelGammas(), 2)

        ## The list of clusters.
        ks = kf.getListOfKlusters()

        # Double check the number of clusters found.
        self.assertEqual(len(ks), 34)

        # The first - and largest - cluster.

        # Cluster size (number of pixels).
        self.assertEqual(ks[0].getNumberOfPixels(), 104)

        # Cluster location (raw pixels).
        self.assertEqual(ks[0].getXMin(), 141)
        self.assertEqual(ks[0].getXMax(), 153)
        self.assertEqual(ks[0].getYMin(), 230)
        self.assertEqual(ks[0].getYMax(), 244)

        # Cluster width and height.
        self.assertEqual(ks[0].getWidth(), 13)
        self.assertEqual(ks[0].getHeight(), 15)

        # Cluster properties based on the unweighted (UW) mean.

        # * Location.
        self.assertAlmostEqual(ks[0].getXUW(), 146.673077, places=6)
        self.assertAlmostEqual(ks[0].getYUW(), 237.375000, places=6)

        # * Radius and density.
        self.assertAlmostEqual(ks[0].getRadiusUW(), 8.550607, places=6)
        self.assertAlmostEqual(ks[0].getDensityUW(), 0.452782, places=6)

        # Counts.
        self.assertEqual(ks[0].getTotalCounts(), 8854)
        self.assertEqual(ks[0].getMaxCountValue(), 577)

        # Energy.
        self.assertAlmostEqual(ks[0].getTotalEnergy(), 0.0, places=6)
        self.assertAlmostEqual(ks[0].getMaxEnergy(), 0.0, places=6)

        # Linearity.
        m, c, sumR = ks[0].getLineOfBestFitValues()
        self.assertAlmostEqual(m, -0.827317, places=6)
        self.assertAlmostEqual(c, 358.720154, places=6)
        self.assertAlmostEqual(sumR, 211.088562, places=6)

        # Edge pixels.
        self.assertEqual(ks[0].getNumberOfEdgePixels(), 57)
        self.assertAlmostEqual(ks[0].getInnerPixelFraction(), 0.451923, places=6)
        self.assertAlmostEqual(ks[0].getOuterPixelFraction(), 0.548077, places=6)

        # Is it a Monte Carlo cluster?
        self.assertEqual(ks[0].isMC(), False)

        # Is it an edge cluster?
        self.assertEqual(ks[0].isEdgeCluster(), False)


        # A mid-range cluster.

        # Cluster size (number of pixels).
        self.assertEqual(ks[10].getNumberOfPixels(), 19)

        # Cluster location (raw pixels).
        self.assertEqual(ks[10].getXMin(), 167.0)
        self.assertEqual(ks[10].getXMax(), 173.0)
        self.assertEqual(ks[10].getYMin(), 196.0)
        self.assertEqual(ks[10].getYMax(), 201.0)

        # Cluster width and height.
        self.assertEqual(ks[10].getWidth(), 7.0)
        self.assertEqual(ks[10].getHeight(), 6.0)

        # Cluster properties based on the unweighted (UW) mean.

        # * Location.
        self.assertAlmostEqual(ks[10].getXUW(), 170.315789, places=6)
        self.assertAlmostEqual(ks[10].getYUW(), 198.526316, places=6)

        # * Radius and density.
        self.assertAlmostEqual(ks[10].getRadiusUW(), 3.357301, places=6)
        self.assertAlmostEqual(ks[10].getDensityUW(), 0.536566, places=6)

        # Counts.
        self.assertEqual(ks[10].getTotalCounts(), 612)
        self.assertEqual(ks[10].getMaxCountValue(), 69)

        # Energy.
        self.assertAlmostEqual(ks[10].getTotalEnergy(), 0.0, places=6)
        self.assertAlmostEqual(ks[10].getMaxEnergy(), 0.0, places=6)

        # Linearity.
        m, c, sumR = ks[10].getLineOfBestFitValues()
        self.assertAlmostEqual(m, 0.180385, places=6)
        self.assertAlmostEqual(c, 167.803853, places=6)
        self.assertAlmostEqual(sumR, 20.854321, places=6)

        # Edge pixels.
        self.assertEqual(ks[10].getNumberOfEdgePixels(), 19)
        self.assertAlmostEqual(ks[10].getInnerPixelFraction(), 0.000000, places=6)
        self.assertAlmostEqual(ks[10].getOuterPixelFraction(), 1.000000, places=6)

        # Is it a Monte Carlo cluster?
        self.assertEqual(ks[10].isMC(), False)

        # Is it an edge cluster?
        self.assertEqual(ks[10].isEdgeCluster(), False)


        # The last - and small - cluster.

        # Cluster size (number of pixels).
        self.assertEqual(ks[33].getNumberOfPixels(), 1)

        # Cluster location (raw pixels).
        self.assertEqual(ks[33].getXMin(), 97.0)
        self.assertEqual(ks[33].getXMax(), 97.0)
        self.assertEqual(ks[33].getYMin(), 135.0)
        self.assertEqual(ks[33].getYMax(), 135.0)

        # Cluster width and height.
        self.assertEqual(ks[33].getWidth(), 1)
        self.assertEqual(ks[33].getHeight(), 1)

        # Cluster properties based on the unweighted (UW) mean.

        # * Location.
        self.assertAlmostEqual(ks[33].getXUW(),  97.000000, places=6)
        self.assertAlmostEqual(ks[33].getYUW(), 135.000000, places=6)

        # * Radius and density.
        self.assertAlmostEqual(ks[33].getRadiusUW(), 0.000000, places=6)
        self.assertAlmostEqual(ks[33].getDensityUW(), 0.000000, places=6)

        # Counts.
        self.assertEqual(ks[33].getTotalCounts(), 18)
        self.assertEqual(ks[33].getMaxCountValue(), 18)

        # Energy.
        self.assertAlmostEqual(ks[33].getTotalEnergy(), 0.0, places=6)
        self.assertAlmostEqual(ks[33].getMaxEnergy(), 0.0, places=6)

        # Linearity.
        m, c, sumR = ks[33].getLineOfBestFitValues()
        self.assertAlmostEqual(m, 0.000000, places=6)
        self.assertAlmostEqual(c, 97.000000, places=6)
        self.assertAlmostEqual(sumR, 0.000000, places=6)

        # Edge pixels.
        self.assertEqual(ks[33].getNumberOfEdgePixels(), 1)
        self.assertAlmostEqual(ks[33].getInnerPixelFraction(), 0.000000, places=6)
        self.assertAlmostEqual(ks[33].getOuterPixelFraction(), 1.000000, places=6)

        # Is it a Monte Carlo cluster?
        self.assertEqual(ks[33].isMC(), False)

        # Is it an edge cluster?
        self.assertEqual(ks[33].isEdgeCluster(), False)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_kluster.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("=================================================")
    lg.info(" Logger output from cernatschool/test_kluster.py ")
    lg.info("=================================================")
    lg.info("")

    unittest.main()
