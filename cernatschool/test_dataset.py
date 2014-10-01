#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the dataset wrapper.
from dataset import Dataset

class DatasetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_dataset(self):

        ## The Pixelman dataset object.
        pds = Dataset("testdata/ASCIIxyC/")

        # The tests.

        # The number of datafiles.
        self.assertEqual(pds.getNumberOfDataFiles(), 5)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_dataset.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("=================================================")
    lg.info(" Logger output from cernatschool/test_dataset.py ")
    lg.info("=================================================")
    lg.info("")

    unittest.main()
