#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

from libsearch.processing.searchparser import Parser

# parser = Parser().get_parser(dir_path + "/../libsearch/tests/samples/classes.dex")
parser = Parser().get_parser(dir_path + "/../libsearch/tests/samples/sample.apk")
print parser.parse()
