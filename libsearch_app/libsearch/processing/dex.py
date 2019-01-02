from libsearch.processing.base import ParserBase
from libsearch.enrichment.module_mapper import ModuleMapper
# import pydexinfo
from androguard.core.bytecodes import dvm
import godex
from itertools import groupby
from tempfile import NamedTemporaryFile
import subprocess
import re
import os
import gc

re_base64 = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
re_hex_16 = re.compile(r"([a-f\d]{16}|[A-F\d]{16})")
re_hex_32 = re.compile(r"([a-f\d]{32}|[A-F\d]{32})")
re_hex_64 = re.compile(r"([a-f\d]{64}|[A-F\d]{64})")


def whitelist_strings(s):
    # return True
    s = s.lower()
    if "https://" in s or "http://" in s:
        return True
    if "private" in s:
        return True
    if "secret" in s:
        return True
    if "key=" in s:
        return True
    if ".php" in s or ".aspx/" in s or ".asmx" in s or ".asmx" in s or ".asmx" in s:
        return True
    if len(s) > 30 and re_base64.match(s) is not None:
        return True
    if re_hex_16.match(s) is not None or re_hex_32.match(s) is not None or re_hex_64.match(s):
        return True
    return False

class DEXParser(ParserBase):

    def __init__(self, filename):
        ParserBase.__init__(self, filename)

    parsetype = "application/octet-stream"
    ext = "dex"

    def readFromDEX(self, f):
        tmpname = ""
        modules = []
        with NamedTemporaryFile() as tmp:
            tmp.write(f.read())
            modules = godex.getClasses(tmp.name)

        return {
                 "classes": modules,
                 "strings": []
        }
        
    def _parse(self, f):
        print "PARSING DEX"
        information = []
        dex_file = self.readFromDEX(f)

        for s in dex_file["strings"]:
            information.append(self.createData("main","STRING", STRING_DATA=s))

        for module,classes_iter in groupby(dex_file["classes"],lambda f: ".".join(f.split('.')[:-1])):

            information.append(self.createData("main", "MODULE", MODULE_NAME=module))
            libs = ModuleMapper.instance().search(module)
            information.append(self.createData("main","LIBRARY", LIBRARY_NAMES=libs))

        
        print "DONE DEX"
        return information
