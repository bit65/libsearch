#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from libsearch.fetcher import apk_downloader
from libsearch.fetcher import apk_search
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='csv file with apps')
args = parser.parse_args()

if args.csv is not None:
	with open(args.csv) as f:
		apps = ["/en/" + line.strip() for line in f]
		apk_search(apps)