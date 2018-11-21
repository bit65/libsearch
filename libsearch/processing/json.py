from libsearch.processing.base import ParserBase

class JSONParser(ParserBase):
    parsetype = "text/json"
    ext = "json"

    def parse(file_name):
        print "json", file_name
