from libsearch.processing.base import ParserBase
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle
import os

# TODO - ADD CHECKSUM OF ELF
# TODO - GET VERSION FROM ?? (Strings,...)

class ELFParser(ParserBase):

    parsetype = ['application/x-executable', 'application/x-sharedlib']
    ext = "so"

    def _parse(self, f):
        return []
        print "ELF Parsing"
        information = []
        
        e = ELFFile(f)
        for s in e.iter_sections():
            if s['sh_type'] == 'SHT_STRTAB':
                for x in s.data().split("\x00"):
                    if x != "":
                        # Get Symbols
                        information.append(
                            {
                                "VALUE": demangle(x),
                                "ASSET": self.filename_w,
                                "TYPE": "ELF-FUNCTIONS"
                            })
        
        return information

