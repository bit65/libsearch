from libsearch.processing.base import ParserBase
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle

class ELFParser(ParserBase):
    parsetype = ['application/x-executable', 'application/x-sharedlib']
    ext = "so"

    def parse(self, orig_name):
        if orig_name.startswith("lib/"):
            _, system, name =  orig_name.split('/')

            print "LIB", system, name
        else:
            print "SO", orig_name

        with open(orig_name, "rb") as f:
            e = ELFFile(f)
            for s in e.iter_sections():
                if s['sh_type'] == 'SHT_STRTAB':
                    print [demangle(x) for x in s.data().split("\x00")]
