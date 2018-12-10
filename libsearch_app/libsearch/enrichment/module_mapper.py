#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import lucene
import os
import sys
import re

from java.nio.file import Paths

from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.index import Term
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import RegexpQuery
from org.apache.lucene.search import WildcardQuery
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer

asset_blacklist = ["io", "com", "org", "net", "java"]

asset_whitelist = {
    "okhttp3": "OK HTTP-LIB",
    "bolts": "Bolts?",
    "javax.swing": "Swing Library",
    "me.dm7": "ME DM7",
    "retrofit2": "Retrofit",
    "retrofit": "Retrofit",
    "com.anagog": "Anagog SDK",
    "anagog.pd": "Anagog SDK",
    "com.unicell.pangoandroid": "Pango Android",
    "com.neura": "Neura SDK",
    "com.google.ads": "Google Ads",
    "dagger": "Dagger?",
    "io.fabric": "io.fabric",
    "com.bumptech": "Bumptech?",
    "com.skyfishjy": "SkyFish?",
    "com.waze": "Waze?",
    "com.tjerkw": "tjerkw?",
    "com.crashlytics": "Crashlytics",
    "com.google.gson": "Google GSON",
    "com.google.android.gms": "Google GMS",
    "com.google.android.material": "Google Material",
    "com.google.analytics": "Google Analytics",
    "android": "Android Libraries",
    "androidx": "Android Libraries",
    "java": "Java Libraries",
    "javax": "Java Libraries",
    "org.apache.log4j": "LOG4J",
    "okio": "OKIO",
    "com.google.android.finsky": "FINSKY?",
    "com.zopim.android.sdk": "Zendesk chat SDK",
    "com.lemurmonitors.bluedriver": "Lemur Monitors BlueDriver",
    "com.carly": "Carly OBD2",
    "com.iViNi": "iVini",
    "iViNi": "iVini",
    "dalvik": "Dalvik",
    "zendesk": "Zendesk",
    "com.google": "Google Library",
    "org.apache.http": "Apache HTTP",
    "ru.car2.dacarpro": "Dacar Pro",
    "kotlin": "Kotlin JVM",
    "mureung.obdproject": "Mureung OBD Project",
    "com.outilsobdfacile.obd": "OUTILS OBD FACILE",
    "com.michele.administrator.obdkontrol": "Michele OBD Kontrol",
    "com.obdeleven": "OBD ELEVEN",
    "com.voltasit.obdeleven": "OBD ELEVEN",
    "com.company.ahmetunal.VehicleSensorMonitor": "Ahmetunal VehicleSensorMonitor",
    "com.kakao": "Kakao"
}


class ModuleMapper:
    _instance = None

    @staticmethod
    def instance():
        if ModuleMapper._instance == None:
            ModuleMapper._instance = ModuleMapper()

        return ModuleMapper._instance

    def __init__(self):
        lucene.initVM()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        INDEX_DIR = "../../central-lucene-index"
        directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
        self.searcher = IndexSearcher(DirectoryReader.open(directory))
    
    def search(self, module):
        print "searching for module", module
        # Hack for mono modules
        module = re.sub('^mono.','',module)

        testsearch = module.replace("/",'.') + ".stub"
        topDocs = self.searcher.search(WildcardQuery(Term("u", testsearch + "|*")), 10)
        # print testsearch
        
        while topDocs.totalHits == 0:
            
            splitted_arr = testsearch.split(".")
            if len(splitted_arr) < 2:
                break
            testsearch = ".".join(splitted_arr[:-1])
            
            if testsearch in asset_whitelist:
                return [asset_whitelist[testsearch]]

            if testsearch in asset_blacklist:
                break
            
            topDocs = self.searcher.search(WildcardQuery(Term("u", testsearch + "|*")), 10)

        scoreDocs = topDocs.scoreDocs
        libs = list(set([self.searcher.doc(scoreDoc.doc)["n"] for scoreDoc in scoreDocs]))
        return libs