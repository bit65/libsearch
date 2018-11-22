#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from libsearch.processing.serachparser import Parser
import os

files = os.listdir("./cache")
for f in files:
    # parse_apk("./cache/" + f, f)
    results = Parser().parse("./cache/" + f, index=True, parent=f)
    print results
    
# apk_downloader("auto_and_vehicles")