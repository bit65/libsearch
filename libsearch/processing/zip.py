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

        try:
            temp_dir = mkdtemp()
            zipfile.extractall(temp_dir)

            for x in zipfile.infolist():
                # Add File
                information.append(
                    {
                        "VALUE": x.filename,
                        "CRC":   x.CRC,
                        "ASSET": self.filename,
                        "TYPE": "FILE"
                    })

                # Process File
                full_path = temp_dir + os.sep + x.filename
                parser = gParser.get_parser(x.filename)

                if parser is None:
                    # print "No parser for %s" % x.filename
                    continue

                try:
                    results = parser.parse(zipfile.open(x.filename))

                    if results is not None:
                        information += results

                except Exception as e:
                    print "Cannot process %s" % x.filename
                    print e
                        

        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print e

        return information
