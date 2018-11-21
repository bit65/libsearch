import os
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from base import ParserBase
"""
from ..dbmodels import *
# from .general import parse_file

from .xml import parse_xml
from .elf import parse_elf
from .properties import parse_properties
from .json import parse_json
from .dex import parse_dex
from parser import Parser
"""

from magic import Magic, MAGIC_MIME_TYPE

class ZIPParser(ParserBase):
    parsetype = "application/zip"
    ext = "zip"

    def parse(self, file_name):
        print("ZIP Parsing %s" % file_name)

        full_path = os.path.abspath(file_name)
        resp = urlopen(full_path)
        zipfile = ZipFile(StringIO(resp.read()))

        # Get files from zip
        new_items = [{"data": i.filename, "metadata": {"crc":i.CRC}} for i in zipfile.infolist()]
        # save_data(new_items, "ZIP_NAMES", file_name)

        # Process files inside zip
        self.extract_names(zipfile)

        return new_items

    def extract_names(self, zipfile):
        for name in zipfile.namelist():
            try:
                with NamedTemporaryFile(delete=True) as temp:
                    temp.write(zipfile.open(name).read())
                    temp.flush()
                    filetype = self.parser.m.id_filename(temp.name)
                    name, ext = os.path.splitext(name)

                    # Remove '.' from extention
                    ext = ext[1:]

                    if filetype in self.parser.parsers and ext in self.parser.parsers[filetype]:
                        print "File: %s Type: %s Ext: %s" % (name, filetype, ext)
                        self.parser.parsers[filetype][ext].parse(temp.name)
                    else:
                        print "Unsupported type: %s %s" % (name, filetype)

            except Exception as e:
                print e
                pass
