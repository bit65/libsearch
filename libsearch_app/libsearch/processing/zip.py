
from zipfile import ZipFile

from libsearch.processing.base import ParserBase
from libsearch.processing.searchparser import Parser as P

import datetime

class ZIPParser(ParserBase):
    parsetype = "application/zip"
    ext = "zip"

    def _parse(self, f):
        print "Parsing ZIP"
        information = []

        zipfile = ZipFile(f)

        # try:
        for x in zipfile.infolist():
            # Add File to index
            data = self.createData("FILE",filename=x.filename)
            data["CRC"] = x.CRC
            information.append(data)

            # Process File
            parser = P.instance().get_parser(x.filename)

            if parser is None:
                continue
            
            try:
                before = datetime.datetime.now()
                results = parser.parse(zipfile.open(x.filename), parent=self.filename_w)
                after = datetime.datetime.now()
                if (after - before) > datetime.timedelta(seconds=1):
                    print "Parsed %s in %s" % (x.filename, str(after - before))

                if results is not None:
                    information += results

            except Exception as e:
                print "Cannot process %s" % x.filename
                print e

        return information
