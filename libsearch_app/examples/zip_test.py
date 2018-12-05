#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
from libsearch.processing.searchparser import Parser
from libsearch.storage.indexer import Indexer

host = os.getenv('ES_HOST', "localhost")
aws_options = {
    "hosts":[{'host': host, 'port': 443}],
    "use_ssl":True,
    "verify_certs":True
}


import pprint
pp = pprint.PrettyPrinter(indent=4)

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../../cache"

files = os.listdir(dir_path)
files = files[:10]
for f in files:
    parser = Parser.instance().get_parser(dir_path + os.sep + f)
    if parser != None:
        index_data = parser.parse()
        Indexer.instance(aws_options).save(index_data)
print "Done"


