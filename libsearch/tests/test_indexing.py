#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import unittest
from libsearch.storage.indexer import Indexer

class TestIndexing(unittest.TestCase):

    def test_indexing(self):
        indexer = Indexer()
        
        indexer.save({
            "TYPE": "TEST",
            "ASSET": "TEST",
            "VALUE": "TEST"
        })


if __name__ == '__main__':
    unittest.main()