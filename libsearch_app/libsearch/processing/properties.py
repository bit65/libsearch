from libsearch.processing.base import ParserBase

class PROPParser(ParserBase):
    parsetype = "text/plain"
    ext = "properties"

    def _parse(self, f):
        # print "properties", self.filename
        return []
