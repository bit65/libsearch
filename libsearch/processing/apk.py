import subprocess
import tempfile
import shutil
import os

from ..dbmodels import *

from libsearch.processing import dex
from libsearch.processing import json
from libsearch.processing import so
from libsearch.processing import xml
from libsearch.processing import zip

def parse_apk(file_name, orig_name):
    parse_directory('/tmp/tmpfdnzX1', orig_name)
    return

    zip.parse_zip(file_name, orig_name, extract=False)

    tmp_dir = tempfile.mkdtemp()
    print "Temp dir %s" % tmp_dir
    args = ['/usr/bin/java', '-jar', './ext/apktool.jar', 'd', '-f', '--no-src', '-o', tmp_dir, file_name]
    process_java = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    modules = (process_java.communicate()[0]).splitlines()

    parse_directory(tmp_dir, orig_name)

    process_java.stdout.close()

    shutil.rmtree(tmp_dir)

def parse_none(file_name, orig_name):
    pass

parsers = {
    "apk": parse_apk,
    "dex": dex.parse_dex,
    "json": json.parse_json,
    "so": so.parse_so,
    "xml": xml.parse_xml,
    "zip": zip.parse_zip,
    "png": parse_none,
    "jpg": parse_none,
    "jpeg": parse_none,
    "bmp": parse_none,
    "gif": parse_none,
    "svg": parse_none,
    "svg": parse_none,
    "eot": parse_none,
    "woff2": parse_none,
    "woff": parse_none,
    "ttf": parse_none

}

def parse_directory(tmp_dir, orig_name):

    for root, dirs, files in os.walk(tmp_dir):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            file_extension = file_extension.lstrip('.')
            path = "%s%s%s" %(root, os.sep, file)

            if file_extension in parsers.keys():
                ret_modules = parsers[file_extension](path, orig_name)
                if ret_modules != None:
                    for name, data_list in ret_modules:
                        save_data(data_list, name, orig_name)
            else:
                print "File not supported - %s" % file
                pass
        