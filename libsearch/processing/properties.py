from libsearch.processing.base import ParserBase

class PROPParser(ParserBase):
    parsetype = "text/plain"
    ext = "properties"

    def parse(self, orig_name):
        print "properties", orig_name
