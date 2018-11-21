from libsearch.processing.base import ParserBase
import subprocess

# from ..dbmodels import *

class DEXParser(ParserBase):
    parsetype = "application/octet-stream"
    ext = "dex"

    def parse(self, file_name):
        args = ['./ext/dexinfo/dexinfo', file_name, '-V']
        args2 = ['grep', '-oP', 'class_idx.*?L\K([^;\$]*)']

        process_dex = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
        process_grep = subprocess.Popen(args2, stdin=process_dex.stdout,
                                stdout=subprocess.PIPE, shell=False)
        process_dex.stdout.close()

        modules = (process_grep.communicate()[0]).splitlines()

        return modules

        # new_modules = [SaveData(data=m) for m in modules]

        # return [
        #    ("MODULES",new_modules)
        #    ]
