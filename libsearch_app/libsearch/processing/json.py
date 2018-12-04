from libsearch.processing.base import ParserBase

class JSONParser(ParserBase):
    parsetype = "text/json"
    ext = "json"

    def _parse(self, file_name):
        # print "Handle json", self.filename
        return []
