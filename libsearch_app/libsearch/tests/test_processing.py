#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest
import os

from collections import defaultdict
from libsearch.processing.searchparser import Parser


dir_path = os.path.dirname(os.path.realpath(__file__))

class TestProcessing(unittest.TestCase):

    def test_manifest_xml(self):
        results = Parser().get_parser(dir_path + "/samples/AndroidManifest.xml")
        print len(results.parse())

    def test_so(self):
        results = Parser().get_parser(dir_path + "/samples/libJniBitmapOperator.so")
        print len(results.parse())

    def test_apk(self):
        results = Parser().get_parser(dir_path + "/samples/sample.apk")
        print len(results.parse())

    def test_dex(self):

        results = Parser().get_parser(dir_path + "/samples/classes.dex")
        print len(results.parse())



if __name__ == '__main__':
    unittest.main()