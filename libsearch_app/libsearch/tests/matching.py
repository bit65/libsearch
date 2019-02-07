#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest
import os
from libsearch.enrichment.module_mapper import ModuleMapper

dir_path = os.path.dirname(os.path.realpath(__file__))

class TestMatching(unittest.TestCase):

    def modules(self):
        with open(dir_path + '/samples/modules.csv') as f:
            content = f.readlines()
            content = [x.strip() for x in content]

    	modules = ModuleMapper.instance().search_all(content)
        # for i in modules:
        #     print i['name']
        pass
        # print VersionMapper.instance().learn("g","a")

        # results = Parser().get_parser(dir_path + "/samples/AndroidManifest.xml")
        # print len(results.parse()), "Modules Found"
