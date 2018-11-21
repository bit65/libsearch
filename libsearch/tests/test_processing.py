#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest
import os

from libsearch.processing.serachparser import Parser

dir_path = os.path.dirname(os.path.realpath(__file__))

class TestProcessing(unittest.TestCase):

    def test_manifest_xml(self):
        results = Parser().parse(dir_path + "/samples/AndroidManifest.xml")
        print results
    
    def test_so(self):
        results = Parser().parse(dir_path + "/samples/libJniBitmapOperator.so")
        print results
        # self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()