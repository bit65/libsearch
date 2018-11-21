#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from libsearch.processing.apk import parse_apk
import os


# apk_downloader("auto_and_vehicles")

files = os.listdir("./cache")
for f in files:
    parse_apk("./cache/" + f, f)

# parse_apk("./cache/Porsche Center_v1.2.10_apkpure.com.apk", "Porsche Center_v1.2.10_apkpure.com.apk")