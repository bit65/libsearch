import os

parsetype = ""
ext = ""

class ParserBase:
    def __init__(self, filename):
        self.filename = filename
        self.filename_w = self.parent = filename.split(os.sep)[-1]

    def parse(self, fileobj = None, parent=None):
        # Choose one out of two paths:
        # 1. If no argument is given, open a file named self.filename
        # 2. If an argument is give, just pass it on.
        if parent:
            self.parent = parent

        close = False

        if fileobj is None:
            fileobj = open(self.filename, "rb")
            close = True

        ret = self._parse(fileobj)

        if close:
            fileobj.close()

        return ret
    
    def createData(self, dtype, dvalue):
        return {
            "VALUE": dvalue,
            "FILE": self.filename_w,
            "ASSET": self.parent,
            "TYPE": dtype
        }
