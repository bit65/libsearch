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
        # self.module_mapper = ModuleMapper()
        ParserBase.__init__(self, filename)

    parsetype = "application/octet-stream"
    ext = "dex"
    
    def _parse_modules(self, s):
        module_info = []
        # print s
        modules = set(re.findall("class_idx.*?L([^;\\$]*)", s))
        
        

        modules = list(set([".".join(m.split("/")[:-1]) for m in modules]))

        libs = []
        missing_module_libs = []
        for m in modules:
            module_info.append(self.createData("MODULES", m))
            # _libs = self.module_mapper.search(m)
            # libs += _libs
            # if len(_libs) == 0:
            #     missing_module_libs.append(m)            

        for lib in list(set(libs)):
            module_info.append(self.createData("LIB", lib))

        print "****************\nMISSSING MODULES\n*****************"
        for m in missing_module_libs:
            print "* %s" %  m
        print "****************************"

            

        # module_info = self.module_finder._analyze(module_info, parent=self.parent)

        return module_info

    def readFromDEX(self, f):
        d = dvm.DalvikVMFormat(f.read())
        classes = []
        for c in d.get_classes():
            classes.append('.'.join(c.get_name().split('/')[:-1])[1:])

        del d
        gc.collect()
        return list(set(classes))


    def _parse(self, f):
        print "PARSING DEX"
        # TODO: Remove when done
        return []
                
        classes = self.readFromDEX(f)

        # s = pydexinfo.parse(f, True)
        information = [self.createData("MODULES", i) for i in classes]

        # information += self._parse_modules(s)

        print "DONE DEX"
        return information
