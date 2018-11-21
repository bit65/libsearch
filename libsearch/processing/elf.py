from libsearch.processing.base import ParserBase
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle
import os

class ELFParser(ParserBase):

    parsetype = ['application/x-executable', 'application/x-sharedlib']
    ext = "so"

    def parse(self, file_name):
        
        information = []
        filename_w_ext = os.path.basename(file_name)
        with open(file_name, "rb") as f:
            e = ELFFile(f)
            for s in e.iter_sections():
                if s['sh_type'] == 'SHT_STRTAB':
                    for x in s.data().split("\x00"):
                        if x != "":
                            # Get Permissions
                            information.append(
                                {
                                    "VALUE": demangle(x),
                                    "ASSET": filename_w_ext,
                                    "TYPE": "ELF-FUNCTIONS"
                                })
        
        return information

