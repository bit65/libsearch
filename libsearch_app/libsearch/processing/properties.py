from libsearch.processing.base import ParserBase
from unidecode import unidecode

class PROPParser(ParserBase):
    parsetype = "text/plain"
    ext = "properties"

    def _parse(self, f):
        information = []
        # return []
        
        for line in f:
            csv = line.strip().split('=', 2)
            if len(csv) > 1:
                try:
                    information.append(self.createData("meta","properties", key=unidecode(csv[0]), value=unidecode(csv[1])))
                except:
                    pass
                
                
        return information
