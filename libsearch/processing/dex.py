from libsearch.processing.base import ParserBase
import pydexinfo
import subprocess
import re
import os
# from ..dbmodels import *

class DEXParser(ParserBase):
    parsetype = "application/octet-stream"
    ext = "dex"

    def parse(self, file_name):
        filename_w_ext = os.path.basename(file_name)
        s = pydexinfo.dexinfo(file_name, True)
        information = []

        modules = set(re.findall("class_idx.*?L([^;\$]*)", s))
        for m in modules:
            information.append(
                {
                    "VALUE": m,
                    "ASSET": filename_w_ext,
                    "TYPE": "MODULES"
                })


        return information