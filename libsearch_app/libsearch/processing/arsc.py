from libsearch.processing.base import ParserBase
from androguard.core.bytecodes.axml import ARSCParser as ARCP
import code

class ARSCParser(ParserBase):
    parsetype = "text/plain"
    ext = "arsc"

    def _parse(self, file):
        return []
        
        file_data = file.read()
        arcObject = ARCP(file_data)

        code.interact(local=locals())
        print "arsc", self.filename
        return []
