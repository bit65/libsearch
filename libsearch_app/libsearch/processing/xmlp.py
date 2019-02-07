from libsearch.processing.base import ParserBase

class XMLParser(ParserBase):
    
    parsetype = ["application/octet-stream", "text/plain", "text/xml"]
    ext = "xml"

    def _parse(self, file, options={}):
        # print "Parse Generic XML", file
        pass