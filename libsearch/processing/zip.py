
from StringIO import StringIO
from zipfile import ZipFile

from libsearch.processing.base import ParserBase
# from libsearch.processing.serachparser import Parser
import os


class ZIPParser(ParserBase):
    parsetype = "application/zip"
    ext = "zip"

    def parse(self, file_name):

        filename_w_ext = os.path.basename(file_name)
        information = []

        zipfile = ZipFile(file_name)

        # gParser = Parser()

        for x in zipfile.infolist():
            information.append(
                {
                    "VALUE": x.filename,
                    "CRC":   x.CRC,
                    "ASSET": filename_w_ext,
                    "TYPE": "FILE"
                })
            
            # gParser.parse(x.file_name)

        return information

        # Get files from zip
        # new_items = [{"data": i.filename, "metadata": {"crc":i.CRC}} for i in zipfile.infolist()]
        # save_data(new_items, "ZIP_NAMES", file_name)

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

    # def extract_names(self, zipfile):
    #     for name in zipfile.namelist():
    #         try:
    #             with NamedTemporaryFile(delete=True) as temp:
    #                 temp.write(zipfile.open(name).read())
    #                 temp.flush()
    #                 filetype = self.parser.m.id_filename(temp.name)
    #                 name, ext = os.path.splitext(name)

    #                 # Remove '.' from extention
    #                 ext = ext[1:]

    #                 if filetype in self.parser.parsers and ext in self.parser.parsers[filetype]:
    #                     print "File: %s Type: %s Ext: %s" % (name, filetype, ext)
    #                     self.parser.parsers[filetype][ext].parse(temp.name)
    #                 else:
    #                     print "Unsupported type: %s %s" % (name, filetype)

    #         except Exception as e:
    #             print e
    #             pass
