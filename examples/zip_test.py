#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libsearch.processing.searchparser import Parser

parser = Parser().get_parser("../libsearch/tests/samples/sample.apk")
print parser.parse()
