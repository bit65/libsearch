from libsearch.processing.base import ParserBase
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle
import tempfile
from libident import ReferenceDB, handle_library

import os

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

        with tempfile.NamedTemporaryFile(mode = "wb", prefix = "lib", suffix = ".so", delete = False) as tmp_f:
            tmp_f.write(f.read())
            tmpname = tmp_f.name

        if not os.path.exists(db):
            os.mkdir(db)
        rdb = ReferenceDB(db)

        if not rdb.exists_in_db(self.filename, tmpname):
            handle_library(rdb, (self.filename, tmpname))

            with open(tmpname, "rb") as f:
                e = ELFFile(open(tmpname, "rb"))
                for s in e.iter_sections():
                    if s['sh_type'] == 'SHT_STRTAB':
                        for x in s.data().split("\x00"):
                            if x != "":
                                # Get Symbols
                                try:
                                    information.append(self.createData("ELF-FUNCTIONS", demangle(x)))
                                except:
                                    information.append(self.createData("ELF-FUNCTIONE", x))

        os.unlink(tmpname)
        return information

