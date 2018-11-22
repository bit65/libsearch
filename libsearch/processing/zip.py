from tempfile import mkdtemp
from StringIO import StringIO
from zipfile import ZipFile

from libsearch.processing.base import ParserBase
from libsearch.processing.serachparser import Parser as P
import os
import shutil

class ZIPParser(ParserBase):
    parsetype = "application/zip"
    ext = "zip"

    def parse(self, file_name):
        filename_w_ext = os.path.basename(file_name)
        information = []

        zipfile = ZipFile(file_name)

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
                        "ASSET": filename_w_ext,
                        "TYPE": "FILE"
                    })

                # Process File
                full_path = temp_dir + os.sep + x.filename
                try:
                    results = gParser.parse(full_path, parent=filename_w_ext)
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