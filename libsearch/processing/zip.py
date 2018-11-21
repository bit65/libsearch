# import os
# from StringIO import StringIO
# from urllib import urlopen
# from zipfile import ZipFile
# from tempfile import NamedTemporaryFile
# from base import ParserBase
# """
# from ..dbmodels import *
# # from .general import parse_file

# from .xml import parse_xml
# from .elf import parse_elf
# from .properties import parse_properties
# from .json import parse_json
# from .dex import parse_dex
# from parser import Parser
# """

# from magic import Magic, MAGIC_MIME_TYPE

from libsearch.processing.base import ParserBase

parsetype = "application/zip"
ext = "zip"

class ZIPParser(ParserBase):
    def parse(self, file_name):
        pass
#         full_path = os.path.abspath(file_name)
#         resp = urlopen(full_path)
#         zipfile = ZipFile(StringIO(resp.read()))

#         # Get files from zip
#         new_items = [{"data": i.filename, "metadata": {"crc":i.CRC}} for i in zipfile.infolist()]
#         # save_data(new_items, "ZIP_NAMES", file_name)

#         # Process files inside zip
#         self.extract_names(zipfile)

#         return new_items

#     def extract_names(self, zipfile):
#         for name in zipfile.namelist():
#             try:
#                 with NamedTemporaryFile(delete=True) as temp:
#                     temp.write(zipfile.open(name).read())
#                     temp.flush()
#                     filetype = self.parser.m.id_filename(temp.name)

# from tempfile import NamedTemporaryFile

# def parse_file(zipfile, function, file_name):
#     try:
#         with NamedTemporaryFile(delete=True) as temp:
#             temp.write(zipfile.open(file_name).read())

#             ret_modules = function(temp.name, file_name)
#             if ret_modules != None:
#                 for name, data_list in ret_modules:
#                     save_data(data_list, name, file_name)
                
#     except Exception as e:
#         print e
#         pass


# def parse_zip(file_name, orig_name, extract=True):
#     full_path = os.path.abspath(file_name)
#     resp = urlopen(full_path)
#     zipfile = ZipFile(StringIO(resp.read()))

#     # Get files from zip
#     new_items = [SaveData(data=i.filename, metadata={"crc":i.CRC}) for i in zipfile.infolist()]
#     save_data(new_items, "ZIP_NAMES", file_name)

#     # Process files inside zip
#     if extract:
#         extract_names(zipfile)
    
# def extract_names(zipfile):
#     for name in zipfile.namelist():
        
#         if name.endswith(".so"):
#             parse_file(zipfile, parse_so, name)

#         elif name.endswith(".xml"):
#             parse_file(zipfile, parse_xml, name)
            
#         elif name.endswith(".json"):
#             parse_file(zipfile, parse_json, name)
        
#         elif name.endswith(".properties"):
#             parse_file(zipfile, parse_properties, name)

#         elif name.endswith(".dex"):
#             parse_file(zipfile, parse_dex, name)

#         elif name.endswith(".zip") or name.endswith(".apk"):
#             parse_file(zipfile, parse_zip, name)

#         elif name.endswith(".js"):
#             pass
#         elif name.endswith(".png") or name.endswith(".jpg"):
#             pass
#         else:
#             print "file not supported - %s" % name
#                     self.parser.parsers[self.parser.m.id_filename(temp.name)](temp.name)
#                     print "File: %s Type: %s" % (name, filetype)

#             except Exception as e:
#                 pass
