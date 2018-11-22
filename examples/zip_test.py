#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libsearch.processing.searchparser import Parser

parser = Parser().get_parser("cache/Carista OBD2_v3.7.3_apkpure.com.apk"
print parser.parse()
print Parser().parse("cache/Carista OBD2_v3.7.3_apkpure.com.apk", index = False)
