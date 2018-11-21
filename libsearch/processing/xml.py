from libsearch.processing.base import ParserBase

class XMLParser(ParserBase):
    parsetype = ["application/octet-stream", "text/plain"]
    ext = "xml"

    def parse(self, orig_name):
        print "xml", orig_name
