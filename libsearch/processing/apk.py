from libsearch.processing.base import ParserBase
from libsearch.processing.zip import ZIPParser

parsetype = "application/zip"
ext = "apk"

class APKParser(ZIPParser):
    def parse(self, file_name):
        print "APK Parsing"
        super().parse(file_name)

# import subprocess
# import tempfile
# import shutil
# import os

# from ..dbmodels import *

# from libsearch.processing import dex
# from libsearch.processing import json
# from libsearch.processing import so
# from libsearch.processing import xmlp
# from libsearch.processing import zip

# def parse_apk(file_name, orig_name):
#     parse_directory('/tmp/tmpfdnzX1', orig_name)
#     return

#     zip.parse_zip(file_name, orig_name, extract=False)

#     tmp_dir = tempfile.mkdtemp()
#     print "Temp dir %s" % tmp_dir
#     args = ['/usr/bin/java', '-jar', './ext/apktool.jar', 'd', '-f', '--no-src', '-o', tmp_dir, file_name]
#     process_java = subprocess.Popen(args, stdout=subprocess.PIPE,
#                                     shell=False)
#     modules = (process_java.communicate()[0]).splitlines()

#     parse_directory(tmp_dir, orig_name)

#     process_java.stdout.close()

#     shutil.rmtree(tmp_dir)

# def parse_none(file_name, orig_name):
#     pass

# def parse_save(file_name, orig_name):
#     ret_data = []
#     with open(file_name, "r") as file:
#         file_data = file.read()
#         _, file_extension = os.path.splitext(file_name)
        
#         real_path = '/' + '/'.join(file_name.split('/')[3:])
#         saved_data = [SaveData(data=file_data, metadata={"name": real_path})]
#         ret_data.append((file_extension[1:].upper() + "_DATA", saved_data))
#     return ret_data

# parsers = {
#     "apk": parse_apk,
#     "dex": dex.parse_dex,
#     "so": so.parse_so,
#     "xml": xmlp.parse_xml,
#     "zip": zip.parse_zip,
    
#     # TODO
#     "json": parse_save,
#     "yml": parse_save,
#     "properties": parse_save,
#     "html": parse_none,
#     "css": parse_none,
#     "version": parse_save,
#     "js": parse_save,
#     "ts": parse_none,
#     "txt": parse_save,
#     "map": parse_none,
#     "RSA": parse_save,
#     "DSA": parse_save,
#     "meta": parse_save,
    

#     # Don't parse
#     "ico": parse_none,
#     "png": parse_none,
#     "jpg": parse_none,
#     "jpeg": parse_none,
#     "bmp": parse_none,
#     "gif": parse_none,
#     "svg": parse_none,
#     "svg": parse_none,
#     "eot": parse_none,
#     "woff2": parse_none,
#     "woff": parse_none,
#     "ttf": parse_none

# }

# def parse_directory(tmp_dir, orig_name):

#     for root, dirs, files in os.walk(tmp_dir):
#         for file in files:
            
#             # Bypass original files
#             if root.startswith(tmp_dir + os.sep + "original"):
#                 continue

#             filename, file_extension = os.path.splitext(file)
#             file_extension = file_extension.lstrip('.')
#             path = "%s%s%s" %(root, os.sep, file)

#             if file_extension in parsers.keys():
#                 ret_modules = parsers[file_extension](path, file)
                
#                 if ret_modules != None:
#                     for name, data_list in ret_modules:
#                         save_data(data_list, name, orig_name)
#             else:
#                 print "File not supported - %s" % file
#                 pass
        