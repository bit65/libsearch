from libsearch.processing.base import ParserBase
from libsearch.enrichment.module_mapper import ModuleMapper
# import pydexinfo
from androguard.core.bytecodes import dvm
import subprocess
import re
import os
import gc
# from ..dbmodels import *

class DEXParser(ParserBase):

    def __init__(self, filename):
        ParserBase.__init__(self, filename)

    parsetype = "application/octet-stream"
    ext = "dex"

    def readFromDEX(self, f):
        d = dvm.DalvikVMFormat(f.read())
        classes = []
        for c in d.get_classes():
            classes.append('.'.join(c.get_name().split('/')[:-1])[1:])

        return list(set(classes))


    def _parse(self, f):
        print "PARSING DEX"
        information = []        
        modules = self.readFromDEX(f)

        libs = []
        missing_module_libs = []
        for m in modules:
            libs += ModuleMapper.instance().search(m)

        for lib in list(set(libs)):
            information.append(self.createData("APK-LIBRARY", library=lib))
            # print lib

        information += [self.createData("MODULES", module=i) for i in modules]

        
        print "DONE DEX"
        return information
