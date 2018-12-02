from libsearch.processing.base import ParserBase
from libsearch.processing.zip import ZIPParser

class APKParser(ZIPParser):
    parsetype = "application/zip"
    ext = "apk"

    def _parse(self, f):
        print "APK Parsing"
        information = ZIPParser._parse(self, f)

        return information