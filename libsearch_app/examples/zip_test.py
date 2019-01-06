#!/usr/bin/env python
# encoding: utf-8

import os
from libsearch.processing.searchparser import Parser
from libsearch.storage.indexer import Indexer
import traceback

import datetime

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../cache"

files = os.listdir(dir_path)
for f in files:
    if f.endswith(".apk"):
        if os.path.isfile(dir_path + os.sep + f + '.indexed'):
            print "Already indexed: %s" % (dir_path + os.sep + f)
            continue

        try:
            parser = Parser.instance().get_parser(dir_path + os.sep + f)
            if parser != None:
                index_data = parser.parse(save=True)
                # Indexer.instance().save(index_data)
                # with open(dir_path + os.sep + f + '.indexed', 'w') as cached:
                #     cached.write(str(datetime.date.today()))
        except Exception:
            print(traceback.format_exc())
            pass

print "Done"
