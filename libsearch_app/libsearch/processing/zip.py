from tempfile import mkdtemp
from StringIO import StringIO
from zipfile import ZipFile

from libsearch.processing.base import ParserBase
from libsearch.processing.searchparser import Parser as P
import os
import shutil
import traceback

class ZIPParser(ParserBase):
    parsetype = "application/zip"
    ext = "zip"

    def _parse(self, f):
        information = []

        zipfile = ZipFile(f)

        gParser = P()

        # try:
        for x in zipfile.infolist():
            # Add File to index
            data = self.createData("FILE",x.filename)
            data["CRC"] = x.CRC
            information.append(data)

            # Process File
            parser = gParser.get_parser(x.filename)

            if parser is None:
                continue
            
            try:
                results = parser.parse(zipfile.open(x.filename), parent=self.filename_w)

                if results is not None:
                    information += results

            except Exception as e:
                print "Cannot process %s" % x.filename
                print e

        return information
