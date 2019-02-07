from libsearch.processing.base import ParserBase
from unidecode import unidecode

class PROPParser(ParserBase):
    parsetype = "text/plain"
    ext = "properties"

    def _parse(self, f, options={}):
        information = []
        return []
        
        for line in f:
            csv = line.strip().split('=', 2)
            if len(csv) > 1:
                try:
                    information.append(self.createData("main","META", META_KEY=unidecode(csv[0]), META_VALUE=unidecode(csv[1], META_TYPE="PROPERTIES")))
                except:
                    pass
                
                
        return information
