from libsearch.processing.base import ParserBase

parsetype = "text/json"
ext = "json"

class JSONParser(ParserBase):
    def parse(file_name):
        print "json", file_name
