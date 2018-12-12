from libsearch.processing.base import ParserBase
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle
import tempfile
import inspectelf
import itertools
import operator
import hashlib
import os
import json

# TODO - ADD CHECKSUM OF ELF
# TODO - GET VERSION FROM ?? (Strings,...)
db = "db/"

class ELFParser(ParserBase):

    parsetype = ['application/x-executable', 'application/x-sharedlib']
    ext = "so"

    def _parse(self, f):
        global db
        print "ELF Parsing"
        information = []
        tmpname = ""

        with open("/tmp/%s" % os.path.basename(self.filename), "wb") as tmp_f:
            tmp_f.write(f.read())
            tmpname = tmp_f.name

        with open(tmpname, "rb") as f:
            e = ELFFile(open(tmpname, "rb"))

            # Add arch
            information.append(self.createData("ELF-ARCH", e.header.e_machine[3:]))

            for s in e.iter_sections():
                if s['sh_type'] == 'SHT_STRTAB':
                    for x in s.data().split("\x00"):
                        if x != "":
                            # Get Symbols
                            try:
                                information.append(self.createData("ELF-FUNCTIONS", demangle(x)))
                            except:
                                information.append(self.createData("ELF-FUNCTIONS", x))

        flags = inspectelf.inspect(tmpname, recursive = False, cfg = True, force = True)

        information.append(self.createData("ELF-FLAGS", self.filename, **flags[tmpname]))

        os.unlink(tmpname)
        return information

