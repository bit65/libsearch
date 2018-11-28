from libsearch.processing.base import ParserBase
import pydexinfo
import subprocess
import re
import os
# from ..dbmodels import *

class DEXParser(ParserBase):
    parsetype = "application/octet-stream"
    ext = "dex"

    def _parse(self, f):
        s = pydexinfo.parse(f, True)
        information = []

        modules = set(re.findall("class_idx.*?L([^;\$]*)", s))

        #modules = set(re.findall("class_idx.*?L([^;\$]*)", s))
        for m in modules:
            information.append(
                {
                    "VALUE": m,
                    "ASSET": self.filename,
                    "TYPE": "MODULES"
                })


        return information
