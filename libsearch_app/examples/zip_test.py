#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
from libsearch.processing.searchparser import Parser
from libsearch.storage.indexer import Indexer

import pprint
pp = pprint.PrettyPrinter(indent=4)

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../../cache"

files = os.listdir(dir_path)
files = files[:10]
for f in files:
    parser = Parser.instance().get_parser(dir_path + os.sep + f)
    if parser != None:
        index_data = parser.parse()
        print len(index_data)
        # Indexer.instance().save(index_data)
print "Done"


