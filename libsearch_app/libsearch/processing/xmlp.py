from libsearch.processing.base import ParserBase

class XMLParser(ParserBase):
    
    parsetype = ["application/octet-stream", "text/plain", "text/xml"]
    ext = "xml"

    def _parse(self, file):
        # print "Parse Generic XML", file
        pass