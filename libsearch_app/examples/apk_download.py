#!/usr/bin/env python
# encoding: utf-8

import os
from libsearch.processing.searchparser import Parser
from libsearch.storage.indexer import Indexer
from libsearch.fetcher import apk_downloader

import urllib3
urllib3.disable_warnings()

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='csv file with apps')
parser.add_argument('--download', help='download apk first', action="store_true")
args = parser.parse_args()


if args.csv is not None:
    with open(args.csv) as f:
        apps = ["/en/" + line.strip() for line in f]
        for apk in apps:
            try:
                link_download = apk_downloader(apk, download=args.download)
                if link_download is not None:
                    apk_parser = Parser.instance().parsers['apk'](apk)
                    apk_parser.parse(fileobj=link_download, save=True)
            except Exception as e:
                print "failed downloading %s" % apk
                print e
                pass
