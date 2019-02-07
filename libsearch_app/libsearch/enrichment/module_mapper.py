#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import lucene
import os
import sys
import re

from java.nio.file import Paths

import requests
import requests_cache
# requests_cache.install_cache('mapper_cache', expire_after=60*60*24*30, allowable_codes=(200,404))

from lxml import etree
from lxml import html

from collections import defaultdict


# 'latest_version' = 'r7'
# 'src' = path
# 'module' = module
mappings = {
    "android.support.v4": 
    {
        'name': 'Android Support V4',
        'description': 'Android Support V4',
        'groupId': 'com.google.android',
        'artifactId': 'support-v4'
    },
    "android.support.v7": 
    {
        'name': 'Android Support V7',
        'description': 'Android Support V7',
        'groupId': 'com.google.android',
        'artifactId': 'support-v7'
    },
    "android.support.v13": 
    {
        'name': 'Android Support V13',
        'description': 'Android Support V13',
        'groupId': 'com.google.android',
        'artifactId': 'support-v13'
    },
    "io.fabric.sdk.android": 
     {
        'name': 'Android SDK Fabric',
        'description': 'Android SDK Fabric ',
        'groupId': 'io.fabric.sdk.android',
        'artifactId': 'fabric'
    },
    "zendesk":
    {
        'name': 'Zendesk',
        'description': 'Zendesk Support',
        'groupId': 'com.zendesk',
        'artifactId': 'zendesk'
    },
    "com.google.android.gms": 
    {
        'name': 'Google Play Services',
        'description': 'Google Play Services',
        'groupId': 'com.google.android.gms',
        'artifactId': 'play-services'
    },
    # "android.support": None,
    # "android.":None,
    # "androidx.": None
}

translation = {
    "com.google.zxing": "com.google.zxing.core",
    "org.apache": "org.apache.apache",
    "okhttp3": "com.squareup.okhttp3.okhttp",
    "com.squareup.okhttp": "com.squareup.okhttp3.okhttp",
    "com.bumptech.glide": "com.github.bumptech.glide.glide",
    "com.google.firebase": "com.google.firebase.firebase-server-sdk",
    "com.google.gson": "com.google.code.gson.gson",
    "com.google.ads": "com.google.api-ads.google-ads",
    "retrofit2": "com.squareup.retrofit2.retrofit",
    "com.crashlytics.android": "com.crashlytics.sdk.android.crashlytics",
    "com.facebook": "com.facebook.android.facebook-core",
    "org.jsoup": "org.jsoup.jsoup",
    "org.bouncycastle": "org.bouncycastle.bcpg-jdk16",
    "com.shaded.fasterxml":"com.fasterxml.jackson.jackson-base",
    "com.nostra13.universalimageloader":"com.nostra13.universalimageloader.universal-image-loader",
    "org.springframework": "org.springframework.integration.spring-integration-core",
    # "com.google.a":None,

    
}

class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self))

class ModuleMapper:
    _instance = None

    @staticmethod
    def instance():
        if ModuleMapper._instance == None:
            ModuleMapper._instance = ModuleMapper()

        return ModuleMapper._instance

    def __init__(self):
        self.cache = requests_cache.core.CachedSession('mapper_cache', expire_after=60*60*24*30, allowable_codes=(200,404))
        pass 
    
    def map_modules(self, libs, modules):

        for m in modules:
            orig_module = m

            for k,v in translation.iteritems():
               
                if m.startswith(k):
                    if v is not None:
                        m = v                    
            
            for k,v in mappings.iteritems():
                if m.startswith(k):
                    if v is not None:
                        lib = dict(v)
                        lib['actual_module'] = orig_module
                        lib['module'] = k

                        libs.append(Hashabledict(lib))
        return

    def search_all(self, modules):
        all_libs = []
        # cache = set()
        tree = {}

        # libs = []
        self.map_modules(all_libs, modules)
        
        for m in modules:
            m = m.replace('/', '.').split('.')
            t = tree    
            for part in m:
                t = t.setdefault(part, {})
    
        
        # ,"http://central.maven.org/maven2/%s",
        # bases = ["http://central.maven.org/maven2/%s","http://jcenter.bintray.com/%s", "https://oss.sonatype.org/content/repositories/releases/%s"]

        bases = [
            "https://oss.sonatype.org/content/repositories/releases/%s", 
            "http://repo1.maven.org/maven2/%s",
            "http://central.maven.org/maven2/%s",
            "http://repository.ops4j.org/maven2/%s"
            ]
        
        for base in bases:
            t_libs = self.parseTree(base, tree, [])
            if len(t_libs) > 0:
                all_libs += t_libs

        return all_libs

    def parseTree(self, base, tree, libs, path="", orig_path=""):

        moduleId = path.replace('/','.').strip('.')
        origId = moduleId

        files = self.get_online_dirlist(base, path)

        if files:
            if "maven-metadata.xml" in files:
                
                if orig_path != "":
                    origId = moduleId
                    moduleId = orig_path.replace('/','.').strip('.')

                lib = self.parse_maven(base % path.lstrip('/'), moduleId, origId)
                if lib:
                    libs.append(lib)

            # Hack to get same parent artificat
            if path.split('/')[-1] in files:
                self.parseTree(base, tree, libs, "%s/%s" % (path, path.split('/')[-1]), path)

            for k, v in tree.iteritems():
                if k in files:
                    self.parseTree(base, v, libs, "%s/%s" % (path, k))
                                        
        return libs

    def get_online_dirlist(self, base, path):

        r = self.cache.get(base % path.lstrip('/'))
        if r.status_code == 200:
            tree = html.fromstring(r.content)
            return [f.rstrip('/') for f in tree.xpath('//a/text()')]
        
    def parse_maven(self, path, module, orig_module):

        try:
            r = self.cache.get(path + "/maven-metadata.xml")
            
            if r.status_code == 200:

                tree = html.fromstring(r.content)
                
                groupId = tree.xpath('//groupid/text()')
                artifactId = tree.xpath('//artifactid/text()')
                # import code
                # code.interact(local=locals())
                if len(groupId) != 0 and len(artifactId) != 0:
                    groupId = groupId[0]
                    artifactId = artifactId[0]

                    latest_version = tree.xpath('//versioning/latest/text()')
                    all_versions = tree.xpath('//versions/version/text()')

                    if len(latest_version) != 0:
                        latest_version = latest_version[0]
                        r = self.cache.get(path + "/" + latest_version + "/")
                            
                        if r.status_code == 200:
                            tree = html.fromstring(r.content)
                            for f in tree.xpath('//a/text()'):
                                # print f
                                if f.endswith(".pom"):
                                    r = self.cache.get(path + "/"+latest_version+"/"+f)
                                    if r.status_code == 200:
                                        tree = html.fromstring(r.content)

                                        lib = {}
                                        lib['name'] = tree.xpath('//project/name/text()')[0]
                                        lib['description'] = tree.xpath('//project/name/text()')[0]
                                        lib['latest_version'] = latest_version
                                        lib['groupId'] = groupId
                                        lib['artifactId'] = artifactId
                                        # lib['src'] = path
                                        lib['actual_module'] = module
                                        lib['module'] = orig_module

                                        return lib
        except Exception as e:
            print "error", e
        return None