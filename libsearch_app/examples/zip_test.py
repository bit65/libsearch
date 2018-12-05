#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from libsearch.processing.searchparser import Parser
from libsearch.storage.indexer import Indexer

import datetime

host = os.getenv('ES_HOST', "localhost")
aws_options = {
    "hosts": [{'host': host, 'port': 443}],
    "use_ssl": True,
    "verify_certs": True
}

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../../cache"

files = os.listdir(dir_path)
for f in files:
    if f.endswith(".apk"):
        if os.path.isfile(dir_path + os.sep + f + '.indexed'):
            continue

        try:
            parser = Parser.instance().get_parser(dir_path + os.sep + f)
            if parser != None:
                index_data = parser.parse()
                Indexer.instance(aws_options).save(index_data)
                with open(dir_path + os.sep + f + '.indexed', 'w') as cached:
                    cached.write(str(datetime.date.today()))
        except Exception as e:
            pass

print "Done"
