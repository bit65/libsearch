from libsearch.processing.base import ParserBase

parsetype = "text/plain"
ext = "properties"

class PROPParser(ParserBase):
    def parse(self, orig_name):
        print "properties", orig_name
